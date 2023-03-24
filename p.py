import random
import math
import PySimpleGUI as sg

# Define the score of each possible game outcome
SCORES = {"X": 1, "O": -1, "Tie": 0}

class TicTacToe:
    def __init__(self):
        self.board = [" "] * 9
        self.current_player = "X"

    def make_move(self, move):
        self.board[move] = self.current_player
        self.current_player = "O" if self.current_player == "X" else "X"

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == " "]

    def winner(self):
        win_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for combo in win_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != " ":
                return self.board[combo[0]]
        if " " not in self.board:
            return "Tie"
        return None

    def score(self):
        winner = self.winner()
        if winner is not None:
            return SCORES[winner]
        else:
            return None

    def copy(self):
        new_board = TicTacToe()
        new_board.board = self.board.copy()
        new_board.current_player = self.current_player
        return new_board

    def __str__(self):
        rows = [" ".join(self.board[i:i+3]) for i in range(0, 9, 3)]
        return "\n".join(rows)

def simulated_annealing(game):
    T = 1.0
    T_min = 0.01
    alpha = 0.9

    while T > T_min:
        move = random.choice(game.available_moves())
        new_game = game.copy()
        new_game.make_move(move)
        delta_E = new_game.score() - game.score()
        if delta_E > 0:
            game = new_game
        elif random.uniform(0, 1) < math.exp(delta_E / T):
            game = new_game
        T *= alpha

    return game


def main():
    layout = [
        [sg.Text("Tic Tac Toe")],
        [sg.Button("", size=(4, 2), key="-0-"), sg.Button("", size=(4, 2), key="-1-"), sg.Button("", size=(4, 2), key="-2-")],
        [sg.Button("", size=(4, 2), key="-3-"), sg.Button("", size=(4, 2), key="-4-"), sg.Button("", size=(4, 2), key="-5-")],
        [sg.Button("", size=(4, 2), key="-6-"), sg.Button("", size=(4, 2), key="-7-"), sg.Button("", size=(4, 2), key="-8-")],
        [sg.Button("Reset", size=(10, 1), key="-RESET-")]
    ]

    window = sg.Window("Tic Tac Toe", layout)

    game = TicTacToe()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event.startswith("-"):
            # Get the button position from the event key
            row, col = int(event[1]) // 3, int(event[1]) % 3

            if game.board[row * 3 + col] == " ":
                # Make a move on the Tic Tac Toe board
                game.make_move(row * 3 + col)

                # Update the button text and disable it
                window[event].update(game.current_player)
                window[event].disable()

                # Check for game over
                winner = game.winner()
                if winner is not None:
                    sg.popup(f"{winner} wins!" if winner != "Tie" else "It's a tie!")
                    break

                # Run simulated annealing to make a move for the computer
                game = simulated_annealing(game)

                # Update the GUI with the computer's move
                for i, char in enumerate(game.board):
                    if char != " ":
                        window[f"-{i}-"].update(char)
                        window[f"-{i}-"].disable()

                # Check for game over again
                winner = game.winner()
                if winner is not None:
                    sg.popup(f"{winner} wins!" if winner != "Tie" else "It's a tie!")
                    break

        elif event == "-RESET-":
            # Reset the Tic Tac Toe game and GUI
            game = TicTacToe()
            for i in range(9):
                window[f"-{i}-"].update("")
                window[f"-{i}-"].enable()

    window.close()
