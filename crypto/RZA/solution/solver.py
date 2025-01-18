from Crypto.Util.number import *
from pwn import *
from sympy.ntheory.modular import crt

# p = process(['python3', 'chall.py'])
p = remote("localhost", 1337)

e = 65537
p.recvuntil(b'> ')

p.sendline(b'1')
p.recvuntil(b'Encrypted Flag: ')
c = int(p.recvline().strip())

def check_coprime(m: int , n: list) -> bool:
    for i in n:
        if GCD(m, i) != 1:
            return False
    return True
    
crts = []
ms = []

while len(crts) < 20:
    p.sendline(b'2')
    p.recvuntil(b'Hint: ')
    a, b = map(int, p.recvline().strip()[1:-1].split(b', '))
    if check_coprime(b, ms):
        ms.append(b)
        crts.append(a)

assert len(crts) == len(ms)

m = crt(ms,crts)[0] << 14


for i in range(2**14):
    p = m + i
    if isPrime(p):
        try:
            phi = p - 1
            d = inverse(e, phi)
            flag = long_to_bytes(pow(c, d, p))
            if b'CSCCTF{' in flag:
                print(p)
                print(c)
                print(flag)
                break
            
        except:
            continue