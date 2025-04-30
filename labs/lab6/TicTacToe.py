import random

class TicTacToe:
  def __init__(self, user_player='X'):
    self.board = [[' ' for _ in range(3)] for _ in range(3)]
    self.players = ['X', 'O']
    
    if user_player not in self.players:
      raise ValueError("Invalid player. Choose 'X' or 'O'.")
    
    self.user_player = user_player
    self.computer_player = self.otherPlayer(user_player)
    self.current_player = random.choice(self.players)
    
    print(f"You are '{self.user_player}'.")
    print(f"Player {self.current_player} starts the game!")
  
  def otherPlayer(self, player):
    return self.players[1] if player == self.players[0] else self.players[0]
  
  def nextPlayer(self):
    return self.otherPlayer(self.current_player)
    
  def printBoard(self):
    for row in self.board:
      print('|'.join(row))
      print('-' * 5)
      
  def makeMove(self, row, col):
    if self.board[row][col] == ' ':
      self.board[row][col] = self.current_player
      self.nextPlayer()
      return True
    return False
  
  def veriffyWinner(self):
    # Verifica filas
    for row in self.board:
      if row[0] != ' ' and row[0] == row[1] == row[2]:
        return 1 if row[0] == self.user_player else -1

    # Verifica columnas
    for col in range(3):
      if self.board[0][col] != ' ' and self.board[0][col] == self.board[1][col] == self.board[2][col]:
        return 1 if self.board[0][col] == self.user_player else -1

    # Verifica diagonales
    if self.board[0][0] != ' ' and self.board[0][0] == self.board[1][1] == self.board[2][2]:
      return 1 if self.board[0][0] == self.user_player else -1

    if self.board[0][2] != ' ' and self.board[0][2] == self.board[1][1] == self.board[2][0]:
      return 1 if self.board[0][2] == self.user_player else -1

    # Si no hay ganador, pero el tablero está lleno, es empate
    if all(cell != ' ' for row in self.board for cell in row):
      return 0

    # Si no hay ganador y el juego no ha terminado, retorna None
    return None
  
  def printWinner(self):
    winner = self.veriffyWinner()
    if winner is None:
      print("Game is still ongoing.")
    elif winner == 0:
      print("It's a draw!")
    elif winner == 1:
      print("You win!")
    elif winner == -1:
      print("Computer wins!")
      
# game = TicTacToe(user_player='X')
# game.printBoard()