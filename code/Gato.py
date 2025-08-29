import pygame

from code.Personagem import Personagem


class Gato(Personagem):
    def __init__(self, pos_inicial, tela_rect):
        frames = ['assets/personagens/4 Cat 2/1.png',
                  'assets/personagens/4 Cat 2/2.png', 'assets/personagens/4 Cat 2/3.png']
        super().__init__(frames, pos_inicial, (50, 50))

        self.velocidade = 4.5
        self.movendo = False
        self.tela_rect = tela_rect

    def update(self):

        self.movendo = False
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidade
            self.movendo = True
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidade
            self.movendo = True
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidade
            self.movendo = True
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidade
            self.movendo = True

        self.rect.clamp_ip(self.tela_rect)

        self.update_animacao(self.movendo)
