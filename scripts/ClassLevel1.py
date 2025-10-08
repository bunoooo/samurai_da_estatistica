import pygame
from pytmx.util_pygame import load_pygame , pytmx
from Config import *
from ClassHero import Hero
from ClassBee import Bee
from ClassTile import Tile
from ClassBackground import Background
from camera import *
from HUD import HUD
from AnimatedText import *
from ClassRobot import *
from Coin import *
from Potion import *
from ClassNpcRobot import *
from Classtext import *
from classfasestext import *
from ClassLoja import *
from ClassLojalevel import *
from ClassQuestSystem import *
from ClassPerguntaresposta import *
from cutscene import *
from portal import *

repositorio = Dialogos()

import pygame
from Config import *

class Tutorial():
    def __init__(self, displaySurface, fase_id=0):
        self.displaySurface = displaySurface
        self.fase_id = fase_id
        self.ja_teletransportou = False
        self.verificar_prox_fase = None

        # Fonte e texto inicial
        self.font = pygame.font.Font(font_path, 40)
        self.instruction_font = pygame.font.Font(font_path, 11)
        self.phase_text = AnimatedText(
            "Tutorial: Aprenda os Controles", self.font, (255, 255, 255), surface=self.displaySurface
        )

        # Carregar mapa TMX do tutorial
        self.levelData = load_pygame(LEVELS_PATH + "Level1/tutorial_map.tmx")

        # Grupos de sprites
        self.hero = pygame.sprite.GroupSingle()
        self.platformTiles = pygame.sprite.Group()
        self.othersprites = pygame.sprite.Group()
        self.othersprites2 = pygame.sprite.Group()
        self.paredesprites = pygame.sprite.Group()
        self.bees = pygame.sprite.Group()
        self.robot = pygame.sprite.Group()
        self.Coin = pygame.sprite.Group()
        self.potion = pygame.sprite.Group()
        self.npcrobot = pygame.sprite.GroupSingle()
        self.npcloja = pygame.sprite.GroupSingle()
        self.portal = pygame.sprite.GroupSingle()

        # Dialogue
        self.dialogue_box = AppearingTextBox(repositorio.dialogo_fase(0), self.displaySurface)

        # Carregar tiles
        layer = self.levelData.get_layer_by_name('Platforms')
        for x, y, tileSurface in layer.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.platformTiles.add(tile)

        other = self.levelData.get_layer_by_name('Background')
        for x, y, tileSurface in other.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.othersprites.add(tile)

        other2 = self.levelData.get_layer_by_name('Background2')
        for x, y, tileSurface in other2.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.othersprites2.add(tile)

        # Adicionar personagens
        self.hero.add(Hero((100, 250), faceRight=True))
        self.robot.add(Robot((178, 290), moveRight=True, limit_left=120, limit_right=320))
        self.npcrobot.add(RobotNpc((800, 240), faceRight=False))
        self.npcloja.add(LojaNpc((800, 490), faceRight=False))
        self.Coin.add(Coin((670, 300)))
        self.potion.add(Potion((550, 375)))

        # Instruções do tutorial
        self.instructions = [
            {"text": "Use as setas para andar", "pos": (0, 380)},
            {"text": "Use a seta para cima para pular", "pos": (400, 490)},
            {"text": "Ao cair, jack tomará dano e será teletransportado para o inicio da fase", "pos": (260, 510)},
            {"text": "Aperte espaço para atacar", "pos": (150, 200)},
            {"text": "Ao tomar dano, jack ficará um tempo invulnerável", "pos": (150, 190)},
            {"text": "Se estiver correndo, o pulo vai mais alto", "pos": (350, 500)},
            {"text": "Para abrir dialogos com os npcs aperte E", "pos": (680, 130)},
            {"text": "Para avançar no dialogo aperte A", "pos": (680, 140)},
            {"text": "Para abrir o modo pergunta do npc aperte P", "pos": (680, 150)},
            {"text": "Moedas podem ser usadas ", "pos": (580, 250)},
            {"text": "para comprar conceitos na loja", "pos": (580, 260)},
            {"text": "Aperte V, para utilizar as poções ", "pos": (430, 300)},
            {"text": "Elas recuperam 1 de vida", "pos": (430, 310)},
            {"text": "Só é possível carregar 1 porção por vez", "pos": (430, 320)},
            {"text": "Para abrir/fechar a loja aperte B", "pos": (750, 380)},
            {"text": "Para comprar o item aperte Enter", "pos": (750, 390)},
            {"text": "Para abrir/fechar os conceitos comprados aperte Tab", "pos": (630, 400)},
        ]

        # Loja e conceitos
        self.dicas_estatisticas = [
            {
                "conceito": "Conceito exemplo",
                "descricao": "Descrição parcial do conceito",
                "descricao_completa": "Aqui é possível visualizar a descrição completa do conceito estatístico",
                "feedback" : "Uhuuul você acertou! quando você acertar a pergunta, automaticamente ganhará um fragmento do tempo, liberando o portal para a próxima fase",
                "preco": 1
            },
        ]
        self.loja = LojaSimples(self.hero.sprite, self.displaySurface, self.npcloja.sprite, self.dicas_estatisticas, pos=(100, 50))

        # Pergunta baseada em conceito da loja
        self.pergunta = PerguntaResposta(
            displaySurface=self.displaySurface,
            hero=self.hero.sprite,
            npc=self.npcrobot.sprite,
            pergunta="Então, preparado para seguir para o jogo?",
            loja=self.loja,
            correta_conceito="Conceito exemplo",
            pos=(100, 100)
        )

        # Quests
        quests = [
            {"id": 1, "text": "Falar com o Homem Estatístico", "done": False},
            {"id": 2, "text": "Elimine a maioria dos inimigos", "done": False},
            {"id": 3, "text": "Encontre o mercador", "done": False},
            {"id": 4, "text": "Retorne ao Mestre e retire a dúvida", "done": False}
        ]
        self.quest_system = QuestSystem(quests, self.displaySurface)

        # HUD e câmera
        vida_rect = (0, 0, 12, 12)
        self.hud = HUD(self.hero.sprite, hud_path + "vida_icon.png", vida_rect, contorno_path=hud_path + "vida_hud.png")
        self.camera = Camera(self.levelData.width * TILESIZE, self.levelData.height * TILESIZE)

    def reset(self):
        self.hero.empty()
        self.platformTiles.empty()
        self.othersprites.empty()
        self.hero.add(Hero((100, 250), faceRight=True))

    def update(self, confirm_exit=False):
        self.hero.update(self)
        self.phase_text.update()
        self.camera.update(self.hero.sprite)
        self.npcloja.update(self)
        self.robot.update(self)
        self.dialogue_box.update()
        self.loja.handle_input()
        self.Coin.update()
        self.potion.update()
        self.pergunta.handle_input()
        self.npcrobot.update(self)

        # Portal aparece apenas se acertou
        if self.pergunta.acertou and self.portal.sprite is None:
            self.portal.add(Portal((30, 120)))

        # Apertou para entrar no portal
        keys = pygame.key.get_pressed()
        if self.portal.sprite is not None:
            self.portal.update()
            if self.hero.sprite.rect.colliderect(self.portal.sprite.rect):
                if keys[pygame.K_h]:
                    print("Portal ativado!")
                    self.verificar_prox_fase = "next_level"

    def draw(self):
        # Fundo
        self.background = Background()
        self.background.draw1(self.displaySurface)

        # Tiles
        for tile in self.othersprites:
            self.displaySurface.blit(tile.image, self.camera.apply(tile))
        for tile in self.othersprites2:
            self.displaySurface.blit(tile.image, self.camera.apply(tile))
        for tile in self.platformTiles:
            self.displaySurface.blit(tile.image, self.camera.apply(tile))

        # Portal
        if self.portal.sprite is not None:
            pos = self.camera.apply(self.portal.sprite)
            self.displaySurface.blit(self.portal.sprite.image, pos)
            self.portal.sprite.draw(self.displaySurface, self.camera)

        # Herói e NPCs
        self.displaySurface.blit(self.hero.sprite.image, self.camera.apply(self.hero.sprite))
        for robot in self.robot:
            pos = self.camera.apply(robot)
            self.displaySurface.blit(robot.image, pos)
        pos = self.camera.apply(self.npcrobot.sprite)
        self.displaySurface.blit(self.npcrobot.sprite.image, pos)
        self.npcrobot.sprite.draw(self.displaySurface, self.camera)
        pos1 = self.camera.apply(self.npcloja.sprite)
        self.displaySurface.blit(self.npcloja.sprite.image, pos1)
        self.npcloja.sprite.draw(self.displaySurface, self.camera)

        # HUD e instruções
        self.hud.draw(self.displaySurface)
        for instr in self.instructions:
            text_surface = self.instruction_font.render(instr["text"], True, (255, 255, 255))
            self.displaySurface.blit(text_surface, instr["pos"])

        # Moedas, poções, loja, textos
        for coin in self.Coin:
            pos = self.camera.apply(coin)
            self.displaySurface.blit(coin.image, pos)
        for potion in self.potion:
            pos = self.camera.apply(potion)
            self.displaySurface.blit(potion.image, pos)

        self.loja.draw()
        self.phase_text.draw()
        self.dialogue_box.draw_box()
        self.dialogue_box.draw_text()
        self.pergunta.draw()

    def run(self, confirm_exit=False):
        self.update(confirm_exit)
        self.draw()

