import pygame
import sys
from algoritmos.kruskal import generateMazeKruskal
from algoritmos.prim import generateMazePrim


def promptDimensionsUI(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 60)
    text = font.render("Escoge dimensiones en la consola...", True, (255, 255, 255))
    screen.blit(text, (100, 300))
    pygame.display.update()


def promptDimensions():
    print("\n=== Configuración del Laberinto ===")
    print("1. Usar tamaño por defecto (50 x 50)")
    print("2. Ingresar tamaño personalizado")
    choice = input("Selecciona una opción: ")

    if choice == "1":
        return 50, 50
    elif choice == "2":
        try:
            rows = int(input("Filas: "))
            cols = int(input("Columnas: "))
            return rows, cols
        except ValueError:
            print("Entrada inválida. Intenta de nuevo.")
            return promptDimensions()
    else:
        print("Opción inválida.")
        return promptDimensions()


def mainMenu():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Generador de Laberintos")

    font = pygame.font.Font(None, 72)
    titleText = font.render("Selecciona un algoritmo:", True, (255, 255, 255))
    kruskalText = font.render("1. Kruskal", True, (255, 255, 255))
    primText = font.render("2. Prim", True, (255, 255, 255))
    exitText = font.render("ESC. Salir", True, (200, 200, 200))

    fullscreen = False
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(titleText, (50, 100))
        screen.blit(kruskalText, (50, 200))
        screen.blit(primText, (50, 300))
        screen.blit(exitText, (50, 400))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_KP1):
                    promptDimensionsUI(screen)
                    rows, cols = promptDimensions()
                    generateMazeKruskal(rows, cols, seed=42)
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    promptDimensionsUI(screen)
                    rows, cols = promptDimensions()
                    generateMazePrim(rows, cols, seed=42)
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    mainMenu()
