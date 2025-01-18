from Crypto.Cipher import AES
import os
from secret import FLAG, welcome
import random
import string
# القطة الملتفة

class AES_CAT:
    def __init__(self):
        self.key = os.urandom(16)
        self.cipher = AES.new(self.key, AES.MODE_ECB)
        self.block_size = 16
        
        
    def pad(self, m):
        padding = b"OIIAOIIAI OIIAII"
        missing = (self.block_size - len(m) % self.block_size) % 16
        return m + padding[:missing]
    
    
    def encrypt(self, m):
        return self.cipher.encrypt(self.pad(m))
    
menu = """
| [R]egister
| [L]ogin
| [E]xit
"""

def main():
    print(welcome)
    sha7bora = AES_CAT()
    admin_password = "".join(random.choice(string.digits) for _ in range(5)).encode()
    passwords = set()
    passwords.add(admin_password)
    users = {"Hamoor" : sha7bora.encrypt(admin_password)}
    login_attempts = 3
    while True:
        if login_attempts == 0:
            print("Sha7bora had to smell you one too many times, its nap time (:")
            break
        print(menu)
        choice = input("| Enter your choice > ")
        if choice == "R":
            username = input("| Enter your username > ")
            password = input("| Enter your password > ").encode()
            if username == "Hamoor" or username in users:
                print("You can't register this username")
                continue
            if password in passwords:
                print("You can't register this password")
                continue
            users[username] = sha7bora.encrypt(password)
            print("Registered successfully")
        elif choice == "L":
            login_attempts -= 1
            username = input("| Enter your username > ")
            if username not in users:
                print("User not found, please register")
                continue
            password = input("| Enter your password > ").encode()
            if password == admin_password:
                print("You can't use this password to login")
                continue
            if sha7bora.encrypt(password) == users[username]:
                print(f"Welcome {username}")
                if username == "Hamoor":
                    print(f"Here is your flag: {FLAG}")
                    break
    
if __name__ == '__main__':
    main()
