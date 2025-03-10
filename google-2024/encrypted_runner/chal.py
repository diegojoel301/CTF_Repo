import re
import subprocess
import os


def menu():
  print("What do you want to do?")
  print("- encrypt command (e.g. 'encrypt echo test')")
  print("- run command (e.g. 'run fefed6ce5359d0e886090575b2f1e0c7')")
  print("- exit")

print("Welcome to encrypted command runner.")

whitelist = {
    "date": None,
    "echo": "[\\w. ]+",
    "ls": "[/\\w]+",
}

whiteset = set(cmd.encode() for cmd in whitelist)

def helper(cmd, data):
  if cmd == "encrypt":
    data = [ord(c) for c in data]
  else:
    data = list(bytes.fromhex(data))

  while len(data) < 16:
    data.append(0)

  # 16 bytes should be enough for everybody...
  inp = cmd + " " + " ".join("%02x" % c for c in data[:16])
  res = subprocess.check_output("./aes", input = inp.encode())
  return bytes.fromhex(res.decode())

counter = 0
while True:
  counter += 1
  if counter > 100:
    print("All right, I think that's enough for now.")
    break

  menu()
  line = input()
  if line.strip() == "exit":
    print("Bye.")
    break

  what, rest = line.split(" ", 1)
  if what == "encrypt":
    cmd = rest.split(" ")[0]
    if cmd not in whitelist:
      print("I won't encrypt that. ('%s' not in whitelist)" % cmd)
      continue
    regex = [cmd]
    if whitelist[cmd]:
      regex.append(whitelist[cmd])
    regex = " ".join(regex)
    match = re.fullmatch(regex, rest)
    if not match:
      print("I won't encrypt that. ('%s' does not match '%s')" % (rest, regex))
      continue
    res = helper("encrypt", rest)
    print("Encrypted command:", res.hex())
  elif what == "run":
    command = helper("decrypt", rest).rstrip(b"\x00")
    cmd = command.split(b" ")[0]

    # partira en dos el resultado de la desencriptacion en base al espacio
    # por tanto no tendremos el leak que deseamos completo
    # asi que envia tu comando asi: ls ŠŠŠŠŠŠŠŠŠŠŠŠŠ  

    if cmd not in whiteset:
      print("I won't run that. (%s not in whitelist)" % cmd)
      continue

    res = subprocess.run(command, shell = True, stdout = subprocess.PIPE,
                         stderr = subprocess.STDOUT, check = False)
    print("Output:", res.stdout.decode())
  else:
    print("What?")

