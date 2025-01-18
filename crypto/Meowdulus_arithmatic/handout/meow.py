from Crypto.Util.number import *
from secret import FLAG
import random

p = getPrime(10)
a = random.randint(1, p-1)
b = random.randint(1, p-1)
c = random.randint(1, p-1)
d = random.randint(1, p-1)

def m(ch):
    return ch * a % p

def e(ch):
    return ch + b % p

def o(ch):
    return ch - c % p

def w(ch):
    return ch * pow(d, -1, p) % p

ct = []
for ch in FLAG:
    ct.append( m(e(o(w(ch)))) )

print(f"{p=}")
print(f"{a=}")
print(f"{b=}")
print(f"{c=}")
print(f"{d=}")
print(f"{ct=}")


"""
p=709
a=296
b=12
c=148
d=693
ct=[690, 394, 690, 690, 21, 280, 363, 249, 585, 172, 585, 249, 61, 172, 511, 135, 696, 434, 172, 135, 249, 400, 138, 360, 696, 249, 24, 172, 135, 471, 585, 474, 138, 172, 286, 696, 249, 659, 511, 172, 138, 360, 696, 511, 172, 690, 21, 280, 172, 360, 138, 138, 212, 511, 502, 351, 351, 437, 437, 437, 15, 400, 585, 474, 138, 474, 471, 61, 15, 98, 585, 622, 351, 437, 135, 138, 98, 360, 55, 101, 92, 138, 132, 240, 542, 579, 357, 132, 397, 283, 616, 18, 326]
"""