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
