import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import copy
from collections import deque
import heapq

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
        new_history.append(copy.deepcopy(self.board))
        return Puzzle8(new_board, new_actions, new_history)

    def is_solved(self):
        return self.board == list(range(1, 9)) + [0]

    def get_board(self):
        return self.board

    def get_history(self):
        return self.history

    def get_actions(self):
        return self.actions

    def get_possible_moves(self):
        # Retorna todos os estados possíveis a partir do estado atual
        possible_moves = []
        for direction in ['up', 'down', 'left', 'right']:
            new_state = self.move(direction)
            if new_state:
                possible_moves.append(new_state)
        return possible_moves

    def __hash__(self):
        return hash(tuple(self.board))

    def __eq__(self, other):
        return self.board == other.board

    def __lt__(self, other):
        """Define uma comparação baseada no número de movimentos realizados."""
        return len(self.actions) < len(other.actions)

class PuzzleSolver:
    def __init__(self, puzzle, method):
        self.puzzle = puzzle
        self.method = method
        self.visited = set()
        self.queue = None
        self.state_count = 0

    def solve(self):
        if self.method == "BFS":
            self.queue = deque([self.puzzle])
        elif self.method == "DFS":
            self.queue = [self.puzzle]
        elif self.method == "A*":
            self.queue = []
            heapq.heappush(self.queue, (self._heuristic(self.puzzle), self.puzzle))

        while self.queue:
            if self.method == "BFS":
                current_state = self.queue.popleft()
            elif self.method == "DFS":
                current_state = self.queue.pop()
            elif self.method == "A*":
                _, current_state = heapq.heappop(self.queue)

            self.state_count += 1

            if current_state.is_solved():
                return current_state.get_actions(), self.state_count

            for next_state in current_state.get_possible_moves():
                if next_state not in self.visited:
                    self.visited.add(next_state)
                    if self.method == "BFS":
                        self.queue.append(next_state)
                    elif self.method == "DFS":
                        self.queue.append(next_state)
                    elif self.method == "A*":
                        heapq.heappush(self.queue, (self._heuristic(next_state), next_state))
        
        return None, self.state_count

    def _heuristic(self, state):
        # Heurística para o A* (distância de Manhattan)
        return sum(abs(b % 3 - g % 3) + abs(b // 3 - g // 3)
                   for b, g in enumerate(state.get_board()) if b != 0)

class Puzzle8GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Puzzle 8 com IA")
        self.puzzle = Puzzle8()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)

        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.pack()

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.board_frame, font=('Helvetica', 24), width=4, height=2, relief="groove", bg="#f0f0f0", activebackground="#c0c0c0")
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

        self.ia_button = tk.Button(self.main_frame, text="Resolver com IA", command=self.show_ia_options)
        self.ia_button.pack(pady=10)

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
        messagebox.showinfo("Parabéns!", "Você resolveu o puzzle!")

    def show_ia_options(self):
        options_window = tk.Toplevel(self.root)
        options_window.title("Escolha uma IA")

        tk.Button(options_window, text="Busca em Largura", command=lambda: self.solve_with_ai("BFS")).pack()
        tk.Button(options_window, text="Busca em Profundidade", command=lambda: self.solve_with_ai("DFS")).pack()
        tk.Button(options_window, text="Busca A*", command=lambda: self.solve_with_ai("A*")).pack()

    def solve_with_ai(self, method):
        solver = PuzzleSolver(self.puzzle, method)
        solution, states_visited = solver.solve()

        if solution:
            messagebox.showinfo(f"Resolvido com {method}", f"Solução encontrada com {states_visited} estados visitados:\n{solution}")
            for move in solution:
                self.puzzle = self.puzzle.move(move)
                self.update_buttons()
        else:
            messagebox.showinfo(f"{method}", "Sem solução encontrada.")

if __name__ == "__main__":
    root = tk.Tk()
    Puzzle8GUI(root)
    root.mainloop()
