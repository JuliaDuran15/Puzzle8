import tkinter as tk
from tkinter import messagebox
import random
import copy
from collections import deque
import heapq

class Puzzle8:
    def __init__(self, board=None, actions=None, parent=None):
        # Initialize the puzzle state
        if board is None:
            board = self._generate_solvable_board()  # Generate a new solvable board
        self.board = board
        self.empty_pos = self.board.index(0)  # Find the position of the empty tile
        self.actions = actions if actions is not None else []  # Store the actions taken
        self.parent = parent  # Reference to the parent state (instead of keeping full history)

    def _generate_solvable_board(self):
        # Create a random board and ensure it's solvable
        board = list(range(9))  # Generate a list of numbers from 0 to 8
        random.shuffle(board)  # Shuffle to randomize
        while not self._is_solvable(board):
            random.shuffle(board)  # Keep shuffling until a solvable board is found
        return board

    def _is_solvable(self, board):
        # Check if the board is solvable based on the number of inversions
        inversions = 0
        for i in range(8):
            for j in range(i + 1, 9):
                if board[i] > board[j] > 0:
                    inversions += 1  # Count inversions
        return inversions % 2 == 0  # Solvable if inversions are even

    def move(self, direction):
        # Attempt to move the empty tile in the specified direction
        x, y = divmod(self.empty_pos, 3)  # Get current empty position (row, col)
        if direction == 'up' and x > 0:
            return self._create_new_state(x, y, x-1, y, direction)  # Move up
        elif direction == 'down' and x < 2:
            return self._create_new_state(x, y, x+1, y, direction)  # Move down
        elif direction == 'left' and y > 0:
            return self._create_new_state(x, y, x, y-1, direction)  # Move left
        elif direction == 'right' and y < 2:
            return self._create_new_state(x, y, x, y+1, direction)  # Move right
        else:
            return None  # Invalid move

    def _create_new_state(self, x1, y1, x2, y2, direction):
        # Create a new puzzle state after a move
        new_board = copy.deepcopy(self.board)  # Copy current board state
        pos1, pos2 = x1 * 3 + y1, x2 * 3 + y2  # Calculate positions of the tiles to swap
        new_board[pos1], new_board[pos2] = new_board[pos2], new_board[pos1]  # Swap tiles
        new_actions = self.actions + [direction]  # Update actions taken
        return Puzzle8(new_board, new_actions, self)  # Store reference to the parent state

    def is_solved(self):
        # Check if the puzzle is solved (tiles in order)
        return self.board == list(range(1, 9)) + [0]

    def get_board(self):
        return self.board  # Return current board state

    def get_actions(self):
        return self.actions  # Return actions taken

    def get_possible_moves(self):
        # Generate all possible moves from the current state
        possible_moves = []
        for direction in ['up', 'down', 'left', 'right']:
            new_state = self.move(direction)  # Try each move
            if new_state:
                possible_moves.append(new_state)  # Add valid new state
        return possible_moves

    def __hash__(self):
        return hash(tuple(self.board))  # Hash function for the board

    def __eq__(self, other):
        return self.board == other.board  # Equality check for two boards

    def __lt__(self, other):
        """Define a comparison based on the number of moves performed."""
        return len(self.actions) < len(other.actions)  # Compare based on action length

