import random
import time
from TicTacToe import TicTacToe

def heuristic(game):
    winner = game.getWinner()
    if winner == 'X':
        return 1.0
    elif winner == 'O':
        return -1.0
    elif winner == 'D':
        return 0.0
    
    score = 0.0
    lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
             (0, 3, 6), (1, 4, 7), (2, 5, 8),
             (0, 4, 8), (2, 4, 6)]
    
    for i, j, k in lines:
        x_count = sum(1 for idx in [i, j, k] if game.board[idx] == 'X')
        o_count = sum(1 for idx in [i, j, k] if game.board[idx] == 'O')
        if x_count > 0 and o_count == 0:
            score += 0.1 * x_count
        if o_count > 0 and x_count == 0:
            score -= 0.1 * o_count
    
    return score

def minimax(game, depth, max_player):
    nodes_explored = 1
    if game.isTerminal() or depth == 0:
        return heuristic(game), None, nodes_explored
    
    if max_player:
        best_val = float('-inf')
        best_move = None
    else:
        best_val = float('inf')
        best_move = None
    
    for move in game.availableMoves():
        new_game = game.clone()
        new_game.makeMove(move)
        val, _, child_nodes = minimax(new_game, depth - 1, not max_player)
        nodes_explored += child_nodes
        
        if max_player and val > best_val:
            best_val = val
            best_move = move
        elif not max_player and val < best_val:
            best_val = val
            best_move = move
    
    return best_val, best_move, nodes_explored

def minimax_alpha_beta(game, depth, alpha, beta, max_player):
    nodes_explored = 1
    if game.isTerminal() or depth == 0:
        return heuristic(game), None, nodes_explored
    
    if max_player:
        best_val = float('-inf')
        best_move = None
    else:
        best_val = float('inf')
        best_move = None
    
    for move in game.availableMoves():
        new_game = game.clone()
        new_game.makeMove(move)
        val, _, child_nodes = minimax_alpha_beta(new_game, depth - 1, alpha, beta, not max_player)
        nodes_explored += child_nodes
        
        if max_player:
            if val > best_val:
                best_val = val
                best_move = move
            alpha = max(alpha, best_val)
        else:
            if val < best_val:
                best_val = val
                best_move = move
            beta = min(beta, best_val)
        
        if beta <= alpha:
            break
    
    return best_val, best_move, nodes_explored

def get_best_move(game, method='minimax', depth=3):
    max_player = game.currentPlayer == 'X'
    
    if method == 'minimax':
        _, move, nodes = minimax(game, depth, max_player)
    else:
        _, move, nodes = minimax_alpha_beta(game, depth, float('-inf'), float('inf'), max_player)
    
    return move, nodes

def play_random_move(game):
    moves = game.availableMoves()
    if moves:
        return random.choice(moves)
    return None

def run_experiment(method='minimax', depth=3, num_games=1000, player_starts=True):
    wins = 0
    losses = 0
    draws = 0
    total_nodes = 0
    
    for _ in range(num_games):
        game = TicTacToe()
        
        if not player_starts:
            game.currentPlayer = 'O'
            random_move = play_random_move(game)
            game.makeMove(random_move)
        
        while not game.isTerminal():
            if game.currentPlayer == 'X':
                move, nodes = get_best_move(game, method, depth)
                total_nodes += nodes
                game.makeMove(move)
            else:
                move = play_random_move(game)
                game.makeMove(move)
        
        winner = game.getWinner()
        if winner == 'X':
            wins += 1
        elif winner == 'O':
            losses += 1
        else:
            draws += 1
    
    avg_nodes = total_nodes / num_games
    return wins, draws, losses, avg_nodes

depth = 3
num_games = 1000

print("Seleccione el algoritmo a utilizar:")
print("1. Minimax con profundidad limitada")
print("2. Minimax con poda Alpha-Beta")

option = input("Opción \t[1]\t[2]: ")

method = 'minimax' if option == '1' else 'alpha_beta'

print(f"\nEjecutando {num_games} juegos con {method} (profundidad {depth})...")
print("Jugador X (algoritmo) comienza...")

start_time = time.time()
wins_x, draws_x, losses_x, avg_nodes_x = run_experiment(method, depth, num_games, True)
x_time = time.time() - start_time

print("\nJugador O (aleatorio) comienza...")

start_time = time.time()
wins_o, draws_o, losses_o, avg_nodes_o = run_experiment(method, depth, num_games, False)
o_time = time.time() - start_time

total_wins = wins_x + wins_o
total_draws = draws_x + draws_o
total_losses = losses_x + losses_o
avg_nodes = (avg_nodes_x + avg_nodes_o) / 2

print("\nResultados finales:")
print(f"Algoritmo: {method.upper()}")
print(f"Profundidad de búsqueda: {depth}")
print(f"Total de juegos: {num_games * 2}")
print(f"Victorias: {total_wins} ({total_wins/(num_games*2)*100:.2f}%)")
print(f"Empates: {total_draws} ({total_draws/(num_games*2)*100:.2f}%)")
print(f"Derrotas: {total_losses} ({total_losses/(num_games*2)*100:.2f}%)")
print(f"Nodos explorados promedio por juego: {avg_nodes:.2f}")
print(f"Tiempo total: {x_time + o_time:.2f} segundos")

print("\nDesglose por quien comienza:")
print("X (algoritmo) comienza:")
print(f"  Victorias: {wins_x} ({wins_x/num_games*100:.2f}%)")
print(f"  Empates: {draws_x} ({draws_x/num_games*100:.2f}%)")
print(f"  Derrotas: {losses_x} ({losses_x/num_games*100:.2f}%)")
print(f"  Nodos explorados promedio: {avg_nodes_x:.2f}")

print("\nO comienza:")
print(f"  Victorias: {wins_o} ({wins_o/num_games*100:.2f}%)")
print(f"  Empates: {draws_o} ({draws_o/num_games*100:.2f}%)")
print(f"  Derrotas: {losses_o} ({losses_o/num_games*100:.2f}%)")
print(f"  Nodos explorados promedio: {avg_nodes_o:.2f}")

