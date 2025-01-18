from solver import *
from pwn import *

r = remote("challenges.cscpsut.com", 10063)

r.recvuntil("> ")
r.sendline("1")
r.recvuntil("(Top, Right, Bottom, Left)\n")
pieces = r.recvuntil(">").decode().strip().split("\n")[:-2]
pieces = [p.strip() for p in pieces]
pieces = [eval(p.split(', ', 1)[1]) for p in pieces]
# print(pieces)

solutions = solve_jigsaw(pieces, debug=False)

if not solutions:
    print("No solutions found")
    exit()

if len(solutions) > 1:
    print("Multiple solutions found")
    exit()

solution = solutions[0]

for i, row in enumerate(solution):
    for j, piece in enumerate(row):
        if piece is None:
            continue
        r.sendline("2")
        r.recvuntil("[TARS] Enter (index row col) [space-separated]: ")
        r.sendline(f"{piece} {i} {j}")
        r.recvuntil("> ")

r.sendline("5")
r.interactive()