class PuzzleSolver:
    def __init__(self, puzzle, method, depth_limit=None):
        self.puzzle = puzzle  # Current puzzle state
        self.method = method  # Method for solving (BFS, DFS, A*)
        self.visited = set()  # Set of visited states
        if self.method == "DFS":
            self.queue = [(self.puzzle, 0)]  # Stack for DFS with depth tracking
        elif self.method == "BFS":
            self.queue = deque([self.puzzle])  # Queue for BFS
        elif self.method == "A*":
            self.queue = []  # Priority queue for A*
            heapq.heappush(self.queue, (self._heuristic(self.puzzle), self.puzzle))
        self.state_count = 0  # Count of states visited
        self.depth_limit = depth_limit  # Limit for DFS depth

    def solve(self):
        if self.method == "DFS":
            return self._solve_dfs()
        elif self.method == "BFS":
            return self._solve_bfs()
        elif self.method == "A*":
            return self._solve_astar()
        return None, 0  # Default return if no method is matched

    def _solve_dfs(self):
        while self.queue:
            current_state, depth = self.queue.pop()  # Remove the next state for DFS
            self.state_count += 1  # Increment state count

            # Check if depth exceeds the limit
            if self.depth_limit is not None and depth > self.depth_limit:
                continue  # Skip states beyond the depth limit

            if current_state.is_solved():
                return self._reconstruct_path(current_state), self.state_count  # Return solution and count if solved

            for next_state in current_state.get_possible_moves():
                if next_state not in self.visited:
                    self.visited.add(next_state)
                    self.queue.append((next_state, depth + 1))  # Add the next state for DFS with depth

        return None, self.state_count  # Return None if no solution is found

    def _solve_bfs(self):
        while self.queue:
            current_state = self.queue.popleft()  # Remove the next state for BFS
            self.state_count += 1  # Increment state count

            if current_state.is_solved():
                return self._reconstruct_path(current_state), self.state_count  # Return solution and count if solved

            for next_state in current_state.get_possible_moves():
                if next_state not in self.visited:
                    self.visited.add(next_state)
                    self.queue.append(next_state)  # Add the next state for BFS

        return None, self.state_count  # Return None if no solution is found

    def _solve_astar(self):
        while self.queue:
            _, current_state = heapq.heappop(self.queue)  # Remove the state with the best score for A*
            self.state_count += 1  # Increment state count

            if current_state.is_solved():
                return self._reconstruct_path(current_state), self.state_count  # Return solution and count if solved

            for next_state in current_state.get_possible_moves():
                if next_state not in self.visited:
                    self.visited.add(next_state)
                    heapq.heappush(self.queue, (self._heuristic(next_state), next_state))  # Add the next state for A*

        return None, self.state_count  # Return None if no solution is found

    def _reconstruct_path(self, state):
        # Reconstruct the path of actions from the final state back to the initial state
        actions = []
        while state.parent:
            actions.append(state.actions[-1])  # Add the last action taken
            state = state.parent  # Move to the parent state
        return actions[::-1]  # Return the actions in the correct order

    def _heuristic(self, state):
        # Manhattan distance heuristic for A*
        return sum(abs(b % 3 - g % 3) + abs(b // 3 - g // 3)
                   for b, g in enumerate(state.get_board()) if b != 0)

class Puzzle8GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Puzzle 8 com IA")
        self.puzzle = Puzzle8()  # Initialize the puzzle

        # Main frame styling
        self.main_frame = tk.Frame(self.root, bg="#e0f7fa")
        self.main_frame.pack(pady=20)

        self.board_frame = tk.Frame(self.main_frame, bg="#e0f7fa")
        self.board_frame.pack()

        # Create buttons for the puzzle
        self.buttons = []
        for i in range(9):
            button = tk.Button(
                self.board_frame,
                font=('Helvetica', 24),
                width=4,
                height=2,
                relief="groove",
                bg="#4B0082",
                activebackground="#8A2BE2",
                fg="#ffffff"
            )
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)  # Position buttons in grid
            self.buttons.append(button)  # Add button to list

        # New game button to reset the puzzle
        self.new_game_button = tk.Button(self.main_frame, text="Novo Jogo", command=self.new_game,
                                         bg="#4B0082", fg="#ffffff", font=('Helvetica', 16))
        self.new_game_button.pack(pady=10)

        # Button to invoke AI solving options
        self.ia_button = tk.Button(self.main_frame, text="Resolver com IA", command=self.show_ia_options,
                                   bg="#4B0082", fg="#ffffff", font=('Helvetica', 16))
        self.ia_button.pack(pady=10)

        self.update_buttons()  # Initial button update
        # Bind arrow keys for manual movement
        self.root.bind('<Up>', self.key_press)
        self.root.bind('<Down>', self.key_press)
        self.root.bind('<Left>', self.key_press)
        self.root.bind('<Right>', self.key_press)

    def key_press(self, event):
        # Handle key press events for moving tiles
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
            new_puzzle = self.puzzle.move(direction)  # Try to move
            if new_puzzle:
                self.puzzle = new_puzzle  # Update puzzle state
                self.update_buttons()  # Refresh button display
                if self.puzzle.is_solved():
                    self.show_solved_message()  # Notify if solved

    def update_buttons(self):
        # Update button labels to reflect current board state
        board = self.puzzle.get_board()
        for i in range(9):
            text = str(board[i]) if board[i] != 0 else ''  # Set empty tile to blank
            self.buttons[i].config(text=text)  # Update button text

    def show_solved_message(self):
        # Display a message when the puzzle is solved
        messagebox.showinfo("Parabéns!", "Você resolveu o puzzle!")

    def show_ia_options(self):
        # Open a new window for AI solving options
        options_window = tk.Toplevel(self.root)
        options_window.title("Escolha uma IA")
        options_window.configure(bg="#9370DB")

        tk.Button(options_window, text="Busca em Largura", command=lambda: self.solve_with_ai("BFS"),
                  bg="#4B0082", fg="#ffffff").pack(pady=5)
        tk.Button(options_window, text="Busca em Profundidade", command=lambda: self.solve_with_ai("DFS"),
                  bg="#4B0082", fg="#ffffff").pack(pady=5)
        tk.Button(options_window, text="Busca A*", command=lambda: self.solve_with_ai("A*"),
                  bg="#4B0082", fg="#ffffff").pack(pady=5)

    def solve_with_ai(self, method):
        # Defina o limite de profundidade para a busca em profundidade (DFS)
        depth_limit = None
        if method == "DFS":
            # Define um limite de profundidade para DFS, caso seja necessário
            depth_limit = 5000  # Você pode ajustar esse valor conforme necessário

        # Inicializa o solver com o método selecionado e o limite de profundidade (apenas para DFS)
        solver = PuzzleSolver(self.puzzle, method, depth_limit=depth_limit)

        # Resolve o puzzle usando o método selecionado
        solution, states_visited = solver.solve()

        if solution:  # Se uma solução foi encontrada
            # Exibe a solução e o número de estados visitados
            messagebox.showinfo(f"Resolvido com {method}",
                                f"Solução encontrada com {states_visited} estados visitados:\n{solution}")
            for move in solution:
                new_puzzle = self.puzzle.move(move)  # Tenta realizar o movimento
                if new_puzzle:  # Verifica se o movimento é válido
                    self.puzzle = new_puzzle  # Atualiza o estado do puzzle
                    self.update_buttons()  # Atualiza a exibição dos botões
                else:
                    messagebox.showinfo(f"Erro", "Movimento inválido detectado durante a solução automática.")
        else:
            messagebox.showinfo(f"{method}", "Sem solução encontrada.")  # Notifica se nenhuma solução for encontrada

    def new_game(self):
        # Reset the puzzle for a new game
        self.puzzle = Puzzle8()  # Generate a new puzzle
        self.update_buttons()  # Refresh button display


if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    Puzzle8GUI(root)  # Initialize the GUI
    root.mainloop()  # Start the Tkinter event loop
