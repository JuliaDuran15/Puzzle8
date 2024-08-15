import random
import copy

class Puzzle8:
    def __init__(self, board=None, actions=None, history=None):
        # Inicializa o tabuleiro, as ações, e o histórico
        if board is None:
            board = self._generate_solvable_board()
        self.board = board
        self.empty_pos = self.board.index(0)
        self.actions = actions if actions is not None else []
        self.history = history if history is not None else []  # Inicializa o histórico, se não for fornecido, começa vazio

    def _generate_solvable_board(self):
        # Gera um tabuleiro solucionável
        board = list(range(9))
        random.shuffle(board)
        while not self._is_solvable(board):
            random.shuffle(board)
        return board

    def _is_solvable(self, board):
        # Verifica se o tabuleiro é solucionável
        inversions = 0
        for i in range(8):
            for j in range(i + 1, 9):
                if board[i] > board[j] > 0:
                    inversions += 1
        return inversions % 2 == 0

    def print_board(self):
        # Imprime o tabuleiro atual
        for i in range(3):
            print(self.board[i*3:(i+1)*3])
        print()

    def move(self, direction):
        # Move o espaço vazio na direção especificada
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
            print("Movimento inválido!")
            return None

    def _create_new_state(self, x1, y1, x2, y2, direction):
        # Cria um novo estado após o movimento
        new_board = copy.deepcopy(self.board)
        pos1, pos2 = x1 * 3 + y1, x2 * 3 + y2
        new_board[pos1], new_board[pos2] = new_board[pos2], new_board[pos1]
        new_actions = self.actions + [direction]
        new_history = copy.deepcopy(self.history)  # Copia o histórico anterior
        new_history.append(self.board)  # Adiciona o tabuleiro atual ao histórico
        return Puzzle8(new_board, new_actions, new_history)  # Agora passando o histórico corretamente

    def is_solved(self):
        # Verifica se o puzzle foi resolvido
        return self.board == list(range(1, 9)) + [0]

    def print_actions(self):
        # Imprime as ações realizadas
        print("Ações executadas: ", " -> ".join(self.actions))

    def print_history(self):
        # Imprime o histórico de todos os tabuleiros anteriores
        for i, board in enumerate(self.history):
            print(f"Rodada {i+1}:")
            for j in range(3):
                print(board[j*3:(j+1)*3])
            print()
        print("Estado atual:")
        self.print_board()

# Simulação do jogo
puzzle = Puzzle8()

while not puzzle.is_solved():
    puzzle.print_board()
    move = input("Faça um movimento (up, down, left, right), 'history' para ver todas as rodadas ou 'exit' para sair: ")
    if move.lower() == "exit":
        print("Você saiu do jogo.")
        break
    elif move.lower() == "history":
        puzzle.print_history()  # Exibe o histórico completo
    else:
        new_puzzle = puzzle.move(move)
        if new_puzzle:
            puzzle = new_puzzle
            puzzle.print_actions()

if puzzle.is_solved():
    puzzle.print_board()
    print("Parabéns! Você resolveu o puzzle!")
    puzzle.print_actions()
