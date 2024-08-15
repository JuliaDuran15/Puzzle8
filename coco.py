import random

class Puzzle8:
    def __init__(self, board=None):
        if board is None:
            board = self._generate_solvable_board()
        self.board = board
        self.empty_pos = self.board.index(0)

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
        # Se o número de inversões for par, o puzzle é solucionável
        return inversions % 2 == 0

    def print_board(self):
        for i in range(3):
            print(self.board[i*3:(i+1)*3])
        print()

    def move(self, direction):
        x, y = divmod(self.empty_pos, 3)
        if direction == 'up' and x > 0:
            self._swap(x, y, x-1, y)
        elif direction == 'down' and x < 2:
            self._swap(x, y, x+1, y)
        elif direction == 'left' and y > 0:
            self._swap(x, y, x, y-1)
        elif direction == 'right' and y < 2:
            self._swap(x, y, x, y+1)
        else:
            print("Movimento inválido!")

    def _swap(self, x1, y1, x2, y2):
        pos1, pos2 = x1 * 3 + y1, x2 * 3 + y2
        self.board[pos1], self.board[pos2] = self.board[pos2], self.board[pos1]
        self.empty_pos = pos2

    def is_solved(self):
        return self.board == list(range(1, 9)) + [0]

# Simulação
puzzle = Puzzle8()

while not puzzle.is_solved():
    puzzle.print_board()
    move = input("Faça um movimento (up, down, left, right) ou 'exit' para sair: ")
    if move.lower() == "exit":
        print("Você saiu do jogo.")
        break
    puzzle.move(move)

if puzzle.is_solved():
    print("Parabéns! Você resolveu o puzzle!")