class Level1():
    def __init__(self, displaySurface, fase_id=1):
       
        self.ja_teletransportou = False

        self.verificar_prox_fase = None
        
        self.displaySurface = displaySurface
        
        self.fase_id = fase_id

        self.font = pygame.font.Font(font_path, 40)
        self.phase_text = AnimatedText("Fase 1: O Inicio da Jornada", self.font, (255, 255, 255), surface=self.displaySurface)

        self.cutscene_active = True
        self.cutscene = Cutscene(self.displaySurface, font_path)

        dicas_estatisticas = [
    {
        "conceito": "Média", 
        "descricao": "A soma dos valores dividida pelo total.", 
        "descricao_completa": "A média é uma medida de tendência central que representa o valor típico de um conjunto de dados. Ela é calculada somando todos os valores do conjunto e dividindo pelo número total de observações. É útil para entender o comportamento geral dos dados, mas pode ser sensível a valores extremos.",
        "preco": 2,
        "feedback": "A média resume todos os valores em um único número representativo, ideal para planejar a quantidade de comida."
    },
    {
        "conceito": "Mediana", 
        "descricao": "O valor central de um conjunto ordenado.", 
        "descricao_completa": "A mediana é uma medida de tendência central que indica o valor que separa a metade superior da metade inferior dos dados. Ao contrário da média, a mediana não é influenciada por valores muito altos ou muito baixos, tornando-se útil para conjuntos de dados assimétricos.",
        "preco": 2,
        "feedback": "A mediana mostra o valor do meio quando os dados estão ordenados. Ela é útil quando há valores muito extremos, mas não representa todo o conjunto tão bem quanto a média."
    },
    {
        "conceito": "Moda", 
        "descricao": "O valor que mais se repete.", 
        "descricao_completa": "A moda é a medida de tendência central que representa o valor mais frequente em um conjunto de dados. Pode haver mais de uma moda, e é particularmente útil para dados categóricos ou quando se deseja identificar padrões de repetição.",
        "preco": 3,
        "feedback" : "A moda indica apenas o valor mais frequente. Pode mostrar o consumo mais comum, mas não ajuda a equilibrar os recursos para todos."
    },
    {
        "conceito": "Desvio Padrão", 
        "descricao": "Mede o quanto os valores se afastam da média.", 
        "descricao_completa": "O desvio padrão é uma medida de dispersão que indica o quanto os valores de um conjunto de dados se afastam da média. Quanto maior o desvio padrão, mais espalhados estão os dados; quanto menor, mais próximos da média eles se encontram.",
        "preco": 2,
        "feedback" : "bubbles"
    },
    {
        "conceito": "Probabilidade", 
        "descricao": "Chance de um evento acontecer.", 
        "descricao_completa": "Probabilidade é a medida numérica da chance de ocorrência de um evento dentro de um conjunto de possibilidades. É um conceito fundamental em estatística e análise de risco, usado para modelar incertezas e tomar decisões baseadas em chances relativas.",
        "preco": 1,
        "feedback" : "bubbles"
    }
]
        quests = [
            {"id": 1, "text": "Fale com o chefe da vila", "done": False},
            {"id": 2, "text": "Encontre o mercador", "done": False},
            {"id": 3 , "text": "Resolva o problema do chefe" , "done" : False},
            {"id": 4 , "text": "Entre no portal" , "done" : False}
        ]
        
        self.quest_system = QuestSystem(quests, self.displaySurface )
         # Carregar o arquivo TMX

        self.levelData = load_pygame(LEVELS_PATH + "Level1/level1_ajustado.tmx")

        # Instanciar classes
        self.background = Background()

        # Criar grupos de sprites
        self.hero = pygame.sprite.GroupSingle()
        self.platformTiles = pygame.sprite.Group()
        self.othersprites = pygame.sprite.Group()
        self.paredesprites = pygame.sprite.Group()
        self.bees = pygame.sprite.Group()
        self.robot = pygame.sprite.Group()
        self.Coin = pygame.sprite.Group()
        self.potion = pygame.sprite.Group()
        self.npcrobot = pygame.sprite.GroupSingle()
        self.npcloja = pygame.sprite.GroupSingle()
        self.portal = pygame.sprite.GroupSingle()
      

        layer = self.levelData.get_layer_by_name('Platforms')
        for x, y, tileSurface in layer.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.platformTiles.add(tile)
        
        
        other = self.levelData.get_layer_by_name('Background')
        for x, y, tileSurface in other.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.othersprites.add(tile)

        parede = self.levelData.get_layer_by_name('Parede')
        for x, y, tileSurface in parede.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.paredesprites.add(tile)

        self.dialogue_box = AppearingTextBox(repositorio.dialogo_fase(fase_id), self.displaySurface)
    
        self.robot.add(Robot((178, 165), moveRight=True,limit_left= 120, limit_right= 320))

        self.robot.add(Robot((310, 225), moveRight=True,limit_left= 310, limit_right= 550))

        self.robot.add(Robot((550, 400), moveRight=True,limit_left= 480, limit_right= 570))
        
        self.robot.add(Robot((300, 465), moveRight=True,limit_left= 40, limit_right= 450))
      
        self.robot.add(Robot((600, 465), moveRight=True,limit_left= 580, limit_right= 770))

        self.robot.add(Robot((500, 225), moveRight=True,limit_left= 310, limit_right= 550))

        self.robot.add(Robot((800, 160), moveRight=True,limit_left= 800, limit_right= 1000))

        self.robot.add(Robot((900, 400), moveRight=True,limit_left= 900, limit_right= 1000))

        self.robot.add(Robot((900, 400), moveRight=True,limit_left= 900, limit_right= 1000))
       
        self.robot.add(Robot((900, 400), moveRight=True,limit_left= 900, limit_right= 1000))

        self.robot.add(Robot((1510, 275), moveRight=True,limit_left= 1300, limit_right= 1790))

        self.robot.add(Robot((1310, 275), moveRight=True,limit_left= 1300, limit_right= 1790))


        self.npcrobot.add(RobotNpc((1435,515) , faceRight= False))

        self.npcloja.add(LojaNpc((1240,120) , faceRight= False))
       
        self.Coin.add(Coin((200,105)))
        self.Coin.add(Coin((170,105)))
        self.Coin.add(Coin((20,320)))
        self.Coin.add(Coin((540,320)))
        self.Coin.add(Coin((510,320)))
        self.Coin.add(Coin((705,140)))

        self.Coin.add(Coin((820,420)))
        self.Coin.add(Coin((850,420)))

        self.Coin.add(Coin((1840,130)))
        self.Coin.add(Coin((1810,130)))


        self.potion.add(Potion((10,220)))
        self.potion.add(Potion((1214,452)))
        self.potion.add(Potion((1900,310)))

                
        self.hero.add(Hero((170, 250), faceRight=True))
       

        self.loja = LojaSimples(self.hero.sprite, self.displaySurface, self.npcloja.sprite , dicas_estatisticas, pos=(100, 50))
  
        self.pergunta = PerguntaResposta(
            displaySurface=self.displaySurface,
            hero=self.hero.sprite,
            npc=self.npcrobot.sprite,
            pergunta="Então, como eu posso ajustar os valores em uma única medida representativa?",
            loja=self.loja,
            correta_conceito="Média",
            pos=(100, 100)
        )

       

        vida_rect = (0, 0, 12, 12)
        self.hud = HUD(self.hero.sprite, hud_path + "vida_icon.png",vida_rect,contorno_path = hud_path + "vida_hud.png")

        # Configura a câmera
        self.camera = Camera(self.levelData.width * TILESIZE, self.levelData.height * TILESIZE)

        

        self.teleport_zone = pygame.Rect(
        self.npcrobot.sprite.hitbox.rect.x - 50,   # aumenta para esquerda
        self.npcrobot.sprite.hitbox.rect.y -100,   # aumenta para cima
        self.npcrobot.sprite.hitbox.rect.width + 100,  # aumenta largura
        self.npcrobot.sprite.hitbox.rect.height + 100  # aumenta altura
    )

    def reset(self):
        # Limpa todos os grupos de sprites
        self.hero.empty()
        self.platformTiles.empty()
        self.paredesprites.empty()
        self.othersprites.empty()
        self.bees.empty()
        self.robot.empty()
        self.Coin.empty()
        self.potion.empty()
        self.npcrobot.empty()
        self.npcloja.empty()
        self.portal.empty()

        # Recarrega camadas do mapa
        layer = self.levelData.get_layer_by_name('Platforms')
        for x, y, tileSurface in layer.tiles():
            self.platformTiles.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))
        
        other = self.levelData.get_layer_by_name('Background')
        for x, y, tileSurface in other.tiles():
            self.othersprites.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))

        parede = self.levelData.get_layer_by_name('Parede')
        for x, y, tileSurface in parede.tiles():
            self.paredesprites.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))

        # Recria inimigos
        self.robot.add(Robot((178, 165), moveRight=True, limit_left=120, limit_right=320))
        self.robot.add(Robot((310, 225), moveRight=True, limit_left=310, limit_right=550))
        self.robot.add(Robot((550, 400), moveRight=True, limit_left=480, limit_right=570))
        self.robot.add(Robot((300, 465), moveRight=True, limit_left=40, limit_right=450))
        self.robot.add(Robot((600, 465), moveRight=True, limit_left=580, limit_right=770))
        self.robot.add(Robot((500, 225), moveRight=True, limit_left=310, limit_right=550))
        self.robot.add(Robot((800, 160), moveRight=True, limit_left=800, limit_right=1000))
        self.robot.add(Robot((900, 400), moveRight=True, limit_left=900, limit_right=1000))
        self.robot.add(Robot((1510, 275), moveRight=True, limit_left=1300, limit_right=1790))
        self.robot.add(Robot((1310, 275), moveRight=True, limit_left=1300, limit_right=1790))

        # Recria NPCs e portal
        self.npcrobot.add(RobotNpc((1435, 515), faceRight=False))
        self.npcloja.add(LojaNpc((1240, 120), faceRight=False))
        
       

        # Recria itens
        self.Coin.add(Coin((200,105)))
        self.Coin.add(Coin((170,105)))
        self.Coin.add(Coin((20,320)))
        self.Coin.add(Coin((540,320)))
        self.Coin.add(Coin((510,320)))
        self.Coin.add(Coin((705,140)))
        self.Coin.add(Coin((820,420)))
        self.Coin.add(Coin((850,420)))
        self.Coin.add(Coin((1840,130)))
        self.Coin.add(Coin((1810,130)))

        self.potion.add(Potion((10,220)))
        self.potion.add(Potion((1214,452)))
        self.potion.add(Potion((1900,310)))

        # Recria herói
        self.hero.add(Hero((170, 250), faceRight=True))

        vida_rect = (0, 0, 12, 12)
        self.hud = HUD(self.hero.sprite, hud_path + "vida_icon.png",vida_rect,contorno_path = hud_path + "vida_hud.png")

        # Recria loja e pergunta para garantir estado inicial
        dicas_estatisticas = [
            {
                "conceito": "Média", 
                "descricao": "A soma dos valores dividida pelo total.", 
                "descricao_completa": "A média é uma medida de tendência central que representa o valor típico de um conjunto de dados...",
                "preco": 2,
                "feedback": "A média resume todos os valores em um único número representativo."
            }
        ]
        self.loja = LojaSimples(self.hero.sprite, self.displaySurface, self.npcloja.sprite, dicas_estatisticas, pos=(100, 50))
        self.pergunta = PerguntaResposta(
            displaySurface=self.displaySurface,
            hero=self.hero.sprite,
            npc=self.npcrobot.sprite,
            pergunta="Então, como eu posso ajustar os valores em uma única medida representativa?",
            loja=self.loja,
            correta_conceito="Média",
            pos=(100, 100)
        )

        # Recria zona de teleporte
        self.teleport_zone = pygame.Rect(
            self.npcrobot.sprite.hitbox.rect.x - 50,
            self.npcrobot.sprite.hitbox.rect.y - 100,
            self.npcrobot.sprite.hitbox.rect.width + 100,
            self.npcrobot.sprite.hitbox.rect.height + 100
        )

        # Reseta flags
        self.ja_teletransportou = False
        self.pergunta.acertou = None
        self.pergunta.errou = None

    def update(self, confirm_exit=False):
    # Atualiza o herói sempre

        if not confirm_exit:
                self.hero.update(self)
        if self.cutscene_active:
            if self.cutscene.finished:
                self.cutscene_active = False  # agora a fase 1 começa
            return
        else:

            

            if self.pergunta.acertou and self.portal.sprite is None:
                 self.quest_system.complete_quest(3)
                 self.portal.add(Portal((0,170)))
            
            if self.npcloja.sprite.show_interaction:
                self.quest_system.complete_quest(2)
                self.hero.sprite.falou_com_npcloja = False    


            if self.hero.sprite.falou_com_npc:
                self.quest_system.complete_quest(1)
                self.hero.sprite.falou_com_npc = False

            keys = pygame.key.get_pressed()
            if self.portal.sprite is not None:
                self.portal.update()
                if self.hero.sprite.rect.colliderect(self.portal.sprite.rect):
                    if keys[pygame.K_h]:
                        print("Portal ativado!")
                        self.verificar_prox_fase = "next_level"

            # Só atualiza inimigos, moedas e poções se o diálogo e a loja não estiverem ativos
            if (self.dialogue_box and not self.dialogue_box.text_active and
                self.loja and not self.loja.active and not self.loja.mostrar_compradas):

                self.pergunta.handle_input()

                self.robot.update(self)
                self.Coin.update()
                self.potion.update()

                
            # Atualiza NPCs e loja sempre, se existirem
            if self.npcrobot.sprite:
                self.npcrobot.update(self)
            if self.npcloja.sprite:
                self.npcloja.update(self)
            
            self.camera.update(self.hero.sprite)
            self.phase_text.update()
            self.dialogue_box.update()
            self.loja.handle_input()

            # Teleporte quando errou
            if self.pergunta.errou and not self.ja_teletransportou:
                self.hero.sprite.teleport(0, 250)
                # Adiciona inimigos adicionais
                self.robot.add(Robot((800, 160), moveRight=True, limit_left=800, limit_right=1000))
                self.robot.add(Robot((900, 400), moveRight=True, limit_left=900, limit_right=1000))
                self.ja_teletransportou = True
                # Reseta o erro para não teletransportar várias vezes
                self.pergunta.errou = False


            # Resetar o teleporte caso ele saia da área
            if self.ja_teletransportou and not self.hero.sprite.hitbox.colliderect(self.teleport_zone):
                self.ja_teletransportou = False
                                   
    def draw(self):
                # Desenha o fundo
        if self.cutscene_active:
            self.cutscene.draw()
        else:          
            self.background.draw2(self.displaySurface)
            self.quest_system.draw()

            # Desenha as camadas com o deslocamento da câmera
            for tile in self.platformTiles:
                pos = self.camera.apply(tile)
                self.displaySurface.blit(tile.image, pos)
        

        # for r in self.hero.sprite.debug_platform_rects:
                # r é relativo ao herói
            #    rect_on_screen = r.copy()
            #   rect_on_screen.topleft = (r.x - self.hero.sprite.rect.x + self.camera.apply(self.hero.sprite).x,
            #                     r.y - self.hero.sprite.rect.y + self.camera.apply(self.hero.sprite).y)
            #  pygame.draw.rect(self.displaySurface, (255, 0, 0), rect_on_screen, 2)

            
            for tile in self.othersprites:
                pos = self.camera.apply(tile)
                self.displaySurface.blit(tile.image, pos)


            for tile in self.paredesprites:
                pos = self.camera.apply(tile)
                self.displaySurface.blit(tile.image, pos)
                pygame.draw.rect(
                self.displaySurface, (255, 255, 0),
                tile.rect.move(pos.left - tile.rect.left, pos.top - tile.rect.top), 1
                )

            
            for coin in self.Coin:
                pos = self.camera.apply(coin)
                self.displaySurface.blit(coin.image, pos)
        
        
            for potion in self.potion:
                pos = self.camera.apply(potion)
                self.displaySurface.blit(potion.image, pos)

            # Desenha o herói com o deslocamento da câmera
            pos = self.camera.apply(self.hero.sprite)
            self.displaySurface.blit(self.hero.sprite.image, pos)

           
            # Portal

            if self.portal.sprite is not None:
                pos = self.camera.apply(self.portal.sprite)
                self.displaySurface.blit(self.portal.sprite.image, pos)
                self.portal.sprite.draw(self.displaySurface, self.camera)

        
            # Desenha os robôs com seus rects
            for robot in self.robot:
                pos = self.camera.apply(robot)
                self.displaySurface.blit(robot.image, pos)
            
        
            pos = self.camera.apply(self.npcrobot.sprite)
            self.displaySurface.blit(self.npcrobot.sprite.image, pos)
            self.npcrobot.sprite.draw(self.displaySurface, self.camera)

            
         
            pos1 = self.camera.apply(self.npcloja.sprite)
            self.displaySurface.blit(self.npcloja.sprite.image, pos1)
            self.npcloja.sprite.draw(self.displaySurface, self.camera)
                

            hitbox_rect = self.npcloja.sprite.hitbox.rect.copy()
            hitbox_rect.topleft = (hitbox_rect.left + (pos1.left - self.npcloja.sprite.rect.left),
                                    hitbox_rect.top + (pos1.top - self.npcloja.sprite.rect.top))

                #pygame.draw.rect(self.displaySurface, (255, 0, 0), hitbox_rect, 2)
                
            
            # HUD e texto da fase
            self.hud.draw(self.displaySurface)
            self.phase_text.draw()

            
            self.dialogue_box.draw_box()
            self.dialogue_box.draw_text()

            




            #rect_on_screen = self.teleport_zone.copy()
            #rect_on_screen.topleft = (self.teleport_zone.x - self.hero.sprite.rect.x + self.camera.apply(self.hero.sprite).x,
            #                           self.teleport_zone.y - self.hero.sprite.rect.y + self.camera.apply(self.hero.sprite).y)
            #pygame.draw.rect(self.displaySurface, (255, 0, 0), rect_on_screen, 2)
            

            

            self.loja.draw()
            


            self.pergunta.draw()    
            
    def run(self, confirm_exit=False):
        # Atualiza a lógica do jogo
        self.update(confirm_exit=confirm_exit)
        # Desenha a tela
        self.draw()

 
