import pygame
from scripts.Config import *
from scripts.ClassSpriteSheet import *
from scripts.HitboxEmemy import *


class Portal(pygame.sprite.Sprite):
    def __init__(self, position, nome="Portal"):
        super().__init__()
        # --- Carregamento dos frames individuais ---
        self.frames = []
        for i in range(1, 9):  # tile1.png a tile8.png
            img = pygame.image.load(f"{portal_path}tile{i}.png").convert_alpha()
            self.frames.append(img)

        self.portal_show_interaction = False
        # --- Controle de animação ---
        self.animationIndex = 0
        self.animationSpeed = 0.2  # Ajuste fino da velocidade
        self.image = self.frames[int(self.animationIndex)]

        # --- Posição e hitbox --- #
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = Hitbox(self.rect.centerx, self.rect.bottom, 48, 48, scale_x=0.8, scale_y=0.8, offset_y=0)

        # --- Extras ---
        self.nome = nome
        self.font = pygame.font.Font(font_path, 12)
        self.show_interaction = False

    def update(self, level=None):
        # Atualiza a animação
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.frames):
            self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]

        # Atualiza hitbox conforme posição atual
        self.hitbox.update(self.rect.centerx, self.rect.bottom)

    def draw(self, surface, camera):
        # Posição ajustada pela câmera
        screen_pos = camera.apply(self)
        

        # Nome acima
        nome_surface = self.font.render(self.nome, True, (255, 255, 255))
        nome_rect = nome_surface.get_rect(midbottom=(screen_pos.centerx, screen_pos.top + 5))
        surface.blit(nome_surface, nome_rect)

        # Mensagens de interação (exemplo)
        if self.portal_show_interaction:
            msg_entrar = self.font.render("(H) Entrar", True, (255, 255, 255))
            msg_entrar_rect = msg_entrar.get_rect(midbottom=(screen_pos.centerx, screen_pos.top - 5))
            surface.blit(msg_entrar, msg_entrar_rect)
