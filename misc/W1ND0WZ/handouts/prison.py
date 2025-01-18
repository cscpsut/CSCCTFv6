#!usr/bin/env python3

import random
import string

class Jail:
    def __banner__(self):
        print('''
        ╔══════════════════════════════════════╗
        ║       W1ND0WZ 2000 PR0F3SS10N4L      ║
        ║          T3RM1N4L V3.1.337           ║
        ╚══════════════════════════════════════╝
        ''')
        print('INIT: System loaded... Access restricted...')
    def __init__(self):
        self.__banner__()
        self.blocked = [
            'eval', 'exec', 'os', 'sys', 'subprocess', 'shutil', 'import', 'read', 'flag', 'input', 'locals', 'globals'
        ]

    def check_input(self, user_input):
        if any(bad in user_input.lower() for bad in self.blocked):
            print('ERR0R: n00b d3t3ct3d! Acc3ss d3n13d!')
            exit(0)

    def break_(self, *args, **kwargs):
        for a in args:
            locals()[''.join(random.choices(string.ascii_letters, k=30))] = __import__('os').popen('cat flag.txt').read()
        for k, v in kwargs.items():
            locals()[k] = v
        exec("print('LOL! Ur getting warmer but still fail!')")

def main():
    jail = Jail()
    while True:
        user_input = input("C:\\WINDOWS\\system32> ")
        jail.check_input(user_input)
        try:
            eval(f"jail.break_({user_input})")
        except:
            print('FATAL: Cannot compute! System crash imminent!')
            exit()


if __name__ == "__main__":
    main()