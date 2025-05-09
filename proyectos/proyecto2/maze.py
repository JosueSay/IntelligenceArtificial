class Maze:
    def __init__(self, grid=None, weighted=False):
        """
        :param grid: Matriz del laberinto (0 = camino, 1 = muro).
        :param weighted: Indica si se manejan pesos en las celdas.
        """
        self.grid = grid if grid else []
        self.weights = []
        self.weighted = weighted

    def setGrid(self, grid):
        """Define la estructura base del laberinto."""
        self.grid = grid

    def setWeights(self, weights):
        """Define los pesos asociados a cada celda (si weighted=True)."""
        self.weights = weights
        self.weighted = True

    def getCell(self, row, col):
        """Retorna el valor de la celda: 0 (camino) o 1 (muro)."""
        return self.grid[row][col]

    def getWeight(self, row, col):
        """Retorna el peso de la celda, si no hay pesos definidos retorna 1."""
        if self.weighted and self.weights:
            return self.weights[row][col]
        return 1

    def isWalkable(self, row, col):
        """Indica si la celda es transitable."""
        return self.grid[row][col] == 0

    def getNeighbors(self, row, col):
        """
        Retorna vecinos válidos (transitables).
        """
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        rows = len(self.grid)
        cols = len(self.grid[0]) if rows > 0 else 0

        for dr, dc in moves:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and self.isWalkable(nr, nc):
                neighbors.append((nr, nc))
        return neighbors

