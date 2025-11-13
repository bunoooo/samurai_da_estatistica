import pygame
from scripts.Config import *
from scripts.ClassSpriteSheet import SpriteSheet
from scripts.HitboxEmemy import *

NpcLojaSprites = [(31, 48, 88, 67),
                   (175, 48, 88, 67),
                   (319, 48, 88, 67),
                   (463, 48, 88, 67)]

class LojaNpc(pygame.sprite.Sprite):
    def __init__(self, position, faceRight=True , nome = "Mercador"):
        super().__init__()
        # Carrega spritesheet
        self.idleSpriteSheet = SpriteSheet(loja_path + "idle_loja.png", NpcLojaSprites)
        self.nome = nome  
        self.show_interaction = False
        # Inicializa animação
        self.animationIndex = 0
        self.animationSpeed = 0.075  # velocidade da animação
        self.faceRight = faceRight
        self.currentAnimation = self.idleSpriteSheet.getSprites(flipped=not self.faceRight)
        self.image = self.currentAnimation[int(self.animationIndex)]
        self.font = pygame.font.Font(font_path, 12)
        
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

    def draw(self, surface, camera):
        # Posição ajustada com a câmera
        screen_pos = camera.apply(self)
        surface.blit(self.image, screen_pos)

        # Nome acima
        nome_surface = self.font.render(self.nome, True, (255, 255, 255))
        nome_rect = nome_surface.get_rect(midbottom=(screen_pos.centerx + 5, screen_pos.top + 15))
        surface.blit(nome_surface, nome_rect)

        # Mensagem de interação
        if self.show_interaction:
            msg = self.font.render("(B) Abrir loja", True , (255, 255, 255))
            msg_rect = msg.get_rect(midbottom=(screen_pos.centerx , screen_pos.top + 5))
            surface.blit(msg, msg_rect)

           