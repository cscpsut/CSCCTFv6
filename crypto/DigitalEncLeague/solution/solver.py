from pwn import *
from ecdsa.ecdsa import generator_521
import json
from Crypto.Util.number import inverse, bytes_to_long , long_to_bytes
from hashlib import sha256
n = generator_521.order()
p = process(['python3', 'chall.py'])

def parse_data(msg,k):
    p.recvuntil(b"> ")
    p.sendline(b"1")
    p.recvuntil(b"> ")
    p.sendline(msg.encode())
    p.recvuntil(b"> ")
    p.sendline(str(k).encode())
    p.recvuntil(b"ture:")
    sig = p.recvline().decode().strip()
    sig = json.loads(sig)
    return sig


msg1 = "a"
msg2 = "b"
z1 = bytes_to_long(sha256(msg1.encode()).digest())
z2 = bytes_to_long(sha256(msg2.encode()).digest())


k1 = 1561561
k2 =  1561561 + int(n)
sig1 = parse_data(msg1,k1)
sig2 = parse_data(msg2,k2)
p.close()



k = (z1 - z2) * inverse(sig1["s"] - sig2["s"], n) % n

Flag = inverse(sig1["r"], n) * (k * sig1["s"] - z1) % n 

print(long_to_bytes(Flag))