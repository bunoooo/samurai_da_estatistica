import pygame
from scripts.Config import *
from scripts.ClassSpriteSheet import *

CoinSprites = [(0, 0, 8, 8)]
PotionSprites = [(0, 0, 8, 8)]

class HUD:
    def __init__(self, hero, vida_hud_path, vida_icon_rect, contorno_path, font_path = font_path, font_size = 22):
        """
        hero: objeto com atributo `lives`
        vida_hud_path: caminho da imagem com os ícones de vida
        vida_icon_rect: (x, y, w, h) do sprite de vida na imagem
        contorno_path: imagem de contorno ao redor de todas as vidas
        """

        self.coinSpriteSheet = SpriteSheet(hud_path + "SpinningCoin.png", CoinSprites)
        self.potionSpriteSheet = SpriteSheet(hud_path + "health_medium.png", PotionSprites)

        self.icon_perso = hud_path + "life_icon.png"
        self.icon_perso_hud = hud_path + "icon_perso_hud.png"

        self.tempo_hud = hud_path + "tempo_hud.png"

        self.coin_hud = hud_path + "coin_hud.png"

        self.potion_hud = hud_path + "potion_hud1.png"

        self.vida_hud_path = vida_hud_path
        self.vida_icon_rect = vida_icon_rect
        self.contorno_path = contorno_path
        self.font_path = font_path
        self.font_size = font_size
        self._load_resources(hero)

        self.start_time = pygame.time.get_ticks()  # tempo de início da fase
        self.invincibility_font = pygame.font.Font(self.font_path, self.font_size)  # fonte menor opcional

        self.icon_perso_img = pygame.image.load(self.icon_perso).convert_alpha()
        self.icon_perso_hud_img = pygame.image.load(self.icon_perso_hud).convert_alpha()
        self.tempo_hud_img = pygame.image.load(self.tempo_hud).convert_alpha()
        self.coin_hud_img = pygame.image.load(self.coin_hud).convert_alpha()
        self.potion_hud_img = pygame.image.load(self.potion_hud).convert_alpha()


    def _load_resources(self, hero):
        self.hero = hero

        # Ícone de vida
        vida_img = pygame.image.load(self.vida_hud_path).convert_alpha()
        x, y, w, h = self.vida_icon_rect
        self.vida_icon = vida_img.subsurface(pygame.Rect(x, y, w, h)).copy()

        self.icon_w = w
        self.icon_h = h

        # Imagem de contorno que envolve todos os ícones de vida
        self.vida_hud = pygame.image.load(self.contorno_path).convert_alpha()

        self.start_time = pygame.time.get_ticks()

        # Fonte
        if self.font_path:
            self.font = pygame.font.Font(self.font_path, self.font_size)
        else:
            self.font = pygame.font.Font(self.font_path, self.font_size)

    def draw(self, surface):
        # Posição inicial do HUD
        x_start = 65
        y_start = 0

        # --- HUD de Vida ---
        surface.blit(self.vida_hud, (x_start, y_start))

        spacing = self.icon_w
        for i in range(self.hero.lives):
            x = x_start + 9 + i * spacing
            y = y_start + 9
            surface.blit(self.vida_icon, (x, y))

       

        
        ################################## HUD MOEDA ############################################
        # Fonte para contagem de moedas
        coin_font = pygame.font.Font(self.font_path, 14)

        # Obtém a surface do frame da moeda
        coin_frame = self.coinSpriteSheet.getSprites(0)[0]
        coin_frame = pygame.transform.scale(coin_frame, (10, 10))

        # Posição do HUD da moeda
        coin_x, coin_y = 2, 60

        # Desenha fundo do HUD da moeda
        surface.blit(self.coin_hud_img, (coin_x, coin_y))

        
        surface.blit(coin_frame, (coin_x + 15, coin_y + 17))

        # Texto da quantidade
        x_font = pygame.font.Font(self.font_path, 9)
        x_surface = x_font.render("x", True, (49, 59, 114))
        
        coin_text = f"{self.hero.coins_count}"
        coin_surface = coin_font.render(coin_text, True, (49, 59, 114))

        # Centralizar texto verticalmente dentro do coin_hud_img
        hud_rect = self.coin_hud_img.get_rect(topleft=(coin_x, coin_y))
        
        coin_rect = coin_surface.get_rect(midleft=(
            hud_rect.left + coin_frame.get_width() + 22,  # espaço depois da moeda
            hud_rect.centery
        ))

        coin_rect_x = coin_surface.get_rect(midleft=(
            hud_rect.left + coin_frame.get_width() + 15,  # espaço depois da moeda
            hud_rect.centery + 3
        ))

        surface.blit(x_surface,coin_rect_x)
        surface.blit(coin_surface, coin_rect)


       #################################### Potion HUD ########################################################


        surface.blit(self.potion_hud_img, (coin_x + 60, coin_y - 1))
       
        

        potion_frame = self.potionSpriteSheet.getSprites(0)[0]
        potion_frame = pygame.transform.scale(potion_frame, (12, 12))

        
        if self.hero.health:
            # Rect do HUD
            hud_rect = self.potion_hud_img.get_rect(topleft=(coin_x + 60, coin_y - 1))
            # Rect da poção centralizado dentro do HUD
           
            potion_rect = potion_frame.get_rect(center=hud_rect.center)
            
            surface.blit(potion_frame, potion_rect)


      ##################################### renderização do icone de personagem ###############################
        
     
       # icon render
       
        perso_x = 0
        perso_y = 60 - self.icon_perso_hud_img.get_height()   # acima do HUD de vida

        surface.blit(self.icon_perso_hud_img, (perso_x, perso_y))  # contorno
        surface.blit(self.icon_perso_img, (perso_x + 12, perso_y + 10))
       
        
        ################################# relogio de tempo #######################################################      
        # Tempo de fase no mesmo estilo da HUD de vidas
        
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_text = f"{minutes:02}:{seconds:02}"

        # Renderiza o texto
        time_surface = self.font.render(time_text, True, (255, 255, 255))

        # Define posição com base na HUD (por exemplo, abaixo das vidas)
        hud_x = 450
        hud_y = 0   
        surface.blit(self.tempo_hud_img, (hud_x, hud_y))

        # Centraliza o texto dentro da HUD
        text_rect = time_surface.get_rect(center=(hud_x + self.tempo_hud_img.get_width() // 2,
                                                hud_y + 2 + self.tempo_hud_img.get_height() // 2))
        surface.blit(time_surface, text_rect)



        ############################## invencibilidade Timer #######################################################################
        # --- Invencibilidade (usando o mesmo fundo do HUD de vida) ---
        
        inv_y_start = y_start + self.vida_hud.get_height()   # abaixo do HUD de vida

            # Fundo igual
        surface.blit(self.vida_hud, (x_start, inv_y_start))


        if self.hero.isInvincible:
            # Texto no centro do HUD
            max_time = invicible_time # Valor máximo do timer (ex: 300 frames = 5s)
            current_time = self.hero.invincibleTimer  # Valor atual

            # Tamanho máximo da barra
            bar_max_width = 50
            bar_height = 12

            # Cálculo da largura proporcional
            bar_width = int((current_time / max_time) * bar_max_width)

            # Posição na tela
            bar_x = x_start + 7
            bar_y = inv_y_start + 9
            
                

            # Barra atual (amarelo ouro)
            pygame.draw.rect(surface, (255, 215, 0), (bar_x, bar_y, bar_width, bar_height))

           

           



    def reset(self, new_hero):
        self._load_resources(new_hero)
