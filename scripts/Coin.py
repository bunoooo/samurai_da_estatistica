import pygame
from scripts.Config import *
from scripts.ClassSpriteSheet import SpriteSheet
from scripts.HitboxEmemy import *
# Frames da moeda no spritesheet
CoinSprites = [(x, 0, 8, 8) for x in range(0, 144,8)]

class Coin(pygame.sprite.Sprite):
    def __init__(self, position, scale=2):
        super().__init__()
        self.coinSpriteSheet = SpriteSheet(hud_path + "SpinningCoin.png", CoinSprites)

        self.animationSpeed = 0.15
        self.animationIndex = 0
        
        # Carrega frames e aplica escala
        self.frames = [pygame.transform.scale(frame, 
                       (frame.get_width() * scale, frame.get_height() * scale))
                       for frame in self.coinSpriteSheet.getSprites(flipped=False)]
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=position)

        self.hitbox = Hitbox(self.rect.centerx, self.rect.y, 8, 8, scale_x = 1, scale_y = 1.4, offset_y=0)


    def update(self):
        # Atualiza animação
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.frames):
            self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]

    def die(self):
        self.kill()
    