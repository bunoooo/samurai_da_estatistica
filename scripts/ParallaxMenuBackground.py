import pygame
from pytmx.util_pygame import load_pygame
from scripts.Config import LEVELS_PATH, TILESIZE
from scripts.ClassBackground import Background
from scripts.ClassHero import Hero

class StaticMenuBackground:
    def __init__(self, surface):
        self.display_surface = surface

        # Carrega o mapa do fundo do menu
        self.levelData = load_pygame(LEVELS_PATH + "Level1/level_ajustado.tmx")

        self.background = Background()
        self.hero = pygame.sprite.GroupSingle()

        # Carrega camadas do fundo
        self.background_layer = self.load_layer('Background')
        self.arvores_layer = self.load_layer('Arvores')
        self.background2_layer = self.load_layer('Background2')
        self.platform_layer = self.load_layer('Platforms')

        
    def load_layer(self, name):
        layer = []
        tmx_layer = self.levelData.get_layer_by_name(name)
        for x, y, tileSurface in tmx_layer.tiles():
            rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
            layer.append((tileSurface, rect))
        return layer

    def draw_layer(self, layer):
        for tileSurface, rect in layer:
            self.display_surface.blit(tileSurface, rect.topleft)

    def draw(self):
        
        self.background.draw1(self.display_surface)
        self.draw_layer(self.arvores_layer)
        self.draw_layer(self.background_layer)
        self.draw_layer(self.background2_layer)
        self.draw_layer(self.platform_layer)
        self.hero.add(Hero((0, 250), faceRight=True))
