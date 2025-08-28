import pygame


class Game:
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode(size=(576, 324))

        pygame.display.set_caption("Sun & Sky")

        try:
            self.surf = pygame.image.load(
                "assets/background/city 8/6.png").convert()
        except pygame.error as e:
            print(f"Erro ao carregar a imagem: {e}")
            print("Verifique se o caminho 'assets/background/city 8/6.png' está correto.")
            quit()

        self.rect = self.surf.get_rect(topleft=(0, 0))

    def run(self):
        while True:
            # --- 1. Eventos ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.window.blit(source=self.surf, dest=self.rect)

            pygame.display.flip()
