import pygame
from scripts.Config import *
from scripts.ClassSpriteSheet import SpriteSheet
from scripts.HitboxEmemy import *
# Frames da moeda no spritesheet

PotionSprites = [(0, 0, 8, 8), (8, 0, 8, 8), (16, 0, 8, 8), (24, 0, 8, 8)]

class Potion(pygame.sprite.Sprite):
    def __init__(self, position, scale=2):
        super().__init__()
        self.potionSpriteSheet = SpriteSheet(hud_path + "health_medium.png", PotionSprites)

        self.animationSpeed = 0.15
        self.animationIndex = 0
        
        # Carrega frames e aplica escala
        self.frames = [pygame.transform.scale(frame, 
                       (frame.get_width() * scale, frame.get_height() * scale))
                       for frame in self.potionSpriteSheet.getSprites(flipped=False)]
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=position)

        self.hitbox = Hitbox(self.rect.centerx, self.rect.y, 8, 8, scale_x = 1, scale_y = 1, offset_y=0)

    def update(self):
        # Atualiza animação
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.frames):
            self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]

    def die(self):
        self.kill()
    