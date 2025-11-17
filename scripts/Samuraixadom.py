import pygame
from scripts.Config import *
from scripts.ClassSpriteSheet import SpriteSheet
from scripts.HitboxEmemy import *

# --- SPRITESHEETS CONFIG --- #
SamuraiSpritesrun = [(x, 0, 48, 50) for x in range(0, 672, 96)]
SamuraiSpritesAttackPaths = [ samuraixamom_path + f"{i}.png" for i in range(0, 6)]


class Samuraixamom(pygame.sprite.Sprite):
    def __init__(self, position, moveRight, limit_left, limit_right):
        super().__init__()
        self.walkSpriteSheet = SpriteSheet(samuraixamom_path + "RUN.png", SamuraiSpritesrun)
        self.attackSprites = [pygame.image.load(path).convert_alpha() for path in SamuraiSpritesAttackPaths]

        self.limit_left = limit_left
        self.limit_right = limit_right
        self.image = self.walkSpriteSheet.getSprites(moveRight)[0]
        self.rect = self.image.get_rect(bottomleft=position)
        self.movingRight = moveRight

        # Estado e animação
        self.animationIndex = 0
        self.currentState = 'WALK'
        self.heroDetected = False
        self.baseSpeed = SPEED_ROBOT
        self.animationSpeed = ANIMSPEED_BEE
        self.currentAnimation = self.walkSpriteSheet.getSprites(self.movingRight)
        self.yDir = 0

        # Hitboxes
        self.hitbox = Hitbox(self.rect.centerx, self.rect.bottom, 22, 32, scale_x=0.6, scale_y=1, offset_y=0)
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)  # inicializada vazia

    def update(self, level):
        hero_rect = level.hero.sprite.rect
        hero_hitbox = level.hero.sprite.hitbox

        # Direção e distância
        if self.movingRight:
            in_front = hero_rect.centerx > self.rect.centerx
            distance_to_hero = hero_rect.left - self.rect.right + 25
        else:
            in_front = hero_rect.centerx < self.rect.centerx
            distance_to_hero = self.rect.left - hero_rect.right + 15

        vertical_diff = abs(self.rect.centery - hero_rect.centery)
        vertical_limit = 10
        self.heroDetected = in_front and vertical_diff <= vertical_limit

        min_attack_distance = 6  # distância mínima para ataque

        if self.currentState != 'DYING':
            if self.heroDetected:
                if distance_to_hero > min_attack_distance:
                    # Aproxima
                    self.currentState = 'WALK'
                    self.align_to_ground()
                    speed = self.baseSpeed
                    self.rect.x += speed if self.movingRight else -speed
                    self.attack_hitbox = pygame.Rect(0, 0, 0, 0)  # sem hitbox
                else:
                    # Ataca
                    if self.currentState != 'ATTACK':
                        self.currentState = 'ATTACK'
                        self.align_to_ground()

                    # Cria hitbox próxima do herói
                    offset = 5
                    if self.movingRight:
                        self.attack_hitbox = pygame.Rect(
                            self.rect.right - offset, self.rect.top + 10, 30, 35
                        )
                    else:
                        self.attack_hitbox = pygame.Rect(
                            self.rect.left - 30 + offset, self.rect.top + 10, 30, 35
                        )

            else:
                # Patrulha
                if self.currentState != 'WALK':
                    self.currentState = 'WALK'
                    self.align_to_ground()
                speed = self.baseSpeed
                self.rect.x += speed if self.movingRight else -speed
                self.attack_hitbox = pygame.Rect(0, 0, 0, 0)

        # Limites
        if self.rect.left <= self.limit_left:
            self.movingRight = True
        elif self.rect.right >= self.limit_right:
            self.movingRight = False

        # Gravidade e remoção
        if self.currentState == 'DYING':
            self.yDir += GRAVITY
            self.rect.y += self.yDir
            if self.rect.top > WINDOW_HEIGHT:
                self.kill()

        # Atualiza animação e hitbox
        self.selectAnimation()
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.currentAnimation):
            self.animationIndex = 0
        self.image = self.currentAnimation[int(self.animationIndex)]
        self.hitbox.update(self.rect.centerx, self.rect.bottom)

    def selectAnimation(self):
        if self.currentState == 'DYING':
            self.currentAnimation = [self.image]
        elif self.currentState == 'ATTACK':
            if self.movingRight:
                self.currentAnimation = self.attackSprites
            else:
                self.currentAnimation = [pygame.transform.flip(img, True, False) for img in self.attackSprites]
        else:
            self.currentAnimation = self.walkSpriteSheet.getSprites(flipped=not self.movingRight)

    def align_to_ground(self):
        bottom = self.rect.bottom
        centerx = self.rect.centerx
        self.selectAnimation()
        self.image = self.currentAnimation[0]
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.centerx = centerx

    def die(self):
        if self.currentState != 'DYING':
            self.currentState = 'DYING'
            self.animationIndex = 0
            self.yDir = 0

    def draw_hitbox(self, surface):
        self.hitbox.draw(surface)
        if self.attack_hitbox.width > 0:
            pygame.draw.rect(surface, (255, 0, 0), self.attack_hitbox, 2)

    def draw_detection_zone(self, surface):
        color = (255, 0, 0) if self.heroDetected else (100, 0, 0)
        if self.movingRight:
            zone_rect = pygame.Rect(self.rect.right, self.rect.top, 60, self.rect.height)
        else:
            zone_rect = pygame.Rect(self.rect.left - 60, self.rect.top, 60, self.rect.height)
        pygame.draw.rect(surface, color, zone_rect, 2)
