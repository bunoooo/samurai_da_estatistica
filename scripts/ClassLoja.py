import pygame
from Config import *
from ClassSpriteSheet import SpriteSheet
from HitboxEmemy import *

NpcLojaSprites = [(31, 48, 88, 67),
                   (175, 48, 88, 67),
                   (319, 48, 88, 67),
                   (463, 48, 88, 67)]

class LojaNpc(pygame.sprite.Sprite):
    def __init__(self, position, faceRight=True):
        super().__init__()
        # Carrega spritesheet
        self.idleSpriteSheet = SpriteSheet(loja_path + "idle_loja.png", NpcLojaSprites)
        
        # Inicializa animação
        self.animationIndex = 0
        self.animationSpeed = 0.075  # velocidade da animação
        self.faceRight = faceRight
        self.currentAnimation = self.idleSpriteSheet.getSprites(flipped=not self.faceRight)
        self.image = self.currentAnimation[int(self.animationIndex)]
        
        # Posição e retângulo
        self.rect = self.image.get_rect(bottomleft=position)
        
        # Hitbox
        self.hitbox = Hitbox(self.rect.centerx, self.rect.bottom, 48, 48, scale_x=0.4, scale_y=0.8, offset_y=0)
        
        # Estado
        self.currentState = 'IDLE'

    def update(self, level=None):
        # Atualiza animação
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.currentAnimation):
            self.animationIndex = 0
        
        # Atualiza sprite com flip dependendo da direção
        self.currentAnimation = self.idleSpriteSheet.getSprites(flipped=not self.faceRight)
        self.image = self.currentAnimation[int(self.animationIndex)]
        
        # Atualiza hitbox
        self.hitbox.update(self.rect.centerx, self.rect.bottom)

    def draw_hitbox(self, surface):
        self.hitbox.draw(surface)