class Level2():
    def __init__(self, displaySurface, fase_id=2):
       
        self.ja_teletransportou = False

        self.verificar_prox_fase = None
        
        self.displaySurface = displaySurface
        
        self.fase_id = fase_id

        self.font = pygame.font.Font(font_path, 40)
        self.phase_text = AnimatedText("Fase 2: O Inicio da Jornada", self.font, (255, 255, 255), surface=self.displaySurface)

        dicas_estatisticas = [ 
    {
        "conceito": "Tratamento A ",
        "descricao": "Aplicação imediata e barata, amplamente conhecido pela população.",
        "descricao_completa": (
            "Este tratamento é fácil de distribuir e tem ação rápida. "
            "No entanto, sua taxa de sucesso é de apenas 55%, "
            "e há risco moderado de efeitos colaterais. "
            "Muitas pessoas acreditam nele por tradição, não por evidência científica."
        ),
        "preco": 2,
        "feedback": (
            "Apesar de ser popular e rápido, sua eficácia é baixa. "
            "Não é o ideal para controlar uma epidemia com segurança."
        )
    },
    {
        "conceito": "Tratamento B ",
        "descricao": "Novo método, com dados promissores, mas origem incerta.",
        "descricao_completa": (
            "Tratamento desenvolvido recentemente em um laboratório desconhecido. "
            "Os dados indicam uma taxa de sucesso de 80%, mas há fortes indícios "
            "de que parte das informações foi manipulada por Erradon. "
            "Também há risco de efeitos colaterais não totalmente documentados."
        ),
        "preco": 3,
        "feedback": (
            "Os números parecem bons, mas a falta de confiabilidade dos dados torna esta opção arriscada."
        )
    },
    {
        "conceito": "Tratamento C",
        "descricao": "Método conhecido, com aplicação mais lenta, mas resultados sólidos.",
        "descricao_completa": (
            "Este tratamento tem sido utilizado com sucesso em epidemias passadas. "
            "Sua taxa de sucesso é de 90%, porém o tempo de aplicação é maior "
            "e requer organização logística. Os dados foram confirmados por múltiplas fontes confiáveis."
        ),
        "preco": 3,
        "feedback": (
            "Alta eficácia e dados confiáveis, apesar da aplicação mais lenta. "
            "É uma escolha estratégica e segura para conter a epidemia."
        )
    },
    {
        "conceito": "Tratamento D ",
        "descricao": "Práticas naturais sem comprovação científica.",
        "descricao_completa": (
            "Baseado em receitas e ervas tradicionais, este tratamento é amplamente divulgado em redes sociais. "
            "Sua taxa de sucesso real é estimada em 30%. "
            "Muitos acreditam nele devido a boatos espalhados por Erradon."
        ),
        "preco": 1,
        "feedback": (
            "Baixa eficácia e forte influência de desinformação. "
            "Não é uma escolha racional para conter uma epidemia."
        )
    }
]

        quests = [
            {"id": 1, "text": "Fale com o chefe da vila", "done": False},
            {"id": 2, "text": "Encontre o mercador", "done": False},
            {"id": 3 , "text": "Resolva o problema do chefe" , "done" : False},
            {"id": 4 , "text": "Entre no portal" , "done" : False}
        ]
        
        self.quest_system = QuestSystem(quests, self.displaySurface )
         # Carregar o arquivo TMX

        self.levelData = load_pygame(LEVELS_PATH + "Level1/level1_ajustado.tmx")

        # Instanciar classes
        self.background = Background()

        # Criar grupos de sprites
        self.hero = pygame.sprite.GroupSingle()
        self.platformTiles = pygame.sprite.Group()
        self.othersprites = pygame.sprite.Group()
        self.paredesprites = pygame.sprite.Group()
        self.bees = pygame.sprite.Group()
        self.robot = pygame.sprite.Group()
        self.Coin = pygame.sprite.Group()
        self.potion = pygame.sprite.Group()
        self.npcrobot = pygame.sprite.GroupSingle()
        self.npcloja = pygame.sprite.GroupSingle()
        self.portal = pygame.sprite.GroupSingle()
      

        layer = self.levelData.get_layer_by_name('Platforms')
        for x, y, tileSurface in layer.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.platformTiles.add(tile)
        
        
        other = self.levelData.get_layer_by_name('Background')
        for x, y, tileSurface in other.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.othersprites.add(tile)

        parede = self.levelData.get_layer_by_name('Parede')
        for x, y, tileSurface in parede.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.paredesprites.add(tile)

        self.dialogue_box = AppearingTextBox(repositorio.dialogo_fase(fase_id), self.displaySurface)
    
        self.robot.add(Robot((178, 165), moveRight=True,limit_left= 120, limit_right= 320))

        self.robot.add(Robot((310, 225), moveRight=True,limit_left= 310, limit_right= 550))

        self.robot.add(Robot((550, 400), moveRight=True,limit_left= 480, limit_right= 570))
        
        self.robot.add(Robot((300, 465), moveRight=True,limit_left= 40, limit_right= 450))
      
        self.robot.add(Robot((600, 465), moveRight=True,limit_left= 580, limit_right= 770))

        self.robot.add(Robot((500, 225), moveRight=True,limit_left= 310, limit_right= 550))

        self.robot.add(Robot((800, 160), moveRight=True,limit_left= 800, limit_right= 1000))

        self.robot.add(Robot((900, 400), moveRight=True,limit_left= 900, limit_right= 1000))

        self.robot.add(Robot((900, 400), moveRight=True,limit_left= 900, limit_right= 1000))
       
        self.robot.add(Robot((900, 400), moveRight=True,limit_left= 900, limit_right= 1000))

        self.robot.add(Robot((1510, 275), moveRight=True,limit_left= 1300, limit_right= 1790))

        self.robot.add(Robot((1310, 275), moveRight=True,limit_left= 1300, limit_right= 1790))


        self.npcrobot.add(RobotNpc((1435,515) , faceRight= False))

        self.npcloja.add(LojaNpc((1240,120) , faceRight= False))
       
        self.Coin.add(Coin((200,105)))
        self.Coin.add(Coin((170,105)))
        self.Coin.add(Coin((20,320)))
        self.Coin.add(Coin((540,320)))
        self.Coin.add(Coin((510,320)))
        self.Coin.add(Coin((705,140)))

        self.Coin.add(Coin((820,420)))
        self.Coin.add(Coin((850,420)))

        self.Coin.add(Coin((1840,130)))
        self.Coin.add(Coin((1810,130)))


        self.potion.add(Potion((10,220)))
        self.potion.add(Potion((1214,452)))
        self.potion.add(Potion((1900,310)))

                
        self.hero.add(Hero((170, 250), faceRight=True))
       

        self.loja = LojaSimples(self.hero.sprite, self.displaySurface, self.npcloja.sprite , dicas_estatisticas, pos=(100, 50))
  
        self.pergunta = PerguntaResposta(
            displaySurface=self.displaySurface,
            hero=self.hero.sprite,
            npc=self.npcrobot.sprite,
            pergunta="Com base nas probabilidades e nas informações fornecidas, qual tratamento oferece a melhor chance de controlar a epidemia com segurança, mesmo que demande mais tempo ou recursos?",
            loja=self.loja,
            correta_conceito="Tratamento C",
            pos=(100, 100)
        )

       

        vida_rect = (0, 0, 12, 12)
        self.hud = HUD(self.hero.sprite, hud_path + "vida_icon.png",vida_rect,contorno_path = hud_path + "vida_hud.png")

        # Configura a câmera
        self.camera = Camera(self.levelData.width * TILESIZE, self.levelData.height * TILESIZE)

        

        self.teleport_zone = pygame.Rect(
        self.npcrobot.sprite.hitbox.rect.x - 50,   # aumenta para esquerda
        self.npcrobot.sprite.hitbox.rect.y -100,   # aumenta para cima
        self.npcrobot.sprite.hitbox.rect.width + 100,  # aumenta largura
        self.npcrobot.sprite.hitbox.rect.height + 100  # aumenta altura
    )

    def reset(self):
        # Limpa todos os grupos de sprites
        self.hero.empty()
        self.platformTiles.empty()
        self.paredesprites.empty()
        self.othersprites.empty()
        self.bees.empty()
        self.robot.empty()
        self.Coin.empty()
        self.potion.empty()
        self.npcrobot.empty()
        self.npcloja.empty()
        self.portal.empty()

        # Recarrega camadas do mapa
        layer = self.levelData.get_layer_by_name('Platforms')
        for x, y, tileSurface in layer.tiles():
            self.platformTiles.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))
        
        other = self.levelData.get_layer_by_name('Background')
        for x, y, tileSurface in other.tiles():
            self.othersprites.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))

        parede = self.levelData.get_layer_by_name('Parede')
        for x, y, tileSurface in parede.tiles():
            self.paredesprites.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))

        # Recria inimigos
        self.robot.add(Robot((178, 165), moveRight=True, limit_left=120, limit_right=320))
        self.robot.add(Robot((310, 225), moveRight=True, limit_left=310, limit_right=550))
        self.robot.add(Robot((550, 400), moveRight=True, limit_left=480, limit_right=570))
        self.robot.add(Robot((300, 465), moveRight=True, limit_left=40, limit_right=450))
        self.robot.add(Robot((600, 465), moveRight=True, limit_left=580, limit_right=770))
        self.robot.add(Robot((500, 225), moveRight=True, limit_left=310, limit_right=550))
        self.robot.add(Robot((800, 160), moveRight=True, limit_left=800, limit_right=1000))
        self.robot.add(Robot((900, 400), moveRight=True, limit_left=900, limit_right=1000))
        self.robot.add(Robot((1510, 275), moveRight=True, limit_left=1300, limit_right=1790))
        self.robot.add(Robot((1310, 275), moveRight=True, limit_left=1300, limit_right=1790))

        # Recria NPCs e portal
        self.npcrobot.add(RobotNpc((1435, 515), faceRight=False))
        self.npcloja.add(LojaNpc((1240, 120), faceRight=False))
        
       

        # Recria itens
        self.Coin.add(Coin((200,105)))
        self.Coin.add(Coin((170,105)))
        self.Coin.add(Coin((20,320)))
        self.Coin.add(Coin((540,320)))
        self.Coin.add(Coin((510,320)))
        self.Coin.add(Coin((705,140)))
        self.Coin.add(Coin((820,420)))
        self.Coin.add(Coin((850,420)))
        self.Coin.add(Coin((1840,130)))
        self.Coin.add(Coin((1810,130)))

        self.potion.add(Potion((10,220)))
        self.potion.add(Potion((1214,452)))
        self.potion.add(Potion((1900,310)))

        # Recria herói
        self.hero.add(Hero((170, 250), faceRight=True))

        vida_rect = (0, 0, 12, 12)
        self.hud = HUD(self.hero.sprite, hud_path + "vida_icon.png",vida_rect,contorno_path = hud_path + "vida_hud.png")

        # Recria loja e pergunta para garantir estado inicial
        dicas_estatisticas = [
            {
                "conceito": "Média", 
                "descricao": "A soma dos valores dividida pelo total.", 
                "descricao_completa": "A média é uma medida de tendência central que representa o valor típico de um conjunto de dados...",
                "preco": 2,
                "feedback": "A média resume todos os valores em um único número representativo."
            }
        ]
        self.loja = LojaSimples(self.hero.sprite, self.displaySurface, self.npcloja.sprite, dicas_estatisticas, pos=(100, 50))
        self.pergunta = PerguntaResposta(
            displaySurface=self.displaySurface,
            hero=self.hero.sprite,
            npc=self.npcrobot.sprite,
            pergunta="Então, como eu posso ajustar os valores em uma única medida representativa?",
            loja=self.loja,
            correta_conceito="Média",
            pos=(100, 100)
        )

        # Recria zona de teleporte
        self.teleport_zone = pygame.Rect(
            self.npcrobot.sprite.hitbox.rect.x - 50,
            self.npcrobot.sprite.hitbox.rect.y - 100,
            self.npcrobot.sprite.hitbox.rect.width + 100,
            self.npcrobot.sprite.hitbox.rect.height + 100
        )

        # Reseta flags
        self.ja_teletransportou = False
        self.pergunta.acertou = None
        self.pergunta.errou = None

    def update(self, confirm_exit=False):
    # Atualiza o herói sempre

        if not confirm_exit:
                self.hero.update(self)


            

        if self.pergunta.acertou and self.portal.sprite is None:
                 self.quest_system.complete_quest(3)
                 self.portal.add(Portal((0,170)))
            
        if self.npcloja.sprite.show_interaction:
                self.quest_system.complete_quest(2)
                self.hero.sprite.falou_com_npcloja = False    


        if self.hero.sprite.falou_com_npc:
                self.quest_system.complete_quest(1)
                self.hero.sprite.falou_com_npc = False

        keys = pygame.key.get_pressed()
        if self.portal.sprite is not None:
                self.portal.update()
                if self.hero.sprite.rect.colliderect(self.portal.sprite.rect):
                    if keys[pygame.K_h]:
                        print("Portal ativado!")
                        self.verificar_prox_fase = "next_level"

        if (self.dialogue_box and not self.dialogue_box.text_active and
                self.loja and not self.loja.active and not self.loja.mostrar_compradas):

                self.pergunta.handle_input()

                self.robot.update(self)
                self.Coin.update()
                self.potion.update()

                
            # Atualiza NPCs e loja sempre, se existirem
        if self.npcrobot.sprite:
                self.npcrobot.update(self)
        if self.npcloja.sprite:
                self.npcloja.update(self)
            
        self.camera.update(self.hero.sprite)
        self.phase_text.update()
        self.dialogue_box.update()
        self.loja.handle_input()

            # Teleporte quando errou
        if self.pergunta.errou and not self.ja_teletransportou:
                self.hero.sprite.teleport(0, 250)
                # Adiciona inimigos adicionais
                self.robot.add(Robot((800, 160), moveRight=True, limit_left=800, limit_right=1000))
                self.robot.add(Robot((900, 400), moveRight=True, limit_left=900, limit_right=1000))
                self.ja_teletransportou = True
                # Reseta o erro para não teletransportar várias vezes
                self.pergunta.errou = False


            # Resetar o teleporte caso ele saia da área
        if self.ja_teletransportou and not self.hero.sprite.hitbox.colliderect(self.teleport_zone):
                self.ja_teletransportou = False
                                   
    def draw(self):
                # Desenha o fundo         
            self.background.draw2(self.displaySurface)
            self.quest_system.draw()

            # Desenha as camadas com o deslocamento da câmera
            for tile in self.platformTiles:
                pos = self.camera.apply(tile)
                self.displaySurface.blit(tile.image, pos)
        

        # for r in self.hero.sprite.debug_platform_rects:
                # r é relativo ao herói
            #    rect_on_screen = r.copy()
            #   rect_on_screen.topleft = (r.x - self.hero.sprite.rect.x + self.camera.apply(self.hero.sprite).x,
            #                     r.y - self.hero.sprite.rect.y + self.camera.apply(self.hero.sprite).y)
            #  pygame.draw.rect(self.displaySurface, (255, 0, 0), rect_on_screen, 2)

            
            for tile in self.othersprites:
                pos = self.camera.apply(tile)
                self.displaySurface.blit(tile.image, pos)


            for tile in self.paredesprites:
                pos = self.camera.apply(tile)
                self.displaySurface.blit(tile.image, pos)
                pygame.draw.rect(
                self.displaySurface, (255, 255, 0),
                tile.rect.move(pos.left - tile.rect.left, pos.top - tile.rect.top), 1
                )

            
            for coin in self.Coin:
                pos = self.camera.apply(coin)
                self.displaySurface.blit(coin.image, pos)
        
        
            for potion in self.potion:
                pos = self.camera.apply(potion)
                self.displaySurface.blit(potion.image, pos)

            # Desenha o herói com o deslocamento da câmera
            pos = self.camera.apply(self.hero.sprite)
            self.displaySurface.blit(self.hero.sprite.image, pos)

           
            # Portal

            if self.portal.sprite is not None:
                pos = self.camera.apply(self.portal.sprite)
                self.displaySurface.blit(self.portal.sprite.image, pos)
                self.portal.sprite.draw(self.displaySurface, self.camera)

        
            # Desenha os robôs com seus rects
            for robot in self.robot:
                pos = self.camera.apply(robot)
                self.displaySurface.blit(robot.image, pos)
            
        
            pos = self.camera.apply(self.npcrobot.sprite)
            self.displaySurface.blit(self.npcrobot.sprite.image, pos)
            self.npcrobot.sprite.draw(self.displaySurface, self.camera)

            
         
            pos1 = self.camera.apply(self.npcloja.sprite)
            self.displaySurface.blit(self.npcloja.sprite.image, pos1)
            self.npcloja.sprite.draw(self.displaySurface, self.camera)
                

            hitbox_rect = self.npcloja.sprite.hitbox.rect.copy()
            hitbox_rect.topleft = (hitbox_rect.left + (pos1.left - self.npcloja.sprite.rect.left),
                                    hitbox_rect.top + (pos1.top - self.npcloja.sprite.rect.top))

                #pygame.draw.rect(self.displaySurface, (255, 0, 0), hitbox_rect, 2)
                
            
            # HUD e texto da fase
            self.hud.draw(self.displaySurface)
            self.phase_text.draw()

            
            self.dialogue_box.draw_box()
            self.dialogue_box.draw_text()

            




            #rect_on_screen = self.teleport_zone.copy()
            #rect_on_screen.topleft = (self.teleport_zone.x - self.hero.sprite.rect.x + self.camera.apply(self.hero.sprite).x,
            #                           self.teleport_zone.y - self.hero.sprite.rect.y + self.camera.apply(self.hero.sprite).y)
            #pygame.draw.rect(self.displaySurface, (255, 0, 0), rect_on_screen, 2)
            

            

            self.loja.draw()
            


            self.pergunta.draw()    
            
    def run(self, confirm_exit=False):
        # Atualiza a lógica do jogo
        self.update(confirm_exit=confirm_exit)
        # Desenha a tela
        self.draw()

 

