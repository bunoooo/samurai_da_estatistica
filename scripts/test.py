import pygame

class Dialogo:
    def __init__(self, font, largura, altura):
        self.font = font
        self.largura = largura
        self.altura = altura
        self.caixa = pygame.Rect(50, altura - 150, largura - 100, 100)
        self.texto = ""
        self.falas = []
        self.indice = 0
        self.ativo = False
        self.respostas = {}  # {indice_fala: ("pergunta", ["opcao1","opcao2"], resposta_certa)}

    def iniciar(self, falas, respostas=None):
        """Inicia o diálogo com uma lista de falas e, opcionalmente, perguntas"""
        self.falas = falas
        self.respostas = respostas if respostas else {}
        self.indice = 0
        self.ativo = True
        self.texto = self.falas[self.indice]

    def avancar(self):
        """Avança para a próxima fala"""
        if self.indice < len(self.falas) - 1:
            self.indice += 1
            self.texto = self.falas[self.indice]
        else:
            self.ativo = False

    def checar_resposta(self, escolha):
        """Verifica resposta do jogador em uma fala que contém pergunta"""
        if self.indice in self.respostas:
            _, opcoes, correta = self.respostas[self.indice]
            if escolha == correta:
                return True
            else:
                return False
        return None

    def desenhar(self, tela):
        if self.ativo:
            pygame.draw.rect(tela, (0, 0, 0), self.caixa)
            pygame.draw.rect(tela, (255, 255, 255), self.caixa, 2)

            # Renderiza o texto
            texto_render = self.font.render(self.texto, True, (255, 255, 255))
            tela.blit(texto_render, (self.caixa.x + 10, self.caixa.y + 10))

            # Se houver pergunta nesta fala
            if self.indice in self.respostas:
                pergunta, opcoes, _ = self.respostas[self.indice]
                pergunta_render = self.font.render(pergunta, True, (200, 200, 0))
                tela.blit(pergunta_render, (self.caixa.x + 10, self.caixa.y + 40))
                for i, opcao in enumerate(opcoes):
                    opcao_render = self.font.render(f"{i+1}) {opcao}", True, (200, 200, 200))
                    tela.blit(opcao_render, (self.caixa.x + 20, self.caixa.y + 60 + i*20))
