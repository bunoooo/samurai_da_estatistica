import pygame
import io
from scripts.Config import *

class PerguntaGrafico:
    def __init__(self, displaySurface, hero, npc, pergunta, grafico_func=None, grafico_path=None,
                 loja=None, correta_conceito=None, pos=(100, 100)):
        self.displaySurface = displaySurface
        self.hero = hero
        self.npc = npc
        self.pergunta = pergunta
        self.loja = loja
        self.pos = pos
        self.correta_conceito = correta_conceito

        # --- Carrega gráfico ---
        if grafico_path is not None:
            self.grafico_surface = self._carregar_grafico_imagem(grafico_path)
        elif grafico_func is not None:
            self.grafico_surface = self._gerar_grafico_surface_func(grafico_func)
        else:
            self.grafico_surface = None

        self.acertou = None
        self.errou = None
        self.index_resposta = None

        # --- Painel maior ---
        self.painel = pygame.image.load(menu_path + "HUD/perguntarespostahud.png").convert_alpha()
        largura_painel = displaySurface.get_width() - 300
        altura_painel = 410
        self.painel = pygame.transform.smoothscale(self.painel, (largura_painel, altura_painel))
        self.painel_rect = self.painel.get_rect(center=(displaySurface.get_width() // 2,
                                                        displaySurface.get_height() - 200))

        # Aparência
        self.text_color = (49, 59, 114)
        self.highlight_color = (255, 255, 255)
        self.font = pygame.font.Font(font_path, 16)

        # Controle
        self.active = False
        self.feedback_mode = False
        self.selected_index = 0

        # Controle de teclas
        self.p_pressed_last_frame = False
        self.enter_pressed_last_frame = False
        self.up_pressed_last_frame = False
        self.down_pressed_last_frame = False

        # Listas
        self.opcoes = []
        self.feedbacks = []
        self.feedback_images = []  


    def _carregar_grafico_imagem(self, path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(image, (300, 200))

    def _gerar_grafico_surface_func(self, func):
        fig = func()
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        img = pygame.image.load(buf).convert_alpha()
        buf.close()
        return pygame.transform.smoothscale(img, (300, 200))

    def atualizar_opcoes(self):
        if self.loja is None or not hasattr(self.loja, "compradas") or not self.loja.compradas:
            self.opcoes = ["(Nenhum conceito disponível)"]
            self.feedbacks = ["Não há conceitos comprados para responder esta pergunta."]
            self.feedback_images = [None]
        else:
            self.opcoes = [d['conceito'] for d in self.loja.compradas]
            self.feedbacks = [d['feedback'] for d in self.loja.compradas]
            self.feedback_images = [d.get("imagem") for d in self.loja.compradas]

        if self.selected_index >= len(self.opcoes):
            self.selected_index = 0


    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.atualizar_opcoes()

        if keys[pygame.K_p] and not self.p_pressed_last_frame:
            if self.hero.hitbox.colliderect(self.npc.hitbox):
                self.active = not self.active
                self.feedback_mode = False
        self.p_pressed_last_frame = keys[pygame.K_p]

        if not self.active:
            return

        if self.feedback_mode:
            if keys[pygame.K_RETURN] and not self.enter_pressed_last_frame:
                # Reset completo
                self.active = False
                self.feedback_mode = False
                self.selected_index = 0
                self.index_resposta = None
                self.acertou = None
                self.errou = None
            self.enter_pressed_last_frame = keys[pygame.K_RETURN]
            return

        if keys[pygame.K_UP] and not self.up_pressed_last_frame:
            self.selected_index = max(0, self.selected_index - 1)

        if keys[pygame.K_DOWN] and not self.down_pressed_last_frame:
            self.selected_index = min(len(self.opcoes) - 1, self.selected_index + 1)

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


    def draw(self):
        if not self.active:
            return

        self.displaySurface.blit(self.painel, self.painel_rect)
        start_x = self.painel_rect.left + 30
        start_y = self.painel_rect.top + 30

        # =====================
        # MODO FEEDBACK
        # =====================
        if self.feedback_mode and self.index_resposta is not None:
            feedback_text = self.feedbacks[self.index_resposta]
            linhas_feedback = self._quebrar_texto(feedback_text, self.painel_rect.width - 220)

            for i, linha in enumerate(linhas_feedback):
                y = start_y + i * 25
                self.displaySurface.blit(self.font.render(linha, True, self.text_color), (start_x, y))

            img_path = None
            try:
                img_path = self.feedback_images[self.index_resposta]
            except:
                img_path = None

            if img_path:
                try:
                    img = pygame.image.load(img_path).convert_alpha()

                    # --- Alinhamento vertical com gráfico ---
                    if self.grafico_surface:
                        grafico_rect = self.grafico_surface.get_rect(
                            midtop=(self.painel_rect.centerx,
                                    self.painel_rect.top + 30 +
                                    (len(self._quebrar_texto(self.pergunta, self.painel_rect.width - 60)) * 25) + 10)
                        )
                        y_alinhado = grafico_rect.top

                        # --- AJUSTE PEDIDO: REDIMENSIONAR PARA TER A MESMA ALTURA DO GRÁFICO ---
                        h_grafico = self.grafico_surface.get_height()
                        w_img, h_img = img.get_size()
                        nova_largura = int(w_img * (h_grafico / h_img))
                        img = pygame.transform.smoothscale(img, (nova_largura, h_grafico))
                    else:
                        y_alinhado = start_y

                    img_rect = img.get_rect()
                    img_rect.midtop = (self.painel_rect.right - 350, y_alinhado + 50)

                    self.displaySurface.blit(img, img_rect)
                except:
                    pass

            # Resultado
            if self.acertou is not None:
                resultado_texto = "Você acertou!" if self.acertou else "Você errou!"
                self.displaySurface.blit(
                    self.font.render(resultado_texto, True, self.highlight_color),
                    (start_x, start_y + len(linhas_feedback) * 25 + 10)
                )

            # Continuar
            sair_surf = self.font.render("Pressione Enter para continuar...", True, self.highlight_color)
            self.displaySurface.blit(sair_surf, (start_x + 290, self.painel_rect.bottom - 40))
            return

        # =====================
        # MODO PERGUNTA
        # =====================

        linhas_pergunta = self._quebrar_texto(self.pergunta, self.painel_rect.width - 60)
        for i, linha in enumerate(linhas_pergunta):
            y = start_y + i * 25
            self.displaySurface.blit(self.font.render(linha, True, self.text_color), (start_x, y))

        altura_pergunta = len(linhas_pergunta) * 25

        # Gráfico
        if self.grafico_surface:
            grafico_rect = self.grafico_surface.get_rect(
                midtop=(self.painel_rect.centerx, start_y + altura_pergunta + 10))
            self.displaySurface.blit(self.grafico_surface, grafico_rect)

        graf_h = (self.grafico_surface.get_height() if self.grafico_surface else 0)
        offset_y = start_y + altura_pergunta + (graf_h + 20 if graf_h else 40)

        # Opções
        for i, opcao in enumerate(self.opcoes):
            y = offset_y + i * 25
            cor = self.highlight_color if i == self.selected_index else self.text_color
            self.displaySurface.blit(self.font.render(f"{i + 1}. {opcao}", True, cor), (start_x + 10, y))

        instrucoes = self.font.render("Selecione uma opção e pressione Enter", True, self.highlight_color)
        self.displaySurface.blit(instrucoes, (start_x + 290, self.painel_rect.bottom - 40))


    def _quebrar_texto(self, texto, max_width):
        palavras = texto.split(" ")
        linhas = []
        linha_atual = ""
        for palavra in palavras:
            teste = linha_atual + palavra + " "
            if self.font.render(teste, True, self.text_color).get_width() <= max_width:
                linha_atual = teste
            else:
                linhas.append(linha_atual.strip())
                linha_atual = palavra + " "
        if linha_atual:
            linhas.append(linha_atual.strip())
        return linhas
