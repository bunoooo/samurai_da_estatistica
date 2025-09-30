import pygame
from Config import *
from ClassSpriteSheet import SpriteSheet
from HitboxEmemy import *

NpcRobotSprites = [(x, 0, 48, 48) for x in range(0, 288, 48)]

class RobotNpc(pygame.sprite.Sprite):
    def __init__(self, position, faceRight=True):
        super().__init__()
        # Carrega spritesheet
        self.idleSpriteSheet = SpriteSheet(robot_path + "npc_robot.png", NpcRobotSprites)
        
        # Inicializa animação
        self.animationIndex = 0
        self.animationSpeed = 0.1  # velocidade da animação
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
