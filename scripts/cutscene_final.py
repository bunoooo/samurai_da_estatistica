import pygame
from scripts.Config import *

class Cutscene_final:
    def __init__(self, display, font_path=None, multi_stage=None):
        self.display = display
        self.multi_stage = multi_stage

        # Carrega imagem
        self.image = pygame.image.load(image_path + "Intro_04.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (500, 300))

        self.image2 = pygame.image.load(image_path + "Ending_04.png").convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, (500, 300))

        # Fonte
        if font_path:
            self.font = pygame.font.Font(font_path, 18)
        else:
            self.font = pygame.font.SysFont("arial", 24)

        self.text1 = (
            "Jack enfrenta Erradon, sentindo a tensão no ar e a força do inimigo. "
            "Cada golpe é testado, mas ele mantém o foco, equilibrando precisão e adaptação. "
            "No ápice do confronto, Jack aplica o Golpe do Equilíbrio e finalmente derrota Erradon."
        )

        self.text2 = (
            "O vento sopra suave sobre os campos onde antes reinava o caos. "
            "O Samurai compreende, enfim, que sua verdadeira arma nunca foi a espada, mas o conhecimento. "
            "Após enfrentar epidemias, maldições e a ignorância, ele aprendeu que a Estatística é a arte de enxergar o invisível "
            "e transformar incerteza em sabedoria. "
            "Agora, em paz, guarda sua lâmina e segue como lenda — o Samurai da Estatística."
        )

        self.text3 = (
            "Obrigado por Jogar!."
            "Desenvolvido por Bruno Paz."
        )

        # Controle
        self.stage = 0
        self.char_index = 0
        self.text_speed = 50
        self.last_update = pygame.time.get_ticks()
        self.finished = False
        self.active_text = self.text1  # Texto atualmente sendo mostrado

    # --- Funções de desenho ---
    def draw_hint(self):
        hint_text = "Pressione ENTER para avançar"
        hint_font = pygame.font.Font(None, 12)
        rendered = hint_font.render(hint_text, True, (200, 200, 200))
        screen_width = self.display.get_width()
        screen_height = self.display.get_height()
        text_rect = rendered.get_rect(bottomright=(screen_width - 10, screen_height - 10))
        self.display.blit(rendered, text_rect)

    def wrap_text(self, text, max_width):
        sentences = []
        temp = ""
        for char in text:
            temp += char
            if char == '.':
                sentences.append(temp.strip())
                temp = ""
        if temp:
            sentences.append(temp.strip())

        lines = []
        for sentence in sentences:
            words = sentence.split(" ")
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if self.font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                lines.append(current_line.strip())
            lines.append("")
        if lines and lines[-1] == "":
            lines.pop()
        return lines

    def draw_scroll(self, text):
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.text_speed:
            self.char_index = min(len(text), self.char_index + 1)
            self.last_update = now

        animated_text = text[:self.char_index]

        max_width = 700
        lines = self.wrap_text(animated_text, max_width)

        line_height = self.font.get_linesize()
        total_text_height = len(lines) * line_height
        center_x = self.display.get_width() // 2
        center_y = self.display.get_height() // 2
        start_y = center_y - total_text_height // 2

        for i, line in enumerate(lines):
            rendered = self.font.render(line, True, (255, 255, 255))
            text_rect = rendered.get_rect(center=(center_x, start_y + i * line_height))
            self.display.blit(rendered, text_rect)

    def draw_image_with_text(self):
        img_rect = self.image2.get_rect(center=(500, 250))
        self.display.blit(self.image2, img_rect)
        self.active_text = self.text1
        max_width = 700
        lines = self.wrap_text(self.text1, max_width)
        start_y = 400
        line_height = self.font.get_linesize()
        for i, line in enumerate(lines):
            rendered = self.font.render(line, True, (255, 255, 255))
            text_rect = rendered.get_rect(center=(500, start_y + i * line_height))
            self.display.blit(rendered, text_rect)

    

    # --- Input ---
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):

            # Cutscene múltipla
            if self.multi_stage:
                if self.stage == 0:
                    if self.char_index < len(self.text1):
                        self.char_index = len(self.text1)
                    else:
                        self.stage = 1
                        self.char_index = 0

                elif self.stage == 1:
                    self.stage = 2
                    self.char_index = 0

                elif self.stage == 2:
                    if self.char_index < len(self.text3):
                        self.char_index = len(self.text3)
                    else:
                        self.finished = True

            # Cutscene simples
            else:
                current_text = getattr(self, "active_text", self.text1)
                if self.char_index < len(current_text):
                    self.char_index = len(current_text)
                else:
                    self.finished = True
                    self.stage = 1

    # --- Draw geral ---
    def draw(self):
        self.display.fill((10, 10, 10))
        if self.multi_stage:
            if self.stage == 0:
                self.draw_image_with_text()
            elif self.stage == 1:
                self.active_text = self.text2
                self.draw_scroll(self.text2)
            elif self.stage == 2:
                self.active_text = self.text3
                self.draw_scroll(self.text3)
        else:
            self.draw_scroll(self.active_text)

        if not self.finished:
            self.draw_hint()

   
    
    