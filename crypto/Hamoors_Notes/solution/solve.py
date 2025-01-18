from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from pwn import xor
import random
import math
from Crypto.Util.number import *


class LCG:
    def __init__(self, seed, a, c, m):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m
        
    def next(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed
    


key = b"SASO935!" * 2
iv = b"meow" * 4 
leak = 'fd77e32f1c81548029f0d787792351d898cb07c988a4b3a1085c7008832a7730a9d658dcee0f186c76f93530bb52b526'
leak = bytes.fromhex(leak)
leak_blocks = [leak[i : i + 16] for i in range(0, len(leak), 16)] 
ct = open("CSC2024/LCG_idea/CTF_notes.pdf.enc", 'rb').read()
ct_blocks = [ct[i : i + 16] for i in range(0, len(ct), 16)]
cipher = AES.new(key, AES.MODE_ECB)

m = 2 ** (len(bin(len(ct_blocks))) - 2)  

for i, block in enumerate(ct_blocks):
    decrepted_block = xor(cipher.decrypt(block), iv)
    if decrepted_block == leak_blocks[0]:
        print("FOUND", i)
        s1 = i
        break
    

for i, block in enumerate(ct_blocks):
    decrepted_block = xor(cipher.decrypt(block), ct_blocks[s1])
    if decrepted_block == leak_blocks[1]:
        print("FOUND", i)
        s2 = i
        break
    
for i, block in enumerate(ct_blocks):
    decrepted_block = xor(cipher.decrypt(block), ct_blocks[s2])
    if decrepted_block == leak_blocks[2]:
        print("FOUND", i)
        s3 = i
        break


lh = (s3 - s2) % m
rh = (s2 - s1) % m
a = lh * pow(rh, -1, m) % m
c = (s2 - a * s1) % m
print(a, c, m)
lcg = LCG(s3, a, c, m)
indecies = [s1, s2, s3]
for _ in range(m):
    val = lcg.next()
    if val < len(ct_blocks):
        indecies.append(val)
        
pt_blocks = [None] * len(ct_blocks)
pt_blocks[s1] = leak_blocks[0]
pt_blocks[s2] = leak_blocks[1]
pt_blocks[s3] = leak_blocks[2]

for i in range(3, len(indecies)):
    idx = indecies[i]
    pt_blocks[idx] = xor(cipher.decrypt(ct_blocks[idx]), ct_blocks[indecies[i - 1]])
    
pt = b"".join(pt_blocks)
open("CSC2024/LCG_idea/CTF_notes_dec.pdf", 'wb').write(pt)