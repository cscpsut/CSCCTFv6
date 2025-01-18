from ecdsa.ecdsa import *
from ecdsa.ellipticcurve import *
from Crypto.Util.number import bytes_to_long
from hashlib import sha256
import random as rand
import json
import os

FLAG = os.getenv["FLAG"].encode()


secret_key = bytes_to_long(FLAG)



# helper functions
def merge(a, b):
    return a + b

class SignMe:
    def __init__(self, curve, generator, secret_key):
        self.curve = curve
        self.generator = generator
        self.public_key = Public_key(generator, generator * secret_key)
        self.private_key = Private_key(self.public_key, secret_key)

            
    def sign_message(self, message, k):
        message = bytes_to_long(sha256(message.encode()).digest())
        return json.dumps({"r": int(self.private_key.sign(message, k).r), "s": int(self.private_key.sign(message, k).s)})




Funky_Monkey = SignMe(curve_521, generator_521, secret_key)



Banner = """|
|    __             _     __                                  _              
|   /  )    _/_    //    /  `                  _/_          _//              
|  /  /o_, o/ __. //    /--  ____ _.__ __  ,_  / o______    /  _ __. _, . ._ 
| /__/<(_)<<_(_/|</_   (___,/ / <(_/ (/ (_//_)<_<(_) / <_  /__</(_/|(_)(_/</_
|       /|                               //                          /|      
|      |/                               ''                          |/       
|"""

print(Banner)
menu = """| 1. Sign a message
| 2. Exit
|    """
signature_counter = 0
Used_inp = []
k = rand.randrange(curve_521.p())
while True:
    print(menu)
    choice = input("| Enter your choice >  ")
    if choice == '1':

        signature_counter += 1
        if signature_counter > 2:
            print("| You have reached the limit of signatures")
            break
        message = input("| Enter the message > ")
        inp = int(input("| Enter the random number inp > "))
        if inp in Used_inp:
            print("| You have already used this inp")
            break
        Used_inp.append(inp)
        
        signature = Funky_Monkey.sign_message(message, merge(inp, k))
        print(f"| Signature: {signature}")
    elif choice == '2':
        break
    else:
        print("| Invalid choice!")