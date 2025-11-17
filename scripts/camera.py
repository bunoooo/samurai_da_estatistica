from scripts.Config import *
import pygame


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)  # Retângulo da câmera
        self.world_size = (width, height)  # Tamanho do mundo (tamanho total do level)
        self.camera_speed = 5  # Velocidade do scroll (ajustável)

    def apply(self, entity):
        # Ajusta a posição de cada entidade com base no deslocamento da câmera
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # Movimenta a câmera de acordo com a posição do alvo (personagem)
        x = -target.rect.centerx + int(WINDOW_WIDTH / 2)
        y = -target.rect.centery + int(WINDOW_HEIGHT / 2)

        # Impede que a câmera ultrapasse os limites do mundo
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.world_size[0] - WINDOW_WIDTH), x)
        y = max(-(self.world_size[1] - WINDOW_HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.camera.width, self.camera.height)
