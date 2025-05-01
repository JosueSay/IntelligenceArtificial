class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.currentPlayer = 'X'
    
    def clone(self):
        clone = TicTacToe()
        clone.board = self.board[:]
        clone.currentPlayer = self.currentPlayer
        return clone

    # devolverá una lista de índices disponibles para jugar
    def availableMoves(self):
        return [i for i, v in enumerate(self.board) if v == ' ']

    def makeMove(self, idx):
        if self.board[idx] != ' ':
            return False
        self.board[idx] = self.currentPlayer
        self.currentPlayer = 'O' if self.currentPlayer == 'X' else 'X'
        return True

    # verifica si el juego ha terminado, ya sea por victoria o empate 'D'
    def isTerminal(self):
        return self.getWinner() is not None or all(v != ' ' for v in self.board)

    def getWinner(self):
        wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for i, j, k in wins:
            if self.board[i] == self.board[j] == self.board[k] != ' ':
                return self.board[i]
        return None if ' ' in self.board else 'D'

    def score(self):
        winner = self.getWinner()
        if winner == 'X':
            return 1
        elif winner == 'O':
            return -1
        else:
            return 0
