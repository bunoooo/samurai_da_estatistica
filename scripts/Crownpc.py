import pygame
from scripts.Config import *
from scripts.ClassSpriteSheet import SpriteSheet
from scripts.HitboxEmemy import *

NpcCrowSprites = [(15, 16, 34, 55),
                   (80, 16, 34, 55),
                   (144,16, 34, 55),
                   (208, 16, 34, 55)]

class CrowNpc(pygame.sprite.Sprite):
    def __init__(self, position, faceRight=True, nome="Dr"):
        super().__init__()
        self.idleSpriteSheet = SpriteSheet(crow_path + "crow_idle.png", NpcCrowSprites)
        self.animationIndex = 0
        self.animationSpeed = 0.05
        self.faceRight = faceRight
        self.currentAnimation = self.idleSpriteSheet.getSprites(flipped=not self.faceRight)
        self.image = self.currentAnimation[int(self.animationIndex)]
        self.rect = self.image.get_rect(bottomleft=position)
        self.hitbox = Hitbox(self.rect.centerx, self.rect.bottom, 48, 48, scale_x=0.4, scale_y=0.8, offset_y=0)
        self.show_interaction = False
        self.currentState = 'IDLE'
        self.nome = nome  
        self.font = pygame.font.Font(font_path, 12)

    def update(self, level=None):
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.currentAnimation):
            self.animationIndex = 0

        self.currentAnimation = self.idleSpriteSheet.getSprites(flipped=not self.faceRight)
        self.image = self.currentAnimation[int(self.animationIndex)]
        self.hitbox.update(self.rect.centerx, self.rect.bottom)

    def draw(self, surface, camera):
        # Posição ajustada com a câmera
        screen_pos = camera.apply(self)
        surface.blit(self.image, screen_pos)

        # Nome acima
        nome_surface = self.font.render(self.nome, True, (255, 255, 255))
        nome_rect = nome_surface.get_rect(midbottom=(screen_pos.centerx, screen_pos.top +5))
        surface.blit(nome_surface, nome_rect)

        # Mensagem de interação
        if self.show_interaction:
            msg_pergunta = self.font.render("(P) Pergunta", True , (244,164,96))
            msg_pergunta_rect = msg_pergunta.get_rect(midbottom=(screen_pos.centerx, screen_pos.top - 15))
            surface.blit(msg_pergunta, msg_pergunta_rect)

            msg_surface = self.font.render("(E) Dialogo ", True, (244,164,96))
            msg_rect = msg_surface.get_rect(midbottom=(screen_pos.centerx, screen_pos.top - 5))
            surface.blit(msg_surface, msg_rect)