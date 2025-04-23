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

def dfs(maze, start, end):
    rows, cols = maze.shape
    stack = [start]
    visited = set([start])
    parent = {start: None}
    nodes_explored = 0
    
    while stack:
        current = stack.pop()
        nodes_explored += 1
        
        if current == end:
            break
            
        # Explorar vecinos
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_r, new_c = current[0] + dr, current[1] + dc
            
            if (0 <= new_r < rows and 0 <= new_c < cols and 
                maze[new_r, new_c] == 0 and (new_r, new_c) not in visited):
                neighbor = (new_r, new_c)
                stack.append(neighbor)
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

def uniform_cost_search(maze, start, end):
    rows, cols = maze.shape
    priority_queue = [(0, start)]  # (costo, posición)
    visited = set()
    parent = {start: None}
    cost_so_far = {start: 0}
    nodes_explored = 0
    
    while priority_queue:
        current_cost, current = heapq.heappop(priority_queue)
        
        if current in visited:
            continue
            
        visited.add(current)
        nodes_explored += 1
        
        if current == end:
            break
            
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_r, new_c = current[0] + dr, current[1] + dc
            
            if (0 <= new_r < rows and 0 <= new_c < cols and 
                maze[new_r, new_c] == 0 and (new_r, new_c) not in visited):
                neighbor = (new_r, new_c)
                new_cost = cost_so_far[current] + 1  
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(priority_queue, (new_cost, neighbor))
                    parent[neighbor] = current
    
    # Reconstruir camino
    path = []
    current = end
    
    if end in parent:
        while current:
            path.append(current)
            current = parent[current]
        path.reverse()
        
    return path, nodes_explored

def heuristic(a, b):
    # Distancia Manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
