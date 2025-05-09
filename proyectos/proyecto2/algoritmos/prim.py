import random
import pygame
import time

def generateMazePrim(rows=50, cols=50, seed=None):
    random.seed(seed)
    pygame.init()

    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Laberinto con Prim")

    def drawAndResize():
        screenWidth, screenHeight = screen.get_size()
        cellSize = min(screenWidth // (2 * cols + 1), screenHeight // (2 * rows + 1))
        mazeWidth = cellSize * (2 * cols + 1)
        mazeHeight = cellSize * (2 * rows + 1)
        offsetX = (screenWidth - mazeWidth) // 2
        offsetY = (screenHeight - mazeHeight) // 2
        return cellSize, offsetX, offsetY

    cellSize, offsetX, offsetY = drawAndResize()
    maze = [[1 for _ in range(2 * cols + 1)] for _ in range(2 * rows + 1)]

    start_r, start_c = random.randint(0, rows - 1), random.randint(0, cols - 1)
    maze[2 * start_r + 1][2 * start_c + 1] = 0

    frontier = []
    def addFrontier(r, c):
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[2 * nr + 1][2 * nc + 1] == 1:
                if (nr, nc) not in frontier:
                    frontier.append((nr, nc))

    addFrontier(start_r, start_c)

    while frontier:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return maze
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return maze

        r, c = random.choice(frontier)
        neighbors = []

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[2 * nr + 1][2 * nc + 1] == 0:
                neighbors.append((nr, nc))

        if neighbors:
            nr, nc = random.choice(neighbors)
            wallR = r + nr + 1
            wallC = c + nc + 1
            maze[2 * r + 1][2 * c + 1] = 0
            maze[wallR][wallC] = 0

            addFrontier(r, c)

        frontier.remove((r, c))

        cellSize, offsetX, offsetY = drawAndResize()
        drawMaze(screen, maze, cellSize, offsetX, offsetY)
        time.sleep(0.005)

    print("Laberinto generado con éxito usando Prim. Pulsa ESC para salir o volver al menú.")
    waitForExit()
    return maze


def drawMaze(screen, maze, cellSize, offsetX, offsetY):
    screen.fill((255, 255, 255))
    for r, row in enumerate(maze):
        for c, val in enumerate(row):
            color = (0, 0, 0) if val == 1 else (255, 255, 255)
            pygame.draw.rect(
                screen,
                color,
                (offsetX + c * cellSize, offsetY + r * cellSize, cellSize, cellSize)
            )
    pygame.display.update()


def waitForExit():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False