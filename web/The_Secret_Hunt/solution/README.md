# Write-Up

1. Obtain a token from the server, save into a file called `jwt`
2. Use hachcat to crack the it using `rockyou.txt` wordlist
```bash
hashcat -a 0 -m 16500 jwt /usr/share/wordlists/rockyou.txt
```
3. The Secret will be `reddington`
4. Go to https://jwt.io
    1. In the last box on the right put the secret
    2. Then paste the old token on the left
    3. In the second box on the right modify the `user` to `admin`
    4. Use the resulting token to access `/admin`
    5. Read the Flag