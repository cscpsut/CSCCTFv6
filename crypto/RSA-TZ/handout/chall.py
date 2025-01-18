from Crypto.Util.number import *
Flag = b'CSCCTF{SXMgSFRVIHNvIGJhZCBhZnRlcmFsbD8}'

Flag = bytes_to_long(Flag)

p = getPrime(512)
q = getPrime(512)
while p >= q:
    q = getPrime(512)

n = p*q
e = 0x10001

def encrypt(m):
    return pow(m, e, n)


with open('out.txt', 'w') as f:
    f.write(f'ct = {encrypt(Flag)}\n')
    f.write(f'n = {n}\n')
    f.write(f'e = {e}\n') 
    f.write(f'TZ = {q%p}\n')