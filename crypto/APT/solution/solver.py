from pwn import *
from Crypto.Util.number import *

context.log_level = 'debug'

# p = process(['python3', 'chall.py'])
p = remote('95.111.237.101', 1337)

p.recvuntil(b'Es: ')
es =  list(map(int,p.recvline().decode().strip()[1:-1].split(', ')))

p.recvuntil(b'N: ')
n = int(p.recvline().strip())

print(es)
print(n)

def attack(c1, c2, e1, e2, N):
    if GCD(e1, e2) != 1:
        raise ValueError("Exponents e1 and e2 must be coprime")
    s1 = inverse(e1,e2)
    s2 = (GCD(e1,e2) - e1 * s1) // e2
    temp = inverse(c2, N)
    m1 = pow(c1,s1,N)
    m2 = pow(temp,-s2,N)
    return (m1 * m2) % N


cts = []

while len(cts) < 2:
    p.recvuntil(b'choice: ')
    p.sendline(b'p')
    data = p.recvuntil(b'shot!')
    ct = int(p.recvline().strip(),16)

    if b'huh' not in data and ct not in cts:
        
        
        cts.append(ct)


for i in es:
    for j in es:
        if i != j:
            try:
                m = attack(cts[0], cts[1], i, j, n)
                print(long_to_bytes(m).decode())
                break
            except:
                pass