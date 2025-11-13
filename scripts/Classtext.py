import pygame
from scripts.Config import *

# Cores
BLACK = (0, 0, 0)
BROWN = (100, 40, 0)

class AppearingTextBox:
    def __init__(self, text_groups, screen):
        self.text_active = False
        self.text_groups = text_groups  # cada grupo: (nome, [linhas])
        self.screen = screen
        self.font = pygame.font.Font(font_path, 12)
        self.name_font = pygame.font.Font(font_path, 12)  # fonte maior pro nome

        # Cores e estilo da caixa
        self.text_color = BLACK
        self.name_color = BROWN
        self.padding = 20

        # Caixa de diálogo (imagem de fundo)
        self.paineltitulo = pygame.image.load(menu_path + "HUD/texto_hud.png").convert_alpha()
        self.paineltitulo_rect = self.paineltitulo.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() - 50)
        )

        # Controle de texto
        self.current_group = 0      
        self.current_text = 0

        # Controle de tecla para evitar avanço automático
        self.e_pressed_last_frame = False
        self.a_pressed_last_frame = False

    def start(self):
        self.text_active = True
        self.current_group = 0
        self.current_text = 0

    def reset(self):
        self.current_group = 0
        self.current_text = 0
        self.text_active = False

    def advance_text(self):
        if not self.text_active:
            return

        self.current_text += 1
        speaker, lines = self.text_groups[self.current_group]
        if self.current_text >= len(lines):
            self.current_group += 1
            self.current_text = 0

            if self.current_group >= len(self.text_groups):
                self.text_active = False

    def draw_box(self):
        if self.text_active:
            self.screen.blit(self.paineltitulo, self.paineltitulo_rect)

    def draw_text(self):
        if not self.text_active:
            return

        speaker, lines = self.text_groups[self.current_group]

        # Nome acima da caixa
        name_surf = self.name_font.render(speaker, True, self.name_color)
        name_rect = name_surf.get_rect(midbottom=(self.paineltitulo_rect.centerx - 195, self.paineltitulo_rect.top + 25))
        self.screen.blit(name_surf, name_rect)

        # Texto dentro da caixa
        start_x = self.paineltitulo_rect.left + self.padding
        start_y = self.paineltitulo_rect.top + self.padding + 25

        for i in range(self.current_text + 1):
            if i < len(lines):
                text_surf = self.font.render(lines[i], True, self.text_color)
                self.screen.blit(text_surf, (start_x - 10, start_y + i * 15))

    def update(self):
        if self.text_active:
            self.draw_box()
            self.draw_text()

    def is_finished(self):
        return not self.text_active
