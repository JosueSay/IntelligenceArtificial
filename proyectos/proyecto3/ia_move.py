def ai_move(board, player):
    """
    IA para Othello/Reversi con:
        • heurística enriquecida  (esquinas, movilidad, piezas peligrosas…)
        • poda alfa-beta + ordenación de jugadas
        • profundidad adaptada  (medio-juego vs final + barrido completo)
        • pequeño libro de aperturas
    Supone la existencia de   valid_movements(board, player) → list[(x,y)].
    """
    import time, random
    from copy import deepcopy

    # -------------- Parámetros globales -----------------
    TIME_LIMIT  = 3.0          # segundos por movimiento
    MID_DEPTH   = 3            # profundidad “normal”
    END_DEPTH   = 5            # final largo, pero con heurística
    SWEEP_LIMIT = 12           # ≤12 huecos ⇒ barrido exacto
    INF         = float("inf")

    # -------------- Libro de aperturas ----------
    OPENING_BOOK = {
        ((2, 3), (2, 2)): (3, 2),  # diagonal paralela
        ((2, 3), (3, 2)): (2, 4),  # diagonal perpendicular
        ((2, 3), (2, 4)): (3, 2),  # perpendicular desplazada
    }

    # -------------- Heurística ------------------
    CORNERS   = {(0, 0), (0, 7), (7, 0), (7, 7)}
    X_SQUARES = {(1, 1), (1, 6), (6, 1), (6, 6)}
    C_SQUARES = {(0, 1), (1, 0), (0, 6), (1, 7),
                 (6, 0), (7, 1), (6, 7), (7, 6)}

    def heuristic(b, p):
        """Evaluación estática desde el punto de vista de `p`."""
        my  = sum(r.count(p)   for r in b)
        opp = sum(r.count(-p)  for r in b)
        score = my - opp

        # esquinas y zonas críticas
        for (x, y) in CORNERS:
            if   b[x][y] == p:   score += 25
            elif b[x][y] == -p:  score -= 25
        for (x, y) in X_SQUARES:
            if   b[x][y] == p:   score -= 12
            elif b[x][y] == -p:  score += 12
        for (x, y) in C_SQUARES:
            if   b[x][y] == p:   score -= 8
            elif b[x][y] == -p:  score += 8

        # movilidad
        score += 2 * (len(valid_movements(b, p)) -
                      len(valid_movements(b, -p)))
        return score

    # -------------- Generar un tablero tras mover --------
    def apply_move(b, move, p):
        nb = deepcopy(b)
        x, y = move
        nb[x][y] = p
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            line = []
            while 0 <= nx < 8 and 0 <= ny < 8 and nb[nx][ny] == -p:
                line.append((nx, ny))
                nx += dx
                ny += dy
            if 0 <= nx < 8 and 0 <= ny < 8 and nb[nx][ny] == p:
                for fx, fy in line:
                    nb[fx][fy] = p
        return nb

    # -------------- Ordenación de jugadas ----------------
    def order_moves(moves):
        """Prioriza esquinas > evitar X-square > resto."""
        def key(m):
            if m in CORNERS:   return 0
            if m in X_SQUARES: return 2
            return 1
        return sorted(moves, key=key)

    # -------------- Minimax con poda alfa-beta ------------
    def alphabeta(b, p, depth, α, β, start):
        # Corte por tiempo
        if time.time() - start > TIME_LIMIT - 0.05:
            return heuristic(b, player), None

        moves = valid_movements(b, p)

        # Sin movimientos: ¿terminó la partida?
        if not moves:
            opp_moves = valid_movements(b, -p)
            if not opp_moves:                     # ambos pasan → posición terminal
                exact = sum(r.count(player) - r.count(-player) for r in b)
                return exact, None
            # Pasa turno
            return alphabeta(b, -p, depth, α, β, start)[0] * -1, None

        # Profundidad cero
        if depth == 0:
            return heuristic(b, player), None

        best_move = None
        if p == player:  # ------- MAX -------
            value = -INF
            for m in order_moves(moves):
                nb = apply_move(b, m, p)
                score, _ = alphabeta(nb, -p, depth - 1, α, β, start)
                if score > value:
                    value, best_move = score, m
                α = max(α, value)
                if α >= β:
                    break                          # poda β
            return value, best_move
        else:             # ------- MIN -------
            value = INF
            for m in order_moves(moves):
                nb = apply_move(b, m, p)
                score, _ = alphabeta(nb, -p, depth - 1, α, β, start)
                if score < value:
                    value, best_move = score, m
                β = min(β, value)
                if α >= β:
                    break                          # poda α
            return value, best_move

    # -------------- Historia para el libro ---------------
    def extract_history(b):
        initial = [[0]*8 for _ in range(8)]
        initial[3][3] = initial[4][4] =  1
        initial[3][4] = initial[4][3] = -1
        moves = [(i, j)
                 for i in range(8)
                 for j in range(8)
                 if b[i][j] != initial[i][j]]
        return tuple(moves[:2]) if len(moves) >= 2 else None

    # -------------- Flujo principal ----------------------
    start = time.time()
    moves = valid_movements(board, player)
    if not moves:                                # sin jugadas
        return None

    # Fase 1 : libro de aperturas
    hist = extract_history(board)
    if hist in OPENING_BOOK and OPENING_BOOK[hist] in moves:
        return OPENING_BOOK[hist]

    # Fase 2 / 3 : búsqueda con profundidad adaptativa
    empties = sum(cell == 0 for row in board for cell in row)

    if empties <= SWEEP_LIMIT:
        depth = empties          # barrido completo (valor exacto)
    else:
        depth = MID_DEPTH if len(moves) > 6 else END_DEPTH

    _, best = alphabeta(board, player, depth, -INF, INF, start)

    # Último recurso: aleatorio
    if best is None:
        best = random.choice(moves)

    print(f"[IA] Tiempo de cálculo: {time.time() - start:.3f}s")
    return best

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
