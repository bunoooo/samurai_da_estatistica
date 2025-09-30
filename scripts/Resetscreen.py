import pygame
from AnimatedText import AnimatedText
from Config import *

def reset_screen(surface, font):
    # Fundo semi-transparente
    background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    background.fill((0, 0, 0, 180))  # Preto translúcido

    text = "Você morreu... \\ Aperte R para reiniciar ou ESC para voltar ao menu"
    text_color = (255, 255, 255)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    surface.blit(background, (0, 0))
    surface.blit(text_surface, text_rect)