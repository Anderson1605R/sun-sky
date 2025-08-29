

import pygame


class Personagem(pygame.sprite.Sprite):
    def __init__(self, frames_paths, pos_inicial, tamanho):
        super().__init__()

        self.frames = [pygame.transform.scale(pygame.image.load(
            p).convert_alpha(), tamanho) for p in frames_paths]
        self.frame_atual = 0
        self.image = self.frames[self.frame_atual]
        self.rect = self.image.get_rect(center=pos_inicial)

        # Variáveis de controle da animação
        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.intervalo_animacao = 150

    def update_animacao(self, is_moving):
        if is_moving:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_ultimo_frame > self.intervalo_animacao:
                self.frame_atual = (self.frame_atual + 1) % len(self.frames)
                self.image = self.frames[self.frame_atual]
                self.tempo_ultimo_frame = tempo_atual
        else:
            self.frame_atual = 0
            self.image = self.frames[self.frame_atual]

    def draw(self, tela):
        tela.blit(self.image, self.rect)
