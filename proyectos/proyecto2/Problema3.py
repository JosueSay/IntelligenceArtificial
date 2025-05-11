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
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# Asignación de colores a algoritmos
COLORS = {
    "BFS": BLUE,
    "DFS": YELLOW,
    "UCS": CYAN,
    "A*": MAGENTA
}

# Tamaño de celda y dimensiones del laberinto
CELL_SIZE = 12
ROWS, COLS = 45, 55
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver Comparison")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 18)

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

def uniform_cost_search(maze, start, end):
    rows, cols = maze.shape
    priority_queue = [(0, start)]
    visited = set()
    parent = {start: None}
    cost_so_far = {start: 0}
    visited_order = []
    
    while priority_queue:
        current_cost, current = heapq.heappop(priority_queue)
        
        if current in visited:
            continue
            
        visited.add(current)
        visited_order.append(current)
        
        if current == end:
            break
            
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] == 0:
                new_cost = cost_so_far[current] + 1
                if (nr, nc) not in cost_so_far or new_cost < cost_so_far[(nr, nc)]:
                    cost_so_far[(nr, nc)] = new_cost
                    heapq.heappush(priority_queue, (new_cost, (nr, nc)))
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

def run_algorithm(maze, start, end, algorithm):
    start_time = time.time()
    path, nodes_explored, visited = algorithm(maze, start, end)
    execution_time = time.time() - start_time
    path_length = len(path) if path else 0
    return {
        "path": path,
        "nodes": nodes_explored,
        "time": execution_time,
        "visited": visited,
        "length": path_length
    }

# Función principal de visualización
def visualize_algorithms(maze, start, end):
    # Ejecutar todos los algoritmos
    results = {
        "BFS": run_algorithm(maze, start, end, bfs),
        "DFS": run_algorithm(maze, start, end, dfs),
        "UCS": run_algorithm(maze, start, end, uniform_cost_search),
        "A*": run_algorithm(maze, start, end, a_star)
    }
    
    # Ordenar por tiempo de ejecución
    sorted_results = sorted(results.items(), key=lambda x: x[1]['time'])
    
    # Imprimir estadísticas en consola
    print("\n=== Comparación de algoritmos ===")
    print(f"{'Algoritmo':<10} | {'Tiempo (s)':<10} | {'Nodos explorados':<15} | {'Longitud camino':<15}")
    for name, data in sorted_results:
        print(f"{name:<10} | {data['time']:<10.4f} | {data['nodes']:<15} | {data['length']:<15}")
    
    print("\nClasificación por tiempo de ejecución:")
    for i, (name, _) in enumerate(sorted_results, 1):
        print(f"{i}. {name} ({COLORS[name]})")
    
    # Configuración de visualización
    current_step = {alg: 0 for alg in results}
    path_step = {alg: 0 for alg in results}
    completed = {alg: False for alg in results}
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        # Dibujar laberinto base
        screen.fill(BLACK)
        for r in range(ROWS):
            for c in range(COLS):
                if maze[r, c] == 0:
                    pygame.draw.rect(screen, WHITE, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Dibujar nodos visitados
        for alg, data in results.items():
            color = COLORS[alg]
            visited = data['visited']
            current = current_step[alg]
            
            if current < len(visited):
                nodes_to_draw = visited[:current+1]
                current_step[alg] += 5  # Velocidad de visualización
            else:
                nodes_to_draw = visited
                completed[alg] = True
                
            for node in nodes_to_draw:
                pygame.draw.rect(screen, color, 
                               (node[1]*CELL_SIZE, node[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Dibujar caminos
        for alg, data in results.items():
            if data['path']:
                color = COLORS[alg]
                path = data['path']
                current_path = path_step[alg]
                
                if current_path < len(path):
                    nodes_to_draw = path[:current_path+1]
                    path_step[alg] += 2  # Velocidad del camino
                else:
                    nodes_to_draw = path
                
                for node in nodes_to_draw:
                    pygame.draw.rect(screen, color,
                                   (node[1]*CELL_SIZE, node[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Dibujar inicio y fin
        pygame.draw.rect(screen, GREEN, (start[1]*CELL_SIZE, start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (end[1]*CELL_SIZE, end[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Dibujar leyenda
        y_pos = 10
        for alg, color in COLORS.items():
            text = font.render(f"{alg}", True, color)
            screen.blit(text, (10, y_pos))
            y_pos += 25
        
        pygame.display.flip()
        clock.tick(30)
        
        # Verificar si todos han terminado
        if all(completed.values()) and all(p >= len(results[alg]['path']) for alg, p in path_step.items()):
            time.sleep(5)
            running = False

# Ejecutar comparación
maze = generate_maze(ROWS, COLS)
start = (0, 0)
end = (ROWS-1, COLS-1)

visualize_algorithms(maze, start, end)
