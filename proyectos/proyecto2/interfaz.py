import pygame
import sys
from algoritmos.kruskal import KruskalMazeGenerator
from algoritmos.prim import PrimMazeGenerator

# ================== CONFIGURACIÓN ==================
WINDOW_SIZE = (1280, 720)
FONT_SIZE = 60
DEFAULT_SEED_STRUCTURE = 1234
DEFAULT_SEED_WEIGHTS = 56789
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
DEFAULT_ROWS = 50
DEFAULT_COLS = 50
# ===================================================

class LaberintoApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
        pygame.display.set_caption("Generador de Laberintos")
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.weighted = False

    def run(self):
        self.mainMenu()
        pygame.quit()
        sys.exit()

    def mainMenu(self):
        selecting = True
        while selecting:
            self.screen.fill(BACKGROUND_COLOR)
            options = [
                "1. Laberinto Ponderado",
                "2. Laberinto No Ponderado",
                "ESC. Salir"
            ]
            self.renderOptions(options)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    selecting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        self.weighted = True
                        self.algorithmSelectionMenu()
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        self.weighted = False
                        self.algorithmSelectionMenu()
                    elif event.key == pygame.K_ESCAPE:
                        selecting = False

    def algorithmSelectionMenu(self):
        selecting = True
        while selecting:
            self.screen.fill(BACKGROUND_COLOR)
            options = [
                "1. Kruskal",
                "2. Prim",
                "ESC. Volver"
            ]
            self.renderOptions(options)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        self.runMazeGenerator("kruskal")
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        self.runMazeGenerator("prim")
                    elif event.key == pygame.K_ESCAPE:
                        selecting = False

    def runMazeGenerator(self, algorithm):
        self.promptDimensionsUI()
        rows, cols = self.promptDimensions()

        if algorithm == "kruskal":
            generator = KruskalMazeGenerator(
                rows=rows, cols=cols, 
                weighted=self.weighted, 
                seed_structure=DEFAULT_SEED_STRUCTURE, 
                seed_weights=DEFAULT_SEED_WEIGHTS
            )
        else:
            generator = PrimMazeGenerator(
                rows=rows, cols=cols, 
                weighted=self.weighted, 
                seed_structure=DEFAULT_SEED_STRUCTURE, 
                seed_weights=DEFAULT_SEED_WEIGHTS
            )

        laberinto = generator.generate()
        self.postGenerationMenu(laberinto)

    def postGenerationMenu(self, laberinto):
        selecting = True
        while selecting:
            self.screen.fill(BACKGROUND_COLOR)
            options = [
                "1. Generar nuevo laberinto",
                "2. Aplicar algoritmo de búsqueda",
                "ESC. Volver al menú principal"
            ]
            self.renderOptions(options)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_1, pygame.K_KP1):
                        self.mainMenu()
                        selecting = False
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        self.searchAlgorithmMenu(laberinto)
                    elif event.key == pygame.K_ESCAPE:
                        selecting = False

    def searchAlgorithmMenu(self, laberinto):
        selecting = True
        while selecting:
            self.screen.fill(BACKGROUND_COLOR)
            options = [
                "1. BFS",
                "2. DFS",
                "3. Cost Uniform Search",
                "4. A*",
                "ESC. Volver"
            ]
            self.renderOptions(options)

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

    def promptDimensionsUI(self):
        self.screen.fill(BACKGROUND_COLOR)
        text = self.font.render("Escoge dimensiones en la consola...", True, TEXT_COLOR)
        self.screen.blit(text, (100, 300))
        pygame.display.update()

    def promptDimensions(self):
        print("\n=== Configuración del Laberinto ===")
        print("1. Usar tamaño por defecto (50 x 50)")
        print("2. Ingresar tamaño personalizado")
        choice = input("Selecciona una opción: ")

        if choice == "1":
            return DEFAULT_ROWS, DEFAULT_COLS
        elif choice == "2":
            try:
                rows = int(input("Filas: "))
                cols = int(input("Columnas: "))
                return rows, cols
            except ValueError:
                print("Entrada inválida. Intenta de nuevo.")
                return self.promptDimensions()
        else:
            print("Opción inválida.")
            return self.promptDimensions()

    def renderOptions(self, options):
        for idx, text in enumerate(options):
            option_text = self.font.render(text, True, TEXT_COLOR)
            self.screen.blit(option_text, (50, 100 + idx * 80))
        pygame.display.update()

if __name__ == "__main__":
    app = LaberintoApp()
    app.run()
