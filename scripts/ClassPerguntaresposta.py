import pygame
from Config import *

class PerguntaResposta:
    def __init__(self, displaySurface, hero, npc, pergunta, opcoes, correta_index, feedbacks, pos=(100, 100)):
        self.displaySurface = displaySurface
        self.hero = hero
        self.npc = npc
        self.pergunta = pergunta
        self.opcoes = opcoes
        self.correta_index = correta_index
        self.feedbacks = feedbacks  # lista de feedbacks por opção
        self.pos = pos
        self.acertou = None
        self.errou = None

        # Painel de fundo
        self.painelpergunta = pygame.image.load(menu_path + "HUD/perguntarespostahud.png").convert_alpha()
        self.painelperguntarect = self.painelpergunta.get_rect(center=(displaySurface.get_width() // 2,
                                                                       displaySurface.get_height() - 120))

        # Aparência
        self.text_color = (49, 59, 114)
        self.highlight_color = (255, 255, 255)

        # Controle
        self.active = False
        self.feedback_mode = False  # modo de exibição do feedback
        self.selected_index = 0
        self.font = pygame.font.Font(font_path, 14)

        # Controle de teclas por frame
        self.p_pressed_last_frame = False
        self.enter_pressed_last_frame = False
        self.up_pressed_last_frame = False
        self.down_pressed_last_frame = False

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Ativa/desativa a pergunta com P (somente se herói colidir com o NPC)
        if keys[pygame.K_p] and not self.p_pressed_last_frame:
            if self.hero.hitbox.colliderect(self.npc.hitbox):
                self.active = not self.active
                self.feedback_mode = False  # reseta feedback
        self.p_pressed_last_frame = keys[pygame.K_p]

        if not self.active:
            return

        # Se estiver mostrando feedback, só fecha com Enter
        if self.feedback_mode:
            if keys[pygame.K_RETURN] and not self.enter_pressed_last_frame:
                self.active = False
                self.feedback_mode = False
            self.enter_pressed_last_frame = keys[pygame.K_RETURN]
            return

        # Navegação nas opções
        if keys[pygame.K_UP] and not self.up_pressed_last_frame:
            self.selected_index = max(0, self.selected_index - 1)
        if keys[pygame.K_DOWN] and not self.down_pressed_last_frame:
            self.selected_index = min(len(self.opcoes) - 1, self.selected_index + 1)

        if keys[pygame.K_RETURN] and not self.enter_pressed_last_frame:
            # Ativa o feedback em vez de só printar
            self.feedback_mode = True

            if self.selected_index == self.correta_index:
                self.acertou = True
            else:
                self.errou = True

        # Atualiza estados de tecla
        self.up_pressed_last_frame = keys[pygame.K_UP]
        self.down_pressed_last_frame = keys[pygame.K_DOWN]
        self.enter_pressed_last_frame = keys[pygame.K_RETURN]

      


    def draw(self):
        if not self.active:
            return

        # Desenha o painel
        self.displaySurface.blit(self.painelpergunta, self.painelperguntarect)

        start_x = self.painelperguntarect.left + 20
        start_y = self.painelperguntarect.top + 20

        if self.feedback_mode:
            # Mostra feedback da opção escolhida
            feedback_text = self.feedbacks[self.selected_index]
            linhas = self._quebrar_texto(feedback_text, self.painelperguntarect.width - 40)
            for i, linha in enumerate(linhas):
                surf = self.font.render(linha, True, self.text_color)
                self.displaySurface.blit(surf, (start_x, start_y + i * 20))

            # Instrução para sair
            sair_surf = self.font.render("Pressione Enter para continuar...", True, self.highlight_color)
            self.displaySurface.blit(sair_surf, (start_x, self.painelperguntarect.bottom - 30))
        else:
            # Pergunta
            linhas = self._quebrar_texto(self.pergunta, self.painelperguntarect.width - 40)
            for i, linha in enumerate(linhas):
                surf = self.font.render(linha, True, self.text_color)
                self.displaySurface.blit(surf, (start_x, start_y + i * 20))

            # Opções
            offset_y = start_y + len(linhas) * 25 + 10
            for i, opcao in enumerate(self.opcoes):
                y = offset_y + i * 30
                color = self.highlight_color if i == self.selected_index else self.text_color
                opcao_surf = self.font.render(opcao, True, color)
                self.displaySurface.blit(opcao_surf, (start_x + 10, y))

    def _quebrar_texto(self, texto, max_width):
        """Quebra o texto em múltiplas linhas baseado no tamanho do painel"""
        palavras = texto.split(" ")
        linhas = []
        linha_atual = ""
        for palavra in palavras:
            teste = linha_atual + palavra + " "
            teste_surf = self.font.render(teste, True, self.text_color)
            if teste_surf.get_width() <= max_width:
                linha_atual = teste
            else:
                linhas.append(linha_atual.strip())
                linha_atual = palavra + " "
        if linha_atual:
            linhas.append(linha_atual.strip())
        return linhas
