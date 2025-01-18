# https://github.com/tna0y/Python-random-module-cracker
## You need to build it from source, as the PyPi package is not updated and would not allow you to run the `offset` method

import requests
from randcrack import RandCrack
from bs4 import BeautifulSoup

URL = 'http://localhost:1337/'

# ChatGPT/Claude generated code
def reverse_hash(known: str, hashed: str) -> str:
    hex_pairs = [int(hashed[i:i+2], 16) for i in range(0, len(hashed), 2)]
    
    max_len = len(hex_pairs)
    known = known.ljust(max_len, '\0')

    result = []
    for i in range(max_len):
        # a ^ b = c, therefore a ^ c = b and b ^ c = a
        recovered_char = chr(hex_pairs[i] ^ ord(known[i]))
        result.append(recovered_char)
    
    return ''.join(result).rstrip('\0')

vals = []
for i in range(624):
    s = requests.Session()
    s.post(
        f'{URL}/signup',
        data={
            'username': str(i),
            'password': str(i),
            'user_info': str(i),
        }
    )
    s.post(
        f'{URL}/login',
        data={
            'username': str(i),
            'password': str(i),
        }
    )
    r = s.get(
        f'{URL}/profile',
    )
    soup = BeautifulSoup(r.text, 'html.parser')
    password_hashes = soup.find_all('div', class_='password-hash')
    for password_hash in password_hashes:
        vals.append(int(reverse_hash(str(i), password_hash.text)))
    print(i, end='\r')


cracker = RandCrack()

for _ in vals:
    cracker.submit(_)

cracker.offset(-624)  # Go back -624 till before the first user
cracker.offset(-1)   # Go back -1 for admin salt
cracker.offset(-2)   # Go back -2 for admin password

print("Admin username:", f"admin-{str(cracker.predict_random())[2:]}")