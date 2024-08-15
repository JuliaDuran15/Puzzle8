import random
import copy

# Classe que representa o jogo do Puzzle 8
class Puzzle8:
    def __init__(self, board=None, actions=None):
        # O método __init__ é o construtor da classe. Ele inicializa o tabuleiro do puzzle.
        # Se 'board' não for fornecido, ele gera um tabuleiro solucionável aleatório.
        # 'actions' é uma lista que armazena os movimentos realizados; se não for fornecida, começa como uma lista vazia.
        if board is None:
            board = self._generate_solvable_board()
        self.board = board  # Armazena o estado atual do tabuleiro
        self.empty_pos = self.board.index(0)  # Encontra a posição do espaço vazio (representado por 0)
        self.actions = actions if actions is not None else []  # Armazena as ações (movimentos) realizados até o momento

    def _generate_solvable_board(self):
        # Gera um tabuleiro aleatório que seja solucionável
        board = list(range(9))  # Cria uma lista de 0 a 8
        random.shuffle(board)  # Embaralha a lista
        while not self._is_solvable(board):  # Continua embaralhando até que o tabuleiro seja solucionável
            random.shuffle(board)
        return board  # Retorna um tabuleiro solucionável

    def _is_solvable(self, board):
        # Verifica se o tabuleiro é solucionável
        inversions = 0
        # Conta o número de inversões no tabuleiro
        for i in range(8):
            for j in range(i + 1, 9):
                if board[i] > board[j] > 0:
                    inversions += 1
        # Se o número de inversões for par, o puzzle é solucionável
        return inversions % 2 == 0

    def print_board(self):
        # Imprime o tabuleiro no console de forma visualmente organizada
        for i in range(3):
            print(self.board[i*3:(i+1)*3])  # Imprime três linhas de três elementos cada
        print()

    def move(self, direction):
        # Move o espaço vazio (0) em uma direção especificada, se possível, e retorna um novo estado (novo objeto Puzzle8)
        x, y = divmod(self.empty_pos, 3)  # Converte a posição linear do espaço vazio para coordenadas x, y
        if direction == 'up' and x > 0:  # Movimento para cima
            return self._create_new_state(x, y, x-1, y, direction)
        elif direction == 'down' and x < 2:  # Movimento para baixo
            return self._create_new_state(x, y, x+1, y, direction)
        elif direction == 'left' and y > 0:  # Movimento para a esquerda
            return self._create_new_state(x, y, x, y-1, direction)
        elif direction == 'right' and y < 2:  # Movimento para a direita
            return self._create_new_state(x, y, x, y+1, direction)
        else:
            print("Movimento inválido!")  # Caso o movimento não seja possível, exibe uma mensagem
            return None

    def _create_new_state(self, x1, y1, x2, y2, direction):
        # Cria um novo estado do puzzle após um movimento
        new_board = copy.deepcopy(self.board)  # Cria uma cópia profunda do tabuleiro atual para preservar o estado anterior
        pos1, pos2 = x1 * 3 + y1, x2 * 3 + y2  # Converte coordenadas x, y para posições lineares no tabuleiro
        new_board[pos1], new_board[pos2] = new_board[pos2], new_board[pos1]  # Troca o espaço vazio com a peça vizinha
        new_actions = self.actions + [direction]  # Adiciona a ação (movimento) à lista de ações
        return Puzzle8(new_board, new_actions)  # Retorna um novo objeto Puzzle8 com o novo estado e as ações atualizadas

    def is_solved(self):
        # Verifica se o puzzle está resolvido (ou seja, se o tabuleiro está em ordem crescente com 0 no final)
        return self.board == list(range(1, 9)) + [0]

    def print_actions(self):
        # Imprime a sequência de ações realizadas até o momento
        print("Ações executadas: ", " -> ".join(self.actions))

# Simulação do jogo
puzzle = Puzzle8()  # Cria um novo puzzle 8 com um tabuleiro aleatório solucionável

while not puzzle.is_solved():
    # Loop que continua até que o puzzle seja resolvido ou o usuário saia do jogo
    puzzle.print_board()  # Exibe o estado atual do tabuleiro
    move = input("Faça um movimento (up, down, left, right) ou 'exit' para sair: ")  # Solicita um movimento ao usuário
    if move.lower() == "exit":
        print("Você saiu do jogo.")  # Se o usuário digitar "exit", o jogo termina
        break
    new_puzzle = puzzle.move(move)  # Tenta realizar o movimento e gerar um novo estado
    if new_puzzle:
        puzzle = new_puzzle  # Atualiza o estado atual do puzzle com o novo estado
        puzzle.print_actions()  # Imprime as ações realizadas até o momento

if puzzle.is_solved():
    # Se o puzzle for resolvido, exibe o estado final e parabeniza o usuário
    puzzle.print_board()  # Exibe o estado final do tabuleiro
    print("Parabéns! Você resolveu o puzzle!")
    puzzle.print_actions()  # Imprime a sequência de ações que levou à solução
