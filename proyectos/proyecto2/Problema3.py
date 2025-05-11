import pygame
import numpy as np
import time
import heapq
from queue import Queue
from sys import exit

# Configuración de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (169, 169, 169)
YELLOW = (255, 255, 0)

# Tamaño de celda y dimensiones del laberinto
CELL_SIZE = 10
ROWS, COLS = 45, 55
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver")
clock = pygame.time.Clock()

# Generación del laberinto usando Recursive Backtracking
def generate_maze(rows, cols):
    maze = np.ones((rows, cols), dtype=int)
    stack = [(0, 0)]
    maze[0, 0] = 0
    
    while stack:
        current = stack[-1]
        r, c = current
        neighbors = []
        
        for dr, dc in [(-2,0), (0,2), (2,0), (0,-2)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] == 1:
                neighbors.append((nr, nc))
        
        if neighbors:
            nr, nc = neighbors[np.random.randint(len(neighbors))]
            maze[nr, nc] = 0
            maze[(r + nr)//2, (c + nc)//2] = 0
            stack.append((nr, nc))
        else:
            stack.pop()
    
    maze[0, 0] = 0
    maze[-1, -1] = 0
    return maze

# Algoritmos de búsqueda modificados para trackear orden de visita
def bfs(maze, start, end):
    rows, cols = maze.shape
    queue = Queue()
    queue.put(start)
    visited = {start}
    parent = {start: None}
    visited_order = []
    
    while not queue.empty():
        current = queue.get()
        visited_order.append(current)
        
        if current == end:
            break
            
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.put((nr, nc))
                parent[(nr, nc)] = current
    
    path = []
    current = end
    while current in parent:
        path.append(current)
        current = parent[current]
    path.reverse()
    
    return path, len(visited_order), visited_order

def dfs(maze, start, end):
    rows, cols = maze.shape
    stack = [start]
    visited = {start}
    parent = {start: None}
    visited_order = []
    
    while stack:
        current = stack.pop()
        visited_order.append(current)
        
        if current == end:
            break
            
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                stack.append((nr, nc))
                parent[(nr, nc)] = current
    
    path = []
    current = end
    while current in parent:
        path.append(current)
        current = parent[current]
    path.reverse()
    
    return path, len(visited_order), visited_order

def a_star(maze, start, end):
    def heuristic(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])
    
    rows, cols = maze.shape
    heap = [(0, start)]
    g_score = {start: 0}
    parent = {start: None}
    visited_order = []
    
    while heap:
        current = heapq.heappop(heap)[1]
        if current in visited_order:
            continue
            
        visited_order.append(current)
        
        if current == end:
            break
            
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            nr, nc = current[0]+dr, current[1]+dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] == 0:
                new_g = g_score[current] + 1
                if (nr, nc) not in g_score or new_g < g_score[(nr, nc)]:
                    g_score[(nr, nc)] = new_g
                    heapq.heappush(heap, (new_g + heuristic(end, (nr, nc)), (nr, nc)))
                    parent[(nr, nc)] = current
    
    path = []
    current = end
    while current in parent:
        path.append(current)
        current = parent[current]
    path.reverse()
    
    return path, len(visited_order), visited_order

# Función principal de visualización
def visualize_algorithm(maze, algorithm, start, end):
    path, nodes_explored, visited_order = algorithm(maze, start, end)
    
    current = 0
    path_index = 0
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        # Dibujar laberinto
        screen.fill(BLACK)
        for r in range(ROWS):
            for c in range(COLS):
                color = WHITE if maze[r, c] == 0 else BLACK
                pygame.draw.rect(screen, color, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Dibujar nodos visitados
        if current < len(visited_order):
            node = visited_order[current]
            pygame.draw.rect(screen, GRAY, (node[1]*CELL_SIZE, node[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            current += 1
        else:
            if path_index < len(path):
                node = path[path_index]
                pygame.draw.rect(screen, BLUE, (node[1]*CELL_SIZE, node[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                path_index += 1
        
        # Dibujar inicio y fin
        pygame.draw.rect(screen, GREEN, (start[1]*CELL_SIZE, start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (end[1]*CELL_SIZE, end[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        pygame.display.update()
        clock.tick(60)
        
        if current >= len(visited_order) and path_index >= len(path):
            time.sleep(3)
            running = False

# Ejecutar comparación
maze = generate_maze(ROWS, COLS)
start = (0, 0)
end = (ROWS-1, COLS-1)

# Visualizar BFS
visualize_algorithm(maze, bfs, start, end)

# Visualizar DFS
visualize_algorithm(maze, dfs, start, end)

# Visualizar A*
visualize_algorithm(maze, a_star, start, end)
