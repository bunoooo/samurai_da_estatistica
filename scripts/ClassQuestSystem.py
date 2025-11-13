import pygame
from scripts.Config import *

WHITE = (255, 255, 255)
GRAY = (160, 160, 160)
GREEN = (0, 200, 0)

class QuestSystem:
    def __init__(self, quests, screen):
        self.quests = quests  # lista de dicionários
        self.screen = screen
        self.font = pygame.font.Font(font_path, 10)

    def complete_quest(self, quest_id):
        """Marca uma quest como concluída"""
        for quest in self.quests:
            if quest["id"] == quest_id:
                quest["done"] = True

    def draw(self):
        """Desenha as quests no canto superior direito"""
        start_x = self.screen.get_width() - 250
        start_y = 10

        title = self.font.render("Objetivos:", True, WHITE)
        self.screen.blit(title, (start_x, start_y))

        offset = 15
        for quest in self.quests:
            color = GREEN if quest["done"] else WHITE
            text = f"(X) {quest['text']}" if quest["done"] else f" ( ) {quest['text']}"
            quest_surf = self.font.render(text, True, color)
            self.screen.blit(quest_surf, (start_x, start_y + offset))
            offset += 10
