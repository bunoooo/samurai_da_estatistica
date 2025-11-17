import pygame
import os
from scripts.Config import *
from scripts.ClassLoja import *

class LojaSimples:
    def __init__(self, hero, displaySurface, npc, dicas, pos=(50, 50)):
        self.hero = hero
        self.displaySurface = displaySurface
        self.npc = npc
        self.dicas = dicas
        self.pos = pos
        self.active = False
        self.selected_index = 0
        self.font = pygame.font.Font(font_path, 12)
        self.width = 400
        self.height = 250
        self.text_color = (49, 59, 114)
        self.highlight_color = (255, 255, 255)
        self.compradas = []
        self.mostrar_compradas = False
        self.compradas_index = 0
        self.modo_descricao = False

        # Controle de teclas por frame
        self.b_pressed_last_frame = False
        self.tab_pressed_last_frame = False
        self.up_pressed_last_frame = False
        self.down_pressed_last_frame = False
        self.enter_pressed_last_frame = False

        print("Dicas recebidas:", self.dicas)
        for i, d in enumerate(self.dicas):
            print(f"Dica {i}: {d['conceito']}, imagem: {d.get('imagem')}")


        # Painel visual
        self.painelloja = pygame.image.load(menu_path + "HUD/lojahud.png").convert_alpha()
        self.painellojarect = self.painelloja.get_rect(center=(
            displaySurface.get_width() // 2,
            displaySurface.get_height() - 200
        ))

        # Pré-carregar imagens das dicas
        for d in self.dicas:
        
            # Garante que as chaves existem
            if 'descricao' not in d:
                d['descricao'] = ""
            if 'descricao_completa' not in d:
                d['descricao_completa'] = d.get('descricao', "")
            # Carrega imagem se existir
            img_path = d.get("imagem")
            
            if img_path :
                try:
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (120, 120))
                    d['imagem_carregada'] = img
                except Exception as e:
                    print(f"Erro ao carregar imagem {img_path}: {e}")
                    d['imagem_carregada'] = None
            else:
                d['imagem_carregada'] = None

    # ------------------------------- FUNÇÕES DE CONTROLE -------------------------------
    def mover_selecao(self, direcao):
        self.selected_index = max(0, min(self.selected_index + direcao, len(self.dicas)-1))

    def mover_selecao_compradas(self, direcao):
        if self.compradas:
            self.compradas_index = max(0, min(self.compradas_index + direcao, len(self.compradas)-1))

    def comprar(self):
        dica = self.dicas[self.selected_index]
        if dica in self.compradas:
            return
        if self.hero.coins_count >= dica['preco']:
            self.hero.coins_count -= dica['preco']
            self.compradas.append(dica)
            

    # ------------------------------- INPUT -------------------------------
    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Mostrar "(B) Abrir Loja"
        self.npc.show_interaction = self.hero.hitbox.colliderect(self.npc.hitbox)

        # Abrir/Fechar loja com B
        if keys[pygame.K_b] and not self.b_pressed_last_frame:
            if self.hero.hitbox.colliderect(self.npc.hitbox):
                self.active = not self.active
                self.mostrar_compradas = False
                self.modo_descricao = False
        self.b_pressed_last_frame = keys[pygame.K_b]

        # Abrir menu das compradas (TAB)
        if keys[pygame.K_TAB] and not self.tab_pressed_last_frame:
            if not self.active:
                self.mostrar_compradas = not self.mostrar_compradas
                self.modo_descricao = False
        self.tab_pressed_last_frame = keys[pygame.K_TAB]

        # ------------------- MENU DAS COMPRADAS -------------------
        if self.mostrar_compradas:
            if not self.modo_descricao:
                if keys[pygame.K_UP] and not self.up_pressed_last_frame:
                    self.mover_selecao_compradas(-1)
                if keys[pygame.K_DOWN] and not self.down_pressed_last_frame:
                    self.mover_selecao_compradas(1)
                if keys[pygame.K_RETURN] and not self.enter_pressed_last_frame:
                    self.modo_descricao = True
            else:
                if keys[pygame.K_RETURN] and not self.enter_pressed_last_frame:
                    self.modo_descricao = False

            self.up_pressed_last_frame = keys[pygame.K_UP]
            self.down_pressed_last_frame = keys[pygame.K_DOWN]
            self.enter_pressed_last_frame = keys[pygame.K_RETURN]
            return

        # Não está na loja → não navega
        if not self.active:
            return

        # ------------------- MENU DA LOJA -------------------
        if keys[pygame.K_UP] and not self.up_pressed_last_frame:
            self.mover_selecao(-1)
        if keys[pygame.K_DOWN] and not self.down_pressed_last_frame:
            self.mover_selecao(1)
        if keys[pygame.K_RETURN] and not self.enter_pressed_last_frame:
            self.comprar()

        self.up_pressed_last_frame = keys[pygame.K_UP]
        self.down_pressed_last_frame = keys[pygame.K_DOWN]
        self.enter_pressed_last_frame = keys[pygame.K_RETURN]

    # ------------------------------- QUEBRA DE TEXTO -------------------------------
    def _quebrar_texto(self, texto, limite):
        palavras = texto.split()
        linhas = []
        atual = ""

        for palavra in palavras:
            if len(atual) + len(palavra) + 1 > limite:
                linhas.append(atual)
                atual = palavra
            else:
                atual += (" " if atual else "") + palavra

        if atual:
            linhas.append(atual)

        return linhas

    # ------------------------------- DESENHO DO MENU DE COMPRADAS -------------------------------
    def draw_compradas(self):
        self.displaySurface.blit(self.painelloja, self.painellojarect)

        # ----- CASO NÃO HAJA COMPRADAS -----
        if not self.compradas:
            vazio = self.font.render("Nenhuma dica adquirida", True, self.text_color)
            self.displaySurface.blit(vazio, (self.painellojarect.x + 10, self.painellojarect.y + 10))
            instrucao = self.font.render("Pressione TAB para fechar", True, self.text_color)
            self.displaySurface.blit(instrucao, (self.painellojarect.x + 10, self.painellojarect.bottom - 25))
            return

        # ----- LISTA DE COMPRADAS -----
        if not self.modo_descricao:
            titulo = self.font.render("Dicas Compradas", True, self.text_color)
            self.displaySurface.blit(titulo, (self.painellojarect.x + 10, self.painellojarect.y + 10))

            y = self.painellojarect.y + 30
            for i, dica in enumerate(self.compradas):
                cor = self.highlight_color if i == self.compradas_index else self.text_color
                texto = f"- {dica['conceito']}"
                self.displaySurface.blit(self.font.render(texto, True, cor), (self.painellojarect.x + 10, y))
                y += 18

        # ----- DESCRIÇÃO DE UMA DICA -----
        else:
            dica = self.compradas[self.compradas_index]
            titulo = self.font.render(dica['conceito'], True, self.highlight_color)
            self.displaySurface.blit(titulo, (self.painellojarect.x + 10, self.painellojarect.y + 10))

            y = self.painellojarect.y + 30
            for linha in self._quebrar_texto(dica['descricao_completa'], 32):
                self.displaySurface.blit(self.font.render(linha, True, self.text_color),
                                         (self.painellojarect.x + 10, y))
                y += 15

            #
        # ----- INSTRUÇÃO PADRÃO NO FINAL -----
        instrucao = self.font.render("Pressione TAB para fechar", True, self.text_color)
        self.displaySurface.blit(instrucao, (self.painellojarect.x + 10, self.painellojarect.bottom - 25))

    # ------------------------------- DESENHO PRINCIPAL -------------------------------
    def draw(self):
        if self.active:
            self.displaySurface.blit(self.painelloja, self.painellojarect)

            # Título
            titulo = self.font.render("Loja de Conceitos Variados", True, self.text_color)
            self.displaySurface.blit(
                titulo,
                (self.painellojarect.centerx - titulo.get_width() // 2, self.painellojarect.y + 10)
            )

            # Lista de itens
            y = self.painellojarect.y + 50
            for i, dica in enumerate(self.dicas):
                cor = self.highlight_color if i == self.selected_index else self.text_color
                status = "(comprado)" if dica in self.compradas else f"- {dica['preco']} moedas"
                texto = f"{dica['conceito']} {status}"
                for linha in self._quebrar_texto(texto, 32):
                    self.displaySurface.blit(self.font.render(linha, True, cor), (self.painellojarect.x + 10, y))
                    y += 15

            # Descrição do item selecionado
            y += 10
            for linha in self._quebrar_texto(self.dicas[self.selected_index]['descricao'], 32):
                self.displaySurface.blit(self.font.render(linha, True, self.text_color),
                                         (self.painellojarect.x + 10, y))
                y += 15

            # INSTRUÇÃO DE FECHAR
            instrucao = self.font.render("Pressione B para fechar a loja", True, self.text_color)
            self.displaySurface.blit(instrucao, (self.painellojarect.x + 10, self.painellojarect.bottom - 25))

        # Menu das compradas
        if self.mostrar_compradas:
            self.draw_compradas()
