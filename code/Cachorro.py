import pygame
import random
import math

from code.Personagem import Personagem


class Cachorro(Personagem):
    def __init__(self, pos_inicial, tela_rect):
        frames = ['assets/personagens/2 Dog 2/1.png',
                  'assets/personagens/2 Dog 2/2.png', 'assets/personagens/2 Dog 2/3.png']
        super().__init__(frames, pos_inicial, (50, 50))

        self.velocidade = 5.0
        self.aceleracao_fuga = 0.08
        self.tela_rect = tela_rect  # Guarda o retângulo da tela para checar limites
        self.IMPULSO_RICOCHETE = 0.4  # Força do "empurrão" para longe da parede
        self.SCATTER_RICOCHETE = 0.3  # Adiciona um pouco de aleatoriedade no ângulo de saída
        self._iniciar_movimento_aleatorio()

    def _iniciar_movimento_aleatorio(self):

        angulo_inicial = random.uniform(0, 2 * math.pi)
        self.dx = math.cos(angulo_inicial)
        self.dy = math.sin(angulo_inicial)

    def update(self, pos_gato):
        """Atualiza a IA do cachorro (fugir, ricochetear) e a animação."""
        # 1. Calcular a força de fuga
        dx_fuga = self.rect.centerx - pos_gato[0]
        dy_fuga = self.rect.centery - pos_gato[1]
        dist_gato = math.hypot(dx_fuga, dy_fuga)
        if dist_gato > 0:
            dx_fuga /= dist_gato
            dy_fuga /= dist_gato

        # 2. Aplicar aceleração para influenciar a direção atual
        self.dx += dx_fuga * self.aceleracao_fuga

        # <<< MUDANÇA IMPORTANTE: A ORDEM FOI ALTERADA >>>
        # A normalização agora acontece DEPOIS de verificar o ricochete.

        # 3. Lógica de Ricochete FORTE (NOVA LÓGICA)
        ricocheteou = False
        if self.rect.left <= 0:
            # Força a direção X para ser positiva (ir para a DIREITA)
            self.dx = abs(self.dx) + self.IMPULSO_RICOCHETE
            # Adiciona aleatoriedade na direção Y
            self.dy += random.uniform(-self.SCATTER_RICOCHETE,
                                      self.SCATTER_RICOCHETE)
            ricocheteou = True

        if self.rect.right >= self.tela_rect.width:
            # Força a direção X para ser negativa (ir para a ESQUERDA)
            self.dx = -abs(self.dx) - self.IMPULSO_RICOCHETE
            self.dy += random.uniform(-self.SCATTER_RICOCHETE,
                                      self.SCATTER_RICOCHETE)
            ricocheteou = True

        if self.rect.top <= 0:
            # Força a direção Y para ser positiva (ir para BAIXO)
            self.dy = abs(self.dy) + self.IMPULSO_RICOCHETE
            # Adiciona aleatoriedade na direção X
            self.dx += random.uniform(-self.SCATTER_RICOCHETE,
                                      self.SCATTER_RICOCHETE)
            ricocheteou = True

        if self.rect.bottom >= self.tela_rect.height:
            # Força a direção Y para ser negativa (ir para CIMA)
            self.dy = -abs(self.dy) - self.IMPULSO_RICOCHETE
            self.dx += random.uniform(-self.SCATTER_RICOCHETE,
                                      self.SCATTER_RICOCHETE)
            ricocheteou = True

        # 4. Normalizar para manter velocidade constante (AGORA É O PASSO 4)
        # Se houve um ricochete, o vetor (dx, dy) foi alterado e precisa ser normalizado
        # para garantir que a velocidade do cachorro não aumente.
        velocidade_atual = math.hypot(self.dx, self.dy)
        if velocidade_atual > 0:
            self.dx /= velocidade_atual
            self.dy /= velocidade_atual

        # 5. Aplicar movimento final
        self.rect.x += self.dx * self.velocidade
        self.rect.y += self.dy * self.velocidade
        # Garante que ele não fique preso fora da tela
        self.rect.clamp_ip(self.tela_rect)

        self.update_animacao(True)  # O cachorro está sempre se movendo

    def reset(self):
        """Reposiciona o cachorro e dá a ele uma nova direção aleatória."""
        self.rect.center = (random.randint(
            50, self.tela_rect.width - 50), random.randint(50, self.tela_rect.height - 50))
        self._iniciar_movimento_aleatorio()
