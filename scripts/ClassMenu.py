import pygame
from scripts.Config import *
from scripts.ParallaxMenuBackground import StaticMenuBackground
from scripts.ClassLevel1 import *
from scripts.ClassHero import Hero

class Menu:
    def __init__(self, surface, start_game_callback, font_path=font_path, font_size=24):
        self.surface = surface
        self.start_game_callback = start_game_callback  # renomeado para clareza
        self.font_tutorial = pygame.font.Font(font_path, 20)
        self.parallax_bg = StaticMenuBackground(surface)

        # Controle global de fase
        self.id_fase = 0

        # Fontes
        self.font_titulo = pygame.font.Font(font_path, 72)
        self.font = pygame.font.Font(font_path, font_size)

        # Título
        self.titulo_surface = self.font_titulo.render("Samurai da Estatística", True, (255, 255, 255))
        self.titulo_rect = self.titulo_surface.get_rect(center=(surface.get_width() // 2, 250))

        # Texto "Pressione ENTER"
        self.entrar_surface = self.font.render("Pressione ENTER", True, (49, 59, 114))
        self.entrar_rect = self.entrar_surface.get_rect(center=(surface.get_width() // 2, 320))

        # Painel do tutorial e título
        self.painel_texto = pygame.image.load(menu_path + "titulo12.png").convert_alpha()
        self.painel_rect = self.painel_texto.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        self.paineltitulo = pygame.image.load(menu_path + "fundo_titulo_edit.png").convert_alpha()
        self.paineltitulo_rect = self.paineltitulo.get_rect(center=(surface.get_width() // 2, 250))

        # Herói animado no menu
        self.hero = Hero(position=(180, 480), faceRight=True)

        # Rects das opções
        self.entrar_text_rect = pygame.Rect(surface.get_width() // 2 - 80, 300, 160, 40)
        self.tutorial_rect = pygame.Rect(surface.get_width() // 2 - 80, 360, 160, 40)
        self.fases_rect = pygame.Rect(surface.get_width() // 2 - 80, 420, 160, 40)
        self.sair_rect = pygame.Rect(surface.get_width() // 2 - 80, 480, 160, 40)

        self.state = "inicio"
        self.selected_index = 0
        self.buttons = [("entrar", self.entrar_rect)]

        self.last_toggle = pygame.time.get_ticks()
        self.show_entrar = True
        self.blink_interval = 800

        # Fases disponíveis
        self.fases_disponiveis = [
          
            ("Fase 1", Level1, 1),
            ("Fase 2", Level2, 2),
            ("Fase 3", Level3, 3),
            ("Fase 4" , Level4, 4),
            ("Fase 5" , Level5, 5),
            ("Fase 6" , Level6, 6),
        ]
        self.selected_fase = 0

    # -----------------------------------------------------------------------
    # DESENHO DO MENU
    # -----------------------------------------------------------------------
    def draw(self):
        self.parallax_bg.draw()
        self.hero.update_dummy()
        self.surface.blit(self.hero.image, self.hero.rect)

        # Tela inicial ou principal
        if self.state in ["inicio", "principal"]:
            self.surface.blit(self.paineltitulo, self.paineltitulo_rect)
            self.surface.blit(self.titulo_surface, self.titulo_rect)

        # Tela inicial: "Pressione ENTER" piscando
        if self.state == "inicio":
            now = pygame.time.get_ticks()
            if now - self.last_toggle > self.blink_interval:
                self.show_entrar = not self.show_entrar
                self.last_toggle = now
            if self.show_entrar:
                self.surface.blit(self.entrar_surface, self.entrar_rect)

        # Menu principal
        elif self.state == "principal":
            for i, (name, rect) in enumerate(self.buttons):
                selected = i == self.selected_index
                color = (49, 59, 114) if selected else (255, 255, 255)
                prefix = "→ " if selected else "   "
                text_surface = self.font.render(prefix + name.capitalize(), True, color)
                text_rect = text_surface.get_rect(center=rect.center)
                self.surface.blit(text_surface, text_rect)

        # Seleção de fases
        elif self.state == "fases":
            self.surface.blit(self.painel_texto, self.painel_rect)
            titulo_surface = self.font.render("Escolha uma Fase:", True, (255, 255, 255))
            titulo_rect = titulo_surface.get_rect(center=(self.painel_rect.centerx, self.painel_rect.top + 50))
            self.surface.blit(titulo_surface, titulo_rect)

            linhas_por_coluna = 3
            espacamento_horizontal = 180
            espacamento_vertical = 50
            total_fases = len(self.fases_disponiveis)
            num_colunas = (total_fases + linhas_por_coluna - 1) // linhas_por_coluna
            num_linhas = min(linhas_por_coluna, total_fases)
            largura_total_grade = (num_colunas - 1) * espacamento_horizontal
            altura_total_grade = (num_linhas - 1) * espacamento_vertical
            margem_esquerda = self.painel_rect.centerx - largura_total_grade // 2 - 40
            margem_topo = self.painel_rect.centery - altura_total_grade // 2 - 10

            for i, (nome, _, _) in enumerate(self.fases_disponiveis):
                coluna = i // linhas_por_coluna
                linha = i % linhas_por_coluna
                x = margem_esquerda + coluna * espacamento_horizontal
                y = margem_topo + linha * espacamento_vertical
                cor = (49, 59, 114) if i == self.selected_fase else (255, 255, 255)
                fase_surface = self.font.render(nome, True, cor)
                fase_rect = fase_surface.get_rect(topleft=(x, y))
                self.surface.blit(fase_surface, fase_rect)

    # -----------------------------------------------------------------------
    # ENTRADAS DO TECLADO
    # -----------------------------------------------------------------------
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            # Tela inicial
            if self.state == "inicio":
                if event.key == pygame.K_RETURN:
                    self.state = "principal"
                    self.buttons = [
                        ("entrar", self.entrar_text_rect),
                        ("tutorial", self.tutorial_rect),
                        ("fases", self.fases_rect),
                        ("sair", self.sair_rect),
                    ]
                    self.selected_index = 0

            # Menu principal
            elif self.state == "principal":
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.buttons)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.buttons)
                elif event.key == pygame.K_RETURN:
                    opcao = self.buttons[self.selected_index][0]

                    if opcao == "entrar":
                        self.id_fase = 1
                        self.start_game_callback(Level1(self.surface, fase_id=self.id_fase))

                    elif opcao == "tutorial":
                        self.id_fase = 0
                        self.start_game_callback(Tutorial(self.surface, fase_id=self.id_fase))

                    elif opcao == "fases":
                        self.state = "fases"
                        self.selected_fase = 0

                    elif opcao == "sair":
                        pygame.quit()
                        exit()

            # Seleção de fases
            elif self.state == "fases":
                if event.key == pygame.K_UP:
                    self.selected_fase = (self.selected_fase - 1) % len(self.fases_disponiveis)
                elif event.key == pygame.K_DOWN:
                    self.selected_fase = (self.selected_fase + 1) % len(self.fases_disponiveis)
                elif event.key == pygame.K_RETURN:
                    nome, classe, fase_id = self.fases_disponiveis[self.selected_fase]
                    self.id_fase = fase_id
                    self.start_game_callback(classe(self.surface, fase_id=fase_id))
                elif event.key == pygame.K_ESCAPE:
                    self.state = "principal"

    def get_selected_option(self):
        return self.buttons[self.selected_index][0]
