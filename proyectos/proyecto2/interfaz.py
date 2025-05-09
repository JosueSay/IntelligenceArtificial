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

def searchAlgorithmMenu(screen):
    selecting = True
    font = pygame.font.Font(None, 60)

    while selecting:
        screen.fill((0, 0, 0))
        options = [
            "1. BFS",
            "2. DFS",
            "3. Cost Uniform Search",
            "4. A*",
            "ESC. Volver"
        ]
        for idx, text in enumerate(options):
            option_text = font.render(text, True, (255, 255, 255))
            screen.blit(option_text, (50, 100 + idx * 80))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_KP1,
                                 pygame.K_2, pygame.K_KP2,
                                 pygame.K_3, pygame.K_KP3,
                                 pygame.K_4, pygame.K_KP4):
                    print("Aquí se aplica el algoritmo de búsqueda.")
                elif event.key == pygame.K_ESCAPE:
                    selecting = False

def postGenerationMenu(screen, laberinto):
    selecting = True
    font = pygame.font.Font(None, 60)

    while selecting:
        screen.fill((0, 0, 0))
        options = [
            "1. Generar nuevo laberinto",
            "2. Aplicar algoritmo de búsqueda",
            "ESC. Volver al menú principal"
        ]
        for idx, text in enumerate(options):
            option_text = font.render(text, True, (255, 255, 255))
            screen.blit(option_text, (50, 100 + idx * 80))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_KP1):
                    runGenerationFlow(screen)
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    searchAlgorithmMenu(screen)
                elif event.key == pygame.K_ESCAPE:
                    selecting = False

def runGenerationFlow(screen):
    font = pygame.font.Font(None, 72)
    selecting_algo = True

    while selecting_algo:
        screen.fill((0, 0, 0))
        screen.blit(font.render("Selecciona un algoritmo:", True, (255, 255, 255)), (50, 100))
        screen.blit(font.render("1. Kruskal", True, (255, 255, 255)), (50, 200))
        screen.blit(font.render("2. Prim", True, (255, 255, 255)), (50, 300))
        screen.blit(font.render("ESC. Salir", True, (255, 255, 250)), (50, 400))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_KP1):
                    promptDimensionsUI(screen)
                    rows, cols = promptDimensions()
                    laberinto = generateMazeKruskal(rows, cols, seed=42)
                    postGenerationMenu(screen, laberinto)
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    promptDimensionsUI(screen)
                    rows, cols = promptDimensions()
                    laberinto = generateMazePrim(rows, cols, seed=42)
                    postGenerationMenu(screen, laberinto)
                elif event.key == pygame.K_ESCAPE:
                    selecting_algo = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Generador de Laberintos")
    runGenerationFlow(screen)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
