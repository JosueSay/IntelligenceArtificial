def ai_move(board, player):
    """
    IA para Othello / Reversi con:

        - heurística
        - poda alfa-beta con ordenación de jugadas
        - profundidad adaptada (medio-juego vs final + barrido exacto)
        - libros de apertura diferenciados por color
        - control de “time-out” con jugada aleatoria

    El tablero contiene  1 = blancas   |   -1 = negras   |   0 = vacío
    """

    import time, random
    from copy import deepcopy

    # -------------------------------------------------------
    #               PARÁMETROS GLOBALES
    # -------------------------------------------------------
    TIME_LIMIT  = 3.0      # seg. máximos de cómputo por movimiento
    MID_DEPTH   = 3        # profundidad “normal” en apertura/medio-juego
    END_DEPTH   = 5        # profundidad cuando el final aún es largo
    SWEEP_LIMIT = 12       # ≤ 12 huecos ⇒ barrido exacto (búsqueda exhaustiva)
    INF         = float("inf")

    # -------------------------------------------------------
    #               LIBROS DE APERTURA
    #   Blancas y negras usan secuencias diferentes
    # -------------------------------------------------------
    OPENING_BOOK_WHITE = {
        ((2, 3), (2, 2)): (3, 2),    # diagonal paralela
        ((2, 3), (3, 2)): (2, 4),    # diagonal perpendicular
        ((2, 3), (2, 4)): (3, 2),    # perpendicular desplazada
    }

    OPENING_BOOK_BLACK = {
        ((5, 4), (5, 5)): (4, 5),    # simétrico para negras
        ((5, 4), (4, 5)): (5, 3),
        ((5, 4), (5, 3)): (4, 5),
    }

    # -------------------------------------------------------
    #               CONSTANTES DE HEURÍSTICA
    # -------------------------------------------------------
    CORNERS   = {(0, 0), (0, 7), (7, 0), (7, 7)}
    X_SQUARES = {(1, 1), (1, 6), (6, 1), (6, 6)}
    C_SQUARES = {(0, 1), (1, 0), (0, 6), (1, 7),
                 (6, 0), (7, 1), (6, 7), (7, 6)}

    # -------------------------------------------------------
    #               FUNCIÓN HEURÍSTICA
    # -------------------------------------------------------
    def heuristic(b, p):
        """Valoración estática de un tablero desde el punto de vista `p`."""

        # Diferencia simple de fichas
        my  = sum(r.count(p)  for r in b)
        opp = sum(r.count(-p) for r in b)
        score = my - opp

        # Esquinas y casillas críticas
        for (x, y) in CORNERS:
            if   b[x][y] == p:   score += 25
            elif b[x][y] == -p:  score -= 25
        for (x, y) in X_SQUARES:
            if   b[x][y] == p:   score -= 12
            elif b[x][y] == -p:  score += 12
        for (x, y) in C_SQUARES:
            if   b[x][y] == p:   score -=  8
            elif b[x][y] == -p:  score +=  8

        # Movilidad
        score += 2 * (len(valid_movements(b, p))
                      - len(valid_movements(b, -p)))

        return score

    # -------------------------------------------------------
    #               GENERAR TABLERO TRAS MOVER
    # -------------------------------------------------------
    def apply_move(b, move, p):
        """Devuelve un nuevo tablero resultante de jugar `move` con color `p`."""
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

    # -------------------------------------------------------
    #               ORDENACIÓN DE MOVIMIENTOS
    # -------------------------------------------------------
    def order_moves(moves):
        """Prioriza esquinas > evita X-squares > resto."""
        def key(m):
            if m in CORNERS:   return 0
            if m in X_SQUARES: return 2
            return 1
        return sorted(moves, key=key)

    # -------------------------------------------------------
    #               MINIMAX + PODA ALFA-BETA
    # -------------------------------------------------------
    def alphabeta(b, p, depth, alpha, beta, start):
        # Corte por tiempo
        if time.time() - start > TIME_LIMIT - 0.05:
            return heuristic(b, player), None

        moves = valid_movements(b, p)

        # Sin movimientos: pasa turno o final de partida
        if not moves:
            opp_moves = valid_movements(b, -p)
            if not opp_moves:  # ambos pasan
                exact = sum(r.count(player) - r.count(-player) for r in b)
                return exact, None
            return alphabeta(b, -p, depth, alpha, beta, start)[0] * -1, None

        if depth == 0:
            return heuristic(b, player), None

        best_move = None
        if p == player:  # MAX
            value = -INF
            for m in order_moves(moves):
                score, _ = alphabeta(apply_move(b, m, p), -p,
                                     depth - 1, alpha, beta, start)
                if score > value:
                    value, best_move = score, m
                alpha = max(alpha, value)
                if alpha >= beta:
                    break   # poda beta
            return value, best_move
        else:              # MIN
            value = INF
            for m in order_moves(moves):
                score, _ = alphabeta(apply_move(b, m, p), -p,
                                     depth - 1, alpha, beta, start)
                if score < value:
                    value, best_move = score, m
                beta = min(beta, value)
                if alpha >= beta:
                    break   # poda alfa
            return value, best_move

    # -------------------------------------------------------
    #               EXTRAER HISTÓRICO (2 primeras jugadas)
    # -------------------------------------------------------
    def extract_history(b):
        """Extrae las primeras dos jugadas que ya se hicieron en la partida"""
        initial = [[0]*8 for _ in range(8)]
        initial[3][3] = initial[4][4] =  1   # blancas
        initial[3][4] = initial[4][3] = -1   # negras
        moves = [(i, j)
                 for i in range(8)
                 for j in range(8)
                 if b[i][j] != initial[i][j]]
        return tuple(moves[:2]) if len(moves) >= 2 else None

    # =======================================================
    #                   FLUJO PRINCIPAL
    # =======================================================
    start = time.time()
    moves = valid_movements(board, player)
    if not moves:           # sin jugadas posibles
        return None

    # --- FASE 1 : APERTURA (según color) ---
    hist = extract_history(board)
    if player == 1:  # blancas
        if hist in OPENING_BOOK_WHITE and OPENING_BOOK_WHITE[hist] in moves:
            return OPENING_BOOK_WHITE[hist]
    else:            # negras
        if hist in OPENING_BOOK_BLACK and OPENING_BOOK_BLACK[hist] in moves:
            return OPENING_BOOK_BLACK[hist]

    # --- FASE 2 / 3 : BÚSQUEDA ---
    empties = sum(cell == 0 for row in board for cell in row)

    if empties <= SWEEP_LIMIT:     # barrido completo (valor exacto)
        depth = empties
    else:                          # profundidad adaptativa
        depth = MID_DEPTH if len(moves) > 6 else END_DEPTH

    _, best = alphabeta(board, player, depth, -INF, INF, start)

    # --- FASE 4 : BACK-UP por tiempo agotado / error ---
    if best is None:
        best = random.choice(moves)
        print(f"[IA] Movimiento ALEATORIO (time-out). "
              f"Tiempo: {time.time() - start:.3f}s")
    else:
        print(f"[IA] Tiempo de cálculo: {time.time() - start:.3f}s")

    return best
