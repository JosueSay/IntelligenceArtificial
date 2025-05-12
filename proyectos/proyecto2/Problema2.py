import pygame
import sys
from queue import Queue
from algoritmos.kruskal import KruskalMazeGenerator
from algoritmos.prim import PrimMazeGenerator
from algoritmos.algoritmos_busqueda import bfs
import time

CELL_SIZE = 12
ROWS, COLS = 60, 80
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE

ANIMATION_DELAY = 0.01
WINDOW_SIZE = (1280, 720)
BACKGROUND_COLOR = (55, 55, 55)
PATH_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 0)
VISITED_COLOR = (0, 0, 255)  # Azul para celdas visitadas
PATH_COLOR_HIGHLIGHT = (255, 165, 0)  # Naranja para el camino encontrado
START_COLOR = (0, 255, 0)  # Verde para inicio
END_COLOR = (255, 0, 0)  # Rojo para fin




generator = KruskalMazeGenerator(
    rows=ROWS, cols=COLS
)
maze = generator.generateWithNograph()


def visualize_search(maze_obj, start, end):
    """Visualiza el proceso de búsqueda BFS en un laberinto."""
    # Inicializar Pygame
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Búsqueda BFS en Laberinto")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 18)
    
    # Ejecutar BFS
    path, nodes_explored, visited_order = bfs(maze_obj, start, end)
    
    if not path:
        print("No se encontró un camino")
        return
    
    # Configuración para visualización
    rows = len(maze_obj.grid)
    cols = len(maze_obj.grid[0])
    cell_width = min(WINDOW_SIZE[0] // cols, WINDOW_SIZE[1] // rows, CELL_SIZE)
    offset_x = (WINDOW_SIZE[0] - cols * cell_width) // 2
    offset_y = (WINDOW_SIZE[1] - rows * cell_width) // 2
    
    # Visualizar el proceso de búsqueda
    current_step = 0
    path_step = 0
    completed = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Dibujar laberinto base
        screen.fill(BACKGROUND_COLOR)
        for r in range(rows):
            for c in range(cols):
                color = PATH_COLOR if maze_obj.grid[r][c] == 0 else WALL_COLOR
                pygame.draw.rect(
                    screen, 
                    color, 
                    (offset_x + c * cell_width, offset_y + r * cell_width, cell_width, cell_width)
                )
        
        # Dibujar celdas visitadas
        if current_step < len(visited_order):
            nodes_to_draw = visited_order[:current_step+1]
            current_step += 5  # Velocidad de visualización
        else:
            completed = True
            nodes_to_draw = visited_order
        
        for node in nodes_to_draw:
            pygame.draw.rect(
                screen, 
                VISITED_COLOR, 
                (offset_x + node[1] * cell_width, offset_y + node[0] * cell_width, cell_width, cell_width)
            )
        
        # Dibujar camino encontrado
        if completed and path:
            if path_step < len(path):
                path_nodes = path[:path_step+1]
                path_step += 1  # Velocidad de visualización
            else:
                path_nodes = path
            
            for node in path_nodes:
                pygame.draw.rect(
                    screen, 
                    PATH_COLOR_HIGHLIGHT, 
                    (offset_x + node[1] * cell_width, offset_y + node[0] * cell_width, cell_width, cell_width)
                )
        
        # Dibujar inicio y fin
        pygame.draw.rect(
            screen, 
            START_COLOR, 
            (offset_x + start[1] * cell_width, offset_y + start[0] * cell_width, cell_width, cell_width)
        )
        pygame.draw.rect(
            screen, 
            END_COLOR, 
            (offset_x + end[1] * cell_width, offset_y + end[0] * cell_width, cell_width, cell_width)
        )
        
        # Mostrar información
        text = font.render(
            f"BFS - Nodos explorados: {nodes_explored} - Longitud del camino: {len(path)}", 
            True, 
            PATH_COLOR
        )
        screen.blit(text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
        
        # Finalizar visualización cuando se complete
        if completed and path_step >= len(path):
            time.sleep(2)  # Pausa para ver el resultado final
            return

def main():

    # Definir dimensiones
    ROWS = 60
    COLS = 80
    
    # Generar laberinto con Kruskal
    generator = KruskalMazeGenerator(rows=ROWS, cols=COLS)
    maze = generator.generateWithNograph()
    
    # Definir puntos de inicio y fin
    start = (1, 1)  # Coordenada (0,0) en el grid 2D
    end = (2 * ROWS - 1, 2 * COLS - 1)  # Coordenada (ROWS-1, COLS-1) en el grid 2D
    
    # Visualizar la búsqueda
    visualize_search(maze, start, end)
    
    # Cerrar Pygame al finalizar
    pygame.quit()

if __name__ == "__main__":
    main()








