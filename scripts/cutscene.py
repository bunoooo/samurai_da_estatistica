import pygame
from Config import *

class Cutscene:
    def __init__(self, display, font_path=None):
        self.display = display

        # Carrega imagem
        self.image = pygame.image.load(image_path + "Intro_04.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (500, 300))

        # Fonte
        if font_path:
            self.font = pygame.font.Font(font_path, 18)
        else:
            self.font = pygame.font.SysFont("arial", 24)

        # Textos
            # Textos da cutscene
        self.text1 = (  "Jack era um jovem samurai treinado na lendária Arte dos Dados, uma disciplina antiga que unia "
    "estratégia de combate com conhecimento estatístico profundo."
    
    "Sua missão era proteger a verdade e combater a desinformação, que se manifestava em entidades "
    "misteriosas que corrompiam os dados e confundiam a população."
    
    "Entre essas entidades, Erradon era o mais perigoso: um ser sombrio que prosperava no caos, "
    "espalhando falsas informações e distorcendo a realidade."
    
    "Durante um confronto épico, Jack enfrentou Erradon no Templo do Conhecimento, um lugar sagrado "
    "onde os registros da Arte dos Dados eram guardados."
    
    "Cada golpe do samurai buscava não apenas ferir, mas restaurar a clareza e a precisão dos dados "
    "que Erradon tentava corromper."
            
        )
        
        self.text2 = (
            "No entanto, Erradon possuía um poder incomum: ele conseguia manipular o tempo e o espaço, "
            "e com um movimento abrupto, lançou Jack em um futuro devastado, uma era em que o conhecimento "
            "havia sido quase totalmente perdido."
        )

        self.text3 = (
    "Nesse futuro, as cidades estavam mergulhadas no caos informacional. "
    "Pessoas eram incapazes de distinguir fatos de mentiras, e decisões eram tomadas com base em dados corrompidos ou inexistentes. "
    "Jack, desorientado, percebeu que suas habilidades eram agora mais importantes do que nunca. "
    "Ele seria o último guardião da Arte dos Dados. "
    "Para sobreviver, ele precisaria reconstruir seu conhecimento, treinar novamente suas técnicas e "
    "voltar para seu tempo."
    "Para que erradon seja derrotado e o futuro salvo."
)

        # Controle da cutscene
        self.stage = 0
        self.char_index = 0        # índice do caractere atual
        self.text_speed = 50       # ms por caractere (tempo fixo)
        self.last_update = pygame.time.get_ticks()  # marca o último incremento
        self.finished = False


    def draw_hint(self):
        """Mostra a dica de avançar no canto inferior direito."""
        hint_text = "Pressione ENTER para avançar"
        hint_font = pygame.font.Font(font_path, 12)
        rendered = hint_font.render(hint_text, True, (200, 200, 200))
        screen_width = self.display.get_width()
        screen_height = self.display.get_height()
        text_rect = rendered.get_rect(bottomright=(screen_width - 10, screen_height - 10))
        self.display.blit(rendered, text_rect)

    def wrap_text(self, text, max_width):
        # mesma função wrap_text que você já tem
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
        """Desenha texto com efeito de digitação baseado em tempo fixo."""
        now = pygame.time.get_ticks()
        # se passou text_speed ms, incrementa o caractere
        if now - self.last_update >= self.text_speed:
            self.char_index = min(len(text), self.char_index + 1)
            self.last_update = now

        animated_text = text[:self.char_index]

        # Quebra de texto
        max_width = 700
        lines = self.wrap_text(animated_text, max_width)

        # Centralização vertical
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
        # imagem central
        img_rect = self.image.get_rect(center=(500, 250))
        self.display.blit(self.image, img_rect)

        # texto fixo abaixo
        max_width = 700
        lines = self.wrap_text(self.text2, max_width)
        start_y = 400
        line_height = self.font.get_linesize()
        for i, line in enumerate(lines):
            rendered = self.font.render(line, True, (255, 255, 255))
            text_rect = rendered.get_rect(center=(500, start_y + i * line_height))
            self.display.blit(rendered, text_rect)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            # Se estiver no estágio de texto digitando
            if self.stage in (0, 2):
                current_text = self.text1 if self.stage == 0 else self.text3
                # Se o texto ainda não terminou, mostrar tudo de uma vez
                if self.char_index < len(current_text):
                    self.char_index = len(current_text)  # completa o texto
                    self.last_update = pygame.time.get_ticks()  # reset timer para evitar salto imediato
                else:
                    # Texto já completo -> avançar estágio
                    self.stage += 1
                    self.char_index = 0
            elif self.stage == 1:
                # estágio da imagem + texto fixo, só avança
                self.stage += 1
                self.char_index = 0
            # Se passar do último estágio
            if self.stage > 2:
                self.finished = True
                


    def draw(self):
        self.display.fill((10, 10, 10))
        if self.stage == 0:
            self.draw_scroll(self.text1)
        elif self.stage == 1:
            self.draw_image_with_text()
        elif self.stage == 2:
            self.draw_scroll(self.text3)
          # Desenha a dica no canto
        if self.stage < 3:  # só enquanto a cutscene não terminou
            self.draw_hint()
