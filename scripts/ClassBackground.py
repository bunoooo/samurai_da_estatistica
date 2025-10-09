import pygame
from Config import *


class Background():

    def __init__(self):
        # Create the sky image
        self.skyImage = pygame.image.load(SPRITESHEET_PATH + "Background.png").convert()
        
        self.skyImage = pygame.transform.scale(self.skyImage, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        self.background_factory = pygame.image.load(SPRITESHEET_PATH + "background_ship.png").convert_alpha()
        self.background_factory = pygame.transform.scale(self.background_factory, (WINDOW_WIDTH, WINDOW_HEIGHT))


        self.auttom = pygame.image.load(SPRITESHEET_PATH + "3.png").convert_alpha()
        self.auttom1 = pygame.image.load(SPRITESHEET_PATH + "2.png").convert_alpha()
        self.auttom2 = pygame.image.load(SPRITESHEET_PATH + "1.png").convert_alpha()

        self.auttom = pygame.transform.scale(self.auttom, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.auttom1 = pygame.transform.scale(self.auttom1, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.auttom2 = pygame.transform.scale(self.auttom2, (WINDOW_WIDTH, WINDOW_HEIGHT))


        self.redcity = pygame.image.load(SPRITESHEET_PATH + "red.png").convert_alpha()
        self.redcity1 = pygame.image.load(SPRITESHEET_PATH + "red1.png").convert_alpha()
        self.redcity2 = pygame.image.load(SPRITESHEET_PATH + "red2.png").convert_alpha()
        self.redcity3 = pygame.image.load(SPRITESHEET_PATH + "red3.png").convert_alpha()

       # self.redcity = pygame.transform.scale(self.redcity, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.redcity1 = pygame.transform.scale(self.redcity1, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.redcity2 = pygame.transform.scale(self.redcity2, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.redcity3 = pygame.transform.scale(self.redcity3, (WINDOW_WIDTH, WINDOW_HEIGHT))






    def draw(self, displaySurface):
       
        displaySurface.blit(self.skyImage, (0, 0))


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

