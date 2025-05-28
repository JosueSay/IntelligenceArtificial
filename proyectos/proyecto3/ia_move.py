def ai_move(board, player):
    import time 
    from copy import deepcopy 
    TIME_LIMIT = 3
    MAX_DEPTH = 3

    # --- Aperturas recomendadas ---
    OPENING_BOOK = {
        ((2, 3), (2, 2)): (3, 2),  # diagonal paralela
        ((2, 3), (3, 2)): (2, 4),  # diagonal perpendicular
        ((2, 3), (2, 4)): (3, 2),  # perpendicular desplazada
    }

    def heuristic(b, p):
        return sum(cell == p for row in b for cell in row) - \
               sum(cell == -p for row in b for cell in row)

    def apply_move(b, move, p):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1),  (1, 0), (1, 1)]
        new_board = deepcopy(b)
        x, y = move
        new_board[x][y] = p
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            line = []
            while 0 <= nx < 8 and 0 <= ny < 8 and new_board[nx][ny] == -p:
                line.append((nx, ny))
                nx += dx
                ny += dy
            if 0 <= nx < 8 and 0 <= ny < 8 and new_board[nx][ny] == p:
                for fx, fy in line:
                    new_board[fx][fy] = p
        return new_board

    def minimax(b, p, depth, maximizing, start):
        if depth == 0 or time.time() - start > TIME_LIMIT - 0.1:
            return heuristic(b, player), None
        moves = valid_movements(b, p)
        if not moves:
            return heuristic(b, player), None
        best_move = None
        if maximizing:
            max_eval = float("-inf")
            for m in moves:
                nb = apply_move(b, m, p)
                eval_score, _ = minimax(nb, -p, depth - 1, False, start)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = m
            return max_eval, best_move
        else:
            min_eval = float("inf")
            for m in moves:
                nb = apply_move(b, m, p)
                eval_score, _ = minimax(nb, -p, depth - 1, True, start)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = m
            return min_eval, best_move

    def extract_history(b):
        initial = [[0]*8 for _ in range(8)]
        initial[3][3] = 1
        initial[4][4] = 1
        initial[3][4] = -1
        initial[4][3] = -1
        moves = []
        for i in range(8):
            for j in range(8):
                if b[i][j] != initial[i][j]:
                    moves.append((i, j))
        return tuple(moves[:2]) if len(moves) >= 2 else None

    # --- INICIO ---
    start_time = time.time()
    valid_moves = valid_movements(board, player)
    if not valid_moves:
        return None

    # Fase 1: apertura
    history = extract_history(board)
    if history in OPENING_BOOK:
        move = OPENING_BOOK[history]
        if move in valid_moves:
            return move

    # Fase 2: medio juego
    if len(valid_moves) > 6:
        _, best = minimax(board, player, MAX_DEPTH, True, start_time)
        if best:
            return best

    # Fase 3: final con más profundidad
    _, best = minimax(board, player, MAX_DEPTH + 2, True, start_time)
    
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"[IA] Tiempo de respuesta: {elapsed:.4f} segundos")
    return best or random.choice(valid_moves)

def move(board, player, x, y):
    if (x, y) not in valid_movements(board, player):
        return board  # Movimiento inválido, no se cambia nada

    board[x][y] = player
    opponent = -player

    for dx, dy in DIRECTIONS:
        i, j = x + dx, y + dy
        path = []

        while in_bounds(i, j) and board[i][j] == opponent:
            path.append((i, j))
            i += dx
            j += dy

        if path and in_bounds(i, j) and board[i][j] == player:
            for px, py in path:
                board[px][py] = player

    return board