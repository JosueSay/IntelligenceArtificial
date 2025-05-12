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
    # Lista de algoritmos a ejecutar en orden
    algorithms = [
        ("BFS", bfs),
        ("DFS", dfs),
        ("UCS", uniform_cost_search),
        ("A*", a_star)
    ]
    
    results = {}
    
    # Ejecutar y visualizar cada algoritmo secuencialmente
    for alg_name, algorithm in algorithms:
        # Ejecutar algoritmo
        result = run_algorithm(maze, start, end, algorithm)
        results[alg_name] = result
        
        # Configurar visualización individual
        current_step = 0
        path_step = 0
        completed = False
        color = COLORS[alg_name]
        
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
                        pygame.draw.rect(screen, WHITE, 
                                       (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
            # Dibujar nodos visitados
            if current_step < len(result['visited']):
                nodes_to_draw = result['visited'][:current_step+1]
                current_step += 8  # Ajustar velocidad de exploración
            else:
                completed = True
                nodes_to_draw = result['visited']
            
            for node in nodes_to_draw:
                pygame.draw.rect(screen, color,
                               (node[1]*CELL_SIZE, node[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
            # Dibujar camino
            if completed and result['path']:
                if path_step < len(result['path']):
                    path_nodes = result['path'][:path_step+1]
                    path_step += 3  # Ajustar velocidad del camino
                else:
                    path_nodes = result['path']
                
                for node in path_nodes:
                    pygame.draw.rect(screen, ORANGE,
                                   (node[1]*CELL_SIZE, node[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
            # Dibujar inicio y fin
            pygame.draw.rect(screen, GREEN, 
                           (start[1]*CELL_SIZE, start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, RED, 
                           (end[1]*CELL_SIZE, end[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
            # Mostrar nombre del algoritmo
            text = font.render(f"{alg_name} - Nodos: {result['nodes']} Tiempo: {result['time']:.2f}s", 
                             True, color)
            screen.blit(text, (10, 10))
            
            pygame.display.flip()
            clock.tick(30)
            
            # Finalizar visualización cuando complete ambos pasos
            if completed and path_step >= len(result['path']):
                time.sleep(2)  # Pausa final
                running = False
        
        # Limpiar pantalla entre algoritmos
        screen.fill(BLACK)
        pygame.display.flip()
        time.sleep(0.5)
    
    # Mostrar estadísticas finales
    print("\n=== Comparación final ===")
    sorted_results = sorted(results.items(), key=lambda x: x[1]['time'])
    print(f"{'Algoritmo':<10} | {'Tiempo (s)':<10} | {'Nodos explorados':<15} | {'Longitud camino':<15}")
    for name, data in sorted_results:
        print(f"{name:<10} | {data['time']:<10.4f} | {data['nodes']:<15} | {data['length']:<15}")

def generate_valid_positions(maze, min_distance=10):
    """Genera posiciones inicial y final válidas en caminos libres con distancia mínima"""
    rows, cols = maze.shape
    free_cells = [(r, c) for r in range(rows) for c in range(cols) if maze[r, c] == 0]
    
    while True:
        start = tuple(free_cells[np.random.randint(len(free_cells))])
        end = tuple(free_cells[np.random.randint(len(free_cells))])
        
        # Calcular distancia Manhattan
        if abs(start[0] - end[0]) + abs(start[1] - end[1]) >= min_distance:
            return start, end

def run_multiple_simulations(num_simulations=25):
    stats = {
        "BFS": {"time": [], "nodes": [], "length": []},
        "DFS": {"time": [], "nodes": [], "length": []},
        "UCS": {"time": [], "nodes": [], "length": []},
        "A*": {"time": [], "nodes": [], "length": []}
    }
    
    algorithms = {
        "BFS": bfs,
        "DFS": dfs,
        "UCS": uniform_cost_search,
        "A*": a_star
    }
    
    for sim in range(num_simulations):
        print(f"\nSimulación {sim+1}/{num_simulations}")
        maze = generate_maze(ROWS, COLS)
        start, end = generate_valid_positions(maze)
        
        # Solo mostrar gráficos en la primera simulación
        if sim == 24:
            print("Mostrando visualización de la primera simulación...")
            visualize_algorithms(maze, start, end)  # Versión gráfica lenta
            # Recoger datos de la simulación visualizada
            for alg_name in algorithms:
                result = run_algorithm(maze, start, end, algorithms[alg_name])
                stats[alg_name]["time"].append(result["time"])
                stats[alg_name]["nodes"].append(result["nodes"])
                stats[alg_name]["length"].append(result["length"])
        else:
            # Ejecución rápida para las demás simulaciones
            for alg_name, algorithm in algorithms.items():
                result = run_algorithm(maze, start, end, algorithm)
                stats[alg_name]["time"].append(result["time"])
                stats[alg_name]["nodes"].append(result["nodes"])
                stats[alg_name]["length"].append(result["length"])
                print(f"{alg_name}: {result['time']:.4f}s | Nodos: {result['nodes']} | Long: {result['length']}")

run_multiple_simulations(25)
