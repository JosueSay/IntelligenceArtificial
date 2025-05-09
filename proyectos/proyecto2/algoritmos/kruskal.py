import random
import pygame
import time
from maze import Maze

# ================== CONFIGURACIÓN ==================
DEFAULT_ROWS = 50
DEFAULT_COLS = 50
DEFAULT_SEED_STRUCTURE = None  # Semilla para la generación de la estructura
DEFAULT_SEED_WEIGHTS = None    # Semilla para la asignación de pesos
ANIMATION_DELAY = 0.005        # segundos
WINDOW_SIZE = (1280, 720)
BACKGROUND_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 0)
USE_WEIGHTED = False            # Indica si se usará un laberinto ponderado
# ===================================================

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1
            return True
        return False

class KruskalMazeGenerator:
    def __init__(self, rows=DEFAULT_ROWS, cols=DEFAULT_COLS, 
                 seed_structure=DEFAULT_SEED_STRUCTURE, seed_weights=DEFAULT_SEED_WEIGHTS, 
                 weighted=USE_WEIGHTED):
        self.rows = rows
        self.cols = cols
        self.seed_structure = seed_structure
        self.seed_weights = seed_weights
        self.weighted = weighted
        self.maze = Maze()

    def displayConfiguration(self):
        print("\n=== Configuración Utilizada ===")
        print(f"Tipo de Laberinto: {'Ponderado' if self.weighted else 'No Ponderado'}")
        print("Algoritmo de Generación: Kruskal")
        print(f"Semilla de Estructura: {self.seed_structure}")
        print(f"Semilla de Pesos: {self.seed_weights if self.weighted else 'N/A'}")
        print("===============================\n")

    def generate(self):
        self.displayConfiguration()
        random.seed(self.seed_structure)
        pygame.init()

        screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
        pygame.display.set_caption("Laberinto con Kruskal")

        def drawAndResize():
            screenWidth, screenHeight = screen.get_size()
            cellSize = min(screenWidth // (2 * self.cols + 1), screenHeight // (2 * self.rows + 1))
            mazeWidth = cellSize * (2 * self.cols + 1)
            mazeHeight = cellSize * (2 * self.rows + 1)
            offsetX = (screenWidth - mazeWidth) // 2
            offsetY = (screenHeight - mazeHeight) // 2
            return cellSize, offsetX, offsetY

        cellSize, offsetX, offsetY = drawAndResize()
        grid = [[1 for _ in range(2 * self.cols + 1)] for _ in range(2 * self.rows + 1)]
        uf = UnionFind(self.rows * self.cols)

        edges = [((r, c), (r, c + 1)) for r in range(self.rows) for c in range(self.cols - 1)] + \
                [((r, c), (r + 1, c)) for r in range(self.rows - 1) for c in range(self.cols)]

        if self.weighted:
            random.seed(self.seed_weights)
            edges_with_weights = [(random.randint(1, 10), edge) for edge in edges]
            edges_with_weights.sort(key=lambda x: x[0])
            edges = [edge for _, edge in edges_with_weights]
        else:
            random.shuffle(edges)

        for (r1, c1), (r2, c2) in edges:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.maze.setGrid(grid)
                    return self.maze
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.maze.setGrid(grid)
                    return self.maze

            idx1 = r1 * self.cols + c1
            idx2 = r2 * self.cols + c2
            if uf.union(idx1, idx2):
                grid[2 * r1 + 1][2 * c1 + 1] = 0
                grid[2 * r2 + 1][2 * c2 + 1] = 0
                grid[r1 + r2 + 1][c1 + c2 + 1] = 0

                cellSize, offsetX, offsetY = drawAndResize()
                self.drawMaze(screen, grid, cellSize, offsetX, offsetY)
                time.sleep(ANIMATION_DELAY)

        print("Laberinto generado con éxito usando Kruskal. Pulsa ESC para salir o volver al menú.")
        self.waitForExit()

        self.maze.setGrid(grid)
        if self.weighted:
            self.assignWeights()

        return self.maze

    def assignWeights(self):
        random.seed(self.seed_weights)
        weights = [[random.randint(1, 10) if cell == 0 else 0 for cell in row] for row in self.maze.grid]
        self.maze.setWeights(weights)

    def drawMaze(self, screen, grid, cellSize, offsetX, offsetY):
        screen.fill(BACKGROUND_COLOR)
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                color = WALL_COLOR if val == 1 else BACKGROUND_COLOR
                pygame.draw.rect(
                    screen,
                    color,
                    (offsetX + c * cellSize, offsetY + r * cellSize, cellSize, cellSize)
                )
        pygame.display.update()

    def waitForExit(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False