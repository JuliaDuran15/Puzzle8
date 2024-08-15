import tkinter as tk
import random
import copy

class Puzzle8:
    def __init__(self, board=None, actions=None, history=None):
        if board is None:
            board = self._generate_solvable_board()
        self.board = board
        self.empty_pos = self.board.index(0)
        self.actions = actions if actions is not None else []
        self.history = history if history is not None else []

    def _generate_solvable_board(self):
        board = list(range(9))
        random.shuffle(board)
        while not self._is_solvable(board):
            random.shuffle(board)
        return board

    def _is_solvable(self, board):
        inversions = 0
        for i in range(8):
            for j in range(i + 1, 9):
                if board[i] > board[j] > 0:
                    inversions += 1
        return inversions % 2 == 0

    def move(self, direction):
        x, y = divmod(self.empty_pos, 3)
        if direction == 'up' and x > 0:
            return self._create_new_state(x, y, x-1, y, direction)
        elif direction == 'down' and x < 2:
            return self._create_new_state(x, y, x+1, y, direction)
        elif direction == 'left' and y > 0:
            return self._create_new_state(x, y, x, y-1, direction)
        elif direction == 'right' and y < 2:
            return self._create_new_state(x, y, x, y+1, direction)
        else:
            return None

    def _create_new_state(self, x1, y1, x2, y2, direction):
        new_board = copy.deepcopy(self.board)
        pos1, pos2 = x1 * 3 + y1, x2 * 3 + y2
        new_board[pos1], new_board[pos2] = new_board[pos2], new_board[pos1]
        new_actions = self.actions + [direction]
        new_history = copy.deepcopy(self.history)
        new_history.append(self.board)
        return Puzzle8(new_board, new_actions, new_history)

    def is_solved(self):
        return self.board == list(range(1, 9)) + [0]

    def get_board(self):
        return self.board

class Puzzle8GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Puzzle 8")
        self.puzzle = Puzzle8()

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.root, font=('Helvetica', 24), width=4, height=2)
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

        self.update_buttons()
        self.root.bind('<Up>', self.key_press)
        self.root.bind('<Down>', self.key_press)
        self.root.bind('<Left>', self.key_press)
        self.root.bind('<Right>', self.key_press)

    def key_press(self, event):
        direction = ''
        if event.keysym == 'Up':
            direction = 'up'
        elif event.keysym == 'Down':
            direction = 'down'
        elif event.keysym == 'Left':
            direction = 'left'
        elif event.keysym == 'Right':
            direction = 'right'

        if direction:
            new_puzzle = self.puzzle.move(direction)
            if new_puzzle:
                self.puzzle = new_puzzle
                self.update_buttons()
                if self.puzzle.is_solved():
                    self.show_solved_message()

    def update_buttons(self):
        board = self.puzzle.get_board()
        for i in range(9):
            text = str(board[i]) if board[i] != 0 else ''
            self.buttons[i].config(text=text)

    def show_solved_message(self):
        tk.messagebox.showinfo("Parabéns!", "Você resolveu o puzzle!")

if __name__ == "__main__":
    root = tk.Tk()
    Puzzle8GUI(root)
    root.mainloop()
