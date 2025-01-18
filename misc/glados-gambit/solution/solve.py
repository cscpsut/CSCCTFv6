from pwn import *
import threading
from queue import Queue
context.log_level = 'DEBUG'

source = ["python3", "CSC2024/Chess_trick/chal.py"] ## replace with remote server address

whitemoves = Queue()
blackmoves = Queue()


def whiteThread():
    r = process(source) # change to remote
    r.recvuntil("Choose your color. White or Black? (w/b). Not that it matters: ")
    r.sendline("w")
    try:
        while True:
            r.recvuntil("Your move in UCI format (try not to disappoint me): ")
            move = whitemoves.get()
            print("From white thread", move, type(move))
            r.sendline(move)

            r.recvuntil("Executing superior move: ")
            move = r.recvline().strip().decode()
            blackmoves.put(move)
    except:
        print(r.recvall())
        r.close()
    
def blackThread():
    r = process(source) # change to remote
    r.recvuntil("Choose your color. White or Black? (w/b). Not that it matters: ")
    r.sendline("b")
    try:
        while True:
            r.recvuntil("Executing superior move: ")
            move = r.recvline().strip().decode()
            whitemoves.put(move)
            r.recvuntil("Your move in UCI format (try not to disappoint me): ")
            move = blackmoves.get()
            print("From black thread", move, type(move))
            r.sendline(move)
    except:
        print(r.recvall())
        r.close()

w = threading.Thread(target=whiteThread)
b = threading.Thread(target=blackThread)

w.start()
b.start()

w.join()
b.join()


'''
loop
lock 1
recv
relese 
send
lock 2
send 
recv
release
'''