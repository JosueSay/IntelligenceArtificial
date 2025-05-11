# Comparacion de algoritmos de busqueda

from algoritmos.algoritmos_busqueda import *
import numpy as np
from queue import Queue
import time
import os
import heapq
import random
import matplotlib.pyplot as plt

def generate_random_maze(rows=45, cols=55, wall_probability=0.3):
    # 0 representa camino libre, 1 representa pared
    maze = np.random.choice([0, 1], size=(rows, cols), p=[1-wall_probability, wall_probability])
    return maze

def get_valid_points(maze, min_distance=10):
    rows, cols = maze.shape
    valid_points = []
    
    for i in range(rows):
        for j in range(cols):
            if maze[i, j] == 0:  # Si es un camino libre
                valid_points.append((i, j))
    
    # Seleccionar punto A y B que estén a una distancia Manhattan >= 10
    while True:
        if len(valid_points) < 2:
            return None, None  # No hay suficientes puntos válidos
            
        start = random.choice(valid_points)
        candidates = []
        
        for point in valid_points:
            manhattan_dist = abs(start[0] - point[0]) + abs(start[1] - point[1])
            if manhattan_dist >= min_distance:
                candidates.append(point)
        
        if candidates:
            end = random.choice(candidates)
            return start, end
        
        # Si no encontramos un punto B válido, elegimos otro punto A
        valid_points.remove(start)

def run_simulation(num_mazes=25):
    # Resultados para cada algoritmo: [nodos explorados, tiempo, longitud de ruta]
    results = {
        'BFS': [],
        'DFS': [],
        'Uniform Cost': [],
        'A*': []
    }
    
    rankings = {
        'BFS': [],
        'DFS': [],
        'Uniform Cost': [],
        'A*': []
    }
    
    for i in range(num_mazes):
        print(f"Generando laberinto {i+1}/{num_mazes}")
        
        # Generar laberinto hasta que encontremos uno válido
        while True:
            maze = generate_random_maze()
            start, end = get_valid_points(maze)
            
            if start and end:
                # Verificar si existe un camino
                test_path, _ = bfs(maze, start, end)
                if test_path:  # Si existe un camino
                    break
        
        maze_results = []
        
        # BFS
        start_time = time.time()
        bfs_path, bfs_nodes = bfs(maze, start, end)
        bfs_time = time.time() - start_time
        results['BFS'].append([bfs_nodes, bfs_time, len(bfs_path)])
        maze_results.append(('BFS', bfs_nodes, bfs_time, len(bfs_path)))
        
        # DFS
        start_time = time.time()
        dfs_path, dfs_nodes = dfs(maze, start, end)
        dfs_time = time.time() - start_time
        results['DFS'].append([dfs_nodes, dfs_time, len(dfs_path)])
        maze_results.append(('DFS', dfs_nodes, dfs_time, len(dfs_path)))
        
        # Uniform Cost Search
        start_time = time.time()
        ucs_path, ucs_nodes = uniform_cost_search(maze, start, end)
        ucs_time = time.time() - start_time
        results['Uniform Cost'].append([ucs_nodes, ucs_time, len(ucs_path)])
        maze_results.append(('Uniform Cost', ucs_nodes, ucs_time, len(ucs_path)))
        
        # A*
        start_time = time.time()
        astar_path, astar_nodes = a_star(maze, start, end)
        astar_time = time.time() - start_time
        results['A*'].append([astar_nodes, astar_time, len(astar_path)])
        maze_results.append(('A*', astar_nodes, astar_time, len(astar_path)))
        
        # Calcular rankings para este laberinto
        # Ranking por nodos explorados (menos es mejor)
        nodes_ranking = sorted(maze_results, key=lambda x: x[1])
        # Ranking por tiempo (menos es mejor)
        time_ranking = sorted(maze_results, key=lambda x: x[2])
        # Ranking por longitud (menos es mejor, aunque BFS, UCS y A* deberían encontrar el camino óptimo)
        length_ranking = sorted(maze_results, key=lambda x: x[3])
        
        # Asignar puntos por ranking (1 punto para el mejor, 4 para el peor)
        alg_points = {'BFS': 0, 'DFS': 0, 'Uniform Cost': 0, 'A*': 0}
        
        for rank, (alg, _, _, _) in enumerate(nodes_ranking):
            alg_points[alg] += rank + 1
        
        for rank, (alg, _, _, _) in enumerate(time_ranking):
            alg_points[alg] += rank + 1
            
        for rank, (alg, _, _, _) in enumerate(length_ranking):
            alg_points[alg] += rank + 1
        
        # El algoritmo con menos puntos es el mejor
        final_ranking = sorted(alg_points.items(), key=lambda x: x[1])
        
        for rank, (alg, _) in enumerate(final_ranking):
            rankings[alg].append(rank + 1)
        
        # Visualización opcional del laberinto y la solución
        if i == 0:  # Solo visualizar el primer laberinto
            visualize_maze(maze, start, end, bfs_path, dfs_path, ucs_path, astar_path)
    
    return results, rankings

def visualize_maze(maze, start, end, bfs_path, dfs_path, ucs_path, astar_path):
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs = axs.flatten()
    
    paths = [bfs_path, dfs_path, ucs_path, astar_path]
    titles = ['BFS', 'DFS', 'Uniform Cost Search', 'A*']
    
    for i, (path, title) in enumerate(zip(paths, titles)):
        maze_vis = maze.copy()
        
        # Marcar camino
        for r, c in path:
            maze_vis[r, c] = 0.5  # Valor intermedio para visualizar
        
        # Marcar inicio y fin
        maze_vis[start] = 0.7
        maze_vis[end] = 0.9
        
        axs[i].imshow(maze_vis, cmap='viridis')
        axs[i].set_title(f"{title} - Path Length: {len(path)}")
        axs[i].axis('off')
    
    plt.tight_layout()
    plt.show()

def create_summary_table(results, rankings):
    algorithms = list(results.keys())
    
    # Calcular promedios
    avg_nodes = {}
    avg_time = {}
    avg_length = {}
    avg_rank = {}
    
    for alg in algorithms:
        avg_nodes[alg] = sum(res[0] for res in results[alg]) / len(results[alg])
        avg_time[alg] = sum(res[1] for res in results[alg]) / len(results[alg])
        avg_length[alg] = sum(res[2] for res in results[alg]) / len(results[alg])
        avg_rank[alg] = sum(rankings[alg]) / len(rankings[alg])
    
    # Crear tabla
    print("\nResultados promedio:")
    print(f"{'Algoritmo':<15} {'Nodos':<10} {'Tiempo (s)':<15} {'Longitud':<10} {'Ranking':<10}")
    print("="*60)
    
    for alg in algorithms:
        print(f"{alg:<15} {avg_nodes[alg]:<10.2f} {avg_time[alg]:<15.6f} {avg_length[alg]:<10.2f} {avg_rank[alg]:<10.2f}")
    
    # Ordenar algoritmos por ranking promedio
    sorted_algs = sorted(avg_rank.items(), key=lambda x: x[1])
    
    print("\nRanking final de algoritmos:")
    for rank, (alg, score) in enumerate(sorted_algs):
        print(f"{rank+1}. {alg} (puntuación: {score:.2f})")

# Ejecutar simulaciones
results, rankings = run_simulation(num_mazes=25)
create_summary_table(results, rankings)


