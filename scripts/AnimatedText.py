import pygame
from scripts.Config import *

class AnimatedText:
    def __init__(self, text, font, color, surface, speed=0.5, duration=180):
        self.text = text
        self.font = font
        self.color = color
        self.surface = surface
        self.speed = speed  # velocidade da digitação
        self.duration = duration  # tempo visível após digitar
        self.counter = 0
        self.timer = 0
        self.done_typing = False
        self.visible = True

        # Centro da tela
        self.center = self.surface.get_rect().center

        # Criar uma superfície semi-transparente para o fundo
        self.background_surf = pygame.Surface((self.surface.get_width(), self.surface.get_height() ), pygame.SRCALPHA)
        self.background_surf.fill((50, 50, 50, 180))  # cinza escuro com alpha (transparente)
        self.background_rect = self.background_surf.get_rect(topleft=(0, 0))

        self.paineltitulo = pygame.image.load(menu_path + "fundo_titulo.png").convert_alpha()
        self.paineltitulo_rect = self.paineltitulo.get_rect(center=(surface.get_width() // 2, 270))

    def update(self):
        if not self.visible:
            return
        if not self.done_typing:
            self.counter += self.speed
            if self.counter >= len(self.text):
                self.counter = len(self.text)
                self.done_typing = True
        else:
            self.timer += 1
            if self.timer >= self.duration:
                self.visible = False

    def draw(self):
        if not self.visible:
            return

        # Texto parcial (efeito de digitação)
        displayed_text = self.text[:int(self.counter)]

        # Renderizar texto
        text_surface = self.font.render(displayed_text, True, self.color)
        text_rect = text_surface.get_rect(center=self.center)


        self.surface.blit(self.background_surf,self.background_rect)

        # Desenhar fundo semi-transparente
        self.surface.blit(self.paineltitulo, self.paineltitulo_rect)

        # Desenhar texto
        self.surface.blit(text_surface, text_rect)

    @property
    def finished(self):
        return not self.visible
    

class ExitMenu:
    def __init__(self, surface, font):
        self.surface = surface
        self.font = font

        # Fundo translúcido
        self.background_surf = pygame.Surface((self.surface.get_width(), self.surface.get_height()), pygame.SRCALPHA)
        self.background_surf.fill((0, 0, 0, 180))  # preto com alpha

        # Painel de título
        self.paineltitulo = pygame.image.load(hud_path + "texto_exit.png").convert_alpha()
        self.paineltitulo_rect = self.paineltitulo.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 40))

        # Texto principal
        self.title_surface = self.font.render("DESEJA REALMENTE SAIR?", True, (255, 255, 255))
        self.title_rect = self.title_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 50))

        # Botões
        self.options = ["SAIR", "NÃO"]
        self.selected_index = 0  # começa no "SAIR"

        self.button_width = 200
        self.button_height = 60
        self.button_spacing = 50
        self.center_y = surface.get_height() // 2 - 20

        # Imagem do botão
        #self.button_image = pygame.image.load(hud_path + "exit_hud.png").convert_alpha()
        #self.button_image = pygame.transform.scale(self.button_image, (self.button_width, self.button_height))

    def draw(self):
        # Fundo escuro translúcido
        self.surface.blit(self.background_surf, (0, 0))

        # Painel e título
        self.surface.blit(self.paineltitulo, self.paineltitulo_rect)
        self.surface.blit(self.title_surface, self.title_rect)

        # Desenhar botões
        screen_center_x = self.surface.get_width() // 2

        for i, option in enumerate(self.options):
            x = screen_center_x + (i - 0.5) * self.button_spacing
            y = self.center_y

            rect = pygame.Rect(0, 0, self.button_width, self.button_height)
            rect.center = (x, y)

            # Blitar a imagem do botão
            #self.surface.blit(self.button_image, rect.topleft)

            # cor do texto se selecionado
            if i == self.selected_index:
                text_color = (49, 59, 114)
            else:
                text_color = (255, 255, 255)

            # texto do botão
            text_surface = self.font.render(option, True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            self.surface.blit(text_surface, text_rect)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_index]
        return None
