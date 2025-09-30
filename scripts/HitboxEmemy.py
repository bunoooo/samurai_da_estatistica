import pygame

class Hitbox:
    def __init__(self, x_center, y_bottom, width, height, scale_x=0.6, scale_y=0.7, offset_y=0, offset_x=0):
        """
        Classe para criar e manipular uma hitbox proporcional à sprite.
        """
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.offset_y = offset_y
        self.offset_x = offset_x
        self.width = width
        self.height = height

        self.update(x_center, y_bottom)

    def update(self, x_center, y_bottom):
        """
        Atualiza a posição da hitbox com base no centro X e na base Y do sprite.
        """
        new_width = int(self.width * self.scale_x)
        new_height = int(self.height * self.scale_y)

        x = x_center - new_width // 2 + self.offset_x
        y = y_bottom - new_height + self.offset_y

        self.rect = pygame.Rect(x, y, new_width, new_height)

    def draw(self, surface, color=(255, 0, 0)):
        """
        (Opcional) Desenha a hitbox para debug.
        """
        pygame.draw.rect(surface, color, self.rect, 2)
