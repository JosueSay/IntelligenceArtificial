import random
import pygame
import time


class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1
            return True
        return False


def generateMazeKruskal(rows=50, cols=50, seed=None):
    random.seed(seed)
    pygame.init()

    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Laberinto con Kruskal")

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
    uf = UnionFind(rows * cols)

    edges = [((r, c), (r, c + 1)) for r in range(rows) for c in range(cols - 1)] + \
            [((r, c), (r + 1, c)) for r in range(rows - 1) for c in range(cols)]
    random.shuffle(edges)

    for (r1, c1), (r2, c2) in edges:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return maze
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return maze

        idx1 = r1 * cols + c1
        idx2 = r2 * cols + c2
        if uf.union(idx1, idx2):
            maze[2 * r1 + 1][2 * c1 + 1] = 0
            maze[2 * r2 + 1][2 * c2 + 1] = 0
            maze[r1 + r2 + 1][c1 + c2 + 1] = 0

            cellSize, offsetX, offsetY = drawAndResize()
            drawMaze(screen, maze, cellSize, offsetX, offsetY)
            time.sleep(0.005)

    print("Laberinto generado con éxito. Pulsa ESC para salir o volver al menú.")
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