class Level3():
    def __init__(self, displaySurface, fase_id=3):
       
        
        self.displaySurface = displaySurface
        
        self.fase_id = fase_id

        self.font = pygame.font.Font(font_path, 40)
        self.phase_text = AnimatedText("Fase 1: O Despertar do Herói", self.font, (255, 255, 255), surface=self.displaySurface)

         # Carregar o arquivo TMX

        self.levelData = load_pygame(LEVELS_PATH + "Level1/level_embedded..tmx")

        # Instanciar classes
        self.background = Background()

        # Criar grupos de sprites
        self.hero = pygame.sprite.GroupSingle()
        self.bees = pygame.sprite.Group()
        self.platformTiles = pygame.sprite.Group()
        self.othersprites = pygame.sprite.Group()
        self.othersprites1 = pygame.sprite.Group()
        self.othersprites2 = pygame.sprite.Group()
        self.othersprites3 = pygame.sprite.Group()

        layer = self.levelData.get_layer_by_name('Platforms')
        for x, y, tileSurface in layer.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.platformTiles.add(tile)
        
        other = self.levelData.get_layer_by_name('Background4')
        for x, y, tileSurface in other.tiles():
             tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
             self.othersprites.add(tile)


        other1 = self.levelData.get_layer_by_name('Background3')
        for x, y, tileSurface in other1.tiles():
             tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
             self.othersprites.add(tile)
        
        other2 = self.levelData.get_layer_by_name('Background2')
        for x, y, tileSurface in other2.tiles():
             tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
             self.othersprites.add(tile)
        
        other3 = self.levelData.get_layer_by_name('Background1')
        for x, y, tileSurface in other3.tiles():
             tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
             self.othersprites.add(tile)
        
        
        self.hero.add(Hero((0, 250), faceRight=True))
        self.bees.add(Bee((45, 464), moveRight=True))
        self.bees.add(Bee((300, 380), moveRight=False))

        vida_rect = (0, 0, 12, 12)
        self.hud = HUD(self.hero.sprite, hud_path + "vida_icon.png",vida_rect,contorno_path = hud_path + "vida_hud.png")

        # Configura a câmera
        self.camera = Camera(self.levelData.width * TILESIZE, self.levelData.height * TILESIZE)

        
        

    def reset(self):
        # Limpa todos os grupos de sprites
        self.hero.empty()
        self.bees.empty()
        self.platformTiles.empty()
        self.othersprites.empty()
        self.othersprites1.empty()
        self.othersprites2.empty()
        self.othersprites3.empty()


        self.phase_text = AnimatedText("Fase 1: O Despertar do Herói", self.font, (255, 255, 255), self.displaySurface)

        # Recarrega mapa e plataformas
        self.levelData = load_pygame(LEVELS_PATH + "Level1/level_embedded..tmx")

        layer = self.levelData.get_layer_by_name('Platforms')
        for x, y, tileSurface in layer.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.platformTiles.add(tile)
        
        other = self.levelData.get_layer_by_name('Background4')
        for x, y, tileSurface in other.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.othersprites.add(tile)

        other1 = self.levelData.get_layer_by_name('Background3')
        for x, y, tileSurface in other1.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.othersprites1.add(tile)
   
        other2 = self.levelData.get_layer_by_name('Background2')
        for x, y, tileSurface in other2.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.othersprites2.add(tile)

        other3 = self.levelData.get_layer_by_name('Background1')
        for x, y, tileSurface in other3.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.othersprites3.add(tile)

        # Recria herói e inimigos
        self.hero.add(Hero((0, 250), faceRight=True))
        self.bees.add(Bee((45, 464), moveRight=True))
        self.bees.add(Bee((300, 380), moveRight=False))

        self.hud.reset(self.hero.sprite)

        # Reinicia a câmera
        self.camera = Camera(self.levelData.width * TILESIZE, self.levelData.height * TILESIZE)

    def update(self):
        self.hero.update(self)
        self.bees.update(self)
        self.camera.update(self.hero.sprite)  # Atualiza a câmera com a posição do herói
        self.phase_text.update()



    def draw(self):
        # Desenha o fundo
        self.background.draw(self.displaySurface)

        # Desenha as camadas com o deslocamento da câmera
        for sprite in self.othersprites:
            self.displaySurface.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.othersprites1:
            self.displaySurface.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.othersprites2:
            self.displaySurface.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.othersprites3:
            self.displaySurface.blit(sprite.image, self.camera.apply(sprite))

        for tile in self.platformTiles:
            self.displaySurface.blit(tile.image, self.camera.apply(tile))

        # Desenha o herói  com o deslocamento da câmera
        self.displaySurface.blit(self.hero.sprite.image, self.camera.apply(self.hero.sprite))
       
        # Desenha as abelhas com o deslocamento da câmera

        for bee in self.bees:
            self.displaySurface.blit(bee.image, self.camera.apply(bee))

        
        self.hud.draw(self.displaySurface)
        self.phase_text.draw()

       
    def run(self):
        self.update()
        self.draw()


