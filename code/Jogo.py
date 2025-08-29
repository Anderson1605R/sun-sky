import pygame

from code.Cachorro import Cachorro
from code.Gato import Gato


LARGURA_TELA = 800
ALTURA_TELA = 600
TITULO = "Sun & Sky"
PRETO = (0, 0, 0)


class Jogo:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.font.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption(TITULO)
        self.relogio = pygame.time.Clock()
        self.rodando = True
        self.placar = 0

        self._carregar_assets()

        tela_rect = self.tela.get_rect()
        self.gato = Gato(pos_inicial=tela_rect.center, tela_rect=tela_rect)
        self.cachorro = Cachorro(pos_inicial=(100, 100), tela_rect=tela_rect)

    def _carregar_assets(self):
        try:
            self.fundo_img = pygame.transform.scale(pygame.image.load(
                'assets/background/city 8/6.png').convert(), (LARGURA_TELA, ALTURA_TELA))
            self.fonte_placar = pygame.font.SysFont('Arial', 30)
            pygame.mixer.music.load('assets/musicas/musicafnd.mp3')
            self.som_ponto = pygame.mixer.Sound('assets/musicas/efeitocpt.wav')
        except pygame.error as e:
            print(f"Erro ao carregar assets: {e}")
            self.rodando = False

    def _processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False

    def _atualizar_estado(self):
        self.gato.update()
        self.cachorro.update(self.gato.rect.center)

        # Checar colisão
        if pygame.sprite.collide_rect(self.gato, self.cachorro):
            self.placar += 1
            self.cachorro.reset()
            self.som_ponto.play()

    def _desenhar_elementos(self):
        self.tela.blit(self.fundo_img, (0, 0))
        self.gato.draw(self.tela)
        self.cachorro.draw(self.tela)
        texto_placar = self.fonte_placar.render(
            f'Capturas: {self.placar}', True, PRETO)
        self.tela.blit(texto_placar, (10, 10))

        pygame.display.flip()

    def run(self):
        pygame.mixer.music.set_volume(0.4)  # Volume em 40%
        pygame.mixer.music.play(-1)
        while self.rodando:
            self.relogio.tick(60)
            self._processar_eventos()
            self._atualizar_estado()
            self._desenhar_elementos()

        pygame.quit()
