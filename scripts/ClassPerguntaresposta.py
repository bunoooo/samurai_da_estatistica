import pygame
from scripts.Config import *

class PerguntaResposta:
    def __init__(self, displaySurface, hero, npc, pergunta, loja, correta_conceito, pos=(100, 100)):
        """
        loja: instância da LojaSimples (ou None)
        correta_conceito: string com o conceito correto
        """
        self.displaySurface = displaySurface
        self.hero = hero
        self.npc = npc
        self.pergunta = pergunta
        self.loja = loja
        self.pos = pos
        self.correta_conceito = correta_conceito

        self.acertou = None
        self.errou = None
        self.index_resposta = None  # índice da opção escolhida

        # Painel de fundo
        self.painelpergunta = pygame.image.load(menu_path + "HUD/perguntarespostahud.png").convert_alpha()
        self.painelperguntarect = self.painelpergunta.get_rect(
            center=(displaySurface.get_width() // 2, displaySurface.get_height() - 120)
        )

        # Aparência
        self.text_color = (49, 59, 114)
        self.highlight_color = (255, 255, 255)

        # Controle
        self.active = False
        self.feedback_mode = False
        self.selected_index = 0
        self.font = pygame.font.Font(font_path, 14)

        # Controle de teclas
        self.p_pressed_last_frame = False
        self.enter_pressed_last_frame = False
        self.up_pressed_last_frame = False
        self.down_pressed_last_frame = False

        # Inicializa listas
        self.opcoes = []
        self.feedbacks = []
        self.feedback_images = []

    # ----------------------------------------------------
    # Atualiza as opções, feedbacks e imagens da loja
    # ----------------------------------------------------
    def atualizar_opcoes(self):
        if self.loja is None or not hasattr(self.loja, "compradas") or not self.loja.compradas:
            self.opcoes = ["(Nenhum conceito disponível)"]
            self.feedbacks = ["Não há conceitos comprados para responder esta pergunta."]
            self.feedback_images = [None]
        else:
            self.opcoes = [d['conceito'] for d in self.loja.compradas]
            self.feedbacks = [d['feedback'] for d in self.loja.compradas]
            # Corrigido: pegar a imagem carregada corretamente
            self.feedback_images = [d.get("imagem") for d in self.loja.compradas]

        if self.selected_index >= len(self.opcoes):
            self.selected_index = 0

    # ----------------------------------------------------
    # Controle de inputs
    # ----------------------------------------------------
    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.atualizar_opcoes()

        # Ativa/desativa a pergunta
        if keys[pygame.K_p] and not self.p_pressed_last_frame:
            if self.hero.hitbox.colliderect(self.npc.hitbox):
                self.active = not self.active
                self.feedback_mode = False
        self.p_pressed_last_frame = keys[pygame.K_p]

        if not self.active:
            return

        # FEEDBACK ATIVO
        if self.feedback_mode:
            if keys[pygame.K_RETURN] and not self.enter_pressed_last_frame:
                self.active = False
                self.feedback_mode = False
            self.enter_pressed_last_frame = keys[pygame.K_RETURN]
            return

        # Navegação
        if keys[pygame.K_UP] and not self.up_pressed_last_frame:
            self.selected_index = max(0, self.selected_index - 1)
        if keys[pygame.K_DOWN] and not self.down_pressed_last_frame:
            self.selected_index = min(len(self.opcoes) - 1, self.selected_index + 1)

        # Seleção
        if keys[pygame.K_RETURN] and not self.enter_pressed_last_frame:
            self.feedback_mode = True
            self.index_resposta = self.selected_index

            opcao_escolhida = self.opcoes[self.index_resposta]

            if opcao_escolhida == "(Nenhum conceito disponível)":
                self.acertou = None
                self.errou = None
            elif opcao_escolhida == self.correta_conceito:
                self.acertou = True
                self.errou = False
            else:
                self.acertou = False
                self.errou = True

        self.up_pressed_last_frame = keys[pygame.K_UP]
        self.down_pressed_last_frame = keys[pygame.K_DOWN]
        self.enter_pressed_last_frame = keys[pygame.K_RETURN]

    # ----------------------------------------------------
    # Desenhar painel
    # ----------------------------------------------------
    def draw(self):
        if not self.active:
            return

        self.atualizar_opcoes()

        # Painel de fundo
        self.displaySurface.blit(self.painelpergunta, self.painelperguntarect)
        start_x = self.painelperguntarect.left + 20
        start_y = self.painelperguntarect.top + 20

        # ----------------------------------------------------
        # MODO FEEDBACK
        # ----------------------------------------------------
        if self.feedback_mode and self.index_resposta is not None:
            # Texto do feedback
            feedback_text = self.feedbacks[self.index_resposta]
            linhas = self._quebrar_texto(feedback_text, self.painelperguntarect.width - 170)

            for i, linha in enumerate(linhas):
                surf = self.font.render(linha, True, self.text_color)
                self.displaySurface.blit(surf, (start_x, start_y + i * 20))

            
            img = self.feedback_images[self.index_resposta]
           
            if img:
                img = pygame.image.load(img).convert_alpha()
                img_rect = img.get_rect()
                img_rect.topright = (self.painelperguntarect.right - 20, start_y)
                self.displaySurface.blit(img, img_rect)
           
            # Resultado (acertou/errou)
            resultado_texto = "Você aeeee" if self.acertou else "Você errou!"
            print(resultado_texto)
            resultado_surf = self.font.render(resultado_texto, True, self.highlight_color)
            self.displaySurface.blit(resultado_surf, (start_x, start_y + len(linhas) * 20 + 10))

            # Botão de sair
            sair_surf = self.font.render("Pressione Enter para continuar...", True, self.highlight_color)
            self.displaySurface.blit(sair_surf, (start_x, self.painelperguntarect.bottom - 30))
            return

        # ----------------------------------------------------
        # MODO PERGUNTA
        # ----------------------------------------------------
        linhas = self._quebrar_texto(self.pergunta, self.painelperguntarect.width - 40)
        for i, linha in enumerate(linhas):
            surf = self.font.render(linha, True, self.text_color)
            self.displaySurface.blit(surf, (start_x, start_y + i * 20))

        # Opções
        offset_y = start_y + len(linhas) * 25 + 10
        for i, opcao in enumerate(self.opcoes):
            y = offset_y + i * 15
            color = self.highlight_color if i == self.selected_index else self.text_color
            opcao_surf = self.font.render(opcao, True, color)
            self.displaySurface.blit(opcao_surf, (start_x + 10, y))

    # ----------------------------------------------------
    # Quebra de texto automática
    # ----------------------------------------------------
    def _quebrar_texto(self, texto, max_width):
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
