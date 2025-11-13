import pygame
from scripts.Config import *
from scripts.ClassSpriteSheet import SpriteSheet
from scripts.HitboxEmemy import *

#RobotSprites = [
 #   (0, 0, 32, 32),
  #  (31, 0, 32, 32),
   # (61, 0, 30, 30),
    #(0,32,30,30),
    #(31,31,30,30),
    #(63,31,30,30)
#]

RobotSprites = [(x, 0, 48, 48) for x in range(0, 672, 48)]


class Robot(pygame.sprite.Sprite):
    def __init__(self, position, moveRight, limit_left, limit_right):
        super().__init__()
        self.walkSpriteSheet = SpriteSheet(robot_path + "npc1-Sheet.png", RobotSprites)
        self.limit_left = limit_left
        self.limit_right = limit_right
        self.image = self.walkSpriteSheet.getSprites(moveRight)[0]
        self.rect = self.image.get_rect(bottomleft=position)
        self.movingRight = moveRight
        self.animationIndex = 0
        self.currentState = 'WALK'
        self.heroDetected = False
        self.baseSpeed = SPEED_ROBOT
        self.alertSpeed = SPEED_ROBOT * 2
        self.animationSpeed = ANIMSPEED_BEE
        self.currentAnimation = self.walkSpriteSheet.getSprites(self.movingRight)
        self.yDir = 0

        # Nova hitbox com classe
        self.hitbox = Hitbox(self.rect.centerx, self.rect.bottom, 48, 48, scale_x=0.6, scale_y=0.8, offset_y=0)

    def update(self, level):
        hero_rect = level.hero.sprite.rect
        distance_to_hero = abs(self.rect.centerx - hero_rect.centerx)
        if distance_to_hero < 80 and abs(self.rect.centery - hero_rect.centery) < 40:
            self.heroDetected = True
        else:
            self.heroDetected = False

        if self.currentState != 'DYING':
            speed = self.alertSpeed if self.heroDetected else self.baseSpeed
            self.rect.x += speed if self.movingRight else -speed

            if self.rect.left <= self.limit_left:
                self.movingRight = True
            elif self.rect.right >= self.limit_right:
                self.movingRight = False

        self.selectAnimation()
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.currentAnimation):
            self.animationIndex = 0
        self.image = self.currentAnimation[int(self.animationIndex)]

        # Atualiza a hitbox com base na posição atual
        self.hitbox.update(self.rect.centerx, self.rect.bottom)

        if self.currentState == 'DYING':
            self.yDir += GRAVITY
            self.rect.y += self.yDir
            if self.rect.top > WINDOW_HEIGHT:
                self.kill()

    def selectAnimation(self):
        if self.currentState == 'DYING':
            self.currentAnimation = [self.image]
        else:
            self.currentAnimation = self.walkSpriteSheet.getSprites(flipped=not self.movingRight)

    def die(self):
        if self.currentState != 'DYING':
            self.currentState = 'DYING'
            self.animationIndex = 0
            self.yDir = 0

    def draw_hitbox(self, surface):
        # (Opcional) Para debug visual
        self.hitbox.draw(surface)
