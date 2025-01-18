from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad
from pwn import xor
import random
import math

class LCG:
    def __init__(self, seed, a, c, m):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m
        
    def next(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed
    


block_size = 16
pt = pad(open(r"CTF_notes.pdf", "rb").read(), 16)
length = len(pt) // block_size
key = b"SASO935!" * 2  # Super secret password no one has ever seen
iv = b"meow" * 4  # Hamoor is a genius

m = 2 ** (len(bin(length)) - 2)  
# Generate valid a, c pairs
while True:
    seed = random.randint(0, m - 1) | 1

    while True:
        a = random.randint(2, m - 1) | 1
        c = random.randint(2, m - 1) | 1
        if (a - 1) % 4 != 0 or math.gcd(m, c) != 1:
            continue
        break
    lcg = LCG(seed, a, c, m)

    pt_blocks = [pt[i * block_size: (i + 1) * block_size] for i in range(length)]
    ct_blocks = [None] * length  

    indecies = []
    for _ in range(m):
        val = lcg.next()
        if val < length:
            indecies.append(val)
    
    assert len(set(indecies)) == length
    if indecies[1] !=(a * indecies[0] + c) % m or indecies[2] != (a * indecies[1] + c) % m:
        continue

    if indecies[0] % 2 != indecies[1] % 2: # yes seleen its invertable
        break
    
    


cipher = AES.new(key, AES.MODE_ECB)

for i in range(len(indecies)):
    idx = indecies[i]
    if i % 10000 == 0:
        print(f"{i} / {length}")
    if i == 0:
        ct_blocks[idx] = cipher.encrypt(xor(pt_blocks[idx], iv))
    else:
        ct_blocks[idx] = cipher.encrypt(xor(pt_blocks[idx], ct_blocks[indecies[i - 1]]))

ct = b"".join(ct_blocks)
open(r"CSC2024/LCG_idea/CTF_notes.pdf.enc", "wb").write(ct)
leak = b"".join([pt_blocks[indecies[i]] for i in range(3)]).hex()
print(f"{leak=}")

"""
leak = '4613cd3f6bf89bb7c35fab005f93bf2983b82018696de64f0ed7ce8eeb9767cd5562b397b2b56226ec4537a50715d983'
"""