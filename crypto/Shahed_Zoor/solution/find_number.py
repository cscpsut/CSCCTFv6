from Crypto.Util.number import *
from math import prod

class Court:
    def __init__(self, jury):
        self.jury = jury
        
    def verdict(self, defendant):
        for juror in self.jury:
            if pow(juror, defendant - 1, defendant) != 1:
                return "Guilty"
            
        return "Innocent"
    
    

court = Court([2, 5, 7, 13, 19, 23, 29])

k = getRandomNBitInteger(128)
p1 = 6 * k + 1
p2 = 12 * k + 1
p3 = 18 * k + 1
while not (isPrime(p1) and isPrime(p2) and isPrime(p3)):
    k = getRandomNBitInteger(128)
    p1 = 6 * k + 1
    p2 = 12 * k + 1
    p3 = 18 * k + 1
    print(len(bin(p1)) - 2)
    print(len(bin(p2)) - 2)
    print(len(bin(p3)) - 2)
    exit()
    
    
print(p1 * p2 * p3)
print(f"{p1 = }")
print(f"{p2 = }")
print(f"{p3 = }")
n = p1 * p2 * p3
print(len(bin(n)) - 2)
print(court.verdict(n))
