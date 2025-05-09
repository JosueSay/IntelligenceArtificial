# Comparacion de algoritmos de busqueda

from algoritmos.algoritmos_busqueda import *
import numpy as np
from queue import Queue, PriorityQueue
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
