from othello_ai import ai_move, valid_movements, in_bounds
import copy

def print_board(board):
    symbols = {0: ".", 1: "W", -1: "B"}
    print("  " + " ".join(str(i) for i in range(8)))
    for i, row in enumerate(board):
        print(i, " ".join(symbols[cell] for cell in row))
    print()

def make_move(board, player, x, y):
    from othello_ai import move
    return move(copy.deepcopy(board), player, x, y)

def play_vs_ai():
    board = [[0]*8 for _ in range(8)]
    board[3][3], board[4][4] = 1, 1
    board[3][4], board[4][3] = -1, -1

    while True:
        first = input("¿Quieres empezar tú? (s/n): ").strip().lower()
        if first in ["s", "n"]:
            break
        print("Entrada inválida. Escribe 's' para sí o 'n' para no.")

    if first == "s":
        human_color = -1
        print("Comienzas tú (B = Negro). La IA es blanco (W).")
    else:
        human_color = 1
        print("La IA comienza como negro (B). Tú juegas como blanco (W).")

    current_player = -1  # Siempre inicia el negro

    while True:
        print_board(board)
        valid = valid_movements(board, current_player)
        if not valid:
            print(f"No hay movimientos válidos para {'B' if current_player == -1 else 'W'}")
            current_player *= -1
            continue

        if current_player == human_color:
            print("Tus movimientos válidos:", valid)
            try:
                x, y = map(int, input("Ingresa tu movimiento (x y): ").split())
                if (x, y) not in valid:
                    print("Movimiento inválido. Intenta de nuevo.")
                    continue
            except:
                print("Entrada inválida. Usa formato: 2 3")
                continue
        else:
            x, y = ai_move(board, current_player)
            print(f"La IA juega en: ({x}, {y})")

        board = make_move(board, current_player, x, y)
        current_player *= -1

        # Fin del juego
        if not valid_movements(board, -1) and not valid_movements(board, 1):
            black = sum(row.count(-1) for row in board)
            white = sum(row.count(1) for row in board)
            print_board(board)
            print(f"Fin del juego. Puntuación - Negro (B): {black}, Blanco (W): {white}")
            if (human_color == -1 and black > white) or (human_color == 1 and white > black):
                print("¡Ganaste!")
            elif black == white:
                print("Empate.")
            else:
                print("La IA gana.")
            break

if __name__ == "__main__":
    play_vs_ai()
