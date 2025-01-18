from secret import PuzzlePiece, Puzzle
import random
import time
import os

FLAG = os.getenv("FLAG", "CSCCTF{this_is_a_fake_flag}").replace("{", "[").replace("}", "]")

def print_slow(text):
    for char in text:
        if char == '‎':
            delay = 1
        else:
            delay = 0.02
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def animate_to_braille(text, frames_per_char=10, frame_delay=0.05, endl='\n'):
    braille_start = 0x2800
    braille_end = 0x28FF

    braille_dict = {
        'A': '⠁', 'B': '⠃', 'C': '⠉', 'D': '⠙', 'E': '⠑',
        'F': '⠋', 'G': '⠛', 'H': '⠓', 'I': '⠊', 'J': '⠚',
        'K': '⠅', 'L': '⠇', 'M': '⠍', 'N': '⠝', 'O': '⠕',
        'P': '⠏', 'Q': '⠟', 'R': '⠗', 'S': '⠎', 'T': '⠞',
        'U': '⠥', 'V': '⠧', 'W': '⠺', 'X': '⠭', 'Y': '⠽',
        'Z': '⠵', ' ': '⠀', '_': '⠸', '[': '⠪', ']': '⠻',
    }
    
    def get_random_braille():
        """Generate a random Braille character."""
        code_point = random.randint(braille_start, braille_end)
        return chr(code_point)
    
    text = text.upper()
    result = ""
    
    for char in text:
        if char in braille_dict:
            target_char = braille_dict[char]
            
            for _ in range(frames_per_char):
                temp_result = result + get_random_braille()
                print(f"\r{temp_result}", end="", flush=True)
                time.sleep(frame_delay)
            
            result += target_char
            print(f"\r{result}", end="", flush=True)
            
        else:
            result += char
            print(f"\r{result}", end="", flush=True)
    
    print(end=endl)

class Game:
    def __init__(self, height=20, width=20):
        self.HEIGHT = height
        self.WIDTH = width
        self.real_puzzle = Puzzle(height=self.HEIGHT, width=self.WIDTH, num_indent_types=6)
        self.piece_pool = [piece for row in self.real_puzzle.grid for piece in row]
        random.shuffle(self.piece_pool)
        self.piece_dict = {k: v for k, v in enumerate(self.piece_pool)}
        self.user_puzzle = Puzzle(height=self.HEIGHT, width=self.WIDTH)
        self.user_indices_map = {}
        self.humor_setting = 75

    def run(self):
        animate_to_braille(" TARS ", endl="")
        print_slow("‎ Initializing‎.‎.‎.‎")
        print_slow("[TARS]‎ Dr. Brand's notes suggest this puzzle piece configuration")
        print_slow("       might reveal coordinates in space-time.‎")
        print_slow(f"[TARS]‎ Humor setting at {self.humor_setting}%‎")
        print_slow("[TARS]‎ WARNING:‎ Space-time fabric is unstable.‎")


        menu = """
[TARS] Available commands:
  1. Analyze pieces
  2. Place piece
  3. Remove piece
  4. Check partial configuration
  5. Verify complete solution
  6. Abort mission
  0. View available commands"""

        print(menu)

        while True:
            
            choice = input("\n> ").strip()
            
            if choice == "1":
                print("[TARS] Format: Index, (Top, Right, Bottom, Left)")
                for k, piece in self.piece_dict.items():
                    print(f"  {k}, ({piece.top}, {piece.right}, {piece.bottom}, {piece.left})")
                
            elif choice == "2":
                try:
                    user_input = input("[TARS] Enter (index row col) [space-separated]: ")
                    index, row, col = map(int, user_input.split())
                except:
                    print("[TARS] Invalid input. Keeping humor setting at 75% to maintain professionalism.")
                    exit()
                    
                if index in self.user_indices_map.keys():
                    print("[TARS] Index is already configured. Honesty setting prevents me from allowing duplicates.")
                    exit()

                if not (0 <= row < self.user_puzzle.height and 0 <= col < self.user_puzzle.width):
                    print("[TARS] Those coordinates are beyond our dimensional boundaries, Cooper.")
                    exit()

                if self.user_puzzle.grid[row][col] is not None:
                    print("[TARS] That space-time coordinate is already occupied.")
                    exit()

                # Use the actual piece object from our pool
                piece = self.piece_dict[index]
                if self.user_puzzle.add_piece(piece, row, col):
                    print("[TARS] Piece locked into quantum configuration.")
                    self.user_indices_map[index] = (row, col)
                else:
                    print("[TARS] Piece rejected by space-time fabric. And that's not my humor setting talking.")
                    exit()
 

            elif choice == "3":
                try:
                    user_input = input("[TARS] Enter (row col) [space-separated]: ")
                    row, col = map(int, user_input.split())
                except:
                    print("[TARS] Invalid input. Keeping humor setting at 75% to maintain professionalism.")
                    exit()
                    
                if not (0 <= row < self.user_puzzle.height and 0 <= col < self.user_puzzle.width):
                    print("[TARS] Those coordinates are beyond our dimensional boundaries, Cooper.")
                    exit()
                    
                if self.user_puzzle.grid[row][col] is None:
                    print("[TARS] No piece found at that space-time coordinate.")
                    exit()
                    
                if self.user_puzzle.remove_piece(row, col):
                    print("[TARS] Piece removed from quantum configuration.")
                else:
                    print("[TARS] Unable to remove piece. Quantum fabric is holding strong.")
                    exit()

                self.user_indices_map = {k: v for k, v in self.user_indices_map.items() if v != (row, col)}
            
            elif choice == "4":
                if len(self.user_indices_map) == 0:
                    print("[TARS] No pieces have been placed. Quantum configuration is empty.")
                elif self.user_puzzle.is_partial_match(self.real_puzzle):
                    print("[TARS] Current configuration aligns with quantum predictions.")
                else:
                    print("[TARS] WARNING: Configuration anomaly detected.")
                    
            elif choice == "5":
                if self.user_puzzle == self.real_puzzle:
                    print_slow("[TARS]‎ Configuration verified.‎ Well done, Cooper.‎")
                    # print_slow("[TARS]‎ Though this puzzle was considerably easier than docking with a spinning Endurance.‎")
                    animate_to_braille(FLAG, frame_delay=0.02)
                    exit()
                else:
                    print("[TARS] Critical configuration error. Unlike the Endurance, we won't survive this spin.")
                    exit()

            elif choice == "6":
                print("[TARS] Mission aborted.")
                exit()
            
            elif choice == "0":
                print(menu)

            else:
                print("[TARS] Invalid command. Not even my humor setting can process that.")
                exit()

if __name__ == "__main__":
    game = Game(height=10, width=10)
    try:
        game.run()
    except:
        exit()