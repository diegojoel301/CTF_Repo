from pwn import *
import time

# b *main+92
# b *main+42
gs = '''
b *main+42
b *main+92
continue
'''

elf = context.binary = ELF("./main")

def start():
    if args.REMOTE:
        return remote("20.244.40.210", 6000)
    else:
        if args.GDB:
            return gdb.debug(elf.path, gdbscript=gs)
        else:
            return process(elf.path)

context.terminal = ['gnome-terminal', '-e']

io = start()
io_rand = process("./randomico")
timestamp = int(time.time())
io_rand.sendline(str(timestamp))
randoms = io_rand.recv().decode().split(",")

print(randoms)

v = [
    "Chocolate Chip", "Sugar Cookie", "Oatmeal Raisin", "Peanut Butter", "Snickerdoodle",
    "Shortbread", "Gingerbread", "Macaron", "Macaroon", "Biscotti", "Butter Cookie",
    "White Chocolate Macadamia Nut", "Double Chocolate Chip", "M&M Cookie",
    "Lemon Drop Cookie", "Coconut Cookie", "Almond Cookie", "Thumbprint Cookie",
    "Fortune Cookie", "Black and White Cookie", "Molasses Cookie", "Pumpkin Cookie",
    "Maple Cookie", "Espresso Cookie", "Red Velvet Cookie", "Funfetti Cookie",
    "S'mores Cookie", "Rocky Road Cookie", "Caramel Apple Cookie", "Banana Bread Cookie",
    "Zucchini Cookie", "Matcha Green Tea Cookie", "Chai Spice Cookie", "Lavender Shortbread",
    "Earl Grey Tea Cookie", "Pistachio Cookie", "Hazelnut Cookie", "Pecan Sandies",
    "Linzer Cookie", "Spritz Cookie", "Russian Tea Cake", "Anzac Biscuit",
    "Florentine Cookie", "Stroopwafel", "Alfajores", "Polvorón", "Springerle",
    "Pfeffernüsse", "Speculoos", "Kolaczki", "Rugelach", "Hamantaschen",
    "Mandelbrot", "Koulourakia", "Melomakarona", "Kourabiedes", "Pizzelle",
    "Amaretti", "Cantucci", "Savoiardi (Ladyfingers)", "Madeleine", "Palmier",
    "Tuile", "Langue de Chat", "Viennese Whirls", "Empire Biscuit",
    "Jammie Dodger", "Digestive Biscuit", "Hobnob", "Garibaldi Biscuit",
    "Bourbon Biscuit", "Custard Cream", "Ginger Nut", "Nice Biscuit", "Shortcake",
    "Jam Thumbprint", "Coconut Macaroon", "Chocolate Crinkle", "Pepparkakor",
    "Sandbakelse", "Krumkake", "Rosette Cookie", "Pinwheel Cookie",
    "Checkerboard Cookie", "Rainbow Cookie", "Mexican Wedding Cookie",
    "Snowball Cookie", "Cranberry Orange Cookie", "Pumpkin Spice Cookie",
    "Cinnamon Roll Cookie", "Chocolate Hazelnut Cookie", "Salted Caramel Cookie",
    "Toffee Crunch Cookie", "Brownie Cookie", "Cheesecake Cookie", "Key Lime Cookie",
    "Blueberry Lemon Cookie", "Raspberry Almond Cookie", "Strawberry Shortcake Cookie",
    "Neapolitan Cookie"
]

for i in range(100):
    print(f"Iteracion: {i}")
    io.sendlineafter("Guess the cookie: ", v[int(randoms[i])])


io.interactive()