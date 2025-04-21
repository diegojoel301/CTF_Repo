import angr
from sys import argv

def colourize(x, colour):
    return colour + x + "\x1b[0m"
def orange(x):
    return colourize(x, "\x1b[33m")
def light_red(x):
    return colourize(x, "\x1b[91m")
def green(x):
    return colourize(x, "\x1b[92m")
def blue(x):
    return colourize(x, "\x1b[94m")

def info(msg):
    print(f"[{blue('*')}] {msg}")
def warning(msg):
    print(f"[{orange('!')}] {orange(msg)}")
def success(msg):
    print(f"[{green('+')}] {green(msg)}")
def error(msg):
    print(f"[{light_red('-')}] {light_red(msg)}")

info("Loading project")

proj = angr.Project(argv[1])
func = "gets"
file = "_IO_2_1_stdin_"

obj = proj.loader.main_object
def addrof(name):
	return obj.get_symbol(name).rebased_addr

func_addr = addrof(func)
file_addr = addrof(file)
scratch_addr = file_addr + 224	# after vtable pointer, in wfile area

def simulate_gets(use_lock=False, input_data=b"A"*0x10+b"\n"):
	options = {
	angr.options.SYMBOL_FILL_UNCONSTRAINED_MEMORY,
	angr.options.SYMBOL_FILL_UNCONSTRAINED_REGISTERS,
	}
	stdin = angr.SimFileStream(name='stdin', content=input_data, has_end=True)
	state = proj.factory.call_state(func_addr,
		prototype="void* gets(void* p)",
		add_options=options,
		stdin=stdin)

	# unbuffer stdin
	flags = state.mem[file_addr].uint64_t.resolved
	flags |= 2	# _IO_UNBUFFERED
	state.mem[file_addr].uint64_t = flags

	lock_addr = state.mem[file_addr+0x88].uint64_t.resolved
	state.regs.rdi = lock_addr if use_lock else scratch_addr

	simgr = proj.factory.simulation_manager(state)
	simgr.run()
	deadends = simgr.deadended
	if len(simgr.deadended) != 1:
		return None
	return simgr.deadended[0].regs.rdi, lock_addr

print()

info("gets(scratch)")
ret = simulate_gets(use_lock=False)
if ret is None:
	error("Simulation failed to run!")
else:
	rdi, lock = ret
	if rdi is lock:
		success("rdi = &_IO_stdfile_0_lock")
	else:
		warning(f"rdi = {rdi}")

print()
info("gets(&_IO_stdfile_0_lock)")
ret = simulate_gets(use_lock=True)
if ret is None:
	error("Simulation failed to run!")
else:
	rdi, lock = ret
	if rdi is lock:
		success("rdi = &_IO_stdfile_0_lock")
	else:
		warning(f"rdi = {rdi}")