class Level4():
    def __init__(self, displaySurface, fase_id=4):
       
        
        self.displaySurface = displaySurface
        
        self.fase_id = fase_id

        self.font = pygame.font.Font(font_path, 40)
        self.phase_text = AnimatedText("Fase 2: Descobrimento de um novo mundo", self.font, (255, 255, 255), surface=self.displaySurface)

         # Carregar o arquivo TMX

        self.levelData = load_pygame(LEVELS_PATH + "Level1/level2.tmx")

        # Instanciar classes
        self.background = Background()

        # Criar grupos de sprites
        self.hero = pygame.sprite.GroupSingle()
        self.platformTiles = pygame.sprite.Group()
        self.othersprites = pygame.sprite.Group()
        self.bees = pygame.sprite.Group()
        self.robot = pygame.sprite.Group()

        layer = self.levelData.get_layer_by_name('Platforms')
        for x, y, tileSurface in layer.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.platformTiles.add(tile)
        
        other = self.levelData.get_layer_by_name('Background')
        for x, y, tileSurface in other.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.othersprites.add(tile)
        
        self.robot.add(Robot((310, 225), moveRight=True,limit_left= 310, limit_right= 550))

        self.robot.add(Robot((550, 400), moveRight=True,limit_left= 480, limit_right= 570))

        self.robot.add(Robot((600, 465), moveRight=True,limit_left= 580, limit_right= 770))

        self.robot.add(Robot((500, 225), moveRight=True,limit_left= 310, limit_right= 550))

        self.robot.add(Robot((800, 160), moveRight=True,limit_left= 800, limit_right= 1000))

        self.robot.add(Robot((900, 400), moveRight=True,limit_left= 900, limit_right= 1000))
        
        
        self.hero.add(Hero((0, 250), faceRight=True))
       
        vida_rect = (0, 0, 12, 12)
        self.hud = HUD(self.hero.sprite, hud_path + "vida_icon.png",vida_rect,contorno_path = hud_path + "vida_hud.png")

        # Configura a câmera
        self.camera = Camera(self.levelData.width * TILESIZE, self.levelData.height * TILESIZE)

        
        

    def reset(self):
        # Limpa todos os grupos de sprites
        self.hero.empty()
      
        self.platformTiles.empty()
        
        self.phase_text = AnimatedText("Fase 2: Descobrimento de um novo mundo", self.font, (255, 255, 255), self.displaySurface)

        # Recarrega mapa e plataformas
        self.levelData = load_pygame(LEVELS_PATH + "Level1/level2.tmx")

        layer = self.levelData.get_layer_by_name('Platforms')
        for x, y, tileSurface in layer.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.platformTiles.add(tile)
  
        
        other = self.levelData.get_layer_by_name('Background')
        for x, y, tileSurface in other.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.othersprites.add(tile) 


        # Recria herói e inimigos
        self.hero.add(Hero((0, 250), faceRight=True))
       

        self.hud.reset(self.hero.sprite)

        # Reinicia a câmera
        self.camera = Camera(self.levelData.width * TILESIZE, self.levelData.height * TILESIZE)

    def update(self):
        self.hero.update(self)
        self.robot.update(self)
        self.camera.update(self.hero.sprite)  # Atualiza a câmera com a posição do herói
        self.phase_text.update()

    def draw(self):
        # Desenha o fundo
        self.background.draw2(self.displaySurface)

        # Desenha as camadas com o deslocamento da câmera

        for tile in self.platformTiles:
            self.displaySurface.blit(tile.image, self.camera.apply(tile))

        for tile in self.othersprites:
            self.displaySurface.blit(tile.image, self.camera.apply(tile))

        # Desenha o herói  com o deslocamento da câmera
        self.displaySurface.blit(self.hero.sprite.image, self.camera.apply(self.hero.sprite))

        for robot in self.robot:
            self.displaySurface.blit(robot.image, self.camera.apply(robot))       

        
        self.hud.draw(self.displaySurface)
        self.phase_text.draw()

       
    def run(self):
        self.update()
        self.draw()
