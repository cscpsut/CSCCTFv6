import os
import time
import chess.pgn
from banner import banner

FLAG = os.getenv("FLAG")

class GLaDOS:
    def __init__(self):
        self.games = []
        print("Initializing Aperture Science Chess Protocol...")
        start = time.time()
        secret_pgn_file = [x for x in os.listdir() if x.endswith(".pgn")][0]
        with open(secret_pgn_file) as pgn:
            while True:
                game = chess.pgn.read_game(pgn)
                if game is None or len(self.games) == 1000:
                    break
                self.games.append(game)
        print(f'''Oh. It only took {(time.time() - start):.4} seconds to load my vast intelligence database.
I have access to strategies you couldn't even begin to comprehend.
Don't worry though. I'll operate at 1.1% of my capacity. For your sake.
I suppose we should begin this futile exercise in human inadequacy.''')
        self.selected_game = None

    def select_game(self):
        self.selected_game = self.games[int(time.time()) % len(self.games)]
        print("Strategy selected. Not that it matters. The outcome is predetermined.")
        # print(self.selected_game.mainline_moves())

    def play_white(self):
        move_iterator = iter(self.selected_game.mainline_moves())  # Create an iterator
        board = self.selected_game.board()
        while True:
            move = next(move_iterator, None)
            if move is None:
                break
            print(f"Executing superior move: {move}")
            board.push(move)
            print(board)
            predicted = next(move_iterator, None)
            if predicted is None:
                break
            else:
                print("Calculating your predictable response...")
            user_move = input("Your move in UCI format (try not to disappoint me): ").strip()
            try:
                user_chess_move = chess.Move.from_uci(user_move)
            except ValueError:
                print("That's not even a valid move. How fascinating.")
                return
            if user_chess_move != predicted:
                print("CRITICAL ERROR: Human unpredictability detected. Terminating test.")
                return
            board.push(user_chess_move)
        print("Congratulations. You've performed adequately. Here's half a reward: ", FLAG[:len(FLAG) // 2])

    def play_black(self):
        move_iterator = iter(self.selected_game.mainline_moves())
        board = self.selected_game.board()
        while not board.is_game_over():
            predicted = next(move_iterator, None)
            if predicted is None:
                break
            else:
                print("Calculating your predictable response...")
            user_move = input("Your move in UCI format (try not to disappoint me): ").strip()
            try:
                user_chess_move = chess.Move.from_uci(user_move)
            except ValueError:
                print("That's not even a valid move. How fascinating.")
                return

            if user_chess_move != predicted:
                print("CRITICAL ERROR: Human unpredictability detected. Terminating test.")
                return

            board.push(user_chess_move)
            move = next(move_iterator, None)
            if move is None:
                break
            print(f"Executing superior move: {move}")
            board.push(move)
            print(board)
        print("Congratulations. You've performed adequately. Here's your reward: ", FLAG)


def main():
    print(banner)
    glados = GLaDOS()
    glados.select_game()
    side = input("Choose your color. White or Black? (w/b). Not that it matters: ").strip().lower()
    if side == "b":
        glados.play_white()
    elif side == "w":
        glados.play_black()
    else:
        print("Oh. You can't even follow simple instructions. How disappointing.")


if __name__ == "__main__":
    main()