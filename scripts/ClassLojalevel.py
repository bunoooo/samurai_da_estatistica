import pygame
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
        self.modo_descricao = False   # Novo: controla se está mostrando descrição

        # Controle de teclas por frame
        self.b_pressed_last_frame = False
        self.tab_pressed_last_frame = False
        self.up_pressed_last_frame = False
        self.down_pressed_last_frame = False
        self.enter_pressed_last_frame = False


        self.painelloja = pygame.image.load(menu_path + "HUD/lojahud.png").convert_alpha()
        self.painellojarect = self.painelloja.get_rect(center=(displaySurface.get_width() // 2,
                                                                       displaySurface.get_height() -200))


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

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if self.hero.hitbox.colliderect(self.npc.hitbox):
            self.npc.show_interaction = True 

        else: 
            self.npc.show_interaction = False

        # Abrir/fechar loja com B
        if keys[pygame.K_b] and not self.b_pressed_last_frame:
            if self.hero.hitbox.colliderect(self.npc.hitbox):
                self.active = not self.active
        self.b_pressed_last_frame = keys[pygame.K_b]

        # Abrir/fechar menu de dicas compradas com TAB
        if keys[pygame.K_TAB] and not self.tab_pressed_last_frame:
            if not self.active:
                self.mostrar_compradas = not self.mostrar_compradas
                self.modo_descricao = False  # Reset para sempre voltar à lista
        self.tab_pressed_last_frame = keys[pygame.K_TAB]

        # Se está no menu de dicas compradas
        if self.mostrar_compradas:
            if not self.modo_descricao:  # Navega pela lista
                if keys[pygame.K_UP] and not self.up_pressed_last_frame:
                    self.mover_selecao_compradas(-1)
                if keys[pygame.K_DOWN] and not self.down_pressed_last_frame:
                    self.mover_selecao_compradas(1)
                if keys[pygame.K_RETURN] and not self.enter_pressed_last_frame:
                    self.modo_descricao = True  # Entra na tela de descrição
            else:
                if keys[pygame.K_RETURN] and not self.enter_pressed_last_frame:
                    self.modo_descricao = False  # Volta para a lista
            self.up_pressed_last_frame = keys[pygame.K_UP]
            self.down_pressed_last_frame = keys[pygame.K_DOWN]
            self.enter_pressed_last_frame = keys[pygame.K_RETURN]
            return  # Não processa a loja quando está no menu compradas

        if not self.active:
            return

        # Navegação dentro da loja
        if keys[pygame.K_UP] and not self.up_pressed_last_frame:
            self.mover_selecao(-1)
        if keys[pygame.K_DOWN] and not self.down_pressed_last_frame:
            self.mover_selecao(1)
        if keys[pygame.K_RETURN] and not self.enter_pressed_last_frame:
            self.comprar()

        self.up_pressed_last_frame = keys[pygame.K_UP]
        self.down_pressed_last_frame = keys[pygame.K_DOWN]
        self.enter_pressed_last_frame = keys[pygame.K_RETURN]

    def draw_compradas(self):
        # Usa a imagem do painel da loja como fundo
        self.displaySurface.blit(self.painelloja, self.painellojarect)

        if not self.compradas:
            titulo = self.font.render("Nenhuma dica adquirida", True, self.text_color)
            self.displaySurface.blit(titulo, (self.painellojarect.x + 10, self.painellojarect.y + 10))
            return

        y = self.painellojarect.y + 30  # posição inicial

        if not self.modo_descricao:
            # Título
            titulo = self.font.render("Dicas Compradas", True, self.text_color)
            self.displaySurface.blit(titulo, (self.painellojarect.x + 10, self.painellojarect.y + 10))

            # Lista de dicas compradas com espaçamento dinâmico
            for i, dica in enumerate(self.compradas):
                color = self.highlight_color if i == self.compradas_index else self.text_color
                linhas = self._quebrar_texto(f"- {dica['conceito']}", 32)
                for linha in linhas:
                    text_surf = self.font.render(linha, True, color)
                    self.displaySurface.blit(text_surf, (self.painellojarect.x + 10, y))
                    y += 10  # altura por linha
                

        else:
            # Mostra descrição da dica selecionada
            dica = self.compradas[self.compradas_index]
            titulo = self.font.render(dica['conceito'], True, self.highlight_color)
            self.displaySurface.blit(titulo, (self.painellojarect.x + 10, self.painellojarect.y + 10))

            y = self.painellojarect.y + 30  # posição inicial para o texto
            linhas = self._quebrar_texto(dica['descricao_completa'], 32)
            for linha in linhas:
                text_surf = self.font.render(linha, True, self.text_color)
                self.displaySurface.blit(text_surf, (self.painellojarect.x + 10, y))
                y += 10  # altura por linha


    def _quebrar_texto(self, texto, max_caracteres_por_linha):
        """
        Quebra o texto em linhas, pulando uma linha extra após cada ponto final.
        max_caracteres_por_linha: número máximo de caracteres por linha antes de quebrar.
        """
        linhas = []
        # Quebra o texto por ponto final
        frases = texto.split('. ')
        
        for frase in frases:
            frase = frase.strip()
            if frase == "":
                continue
            # Adiciona o ponto final de volta
            frase += '.'

            # Quebra frases longas em várias linhas se necessário
            while len(frase) > max_caracteres_por_linha:
                corte = frase.rfind(' ', 0, max_caracteres_por_linha)
                if corte == -1:  # se não achar espaço, corta no max_caracteres
                    corte = max_caracteres_por_linha
                linhas.append(frase[:corte])
                frase = frase[corte:].strip()
            
            linhas.append(frase)
            # Adiciona linha em branco após o ponto final
            linhas.append('')
    
        return linhas


    def draw(self):
        # Painel da loja ativa
        if self.active:
            self.displaySurface.blit(self.painelloja, self.painellojarect)

            # Título centralizado
            titulo = self.font.render("Loja de Conceitos Variados", True, self.text_color)
            titulo_x = self.painellojarect.x + (self.painellojarect.width - titulo.get_width()) // 2
            titulo_y = self.painellojarect.y + 10
            self.displaySurface.blit(titulo, (titulo_x, titulo_y))

            # Lista de dicas disponíveis com espaçamento dinâmico
            y = self.painellojarect.y + 50
            for i, dica in enumerate(self.dicas):
                color = self.highlight_color if i == self.selected_index else self.text_color
                status = "(comprado)" if dica in self.compradas else f"- {dica['preco']} moedas"
                texto = f"{dica['conceito']} {status}"

                # Quebra de texto e desenho linha por linha
                linhas = self._quebrar_texto(texto, 32)
                for linha in linhas:
                    text_surf = self.font.render(linha, True, color)
                    self.displaySurface.blit(text_surf, (self.painellojarect.x + 10, y))
                    y += 10  # altura por linha
                  # espaço extra entre conceitos

            # Descrição da dica selecionada
            selected_dica = self.dicas[self.selected_index]
            linhas_desc = self._quebrar_texto(selected_dica['descricao'], 32)
            y_desc_start = y + 10  # inicia logo abaixo da lista
            for linha in linhas_desc:
                text_surf = self.font.render(linha, True, self.text_color)
                self.displaySurface.blit(text_surf, (self.painellojarect.x + 10, y_desc_start))
                y_desc_start += 18  # altura por linha

        # Painel das dicas compradas
        if self.mostrar_compradas:
            self.displaySurface.blit(self.painelloja, self.painellojarect)
            self.draw_compradas()  # draw_compradas também já usa _quebrar_texto


