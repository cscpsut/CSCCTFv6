from Crypto.Util.number import *
import random
import os

FLAG = os.getenv("FLAG").encode() 


e = 65537
class funny:
    def __init__(self, bitsize: int):
        self.p = getPrime(bitsize)
        self.q = getPrime(bitsize)
        self.n = self.p * self.q
    
    def encrypt(self, m: int):
        return pow(m, e, self.n)

    def get_hint(self):
        m = random.getrandbits(self.p.bit_length() // 10)
        return (self.p >> 14)  % m , m  

RSA = funny(1024)

banner = """| 
| 
|  .----------------.  .----------------.  .----------------. 
| | .--------------. || .--------------. || .--------------. |
| | |  _______     | || |   ________   | || |      __      | |
| | | |_   __ \    | || |  |  __   _|  | || |     /  \     | |
| | |   | |__) |   | || |  |_/  / /    | || |    / /\ \    | |
| | |   |  __ /    | || |     .'.' _   | || |   / ____ \   | |
| | |  _| |  \ \_  | || |   _/ /__/ |  | || | _/ /    \ \_ | |
| | | |____| |___| | || |  |________|  | || ||____|  |____|| |
| | |              | || |              | || |              | |
| | '--------------' || '--------------' || '--------------' |
|  '----------------'  '----------------'  '----------------' 
| 
| """
menu = '''| 
| 1. Encrypt Flag
| 2. Get Hint
| 3. Exit
| '''


print(banner)

print(f'| e = {e}')

while True:
    print(menu)
    choice = input('| Enter your choice > ')
    if choice == '1':
        print(f'| Encrypted Flag: {RSA.encrypt(bytes_to_long(FLAG))}')
    elif choice == '2':
        a, b = RSA.get_hint()
        print(f'| Hint: {a , b}')
    elif choice == '3':
        print('| Ciao ciao!')
        break
    else:
        print('| Invalid choice')
