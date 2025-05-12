import random
import pygame
import time
import heapq
from maze import Maze

# ================== CONFIGURACIÓN ==================
DEFAULT_ROWS = 50
DEFAULT_COLS = 50
DEFAULT_SEED_STRUCTURE = None      # semilla para la generación de la estructura
DEFAULT_SEED_WEIGHTS = None        # semilla para la asignación de pesos
ANIMATION_DELAY = 0.005            # segundos
WINDOW_SIZE = (1280, 720)
BACKGROUND_COLOR = (55, 55, 55)
PATH_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 0)
FRONTIER_COLOR = (255, 0, 0)    # Color para las celdas en la frontera
USE_WEIGHTED = False            # Indica si se usará un laberinto ponderado
USE_LOGS = False
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
            cellSize = min(screenWidth // (2 * self.cols + 1), screenHeight // (2 * self.rows + 1)) # Las posiciones pares en el grid son muros, y las impares son las casillas de paso.
            mazeWidth = cellSize * (2 * self.cols + 1)
            mazeHeight = cellSize * (2 * self.rows + 1)
            offsetX = (screenWidth - mazeWidth) // 2
            offsetY = (screenHeight - mazeHeight) // 2
            return cellSize, offsetX, offsetY

        cellSize, offsetX, offsetY = drawAndResize() # recalcular las dimensiones antes de dibujar el laberinto
        # inicio aleatorio de la casilla (vértices) del laberinto
        grid = [[1 for _ in range(2 * self.cols + 1)] for _ in range(2 * self.rows + 1)]
        weights_grid = [[0 for _ in range(2 * self.cols + 1)] for _ in range(2 * self.rows + 1)]

        start_r, start_c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        grid[2 * start_r + 1][2 * start_c + 1] = 0

        frontier = []
        if self.weighted:
            random.seed(self.seed_weights)

        def addFrontier(r, c):
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and grid[2 * nr + 1][2 * nc + 1] == 1:
                    if self.weighted:
                        weight = random.randint(1, 10)
                        # print(f"Peso de la celda ({nr}, {nc}): {weight}")
                    else:
                        weight = 1
                    heapq.heappush(frontier, (weight, nr, nc))

        addFrontier(start_r, start_c)
        visited = set()
        visited.add((start_r, start_c))
        
        self.drawMaze(screen, grid, cellSize, offsetX, offsetY, frontier, visited)
        time.sleep(ANIMATION_DELAY)

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
                # Ponderado: usar la cola de prioridad para obtener la frontera con menor peso.
                weight, r, c = heapq.heappop(frontier)
            else:
                # No ponderado: mezclar la frontera y seleccionar aleatoriamente.
                random.shuffle(frontier)
                weight, r, c = frontier.pop()

            if (r, c) in visited:
                continue

            neighbors = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and grid[2 * nr + 1][2 * nc + 1] == 0:
                    neighbors.append((nr, nc))

            if neighbors:
                if self.weighted:
                    # Si es ponderado, seleccionar el vecino con menor peso.
                    min_weight = float('inf')
                    selected_neighbor = None
                    for nr, nc in neighbors:
                        wallR = r + nr + 1
                        wallC = c + nc + 1
                        current_weight = weights_grid[wallR][wallC]
                        if current_weight < min_weight:
                            min_weight = current_weight
                            selected_neighbor = (nr, nc)
                    nr, nc = selected_neighbor
                else:
                    # Si no es ponderado, elegir cualquier vecino aleatoriamente.
                    nr, nc = random.choice(neighbors)

                wallR = r + nr + 1
                wallC = c + nc + 1
                grid[2 * r + 1][2 * c + 1] = 0
                grid[wallR][wallC] = 0
                weights_grid[wallR][wallC] = weight

                # LOG:
                if USE_LOGS:
                    with open("prim_verification.txt", "a", encoding="utf-8") as f:
                        f.write(f"Arista conectada: ({r}, {c}) <-> ({nr}, {nc}) | Peso asignado: {weight} con casilla ({wallR}, {wallC})\n")
                        f.write(f"\t- casilla inicio: ({2*r+1}, {2*c+1})\n\t- casilla camino: ({wallR}, {wallC})\n\t- casilla destino: ({2*nr+1}, {2*nc+1})\n")

                addFrontier(r, c)

            visited.add((r, c))

            cellSize, offsetX, offsetY = drawAndResize()
            self.drawMaze(screen, grid, cellSize, offsetX, offsetY, frontier, visited)
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

    def drawMaze(self, screen, grid, cellSize, offsetX, offsetY, frontier, visited):
        screen.fill(BACKGROUND_COLOR)
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                color = WALL_COLOR if val == 1 else PATH_COLOR
                pygame.draw.rect(
                    screen, color, 
                    (offsetX + c * cellSize, offsetY + r * cellSize, cellSize, cellSize)
                )
        # Solo dibujar frontera si hay elementos
        if frontier:
            for _, fr, fc in frontier:
                if (fr, fc) not in visited:
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


    def generateWithNograph(self):
        """
        Genera un laberinto sin visualización gráfica y lo devuelve como un objeto Maze.
        """
        print("\n=== Generando Laberinto Sin Visualización ===")
        print(f"Tipo de Laberinto: {'Ponderado' if self.weighted else 'No Ponderado'}")
        print("Algoritmo de Generación: Prim")
        print(f"Dimensiones: {self.rows}x{self.cols}")
        print("==============================================\n")
    
        if self.seed_structure is not None:
            random.seed(self.seed_structure)
    
        grid = [[1 for _ in range(2 * self.cols + 1)] for _ in range(2 * self.rows + 1)]
        weights_grid = [[0 for _ in range(2 * self.cols + 1)] for _ in range(2 * self.rows + 1)]
    
        start_r, start_c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        grid[2 * start_r + 1][2 * start_c + 1] = 0
    
        frontier = []
        visited = set([(start_r, start_c)])
    
        if self.weighted and self.seed_weights is not None:
            random.seed(self.seed_weights)
        
        def addFrontier(r, c):
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and grid[2 * nr + 1][2 * nc + 1] == 1:
                    if self.weighted:
                        weight = random.randint(1, 10)
                    else:
                        weight = 1
                    heapq.heappush(frontier, (weight, nr, nc))
    
    # Añadir vecinos de la celda inicial a la frontera
        addFrontier(start_r, start_c)
    
    # Proceso principal del algoritmo de Prim
        while frontier:
        # Seleccionar siguiente celda de la frontera
            if self.weighted:
            # En laberinto ponderado, seleccionar la de menor peso
                weight, r, c = heapq.heappop(frontier)
            else:
            # En laberinto no ponderado, seleccionar aleatoriamente
                idx = random.randint(0, len(frontier) - 1)
                weight, r, c = frontier.pop(idx)
        
        # Si ya visitamos esta celda, continuar con la siguiente
            if (r, c) in visited:
                continue
        
        # Buscar vecinos ya visitados
            neighbors = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and (nr, nc) in visited:
                    neighbors.append((nr, nc))
        
        # Si hay vecinos ya visitados, conectar con uno de ellos
            if neighbors:
                if self.weighted:
                # Elegir vecino con menor peso en caso de laberinto ponderado
                    min_weight = float('inf')
                    selected_neighbor = None
                    for nr, nc in neighbors:
                        wallR = r + nr + 1
                        wallC = c + nc + 1
                        current_weight = weights_grid[wallR][wallC]
                        if current_weight < min_weight:
                            min_weight = current_weight
                            selected_neighbor = (nr, nc)
                
                    if selected_neighbor:
                        nr, nc = selected_neighbor
                    else:
                        nr, nc = random.choice(neighbors)
                else:
                # Elegir vecino aleatorio en caso de laberinto no ponderado
                    nr, nc = random.choice(neighbors)
            
            # Abrir camino entre celdas
                wallR = r + nr + 1
                wallC = c + nc + 1
                grid[2 * r + 1][2 * c + 1] = 0  # Marcar celda actual como camino
                grid[wallR][wallC] = 0  # Marcar pared entre celdas como camino
            
            # Asignar peso al camino si es ponderado
                if self.weighted:
                    weights_grid[wallR][wallC] = weight
            
            # Añadir vecinos de la celda actual a la frontera
                addFrontier(r, c)
        
        # Marcar celda como visitada
            visited.add((r, c))
    
    # Asegurar que las celdas de entrada y salida son transitables
        grid[1][1] = 0  # Entrada (0,0)
        grid[2 * self.rows - 1][2 * self.cols - 1] = 0  # Salida (rows-1, cols-1)
    
    # Crear y configurar el objeto Maze
        maze = Maze()
        maze.setGrid(grid)
    
        if self.weighted:
            maze.setWeights(weights_grid)
    
        print("Laberinto generado con éxito.")
        return maze
