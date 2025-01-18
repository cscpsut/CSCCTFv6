from Crypto.Util.number import *
from pwn import xor
import os
FLAG = b"CSCCTF{aGUgd2FzIGEgY3RmIGJveSwgc2hlIHdhcyBhbiBBSSBnaXJs}"

p = getStrongPrime(512)
q = getStrongPrime(512)

import random



class APT:
    def __init__(self, members):
        """
        Initialize the APT. game with members having two hands each.

        Args:
            members (list): List of member names participating in the game.
        """
        self.n = p * q 
        self.members = list(members)
        self.Es = [getPrime(40) for _ in members]
        # Each member has two hands, so the tower starts with twice the member names
        self.tower = self.randomize_hands(members)
        self.shots_taken = {member: 0 for member in members}
        chant = '''Chaeyoung’s favorite random game
Random game
Game start'''
        print(chant)
        print(f'Es: {self.Es}')
        print(f'N: {self.n}')

    def randomize_hands(self, members):
        """
        Randomize the initial order of the hands in the tower.

        Args:
            members (list): List of member names.

        Returns:
            list: Randomized tower with two hands per member.
        """
        members = list(members)
        hands = list(members) * 2  # Each member has 2 hands
        random.shuffle(hands)  # Shuffle the hands
        return hands

    def play_round(self):
        """
        Simulates a single round of the game.
        """
        for i in range(3):
            print("| apateu, apateu")
        print("| tower: ", self.tower)
        # Randomly select a member to call a floor
        caller = random.choice(self.members)
        # Randomly determine a floor number (1 to 10, for example)
        floor_number = self.n + random.randint(1, 1000)

        print(f"| {caller} calls floor {floor_number}.")

        # Simulate moving the bottom hand to the top until the floor number is reached
        for _ in range(floor_number % len(self.tower)):
            self.tower.append(self.tower.pop(0))  # Move the bottom hand to the top

        # The member with the hand on top takes a shot
        shot_taker = self.tower[-1]
        shot = self.take_shot(shot_taker)
        
        return shot

    def distort(self,shot):
        print("| huh?")
 
        shot = bytes_to_long(xor(shot, b'\x10' * (len(shot)//2)))
        for i in self.Es:
            shot = pow(shot, i, self.n)
        shot = str(hex(shot))
        return shot
    
    def take_shot(self, member):
        """
        Simulates a member taking a shot.

        Args:
            member (str): Name of the member taking the shot.
        """


        self.shots_taken[member] += 1
        shot = str(hex(pow(bytes_to_long(FLAG), self.Es[self.members.index(member)], self.n)))
        
        if members[member] < 40:
            return f"| {member} took a shot! {self.distort(shot)}"
        else:
            members[member] = members[member] - 1
            return f"| {member} took a shot! {shot}"
 



banner ='''▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌
▐ ________  ________  _________       ▌
▐|\   __  \|\   __  \|\___   ___\     ▌
▐\ \  \|\  \ \  \|\  \|___ \  \_|     ▌
▐ \ \   __  \ \   ____\   \ \  \      ▌
▐  \ \  \ \  \ \  \___|    \ \  \ ___ ▌
▐   \ \__\ \__\ \__\        \ \__\\___\▌
▐    \|__|\|__|\|__|         \|__\|__|▌
▐▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌
'''
print(f'| flag bits: {len(FLAG)*8}')

print(banner)

members = {"l0mb4rd": random.randint(0,50), "hamoor":random.randint(0,50), "H04X":random.randint(0,50), 'Ziadstr': random.randint(0,50), 'safareto': random.randint(0,50), 'alsa3eedi': random.randint(0,50)}

no_of_heavy_heads = 0
for member in members:
    if members[member] > 39:
        no_of_heavy_heads += 1

while no_of_heavy_heads != 2:
    members[random.choice(list(members.keys()))] = random.randint(0,50)
    no_of_heavy_heads = 0
    for member in members:
        if members[member] > 39:
            no_of_heavy_heads += 1

game =  APT(members)




menu = '''| [P]lay round
| [Q]uit
|'''

def main():

    while True:
        print(menu)
        choice = input("| Enter your choice > ")
        if choice.lower() == 'p':
            print(game.play_round())
        elif choice.lower() == 'q':
            print("| Goodbye!")
            break
        else:
            print("| Invalid choice!")


if '__main__' == __name__:
    main()