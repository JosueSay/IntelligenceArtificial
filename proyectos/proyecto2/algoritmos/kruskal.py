import random
import pygame
import time
from maze import Maze

# ================== CONFIGURACIÓN ==================
DEFAULT_ROWS = 50
DEFAULT_COLS = 50
DEFAULT_SEED_STRUCTURE = None  # semilla para la generación de la estructura
DEFAULT_SEED_WEIGHTS = None    # semilla para la asignación de pesos
ANIMATION_DELAY = 0.005        # segundos
WINDOW_SIZE = (1280, 720)
BACKGROUND_COLOR = (55, 55, 55)
PATH_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 0)
USE_WEIGHTED = False            # indica si se usará un laberinto ponderado
USE_LOGS = False                # indica si se generará un log de la ejecución
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
            cellSize = min(screenWidth // (2 * self.cols + 1), screenHeight // (2 * self.rows + 1)) # Las posiciones pares en el grid son muros, y las impares son las casillas de paso.
            mazeWidth = cellSize * (2 * self.cols + 1)
            mazeHeight = cellSize * (2 * self.rows + 1)
            offsetX = (screenWidth - mazeWidth) // 2
            offsetY = (screenHeight - mazeHeight) // 2
            return cellSize, offsetX, offsetY

        cellSize, offsetX, offsetY = drawAndResize() # recalcular las dimensiones antes de dibujar el laberinto
        grid = [[1 for _ in range(2 * self.cols + 1)] for _ in range(2 * self.rows + 1)]
        weights_grid = [[0 for _ in range(2 * self.cols + 1)] for _ in range(2 * self.rows + 1)]
        uf = UnionFind(self.rows * self.cols) # inicializar parent-rank

        # conexiones horizontales (misma fila, distintas columnas consecutivas) y conexiones verticales (misma columna, distintas filas consecutivas) = grafo (u,v)
        edges = [((r, c), (r, c + 1)) for r in range(self.rows) for c in range(self.cols - 1)] + [((r, c), (r + 1, c)) for r in range(self.rows - 1) for c in range(self.cols)]

        if self.weighted: # tripleta (w, u, v) = (w, arista) con w aleatorizado
            random.seed(self.seed_weights)
            edges_with_weights = [(random.randint(1, 10), edge) for edge in edges]
            edges_with_weights.sort(key=lambda x: x[0])
        else: # tripleta (w, u, v) = (w, arista) con w = 1
            random.shuffle(edges)
            edges_with_weights = [(1, edge) for edge in edges]

        for weight, (r1, c1), (r2, c2) in [(w, *e) for w, e in edges_with_weights]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.maze.setGrid(grid)
                    self.maze.setWeights(weights_grid)
                    return self.maze
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.maze.setGrid(grid)
                    self.maze.setWeights(weights_grid)
                    return self.maze

            # Conversion de vector dimensional a unidimensional u,v -> idx1, idx2 (índices en el array de UnionFind)
            idx1 = r1 * self.cols + c1
            idx2 = r2 * self.cols + c2
            if uf.union(idx1, idx2): # aplicación de union-find para evitar ciclos (se añade o no al MST)
                grid[2 * r1 + 1][2 * c1 + 1] = 0
                grid[2 * r2 + 1][2 * c2 + 1] = 0
                grid[r1 + r2 + 1][c1 + c2 + 1] = 0

                # Asignar peso al camino generado
                weights_grid[r1 + r2 + 1][c1 + c2 + 1] = weight
                # weights_grid[2 * r1 + 1][2 * c1 + 1] = weight
                # weights_grid[2 * r2 + 1][2 * c2 + 1] = weight
                
                # LOG:
                if USE_LOGS:
                    with open("kruskal_verification.txt", "a", encoding="utf-8") as f:  # 'a' para añadir sin sobrescribir
                        f.write(f"Arista conectada: ({r1}, {c1}) <-> ({r2}, {c2}) | Peso asignado: {weight} con casilla ({r1+r2+1}, {c1+c2+1})\n")
                        f.write(f"\t- casilla inicio: ({2*r1+1}, {2*c1+1})\n\t- casilla camino: ({r1+r2+1}, {c1+c2+1})\n\t- casilla destino: ({2*r2+1}, {2*c2+1})\n")

                cellSize, offsetX, offsetY = drawAndResize() # recalcular las dimensiones durante el dibujo del laberinto
                self.drawMaze(screen, grid, cellSize, offsetX, offsetY)
                time.sleep(ANIMATION_DELAY)

        print("Laberinto generado con éxito usando Kruskal. Pulsa ESC para salir o volver al menú.")
        self.waitForExit()

        self.maze.setGrid(grid)
        self.maze.setWeights(weights_grid)
        
        # LOG:
        if USE_LOGS:
            with open("kruskal_verification.txt", "a", encoding="utf-8") as f:
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

    def drawMaze(self, screen, grid, cellSize, offsetX, offsetY):
        screen.fill(BACKGROUND_COLOR)
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                color = WALL_COLOR if val == 1 else PATH_COLOR
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