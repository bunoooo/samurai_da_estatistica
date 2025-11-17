import pygame
from scripts.Config import *


class Background():

    def __init__(self):
        # Create the sky image
        self.skyImage = pygame.image.load(SPRITESHEET_PATH + "Background.png").convert()
        
        self.skyImage = pygame.transform.scale(self.skyImage, (WINDOW_WIDTH, WINDOW_HEIGHT))

        ### background fase 1
        
        self.background_factory = pygame.image.load(SPRITESHEET_PATH + "background_ship.png").convert_alpha()
        self.background_factory = pygame.transform.scale(self.background_factory, (WINDOW_WIDTH, WINDOW_HEIGHT))


        # background fase 4 
        self.background_overlay = pygame.image.load(SPRITESHEET_PATH + "Overlay.png").convert_alpha()
        self.background_layer_1 = pygame.image.load(SPRITESHEET_PATH + "b1.png").convert_alpha()
        self.background_layer_2 = pygame.image.load(SPRITESHEET_PATH + "b2.png").convert_alpha()
        self.background_layer_3 = pygame.image.load(SPRITESHEET_PATH + "b3.png").convert_alpha()
        self.background_layer_4 = pygame.image.load(SPRITESHEET_PATH + "b4.png").convert_alpha()
        self.background_layer_5 = pygame.image.load(SPRITESHEET_PATH + "b5.png").convert_alpha()


        self.background_layer_1 = pygame.transform.scale(self.background_layer_1, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background_layer_2 = pygame.transform.scale(self.background_layer_2, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background_layer_3 = pygame.transform.scale(self.background_layer_3, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background_layer_4 = pygame.transform.scale(self.background_layer_4, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background_layer_5 = pygame.transform.scale(self.background_layer_5, (WINDOW_WIDTH, WINDOW_HEIGHT))


        self.background_overlay.set_alpha(100)



        ### background tutorial e tela inicial
        self.auttom = pygame.image.load(SPRITESHEET_PATH + "3.png").convert_alpha()
        self.auttom1 = pygame.image.load(SPRITESHEET_PATH + "2.png").convert_alpha()
        self.auttom2 = pygame.image.load(SPRITESHEET_PATH + "1.png").convert_alpha()

        self.auttom = pygame.transform.scale(self.auttom, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.auttom1 = pygame.transform.scale(self.auttom1, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.auttom2 = pygame.transform.scale(self.auttom2, (WINDOW_WIDTH, WINDOW_HEIGHT))




        ### background fase 2
        self.redcity = pygame.image.load(SPRITESHEET_PATH + "red.png").convert_alpha()
        self.redcity1 = pygame.image.load(SPRITESHEET_PATH + "red1.png").convert_alpha()
        self.redcity2 = pygame.image.load(SPRITESHEET_PATH + "red2.png").convert_alpha()
        self.redcity3 = pygame.image.load(SPRITESHEET_PATH + "red3.png").convert_alpha()

       # self.redcity = pygame.transform.scale(self.redcity, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.redcity1 = pygame.transform.scale(self.redcity1, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.redcity2 = pygame.transform.scale(self.redcity2, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.redcity3 = pygame.transform.scale(self.redcity3, (WINDOW_WIDTH, WINDOW_HEIGHT))


        ### background fase3

        self.Background_0 = pygame.image.load(SPRITESHEET_PATH + "Background_0.png").convert_alpha()
        self.Background_1 = pygame.image.load(SPRITESHEET_PATH + "Background_1.png").convert_alpha()
        self.Grass_background_1 = pygame.image.load(SPRITESHEET_PATH + "Grass_background_1.png").convert_alpha()
        self.Grass_background_2 = pygame.image.load(SPRITESHEET_PATH + "Grass_background_2.png").convert_alpha()


        self.Background_0 = pygame.transform.scale(self.Background_0, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.Background_1 = pygame.transform.scale(self.Background_1, (WINDOW_WIDTH, WINDOW_HEIGHT))
       # self.Grass_background_1 = pygame.transform.scale(self.Grass_background_1, (WINDOW_WIDTH, WINDOW_HEIGHT))
       # self.Grass_background_2 = pygame.transform.scale(self.Grass_background_2, (WINDOW_WIDTH, WINDOW_HEIGHT))


    def draw(self, displaySurface):
       
        displaySurface.blit(self.background_layer_1, (0, -30))
        displaySurface.blit(self.background_layer_2, (0, -15))
        displaySurface.blit(self.background_layer_3, (0, -20))
        displaySurface.blit(self.background_layer_4, (0, 0))
        displaySurface.blit(self.background_layer_5, (0, 0))
        displaySurface.blit(self.background_overlay, (0, 0))


    def draw1(self, displaySurface):
        displaySurface.blit(self.auttom, (0, 0))
        displaySurface.blit(self.auttom1, (0, 0))
        displaySurface.blit(self.auttom2, (0, 0))

    def draw2(self, displaySurface):
        displaySurface.blit(self.background_factory, (0, 0))

    def draw3(self, displaySurface):
        displaySurface.blit(self.redcity, (0, 0))
        displaySurface.blit(self.redcity1, (0, 70))
        displaySurface.blit(self.redcity2, (0, 70))
        displaySurface.blit(self.redcity3, (0, 70))

    def draw4(self , displaySurface):
       
        displaySurface.blit(self.Background_0, (0, 0))
        displaySurface.blit(self.Background_1, (0,0))
        displaySurface.blit(self.Grass_background_1, (0, 140))
        displaySurface.blit(self.Grass_background_2, (352,140))
        displaySurface.blit(self.Grass_background_1, (704, 140))
        


