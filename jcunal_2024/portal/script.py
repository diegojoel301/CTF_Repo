import struct

local_values = [
    0x62641803151c6664,  # local_78
    0x237028021b621a2d,  # local_70
    0x521574341b77371b,  # local_68
    0x5712395512085239,  # local_60
    0x1b                # local_58 (1 byte)
]

values_bytes = b''.join(struct.pack('<Q', v) for v in local_values[:-1]) + struct.pack('<B', local_values[-1])

xor_keys = [0x56] * 11 + [0x44] * 11 + [0x66] * 11

input_bytes = bytes(values_bytes[i] ^ xor_keys[i] for i in range(len(values_bytes)))

secret_word = input_bytes.decode('latin1') 

print(secret_word)