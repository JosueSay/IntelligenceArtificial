import numpy as np
from queue import Queue, PriorityQueue

# Maze va a ser el laberinto, lo voy a definir posteriormente en Problema3.py

# Algoritmo bfs para recorrer el laberinto
def bfs(maze, start, end):
    rows, cols = maze.shape
    queue = Queue()
    queue.put(start)
    visited = set([start])
    parent = {start: None}
    nodes_exploded = 0

    # Mientras no se haya terminado el laberinto
    while not queue.empty():
        current = queue.get()
        nodes_explored += 1

        if current == end:
            break
    # Ahora a explorar los vecinos
    for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
        new_r, new_c = current[0] + dr, current[1] + dc

        # Verificar si el camino esta libre 
        if (0 <= new_r < rows and 0 <= new_c < cols and maze[new_r, new_c] == 0 and (new_r, new_c) not in visited):
            neighbor = (new_r, new_c)
            queue.put(neighbor)
            visited.add(neighbor)
            parent[neighbor] = current

    path = []
    current = end

    if end in parent:
        while current:
            path.append(current)
            current = parent[current]
        path.reverse()
    return path, nodes_explored

