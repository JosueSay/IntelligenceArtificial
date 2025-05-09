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

class PrimMazeGenerator:
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
        print("Algoritmo de Generación: Prim")
        print(f"Semilla de Estructura: {self.seed_structure}")
        print(f"Semilla de Pesos: {self.seed_weights if self.weighted else 'N/A'}")
        print("===============================\n")
        
    def generate(self):
        self.displayConfiguration()
        random.seed(self.seed_structure)
        pygame.init()

        screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
        pygame.display.set_caption("Laberinto con Prim")

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

        start_r, start_c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        grid[2 * start_r + 1][2 * start_c + 1] = 0

        frontier = []
        def addFrontier(r, c):
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and grid[2 * nr + 1][2 * nc + 1] == 1:
                    if (nr, nc) not in frontier:
                        frontier.append((nr, nc))

        addFrontier(start_r, start_c)

        while frontier:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.maze.setGrid(grid)
                    return self.maze
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.maze.setGrid(grid)
                    return self.maze

            if self.weighted:
                random.seed(self.seed_weights)
                weighted_frontier = [(random.randint(1, 10), cell) for cell in frontier]
                weighted_frontier.sort(key=lambda x: x[0])
                r, c = weighted_frontier[0][1]
            else:
                r, c = random.choice(frontier)

            neighbors = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and grid[2 * nr + 1][2 * nc + 1] == 0:
                    neighbors.append((nr, nc))

            if neighbors:
                nr, nc = random.choice(neighbors)
                wallR = r + nr + 1
                wallC = c + nc + 1
                grid[2 * r + 1][2 * c + 1] = 0
                grid[wallR][wallC] = 0
                addFrontier(r, c)

            frontier.remove((r, c))

            cellSize, offsetX, offsetY = drawAndResize()
            self.drawMaze(screen, grid, cellSize, offsetX, offsetY)
            time.sleep(ANIMATION_DELAY)

        print("Laberinto generado con éxito usando Prim. Pulsa ESC para salir o volver al menú.")
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
