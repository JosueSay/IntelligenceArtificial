import random
import pygame
import time
from maze import Maze

# ================== CONFIGURACIÓN ==================
DEFAULT_ROWS = 50
DEFAULT_COLS = 50
DEFAULT_SEED_STRUCTURE = None  # Semilla para la generación de la estructura
DEFAULT_SEED_WEIGHTS = None    # Semilla para la asignación de pesos
ANIMATION_DELAY = 1        # segundos
WINDOW_SIZE = (1280, 720)
BACKGROUND_COLOR = (55, 55, 55)
PATH_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 0)
FRONTIER_COLOR = (255, 0, 0)    # Color para las celdas en la frontera
USE_WEIGHTED = False            # Indica si se usará un laberinto ponderado
USE_LOGS = True
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
            cellSize = min(screenWidth // (2 * self.cols + 1), screenHeight // (2 * self.rows + 1))  # Las posiciones pares en el grid son muros, y las impares son las casillas de paso.
            mazeWidth = cellSize * (2 * self.cols + 1)
            mazeHeight = cellSize * (2 * self.rows + 1)
            offsetX = (screenWidth - mazeWidth) // 2
            offsetY = (screenHeight - mazeHeight) // 2
            return cellSize, offsetX, offsetY

        cellSize, offsetX, offsetY = drawAndResize() # recalcular las dimensiones antes de dibujar el laberinto
        grid = [[1 for _ in range(2 * self.cols + 1)] for _ in range(2 * self.rows + 1)]
        weights_grid = [[0 for _ in range(2 * self.cols + 1)] for _ in range(2 * self.rows + 1)]


        # inicio aleatorio de la casilla (vértices) del laberinto
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
                weight, (r, c) = weighted_frontier[0]
            else:
                random.seed(self.seed_structure)  # Controla la aleatoriedad de la elección de la celda
                weight = 1
                r, c = random.choice(frontier)

            neighbors = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and grid[2 * nr + 1][2 * nc + 1] == 0:
                    neighbors.append((nr, nc))

            if neighbors:
                random.seed(self.seed_structure)  # Controla la aleatoriedad de la elección de la celda
                nr, nc = random.choice(neighbors)
                wallR = r + nr + 1
                wallC = c + nc + 1
                grid[2 * r + 1][2 * c + 1] = 0
                grid[wallR][wallC] = 0
                weights_grid[wallR][wallC] = weight
                
                # LOGS:
                if USE_LOGS:
                    with open("prim_verification.txt", "a", encoding="utf-8") as f:
                        f.write(f"Arista conectada: ({r}, {c}) <-> ({nr}, {nc}) | Peso asignado: {weight} con casilla ({wallR}, {wallC})\n")
                        f.write(f"\t- casilla inicio: ({2*r+1}, {2*c+1})\n\t- casilla camino: ({wallR}, {wallC})\n\t- casilla destino: ({2*nr+1}, {2*nc+1})\n")
                
                addFrontier(r, c)

            frontier.remove((r, c))

            cellSize, offsetX, offsetY = drawAndResize() # recalcular las dimensiones durante el dibujo del laberinto
            self.drawMaze(screen, grid, cellSize, offsetX, offsetY, frontier)
            time.sleep(ANIMATION_DELAY)

        print("Laberinto generado con éxito usando Prim. Pulsa ESC para salir o volver al menú.")
        self.waitForExit()

        self.maze.setGrid(grid)
        self.maze.setWeights(weights_grid)
        
        # LOGS:
        if USE_LOGS:
            with open("prim_verification.txt", "a", encoding="utf-8") as f:
                f.write("=== Verificación de Pesos en el MST ===\n\n")
                f.write("Grid del Laberinto ('vacio' = Camino, █ = Muro):\n")
                for row in grid:
                    f.write("".join(['█' if cell == 1 else ' ' for cell in row]) + "\n")

                f.write("\nGrid de Pesos:\n")
                for row in weights_grid:
                    f.write(" ".join([str(cell).rjust(2) for cell in row]) + "\n")

                f.write("\nDetalle de Celdas Transitables y sus Pesos:\n")
                for r in range(len(grid)):
                    for c in range(len(grid[0])):
                        if grid[r][c] == 0:
                            f.write(f"Celda ({r}, {c}): Peso {weights_grid[r][c]}\n")

                f.write("\n=======================================\n")
        
        return self.maze

    def drawMaze(self, screen, grid, cellSize, offsetX, offsetY, frontier):
        screen.fill(BACKGROUND_COLOR)
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                color = WALL_COLOR if val == 1 else PATH_COLOR
                pygame.draw.rect(
                    screen,
                    color,
                    (offsetX + c * cellSize, offsetY + r * cellSize, cellSize, cellSize)
                )
        # Dibujar frontera en color especial
        if frontier:
            for fr, fc in frontier:
                pygame.draw.rect(
                    screen,
                    FRONTIER_COLOR,
                    (offsetX + (2 * fc + 1) * cellSize, offsetY + (2 * fr + 1) * cellSize, cellSize, cellSize)
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
