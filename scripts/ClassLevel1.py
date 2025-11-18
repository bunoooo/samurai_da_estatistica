import pygame
from pytmx.util_pygame import load_pygame , pytmx
from scripts.Config import *
from scripts.ClassHero import Hero
from scripts.ClassBee import Bee
from scripts.ClassTile import Tile
from scripts.ClassBackground import Background
from scripts.camera import *
from scripts.HUD import HUD
from scripts.AnimatedText import *
from scripts.ClassRobot import *
from scripts.Coin import *
from scripts.Potion import *
from scripts.ClassNpcRobot import *
from scripts.Classtext import *
from scripts.classfasestext import *
from scripts.ClassLoja import *
from scripts.ClassLojalevel import *
from scripts.ClassQuestSystem import *
from scripts.ClassPerguntaResposta1 import *
from scripts.cutscene import *
from scripts.portal import *
from scripts.Skeleton import *
from scripts.Crownpc import *
from scripts.Reapernpc import *
from scripts.Zombie import *
from scripts.PerguntaGrafico import *
from scripts.Erradon import *
from scripts.Samuraixadom import *
from scripts.SamuraigirlNpc import *
from scripts.cutscene_final import *



repositorio = Dialogos()




class Tutorial():
    def __init__(self, displaySurface, fase_id=0):
        self.displaySurface = displaySurface
        self.fase_id = fase_id
        self.ja_teletransportou = False
        self.verificar_prox_fase = None

        self.background = Background()

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
        self.skeleton = pygame.sprite.Group()
        self.crow = pygame.sprite.GroupSingle()
        self.reaper = pygame.sprite.GroupSingle()
        self.zombie =  pygame.sprite.Group()
        self.erradon = pygame.sprite.GroupSingle()
        self.samuraixamom = pygame.sprite.Group()
        self.samuraigirl = pygame.sprite.GroupSingle()
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
        dicas_estatisticas = [
            {
                "conceito": "Conceito exemplo",
                "descricao": "Descrição parcial do conceito",
                "descricao_completa": "Aqui é possível visualizar a descrição completa do conceito estatístico",
                "feedback" : "Uhuuul você acertou! quando você acertar a pergunta, automaticamente ganhará um fragmento do tempo, liberando o portal para a próxima fase",
                "preco": 1
            },
        ]
        self.loja = LojaSimples(self.hero.sprite, self.displaySurface, self.npcloja.sprite, dicas_estatisticas, pos=(100, 50))

        # Pergunta baseada em conceito da loja
        self.pergunta = PerguntaResposta1(
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
          
        self.camera.update(self.hero.sprite)
        
        self.phase_text.update()
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
      
        self.background.draw1(self.displaySurface)

        # Tiles
        for tile in self.othersprites:
            pos = self.camera.apply(tile)
            self.displaySurface.blit(tile.image, pos)
       
       
        for tile in self.othersprites2:
            pos = self.camera.apply(tile)
            self.displaySurface.blit(tile.image, pos)
       
        for tile in self.platformTiles:
            pos = self.camera.apply(tile)
            self.displaySurface.blit(tile.image, pos)
           

        # Portal
        if self.portal.sprite is not None:
            pos = self.camera.apply(self.portal.sprite)
            self.displaySurface.blit(self.portal.sprite.image, pos)
            self.portal.sprite.draw(self.displaySurface, self.camera)

        # Herói e NPCs
        pos = self.camera.apply(self.hero.sprite)
        self.displaySurface.blit(self.hero.sprite.image, pos)
        
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
        self.cutscene = Cutscene(self.displaySurface, font_path, multi_stage=True)

        dicas_estatisticas = [
    {
        "conceito": "Média", 
        "descricao": "A soma dos valores dividida pelo total.", 
        "descricao_completa": "A média é uma medida de tendência central que representa o valor típico de um conjunto de dados. Ela é calculada somando todos os valores do conjunto e dividindo pelo número total de observações. É útil para entender o comportamento geral dos dados, mas pode ser sensível a valores extremos.",
        "preco": 2,
        "feedback": "A média pode ser distorcida por valores muito altos ou muito baixos, o que pode não refletir bem o consumo da maioria das famílias."
    },
    {
        "conceito": "Mediana", 
        "descricao": "O valor central de um conjunto ordenado.", 
        "descricao_completa": "A mediana é uma medida de tendência central que indica o valor que separa a metade superior da metade inferior dos dados. Ao contrário da média, a mediana não é influenciada por valores muito altos ou muito baixos, tornando-se útil para conjuntos de dados assimétricos.",
        "preco": 2,
        "feedback": "Esta medida considera a posição dos valores, ajudando a entender qual é o consumo típico sem que os extremos influenciem o resultado."
    },
    {
        "conceito": "Moda", 
        "descricao": "O valor que mais se repete.", 
        "descricao_completa": "A moda é a medida de tendência central que representa o valor mais frequente em um conjunto de dados. Pode haver mais de uma moda, e é particularmente útil para dados categóricos ou quando se deseja identificar padrões de repetição.",
        "preco": 3,
        "feedback": "A moda mostra apenas o valor que mais se repete, ignorando a distribuição completa dos dados e podendo não representar o consumo da maioria."
    },
    {
        "conceito": "Desvio Padrão", 
        "descricao": "Mede o quanto os valores se afastam da média.", 
        "descricao_completa": "O desvio padrão é uma medida de dispersão que indica o quanto os valores de um conjunto de dados se afastam da média. Quanto maior o desvio padrão, mais espalhados estão os dados; quanto menor, mais próximos da média eles se encontram.",
        "preco": 2,
        "feedback": "O desvio padrão indica variação e dispersão, mas não fornece um valor central representativo do consumo."
    },
    {
        "conceito": "Probabilidade", 
        "descricao": "Chance de um evento acontecer.", 
        "descricao_completa": "Probabilidade é a medida numérica da chance de ocorrência de um evento dentro de um conjunto de possibilidades. É um conceito fundamental em estatística e análise de risco, usado para modelar incertezas e tomar decisões baseadas em chances relativas.",
        "preco": 1,
        "feedback": "A probabilidade informa a chance de um evento ocorrer, mas não descreve um valor central de consumo."
    },
    {
    "conceito": "Coeficiente de Variação",
    "descricao": "Relação entre o desvio padrão e a média.",
    "descricao_completa": "O coeficiente de variação compara a dispersão dos dados com o valor médio, mostrando proporcionalmente o quanto os valores variam em relação à média. É útil para comparar variabilidade entre conjuntos de dados com escalas diferentes.",
    "preco": 3,
    "feedback": "O coeficiente de variação mostra a variação relativa aos valores médios, mas não indica o valor central do consumo."
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
        self.skeleton = pygame.sprite.Group()
        self.crow = pygame.sprite.GroupSingle()
        self.reaper = pygame.sprite.GroupSingle()
        self.zombie =  pygame.sprite.Group()
        self.erradon = pygame.sprite.GroupSingle()
        self.samuraixamom = pygame.sprite.Group()
        self.samuraigirl = pygame.sprite.GroupSingle()
      

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
  
        self.pergunta = PerguntaResposta1(
            displaySurface=self.displaySurface,
            hero=self.hero.sprite,
            npc=self.npcrobot.sprite,
            pergunta="Samurai, qual seria o conhecimento da arte dos dados mais indicado para o meu problema?",
            loja=self.loja,
            correta_conceito="Mediana",
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
        "descricao_completa": "A média é uma medida de tendência central que representa o valor típico de um conjunto de dados. Ela é calculada somando todos os valores do conjunto e dividindo pelo número total de observações. É útil para entender o comportamento geral dos dados, mas pode ser sensível a valores extremos.",
        "preco": 2,
        "feedback": "A média pode ser distorcida por valores muito altos ou muito baixos, o que pode não refletir bem o consumo da maioria das famílias."
    },
    {
        "conceito": "Mediana", 
        "descricao": "O valor central de um conjunto ordenado.", 
        "descricao_completa": "A mediana é uma medida de tendência central que indica o valor que separa a metade superior da metade inferior dos dados. Ao contrário da média, a mediana não é influenciada por valores muito altos ou muito baixos, tornando-se útil para conjuntos de dados assimétricos.",
        "preco": 2,
        "feedback": "Esta medida considera a posição dos valores, ajudando a entender qual é o consumo típico sem que os extremos influenciem o resultado."
    },
    {
        "conceito": "Moda", 
        "descricao": "O valor que mais se repete.", 
        "descricao_completa": "A moda é a medida de tendência central que representa o valor mais frequente em um conjunto de dados. Pode haver mais de uma moda, e é particularmente útil para dados categóricos ou quando se deseja identificar padrões de repetição.",
        "preco": 3,
        "feedback": "A moda mostra apenas o valor que mais se repete, ignorando a distribuição completa dos dados e podendo não representar o consumo da maioria."
    },
    {
        "conceito": "Desvio Padrão", 
        "descricao": "Mede o quanto os valores se afastam da média.", 
        "descricao_completa": "O desvio padrão é uma medida de dispersão que indica o quanto os valores de um conjunto de dados se afastam da média. Quanto maior o desvio padrão, mais espalhados estão os dados; quanto menor, mais próximos da média eles se encontram.",
        "preco": 2,
        "feedback": "O desvio padrão indica variação e dispersão, mas não fornece um valor central representativo do consumo."
    },
    {
        "conceito": "Probabilidade", 
        "descricao": "Chance de um evento acontecer.", 
        "descricao_completa": "Probabilidade é a medida numérica da chance de ocorrência de um evento dentro de um conjunto de possibilidades. É um conceito fundamental em estatística e análise de risco, usado para modelar incertezas e tomar decisões baseadas em chances relativas.",
        "preco": 1,
        "feedback": "A probabilidade informa a chance de um evento ocorrer, mas não descreve um valor central de consumo."
    },
    {
    "conceito": "Coeficiente de Variação",
    "descricao": "Relação entre o desvio padrão e a média.",
    "descricao_completa": "O coeficiente de variação compara a dispersão dos dados com o valor médio, mostrando proporcionalmente o quanto os valores variam em relação à média. É útil para comparar variabilidade entre conjuntos de dados com escalas diferentes.",
    "preco": 3,
    "feedback": "O coeficiente de variação mostra a variação relativa aos valores médios, mas não indica o valor central do consumo."
}
]
  
        self.loja = LojaSimples(self.hero.sprite, self.displaySurface, self.npcloja.sprite, dicas_estatisticas, pos=(100, 50))
        self.pergunta = PerguntaResposta1(
            displaySurface=self.displaySurface,
            hero=self.hero.sprite,
            npc=self.npcrobot.sprite,
            pergunta="Samurai, qual seria o conhecimento da arte dos dados mais indicado para o meu problema?",
            loja=self.loja,
            correta_conceito="Mediana",
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

        self.cutscene_active = True
        self.cutscene = Cutscene(self.displaySurface, font_path , multi_stage=False)
       

        self.font = pygame.font.Font(font_path, 40)
        self.phase_text = AnimatedText("Fase 2: Cidade Vermelha", self.font, (255, 255, 255), surface=self.displaySurface)

        dicas_estatisticas = [
    {
        "conceito": "Poção de Vitalis",
        "descricao": "Rápido e popular, resultados confiáveis.",
        "descricao_completa": (
            "Aplicação rápida, média de cura 55 porcento. Intervalo de confiança: 50 porcento - 60 porcento. Resultados previsíveis e consistentes, apesar da taxa moderada. Escolha estratégica para quem prioriza segurança e rapidez."
        ),
        "preco": 2,
        "feedback": (
            "Mesmo com média menor, o intervalo estreito garante previsibilidade. "
            "A dispersão relativa é baixa, então os resultados são mais confiáveis."
        )
    },
    {
        "conceito": "Elixir de Erradon",
        "descricao": "Novo método, média mais alta, mas incerto.",
        "descricao_completa": (
            "Desenvolvido recentemente, média de cura 60 porcento. Intervalo de confiança: 40 porcento - 80 porcento. Alta incerteza nos resultados. Pode ser arriscado, mesmo com média maior. Exige avaliação cuidadosa antes de aplicação em larga escala."
        ),
        "preco": 3,
        "feedback": (
            "A média é maior, mas o intervalo largo mostra grande incerteza. "
            "A dispersão relativa é alta, o que significa que os resultados podem variar muito de caso a caso."
        )
    },
    {
        "conceito": "Soro da Fortaleza",
        "descricao": "Método sólido, ligeiramente mais lento, confiável.",
        "descricao_completa": (
            "Usado em epidemias passadas, média de cura 58 porcento. Intervalo de confiança: 55 porcento - 61 porcento. Levemente menor que Elixir de Erradon, mas muito mais previsível."
        ),
        "preco": 3,
        "feedback": (
            "Média razoável com intervalo estreito demonstra alta confiabilidade. "
            "A dispersão relativa é baixa, tornando esta escolha mais segura apesar da média ligeiramente menor."
        )
    },
    {
        "conceito": "Infusão Tradicional",
        "descricao": "Práticas naturais, pouco eficazes e instáveis.",
        "descricao_completa": (
            "Baseado em receitas tradicionais, média de cura 30 porcento. Intervalo de confiança: 20 porcento - 40 porcento. Alta chance de falha e baixa previsibilidade. Não recomendado para controlar a epidemia."
        ),
        "preco": 1,
        "feedback": (
            "Baixa média e intervalo largo indicam resultados pouco confiáveis. "
            "A dispersão relativa é alta, tornando a eficácia deste tratamento imprevisível."
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

        self.levelData = load_pygame(LEVELS_PATH + "Level1/level2_ajustado.tmx")

        # Instanciar classes
        self.background = Background()

        # Criar grupos de sprites
        self.hero = pygame.sprite.GroupSingle()
        self.platformTiles = pygame.sprite.Group()
        self.othersprites = pygame.sprite.Group()
        self.other2sprites = pygame.sprite.Group()
        self.paredesprites = pygame.sprite.Group()
        self.bees = pygame.sprite.Group()
        self.robot = pygame.sprite.Group()
        self.Coin = pygame.sprite.Group()
        self.potion = pygame.sprite.Group()
        self.npcrobot = pygame.sprite.GroupSingle()
        self.npcloja = pygame.sprite.GroupSingle()
        self.portal = pygame.sprite.GroupSingle()
        self.skeleton = pygame.sprite.Group()
        self.crow = pygame.sprite.GroupSingle()
        self.reaper = pygame.sprite.GroupSingle()
        self.zombie = pygame.sprite.GroupSingle()
        self.erradon = pygame.sprite.GroupSingle()
        self.samuraixamom = pygame.sprite.Group()
        self.samuraigirl = pygame.sprite.GroupSingle()
      

        layer = self.levelData.get_layer_by_name('Platforms')
        for x, y, tileSurface in layer.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.platformTiles.add(tile)
        
        
        other = self.levelData.get_layer_by_name('Background')
        for x, y, tileSurface in other.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.othersprites.add(tile)

        other2 = self.levelData.get_layer_by_name('Background2')
        for x, y, tileSurface in  other2.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self. other2sprites.add(tile)

        parede = self.levelData.get_layer_by_name('Parede')
        for x, y, tileSurface in parede.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.paredesprites.add(tile)

        self.dialogue_box = AppearingTextBox(repositorio.dialogo_fase(fase_id), self.displaySurface)
    
       
        self.robot.add(Robot((300, 510), moveRight=True,limit_left= 40, limit_right= 450))
        

        self.robot.add(Robot((550, 365), moveRight=True,limit_left= 480, limit_right= 850))
        
        self.robot.add(Robot((600, 510), moveRight=True,limit_left= 700, limit_right= 850))

        self.robot.add(Robot((500, 160), moveRight=True,limit_left= 480, limit_right= 650))

        self.robot.add(Robot((800, 160), moveRight=True,limit_left= 700, limit_right= 950))
       
        self.robot.add(Robot((950, 445), moveRight=True,limit_left= 950, limit_right= 1150))

        self.robot.add(Robot((1610, 240), moveRight=True,limit_left= 1600, limit_right= 1790))

        self.robot.add(Robot((1670, 240), moveRight=True,limit_left= 1600, limit_right= 1890))


        self.npcrobot.add(RobotNpc((1705,510) , faceRight= False))

        self.npcloja.add(LojaNpc((100,132) , faceRight= True))
       
        self.Coin.add(Coin((200,105)))
        self.Coin.add(Coin((170,105)))
        self.Coin.add(Coin((20,320)))
        self.Coin.add(Coin((40,320)))
        self.Coin.add(Coin((540,300)))
        self.Coin.add(Coin((510,300)))
        self.Coin.add(Coin((705,140)))

        self.Coin.add(Coin((780,400)))
        self.Coin.add(Coin((810,400)))

        self.Coin.add(Coin((1840,130)))
        self.Coin.add(Coin((1810,130)))

        self.Coin.add(Coin((1840,400)))
        self.Coin.add(Coin((1810,400)))


        self.potion.add(Potion((195,385)))
        self.potion.add(Potion((1314,302)))
        self.potion.add(Potion((1900,340)))

                
        self.hero.add(Hero((185, 400), faceRight=True))
       

        self.loja = LojaSimples(self.hero.sprite, self.displaySurface, self.npcloja.sprite , dicas_estatisticas, pos=(100, 50))
  
        self.pergunta = PerguntaResposta1(
            displaySurface=self.displaySurface,
            hero=self.hero.sprite,
            npc=self.npcrobot.sprite,
            pergunta=(
                "Qual tratamento oferece a melhor chance de controlar a epidemia, considerando a taxa média de cura e a confiabilidade dos resultados (intervalo de confiança)?"
            ),
            loja=self.loja,
            correta_conceito="Soro da Fortaleza",
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

        other2 = self.levelData.get_layer_by_name('Background2')
        for x, y, tileSurface in other2.tiles():
            self.other2sprites.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))

        parede = self.levelData.get_layer_by_name('Parede')
        for x, y, tileSurface in parede.tiles():
            self.paredesprites.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))

        # Recria inimigos

        self.robot.add(Robot((300, 510), moveRight=True,limit_left= 40, limit_right= 450))
        

        self.robot.add(Robot((550, 365), moveRight=True,limit_left= 480, limit_right= 850))
        
        self.robot.add(Robot((600, 510), moveRight=True,limit_left= 700, limit_right= 850))

        self.robot.add(Robot((500, 160), moveRight=True,limit_left= 480, limit_right= 650))

        self.robot.add(Robot((800, 160), moveRight=True,limit_left= 700, limit_right= 950))
       
        self.robot.add(Robot((950, 445), moveRight=True,limit_left= 950, limit_right= 1150))

        self.robot.add(Robot((1610, 240), moveRight=True,limit_left= 1600, limit_right= 1790))

        self.robot.add(Robot((1670, 240), moveRight=True,limit_left= 1600, limit_right= 1890))


        self.npcrobot.add(RobotNpc((1705,510) , faceRight= False))

        self.npcloja.add(LojaNpc((100,132) , faceRight= True))
       
        self.Coin.add(Coin((200,105)))
        self.Coin.add(Coin((170,105)))
        self.Coin.add(Coin((20,320)))
        self.Coin.add(Coin((40,320)))
        self.Coin.add(Coin((540,300)))
        self.Coin.add(Coin((510,300)))
        self.Coin.add(Coin((705,140)))

        self.Coin.add(Coin((780,400)))
        self.Coin.add(Coin((810,400)))

        self.Coin.add(Coin((1840,130)))
        self.Coin.add(Coin((1810,130)))

        self.Coin.add(Coin((1840,400)))
        self.Coin.add(Coin((1810,400)))


        self.potion.add(Potion((195,385)))
        self.potion.add(Potion((1314,302)))
        self.potion.add(Potion((1900,340)))

                
        self.hero.add(Hero((185, 400), faceRight=True))


        vida_rect = (0, 0, 12, 12)
        self.hud = HUD(self.hero.sprite, hud_path + "vida_icon.png",vida_rect,contorno_path = hud_path + "vida_hud.png")

        dicas_estatisticas = [
        {
            "conceito": "Poção de Vitalis",
            "descricao": "Rápido e popular, resultados confiáveis.",
            "descricao_completa": (
                "Aplicação rápida, média de cura 55 porcento. Intervalo de confiança: 50 porcento - 60 porcento. Resultados previsíveis e consistentes, apesar da taxa moderada. Escolha estratégica para quem prioriza segurança e rapidez."
            ),
            "preco": 2,
            "feedback": (
                "Mesmo com média menor, o intervalo estreito garante previsibilidade. "
                "A dispersão relativa é baixa, então os resultados são mais confiáveis."
            )
        },
        {
            "conceito": "Elixir de Erradon",
            "descricao": "Novo método, média mais alta, mas incerto.",
            "descricao_completa": (
                "Desenvolvido recentemente, média de cura 60 porcento. Intervalo de confiança: 40 porcento - 80 porcento. Alta incerteza nos resultados. Pode ser arriscado, mesmo com média maior. Exige avaliação cuidadosa antes de aplicação em larga escala."
            ),
            "preco": 3,
            "feedback": (
                "A média é maior, mas o intervalo largo mostra grande incerteza. "
                "A dispersão relativa é alta, o que significa que os resultados podem variar muito de caso a caso."
            )
        },
        {
            "conceito": "Soro da Fortaleza",
            "descricao": "Método sólido, ligeiramente mais lento, confiável.",
            "descricao_completa": (
                "Usado em epidemias passadas, média de cura 58 porcento. Intervalo de confiança: 55 porcento - 61 porcento. Levemente menor que Elixir de Erradon, mas muito mais previsível."
            ),
            "preco": 3,
            "feedback": (
                "Média razoável com intervalo estreito demonstra alta confiabilidade. "
                "A dispersão relativa é baixa, tornando esta escolha mais segura apesar da média ligeiramente menor."
            )
        },
        {
            "conceito": "Infusão Tradicional",
            "descricao": "Práticas naturais, pouco eficazes e instáveis.",
            "descricao_completa": (
                "Baseado em receitas tradicionais, média de cura 30 porcento. Intervalo de confiança: 20 porcento - 40 porcento. Alta chance de falha e baixa previsibilidade. Não recomendado para controlar a epidemia."
            ),
            "preco": 1,
            "feedback": (
                "Baixa média e intervalo largo indicam resultados pouco confiáveis. "
                "A dispersão relativa é alta, tornando a eficácia deste tratamento imprevisível."
            )
        }
    ]


        quests = [
            {"id": 1, "text": "Fale com o chefe da vila", "done": False},
            {"id": 2, "text": "Encontre o mercador", "done": False},
            {"id": 3 , "text": "Resolva o problema do chefe" , "done" : False},
            {"id": 4 , "text": "Entre no portal" , "done" : False}
        ]
        
        self.loja = LojaSimples(self.hero.sprite, self.displaySurface, self.npcloja.sprite , dicas_estatisticas, pos=(100, 50))
        self.quest_system = QuestSystem(quests, self.displaySurface )


        self.pergunta = PerguntaResposta1(
            displaySurface=self.displaySurface,
            hero=self.hero.sprite,
            npc=self.npcrobot.sprite,
            pergunta=(
                "Qual tratamento oferece a melhor chance de controlar a epidemia, considerando a taxa média de cura e a confiabilidade dos resultados (intervalo de confiança)?"
            ),
            loja=self.loja,
            correta_conceito="Soro da Fortaleza",
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
                    self.portal.add(Portal((0,300)))
                
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
                    self.robot.add(Robot((800, 255), moveRight=True, limit_left=700, limit_right=900))
                    self.robot.add(Robot((900, 445), moveRight=True, limit_left=1000, limit_right=1100))
                    self.ja_teletransportou = True
                    # Reseta o erro para não teletransportar várias vezes
                    self.pergunta.errou = False


                # Resetar o teleporte caso ele saia da área
            if self.ja_teletransportou and not self.hero.sprite.hitbox.colliderect(self.teleport_zone):
                    self.ja_teletransportou = False
                                   
    def draw(self):
                # Desenha o fundo         
        if self.cutscene_active:
            self.cutscene.draw2()
        else:  


            self.background.draw3(self.displaySurface)
            

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

            for tile in self.other2sprites:
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

            
            self.quest_system.draw()



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

        self.ja_teletransportou = False
        self.verificar_prox_fase = None
        self.displaySurface = displaySurface
        self.fase_id = fase_id
        
        self.cutscene_active = True
        self.cutscene = Cutscene(self.displaySurface, font_path , multi_stage=False)
        

        self.font = pygame.font.Font(font_path, 40)
        self.phase_text = AnimatedText(
            "Fase 3: A volta dos mortos",
            self.font,
            (255, 255, 255),
            surface=self.displaySurface
        )
        dicas_estatisticas = [
    {
        "conceito": "Ritual de Purificação Violenta",
        "descricao": "Neutraliza a maldição sobre mortes violentas.",
        "descricao_completa": (
            "Este ritual é poderoso para almas perdidas em mortes violentas. Reduz drasticamente o efeito da maldição, permitindo que o ceifador colete a maioria das almas. Requer materiais raros e custa tempo para ser realizado, mas é altamente eficaz."
        ),
        "preco": 3,
        "feedback": (
            "Excelente escolha! A maioria das almas perdidas pela maldição foi recuperada."
        )
    },
    {
        "conceito": "Ritual de Proteção Acidental",
        "descricao": "Reduz os efeitos da maldição sobre acidentes.",
        "descricao_completa": (
            "Protege as almas que morrem em acidentes repentinos. Efetivo, mas não resolve casos de mortes violentas ou naturais."
        ),
        "preco": 3,
        "feedback": (
            "Você conseguiu proteger algumas almas de acidentes, mas essa não é a principal fonte de almas da maldição."
        )
    },
    {
        "conceito": "Ritual da Harmonia Natural",
        "descricao": "Reequilibra o fluxo de almas em mortes naturais.",
        "descricao_completa": (
            "Este ritual é voltado para almas de mortes naturais, restaurando o fluxo normal e permitindo coleta eficiente. Não afeta mortes violentas ou acidentes."
        ),
        "preco": 2,
        "feedback": (
            "As almas de mortes naturais agora podem ser coletadas, mas essa não é a principal fonte de almas da maldição."
        )
    },
    {
        "conceito": "Poção de Cura de Doença",
        "descricao": "Minimiza a maldição sobre mortes por doença.",
        "descricao_completa": (
            "Aplica efeitos mágicos para reduzir a maldição sobre almas que morreram por doença. Não influencia mortes violentas ou acidentais."
        ),
        "preco": 2,
        "feedback": (
            "As almas perdidas por doença podem ser coletadas,  mas essa não é a principal fonte de almas da maldição."
        )
    }
]
        quests = [
            {"id": 1, "text": "Fale com o ceifador do cemiterio", "done": False},
            {"id": 2, "text": "Encontre o mercador", "done": False},
            {"id": 3, "text": "Resolva o problema do ceifador", "done": False},
            {"id": 4, "text": "Entre no portal", "done": False}
        ]

        self.quest_system = QuestSystem(quests, self.displaySurface)

        # Carregar o arquivo TMX
        self.levelData = load_pygame(LEVELS_PATH + "Level1/level3.tmx")

        # Instanciar classes
        self.background = Background()

        # Criar grupos de sprites
        self.hero = pygame.sprite.GroupSingle()
        self.platformTiles = pygame.sprite.Group()
        self.othersprites = pygame.sprite.Group()
        self.other2sprites = pygame.sprite.Group()
        self.paredesprites = pygame.sprite.Group()
        self.bees = pygame.sprite.Group()
        self.robot = pygame.sprite.Group()
        self.Coin = pygame.sprite.Group()
        self.potion = pygame.sprite.Group()
        self.npcrobot = pygame.sprite.GroupSingle()
        self.npcloja = pygame.sprite.GroupSingle()
        self.portal = pygame.sprite.GroupSingle()
        self.skeleton = pygame.sprite.Group()
        self.crow = pygame.sprite.GroupSingle()
        self.reaper = pygame.sprite.GroupSingle()
        self.zombie =  pygame.sprite.Group()
        self.erradon = pygame.sprite.GroupSingle()
        self.samuraixamom = pygame.sprite.Group()
        self.samuraigirl = pygame.sprite.GroupSingle()

        # Carrega tiles
        for layer_name, group in [("Platforms", self.platformTiles),
                                  ("Background", self.othersprites),
                                  ("Background2", self.other2sprites),
                                  ("Parede", self.paredesprites)]:
            layer = self.levelData.get_layer_by_name(layer_name)
            for x, y, tileSurface in layer.tiles():
                group.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))

        # Dialogue box
        self.dialogue_box = AppearingTextBox(repositorio.dialogo_fase(fase_id), self.displaySurface)

        # Inimigos
        skeleton_positions = [
            (60,210,60,270), (350,495,40,450), (400,305,400,650), (300,495,650,900),
            (500,495,550,950), (200,495,50,550), (950,258,910,1100), (1250,210,1200,1400),
            (900,495,950,1400), (1100,495,1150,1400)
        ]
        for x, y, left, right in skeleton_positions:
            self.skeleton.add(Skeleton((x, y), moveRight=True, limit_left=left, limit_right=right))

        self.reaper.add(ReaperNpc((1855,505), faceRight=False))
        self.npcloja.add(LojaNpc((700,215), faceRight=True))

        # Moedas e poções
        for pos in [(120,115),(150,115),(80,370),(50,370),(540,200),(510,200),(1040,200),(1010,200),(1250,140),(1280,140)]:
            self.Coin.add(Coin(pos))
        for pos in [(1800,490),(1600,490),(225,385)]:
            self.potion.add(Potion(pos))

        # Hero
        self.hero.add(Hero((185, 400), faceRight=True))

        # Loja
        self.loja = LojaSimples(self.hero.sprite, self.displaySurface, self.npcloja.sprite, dicas_estatisticas, pos=(100, 50))

        # Pergunta nova
        self.pergunta = PerguntaGrafico(
            displaySurface=self.displaySurface,
            hero=self.hero.sprite,
            npc=self.reaper.sprite,
            pergunta="O gráfico mostra onde a maldição está mais forte, Qual ritual da loja vai me ajudar a coletar a maior quantidade de almas?",
            grafico_path = graficos_path + "almas_perdidas.png",
            loja=self.loja,
            correta_conceito = "Ritual de Purificação Violenta"
        )

        # HUD
        vida_rect = (0,0,12,12)
        self.hud = HUD(self.hero.sprite, hud_path + "vida_icon.png", vida_rect, contorno_path=hud_path + "vida_hud.png")

        # Câmera
        self.camera = Camera(self.levelData.width * TILESIZE, self.levelData.height * TILESIZE)

        # Teleporte
        self.teleport_zone = pygame.Rect(
            self.reaper.sprite.hitbox.rect.x - 50,
            self.reaper.sprite.hitbox.rect.y -100,
            self.reaper.sprite.hitbox.rect.width + 100,
            self.reaper.sprite.hitbox.rect.height + 100
        )

    # --- Função reset --- #
    def reset(self):
        # Limpa todos os grupos
        for group in [self.hero, self.platformTiles, self.paredesprites, self.othersprites, self.other2sprites,
                      self.bees, self.robot, self.Coin, self.potion, self.npcrobot, self.npcloja, self.portal]:
            group.empty()

        # Recarrega tiles
        for layer_name, group in [("Platforms", self.platformTiles),
                                  ("Background", self.othersprites),
                                  ("Background2", self.other2sprites),
                                  ("Parede", self.paredesprites)]:
            layer = self.levelData.get_layer_by_name(layer_name)
            for x, y, tileSurface in layer.tiles():
                group.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))

        # Recria inimigos
        skeleton_positions = [
            (60,210,60,270), (350,495,40,450), (400,305,400,650), (300,495,650,900),
            (500,495,550,950), (200,495,50,550), (950,258,910,1100), (1250,210,1200,1400),
            (900,495,950,1400), (1100,495,1150,1400)
        ]
        for x, y, left, right in skeleton_positions:
            self.skeleton.add(Skeleton((x, y), moveRight=True, limit_left=left, limit_right=right))

        self.reaper.add(ReaperNpc((1855,505), faceRight=False))
        self.npcloja.add(LojaNpc((700,215), faceRight=True))

        # Moedas e poções
        for pos in [(120,115),(150,115),(80,370),(50,370),(540,200),(510,200),(1040,200),(1010,200),(1250,140),(1280,140)]:
            self.Coin.add(Coin(pos))
        for pos in [(1800,490),(1600,490),(225,385)]:
            self.potion.add(Potion(pos))

        # Hero
        self.hero.add(Hero((170,250), faceRight=True))

        # HUD
        vida_rect = (0,0,12,12)
        self.hud = HUD(self.hero.sprite, hud_path + "vida_icon.png", vida_rect, contorno_path=hud_path + "vida_hud.png")

        # Loja e pergunta
        dicas_estatisticas = [d for d in self.loja.dicas]
        self.loja = LojaSimples(self.hero.sprite, self.displaySurface, self.npcloja.sprite, dicas_estatisticas, pos=(100,50))
        
        # Pergunta nova
        self.pergunta = PerguntaGrafico(
            displaySurface=self.displaySurface,
            hero=self.hero.sprite,
            npc=self.reaper.sprite,
            pergunta="O gráfico mostra onde a maldição está mais forte, Qual ritual da loja vai me ajudar a coletar a maior quantidade de almas?",
            grafico_path = graficos_path + "almas_perdidas.png",
            loja=self.loja,
            correta_conceito = "Ritual de Purificação Violenta"
        )
        # Teleporte
        self.teleport_zone = pygame.Rect(
            self.reaper.sprite.hitbox.rect.x - 50,
            self.reaper.sprite.hitbox.rect.y -100,
            self.reaper.sprite.hitbox.rect.width + 100,
            self.reaper.sprite.hitbox.rect.height + 100
        )

        self.ja_teletransportou = False
        self.pergunta.acertou = None
        self.pergunta.errou = None

    # --- Função update --- #
    def update(self, confirm_exit=False):
        if not confirm_exit:
            self.hero.update(self)
        if self.cutscene_active:
            if self.cutscene.finished:
                self.cutscene_active = False  # agora a fase 1 começa
            return
        else:

            # Pergunta acertada libera portal
            if self.pergunta.acertou and self.portal.sprite is None:
                self.quest_system.complete_quest(3)
                self.portal.add(Portal((0,450)))

            # Quest da loja
            if self.npcloja.sprite.show_interaction:
                self.quest_system.complete_quest(2)
                self.hero.sprite.falou_com_npcloja = False

            # Quest do NPC
            if self.hero.sprite.falou_com_npc:
                self.quest_system.complete_quest(1)
                self.hero.sprite.falou_com_npc = False

            # Portal
            keys = pygame.key.get_pressed()
            if self.portal.sprite is not None:
                self.portal.update()
                if self.hero.sprite.rect.colliderect(self.portal.sprite.rect):
                    if keys[pygame.K_h]:
                        print("Portal ativado!")
                        self.verificar_prox_fase = "next_level"

            # Atualiza lógica de jogo
            if self.dialogue_box and not self.dialogue_box.text_active and \
            self.loja and not self.loja.active and not self.loja.mostrar_compradas:
                self.pergunta.handle_input()
                self.robot.update(self)
                self.Coin.update()
                self.potion.update()
                self.skeleton.update(self)

            if self.reaper.sprite:
                self.reaper.update(self)
            if self.npcloja.sprite:
                self.npcloja.update(self)

            self.camera.update(self.hero.sprite)
            self.phase_text.update()
            self.dialogue_box.update()
            self.loja.handle_input()

            # Teleporte quando errou
            if self.pergunta.errou and not self.ja_teletransportou:
                self.hero.sprite.teleport(0, 250)
                self.skeleton.add(Skeleton((1250,210), moveRight=True,limit_left= 1200, limit_right= 1400))
                self.skeleton.add(Skeleton((900,495), moveRight=True,limit_left= 950, limit_right= 1400))
                self.skeleton.add(Skeleton((1100,495), moveRight=True,limit_left= 1150, limit_right= 1400))

                self.ja_teletransportou = True
                self.pergunta.errou = False

            # Resetar teleporte se sair da zona
            if self.ja_teletransportou and not self.hero.sprite.hitbox.colliderect(self.teleport_zone):
                self.ja_teletransportou = False

    # --- Função draw --- #
    def draw(self):

        if self.cutscene_active:
            self.cutscene.draw3()
        else:  

            self.background.draw4(self.displaySurface)

            for group in [self.platformTiles, self.othersprites, self.other2sprites, self.paredesprites]:
                for tile in group:
                    pos = self.camera.apply(tile)
                    self.displaySurface.blit(tile.image, pos)

            for coin in self.Coin:
                pos = self.camera.apply(coin)
                self.displaySurface.blit(coin.image, pos)

            for potion in self.potion:
                pos = self.camera.apply(potion)
                self.displaySurface.blit(potion.image, pos)

            # Herói
            pos = self.camera.apply(self.hero.sprite)
            self.displaySurface.blit(self.hero.sprite.image, pos)

            # Portal
            if self.portal.sprite is not None:
                pos = self.camera.apply(self.portal.sprite)
                self.displaySurface.blit(self.portal.sprite.image, pos)
                self.portal.sprite.draw(self.displaySurface, self.camera)

            # Robôs
            for robot in self.robot:
                pos = self.camera.apply(robot)
                self.displaySurface.blit(robot.image, pos)

            # Skeletons
            for skeleton in self.skeleton:
                pos = self.camera.apply(skeleton)
                self.displaySurface.blit(skeleton.image, pos)
                

            # Reaper NPC
            pos = self.camera.apply(self.reaper.sprite)
            self.displaySurface.blit(self.reaper.sprite.image, pos)
            self.reaper.sprite.draw(self.displaySurface, self.camera)

            # Loja NPC
            pos1 = self.camera.apply(self.npcloja.sprite)
            self.displaySurface.blit(self.npcloja.sprite.image, pos1)
            self.npcloja.sprite.draw(self.displaySurface, self.camera)

            # HUD e texto da fase
            self.hud.draw(self.displaySurface)
            self.phase_text.draw()

            self.dialogue_box.draw_box()
            self.dialogue_box.draw_text()

            self.quest_system.draw()
            self.loja.draw()
            self.pergunta.draw()

    # --- Função run --- #
    def run(self, confirm_exit=False):
        self.update(confirm_exit=confirm_exit)
        self.draw()

class Level4():
    def __init__(self, displaySurface, fase_id=3):
       
        self.ja_teletransportou = False

        self.verificar_prox_fase = None
        
        self.displaySurface = displaySurface
        
        self.fase_id = fase_id

        self.cutscene_active = True
        self.cutscene = Cutscene(self.displaySurface, font_path , multi_stage=False)
        

        self.font = pygame.font.Font(font_path, 40)
        self.phase_text = AnimatedText("Fase 4: Virus CognoZombi", self.font, (255, 255, 255), surface=self.displaySurface)
        
        dicas_estatisticas = [
    {
        "conceito": "Distrito Hélios",
        "descricao": "Primeiro distrito a apresentar aumento real.",
        "descricao_completa": "O Distrito Hélios é o único que começa a subir nos primeiros dias da epidemia. O início da curva aparece antes dos demais distritos. Isso indica que ele é o ponto mais provável de origem.",
        "preco": 3,
        "feedback": "Boa leitura do início da curva! Hélios é o primeiro distrito a apresentar crescimento."
    },
    {
        "conceito": "Distrito Nébula",
        "descricao": "Picos tardios e suspeitos.",
        "descricao_completa": "O Distrito Nébula permanece estável no início. Seu pico surge apenas mais tarde e parece manipulado. Picos tardios não indicam origem de uma epidemia.",
        "preco": 2,
        "feedback": "Nébula tem picos chamativos, mas acontece tarde demais para ser origem."
    },
    {
        "conceito": "Distrito Void",
        "descricao": "Crescimento leve e mais tardio.",
        "descricao_completa": "O Distrito Void apresenta aumento apenas depois que outros distritos já estavam crescendo. Crescimentos tardios não são típicos do ponto inicial de uma epidemia. Por isso, Void não indica origem.",
        "preco": 1,
        "feedback": "Void cresce tarde, então não é um bom candidato para origem."
    }
]

        quests = [
            {"id": 1, "text": "Fale com o dr da cidade", "done": False},
            {"id": 2, "text": "Encontre o mercador", "done": False},
            {"id": 3 , "text": "Resolva o problema do dr" , "done" : False},
            {"id": 4 , "text": "Entre no portal" , "done" : False}
        ]
        
        self.quest_system = QuestSystem(quests, self.displaySurface )
         # Carregar o arquivo TMX

        self.levelData = load_pygame(LEVELS_PATH + "Level1/level4.tmx")

        # Instanciar classes
        self.background = Background()

        # Criar grupos de sprites
        self.hero = pygame.sprite.GroupSingle()
        self.platformTiles = pygame.sprite.Group()
        self.othersprites = pygame.sprite.Group()
        self.other2sprites = pygame.sprite.Group()
        self.other3sprites = pygame.sprite.Group()
        self.paredesprites = pygame.sprite.Group()
        self.bees = pygame.sprite.Group()
        self.robot = pygame.sprite.Group()
        self.Coin = pygame.sprite.Group()
        self.potion = pygame.sprite.Group()
        self.npcrobot = pygame.sprite.GroupSingle()
        self.npcloja = pygame.sprite.GroupSingle()
        self.portal = pygame.sprite.GroupSingle()
        self.skeleton = pygame.sprite.Group()
        self.crow = pygame.sprite.GroupSingle()
        self.zombie =  pygame.sprite.Group()
        self.reaper = pygame.sprite.GroupSingle()
        self.erradon = pygame.sprite.GroupSingle()
        self.samuraixamom = pygame.sprite.Group()
        self.samuraigirl = pygame.sprite.GroupSingle()
      
        layer = self.levelData.get_layer_by_name('Platforms')
        for x, y, tileSurface in layer.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.platformTiles.add(tile)
        
        other = self.levelData.get_layer_by_name('Background')
        for x, y, tileSurface in other.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.othersprites.add(tile)

        other2 = self.levelData.get_layer_by_name('Background2')
        for x, y, tileSurface in  other2.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self. other2sprites.add(tile)

        other3 = self.levelData.get_layer_by_name('Predio')
        for x, y, tileSurface in  other3.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self. other3sprites.add(tile)

        
        parede = self.levelData.get_layer_by_name('Parede')
        for x, y, tileSurface in parede.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.paredesprites.add(tile)

        self.dialogue_box = AppearingTextBox(repositorio.dialogo_fase(fase_id), self.displaySurface)
       
        self.zombie.add(Zombie((120,305), moveRight=True,limit_left= 50, limit_right= 250))
        
        self.zombie.add(Zombie((100,305), moveRight=True,limit_left= 0, limit_right= 300))
     
        self.zombie.add(Zombie((900,260), moveRight=True,limit_left= 700, limit_right= 950))

        self.zombie.add(Zombie((700,450), moveRight=True,limit_left= 700, limit_right= 950))


        self.zombie.add(Zombie((1200,515), moveRight=True,limit_left= 1250, limit_right= 1400))
        
        self.zombie.add(Zombie((1200,405), moveRight=True,limit_left= 1150, limit_right= 1350))

        self.zombie.add(Zombie((1500,240), moveRight=True,limit_left= 1500, limit_right= 1700))
        
        self.zombie.add(Zombie((1600,435), moveRight=True,limit_left= 1600, limit_right= 1800))
        self.zombie.add(Zombie((1600,515), moveRight=True,limit_left= 1600, limit_right= 1850))
        
        

        self.crow.add(CrowNpc((100,515) , faceRight= False))

        self.npcloja.add(LojaNpc((1840,292) , faceRight= False))
       
        self.Coin.add(Coin((120,235)))
        self.Coin.add(Coin((150,235)))
        
        self.Coin.add(Coin((80,470)))
        self.Coin.add(Coin((50,470)))
        
        
        self.Coin.add(Coin((540,200)))
        self.Coin.add(Coin((510,200)))
        
        self.Coin.add(Coin((1040,200)))
        self.Coin.add(Coin((1010,200)))


        self.Coin.add(Coin((1250,140)))
        self.Coin.add(Coin((1280,140)))

        self.potion.add(Potion((1800,490)))

        self.potion.add(Potion((1600,490)))

        self.potion.add(Potion((370,315)))
    
        self.hero.add(Hero((185, 400), faceRight=True))
       

        self.loja = LojaSimples(self.hero.sprite, self.displaySurface, self.npcloja.sprite , dicas_estatisticas, pos=(100, 50))
  
        self.pergunta = PerguntaGrafico(
            displaySurface=self.displaySurface,
            hero=self.hero.sprite,
            npc=self.crow.sprite,
            pergunta="Jack, olhando os dados, qual distrito indica a origem da epidemia?",
            grafico_path = graficos_path + "grafico_zumbis.png",
            loja=self.loja,
            correta_conceito = "Distrito Hélios"
        )

       

        vida_rect = (0, 0, 12, 12)
        self.hud = HUD(self.hero.sprite, hud_path + "vida_icon.png",vida_rect,contorno_path = hud_path + "vida_hud.png")

        # Configura a câmera
        self.camera = Camera(self.levelData.width * TILESIZE, self.levelData.height * TILESIZE)

        

        self.teleport_zone = pygame.Rect(
        self.crow.sprite.hitbox.rect.x - 50,   # aumenta para esquerda
        self.crow.sprite.hitbox.rect.y -100,   # aumenta para cima
        self.crow.sprite.hitbox.rect.width + 100,  # aumenta largura
        self.crow.sprite.hitbox.rect.height + 100  # aumenta altura
    )
    def reset(self):
        # Limpa todos os grupos de sprites
        self.hero.empty()
        self.platformTiles.empty()
        self.paredesprites.empty()
        self.othersprites.empty()
        self.other2sprites.empty()
        self.other3sprites.empty()
        self.zombie.empty()
        self.crow.empty()
        self.npcloja.empty()
        self.portal.empty()
        self.Coin.empty()
        self.potion.empty()
        self.robot.empty()

        # Recarrega camadas do mapa
        layer = self.levelData.get_layer_by_name('Platforms')
        for x, y, tileSurface in layer.tiles():
            self.platformTiles.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))
        
        other = self.levelData.get_layer_by_name('Background')
        for x, y, tileSurface in other.tiles():
            self.othersprites.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))

        other2 = self.levelData.get_layer_by_name('Background2')
        for x, y, tileSurface in other2.tiles():
            self.other2sprites.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))

        other3 = self.levelData.get_layer_by_name('Predio')
        for x, y, tileSurface in other3.tiles():
            self.other3sprites.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))

        parede = self.levelData.get_layer_by_name('Parede')
        for x, y, tileSurface in parede.tiles():
            self.paredesprites.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))

        # Recria inimigos (zumbis)
        self.zombie.add(Zombie((120,305), moveRight=True, limit_left=50, limit_right=250))
        self.zombie.add(Zombie((100,305), moveRight=True, limit_left=0, limit_right=300))
        self.zombie.add(Zombie((900,260), moveRight=True, limit_left=700, limit_right=950))
        self.zombie.add(Zombie((700,450), moveRight=True, limit_left=700, limit_right=950))
        self.zombie.add(Zombie((1200,515), moveRight=True, limit_left=1250, limit_right=1400))
        self.zombie.add(Zombie((1200,405), moveRight=True, limit_left=1150, limit_right=1350))
        self.zombie.add(Zombie((1500,240), moveRight=True, limit_left=1500, limit_right=1700))
        self.zombie.add(Zombie((1600,435), moveRight=True, limit_left=1600, limit_right=1800))
        self.zombie.add(Zombie((1600,515), moveRight=True, limit_left=1600, limit_right=1850))

        # Recria NPCs
        self.crow.add(CrowNpc((100,515), faceRight=False))
        self.npcloja.add(LojaNpc((1840,292), faceRight=False))

        # Recria moedas e poções
        self.Coin.add(Coin((120,235))); self.Coin.add(Coin((150,235)))
        self.Coin.add(Coin((80,470))); self.Coin.add(Coin((50,470)))
        self.Coin.add(Coin((540,200))); self.Coin.add(Coin((510,200)))
        self.Coin.add(Coin((1040,200))); self.Coin.add(Coin((1010,200)))
        self.Coin.add(Coin((1250,140))); self.Coin.add(Coin((1280,140)))

        self.potion.add(Potion((1800,490)))
        self.potion.add(Potion((1600,490)))
        self.potion.add(Potion((370,315)))

        # Recria herói
        self.hero.add(Hero((185, 400), faceRight=True))

        # Recria HUD
        vida_rect = (0, 0, 12, 12)
        self.hud = HUD(self.hero.sprite, hud_path + "vida_icon.png", vida_rect,
                    contorno_path=hud_path + "vida_hud.png")

        # Recria loja e pergunta
        dicas_estatisticas = [
    {
        "conceito": "Distrito Hélios",
        "descricao": "Primeiro distrito a apresentar aumento real.",
        "descricao_completa": "O Distrito Hélios é o único que começa a subir nos primeiros dias da epidemia. O início da curva aparece antes dos demais distritos. Isso indica que ele é o ponto mais provável de origem.",
        "preco": 3,
        "feedback": "Boa leitura do início da curva! Hélios é o primeiro distrito a apresentar crescimento."
    },
    {
        "conceito": "Distrito Nébula",
        "descricao": "Picos tardios e suspeitos.",
        "descricao_completa": "O Distrito Nébula permanece estável no início. Seu pico surge apenas mais tarde e parece manipulado. Picos tardios não indicam origem de uma epidemia.",
        "preco": 2,
        "feedback": "Nébula tem picos chamativos, mas acontece tarde demais para ser origem."
    },
    {
        "conceito": "Distrito Void",
        "descricao": "Crescimento leve e mais tardio.",
        "descricao_completa": "O Distrito Void apresenta aumento apenas depois que outros distritos já estavam crescendo. Crescimentos tardios não são típicos do ponto inicial de uma epidemia. Por isso, Void não indica origem.",
        "preco": 1,
        "feedback": "Void cresce tarde, então não é um bom candidato para origem."
    }
]

        self.loja = LojaSimples(
            self.hero.sprite,
            self.displaySurface,
            self.npcloja.sprite,
            dicas_estatisticas,
            pos=(100, 50)
        )

        self.pergunta = PerguntaGrafico(
            displaySurface=self.displaySurface,
            hero=self.hero.sprite,
            npc=self.crow.sprite,
            pergunta="Jack, olhando os dados, qual distrito indica a origem da epidemia?",
            grafico_path=graficos_path + "grafico_zumbis.png",
            loja=self.loja,
            correta_conceito="Distrito Hélios"
        )

        # Recria zona de teleporte
        self.teleport_zone = pygame.Rect(
            self.crow.sprite.hitbox.rect.x - 50,
            self.crow.sprite.hitbox.rect.y - 100,
            self.crow.sprite.hitbox.rect.width + 100,
            self.crow.sprite.hitbox.rect.height + 100
        )

        # Reseta estados
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
                    self.portal.add(Portal((0,510)))
                
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

                    self.Coin.update()
                    self.potion.update()
                    self.zombie.update(self)

                    
                # Atualiza NPCs e loja sempre, se existirem
            if self.crow.sprite:
                    self.crow.update(self)
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
                    self.zombie.add(Zombie((1500,240), moveRight=True, limit_left=1500, limit_right=1700))
                    self.zombie.add(Zombie((1600,435), moveRight=True, limit_left=1600, limit_right=1800))
                    self.zombie.add(Zombie((1600,515), moveRight=True, limit_left=1600, limit_right=1850))
                    self.ja_teletransportou = True
                    # Reseta o erro para não teletransportar várias vezes
                    self.pergunta.errou = False


                # Resetar o teleporte caso ele saia da área
            if self.ja_teletransportou and not self.hero.sprite.hitbox.colliderect(self.teleport_zone):
                    self.ja_teletransportou = False
                                    
    def draw(self):
            
        if self.cutscene_active:
            self.cutscene.draw4()
        else:  
                # Desenha o fundo         
            self.background.draw(self.displaySurface)
            

            for tile in self.other3sprites:
                pos = self.camera.apply(tile)
                self.displaySurface.blit(tile.image, pos)

            for tile in self.other2sprites:
                pos = self.camera.apply(tile)
                self.displaySurface.blit(tile.image, pos)

            
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
            for zombie in self.zombie:
                pos = self.camera.apply(zombie)
                self.displaySurface.blit(zombie.image, pos)


            pos = self.camera.apply(self.crow.sprite)
            self.displaySurface.blit(self.crow.sprite.image, pos)
            self.crow.sprite.draw(self.displaySurface, self.camera)

            
         
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

            
            self.quest_system.draw()



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

 
class Level5():
    def __init__(self, displaySurface, fase_id=3):
       
        self.ja_teletransportou = False

        self.verificar_prox_fase = None
        
        self.displaySurface = displaySurface

        self.cutscene_active = True
        self.cutscene = Cutscene(self.displaySurface, font_path , multi_stage=False)
        
        self.fase_id = fase_id

        self.font = pygame.font.Font(font_path, 40)
        self.phase_text = AnimatedText("Fase 5: A volta de jack", self.font, (255, 255, 255), surface=self.displaySurface)

        dicas_estatisticas_fase5 = [
    {
        "conceito": "Olhar da Escala Quebrada",
        "descricao": "Percebe quando a escala de um gráfico está distorcida.",
        "descricao_completa": (
            "Uma habilidade especializada em enxergar problemas nos eixos, como escalas comprimidas ou alongadas. No entanto, ela observa apenas a escala, sem avaliar a distribuição ou o contexto dos dados. É um bom começo, mas não resolve completamente a ilusão."
        ),
        "preco": 4,
        "feedback": (
            "Você percebe o problema de escala, mas não o interpreta por completo. "
            "Ainda falta entender como a escala afeta a percepção da correlação."
        ),
        "correta": False
    },
    {
        "conceito": "Visão da Correlação Falsa",
        "descricao": "Identifica quando uma correlação aparente não é real.",
        "descricao_completa": (
            "Uma técnica útil para evitar interpretações equivocadas sobre relações entre variáveis. Porém, sem corrigir a escala do gráfico, a percepção da correlação continua distorcida. Não resolve a manipulação."
        ),
        "preco": 2,
        "feedback": (
            "Você entendeu que não há causalidade, mas com a escala distorcida "
            "a ilusão visual permanece. Algo ainda está fora do lugar."
        ),
        "correta": False
    },
    {
        "conceito": "Filtro da Amostra Pura",
        "descricao": "Remove dados extremos para limpar visualmente um gráfico.",
        "descricao_completa": (
            "Limpar a amostra pode ajudar em algumas análises, mas aqui o problema não está nos dados — está na escala. Remover pontos não muda a ilusão, e pode até ocultar informações importantes."
        ),
        "preco": 2,
        "feedback": (
            "Você ajustou a amostra, mas nada mudou — porque o problema não era "
            "a amostra, e sim a escala manipulada. A ilusão persiste intacta."
        ),
        "correta": False
    },
    {
        "conceito": "Olho do Equilíbrio Gráfico",
        "descricao": "Corrige escalas distorcidas e revela a verdadeira relação entre variáveis.",
        "descricao_completa": (
            "Uma habilidade completa que detecta e corrige manipulações nos eixos, restaurando a proporção verdadeira do gráfico. Ao ajustar a escala, a suposta correlação desaparece e o padrão real dos dados é revelado."
        ),
        "preco": 3,
        "feedback": (
            "Você corrige a escala e devolve o equilíbrio ao gráfico."
            "Com os eixos proporcionais, percebe que não há tendência real"
            "a ilusão criada por Erradon se desfaz instantaneamente."
        ),
        "imagem": image_path + "grafico_dispersao_feedback_fase5.png",
        "correta": True
    }
]

        quests = [
            {"id": 1, "text": "Fale com o rosa na vila", "done": False},
            {"id": 2, "text": "Encontre o mercador", "done": False},
            {"id": 3 , "text": "Resolva o problema da rosa" , "done" : False},
            {"id": 4 , "text": "Entre no portal" , "done" : False}
        ]
        
        self.quest_system = QuestSystem(quests, self.displaySurface )
         # Carregar o arquivo TMX

        self.levelData = load_pygame(LEVELS_PATH + "Level1/level5.tmx")

        # Instanciar classes
        self.background = Background()

        # Criar grupos de sprites
        self.hero = pygame.sprite.GroupSingle()
        self.platformTiles = pygame.sprite.Group()
        self.othersprites = pygame.sprite.Group()
        self.other2sprites = pygame.sprite.Group()
        self.other3sprites = pygame.sprite.Group()
        self.paredesprites = pygame.sprite.Group()
        self.bees = pygame.sprite.Group()
        self.robot = pygame.sprite.Group()
        self.Coin = pygame.sprite.Group()
        self.potion = pygame.sprite.Group()
        self.npcrobot = pygame.sprite.GroupSingle()
        self.npcloja = pygame.sprite.GroupSingle()
        self.portal = pygame.sprite.GroupSingle()
        self.skeleton = pygame.sprite.Group()
        self.crow = pygame.sprite.GroupSingle()
        self.zombie =  pygame.sprite.Group()
        self.reaper = pygame.sprite.GroupSingle()
        self.erradon = pygame.sprite.GroupSingle()
        self.samuraixamom = pygame.sprite.Group()
        self.samuraigirl = pygame.sprite.GroupSingle()
      
        layer = self.levelData.get_layer_by_name('Platforms')
        for x, y, tileSurface in layer.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.platformTiles.add(tile)
        
        other = self.levelData.get_layer_by_name('Background')
        for x, y, tileSurface in other.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.othersprites.add(tile)

        other2 = self.levelData.get_layer_by_name('Background2')
        for x, y, tileSurface in  other2.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self. other2sprites.add(tile)

        other3 = self.levelData.get_layer_by_name('Arvores')
        for x, y, tileSurface in  other3.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self. other3sprites.add(tile)

        
        parede = self.levelData.get_layer_by_name('Parede')
        for x, y, tileSurface in parede.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.paredesprites.add(tile)

        self.dialogue_box = AppearingTextBox(repositorio.dialogo_fase(fase_id), self.displaySurface)
       
     

        self.samuraixamom.add(Samuraixamom((900,240), moveRight=True,limit_left= 700, limit_right= 950))

        self.samuraixamom.add(Samuraixamom((900,240), moveRight=True,limit_left= 710, limit_right= 950))

        self.samuraixamom.add(Samuraixamom((900,485), moveRight=True,limit_left= 690, limit_right= 980))

        self.samuraixamom.add(Samuraixamom((900,485), moveRight=True,limit_left= 700, limit_right= 950))


        self.samuraixamom.add(Samuraixamom((200,290), moveRight=True,limit_left= 180, limit_right= 400))

        self.samuraixamom.add(Samuraixamom((1200,370), moveRight=True,limit_left= 1100, limit_right= 1350))

        self.samuraixamom.add(Samuraixamom((1600,495), moveRight=True,limit_left= 1600, limit_right= 1850))

        self.samuraixamom.add(Samuraixamom((1500,495), moveRight=True,limit_left= 1400, limit_right= 1650))

        self.samuraixamom.add(Samuraixamom((900,240), moveRight=True,limit_left= 700, limit_right= 950))

        self.samuraixamom.add(Samuraixamom((900,240), moveRight=True,limit_left= 700, limit_right= 950))



        self.samuraigirl.add(SamuraigirlNpc((173,481) , faceRight= False))

        self.npcloja.add(LojaNpc((1800,265) , faceRight= False))
       
        self.Coin.add(Coin((120,145)))
        self.Coin.add(Coin((150,145)))
        
        self.Coin.add(Coin((80,370)))
        self.Coin.add(Coin((50,370)))
        
        
        self.Coin.add(Coin((540,300)))
        self.Coin.add(Coin((510,300)))
        
        self.Coin.add(Coin((1040,300)))
        self.Coin.add(Coin((1010,300)))


        self.Coin.add(Coin((1250,280)))
        self.Coin.add(Coin((1280,280)))

        self.potion.add(Potion((1800,490)))

        self.potion.add(Potion((1600,490)))

        self.potion.add(Potion((225,385)))
    
        self.hero.add(Hero((185, 400), faceRight=True))
       

        self.loja = LojaSimples(self.hero.sprite, self.displaySurface, self.npcloja.sprite , dicas_estatisticas_fase5, pos=(100, 50))
  
        self.pergunta = PerguntaGrafico(
        displaySurface=self.displaySurface,
        hero=self.hero.sprite,
        npc=self.samuraigirl.sprite,
        pergunta=(
            "Rosa acredita que o vento faz as flores crescerem mais rápido, "
            "mas algo parece errado neste gráfico... "
            "Qual é o verdadeiro problema que você enxerga?"
        ),
        grafico_path = graficos_path + "grafico_dispersao_fase5.png",
        loja=self.loja,
        correta_conceito ="Olho do Equilíbrio Gráfico"
    )

        vida_rect = (0, 0, 12, 12)
        self.hud = HUD(self.hero.sprite, hud_path + "vida_icon.png",vida_rect,contorno_path = hud_path + "vida_hud.png")

        # Configura a câmera
        self.camera = Camera(self.levelData.width * TILESIZE, self.levelData.height * TILESIZE)

        self.teleport_zone = pygame.Rect(
        self.samuraigirl.sprite.hitbox.rect.x - 50,   # aumenta para esquerda
        self.samuraigirl.sprite.hitbox.rect.y -100,   # aumenta para cima
        self.samuraigirl.sprite.hitbox.rect.width + 100,  # aumenta largura
        self.samuraigirl.sprite.hitbox.rect.height + 100  # aumenta altura
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

        other2 = self.levelData.get_layer_by_name('Background2')
        for x, y, tileSurface in other2.tiles():
            self.other2sprites.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))

        parede = self.levelData.get_layer_by_name('Parede')
        for x, y, tileSurface in parede.tiles():
            self.paredesprites.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))

        dicas_estatisticas_fase5 = [
    {
        "conceito": "Olhar da Escala Quebrada",
        "descricao": "Percebe quando a escala de um gráfico está distorcida.",
        "descricao_completa": (
            "Uma habilidade especializada em enxergar problemas nos eixos, como escalas comprimidas ou alongadas. No entanto, ela observa apenas a escala, sem avaliar a distribuição ou o contexto dos dados. É um bom começo, mas não resolve completamente a ilusão."
        ),
        "preco": 4,
        "feedback": (
            "Você percebe o problema de escala, mas não o interpreta por completo. "
            "Ainda falta entender como a escala afeta a percepção da correlação."
        ),
        "correta": False
    },
    {
        "conceito": "Visão da Correlação Falsa",
        "descricao": "Identifica quando uma correlação aparente não é real.",
        "descricao_completa": (
            "Uma técnica útil para evitar interpretações equivocadas sobre relações entre variáveis. Porém, sem corrigir a escala do gráfico, a percepção da correlação continua distorcida. Não resolve a manipulação."
        ),
        "preco": 2,
        "feedback": (
            "Você entendeu que não há causalidade, mas com a escala distorcida "
            "a ilusão visual permanece. Algo ainda está fora do lugar."
        ),
        "correta": False
    },
    {
        "conceito": "Filtro da Amostra Pura",
        "descricao": "Remove dados extremos para limpar visualmente um gráfico.",
        "descricao_completa": (
            "Limpar a amostra pode ajudar em algumas análises, mas aqui o problema não está nos dados — está na escala. Remover pontos não muda a ilusão, e pode até ocultar informações importantes."
        ),
        "preco": 2,
        "feedback": (
            "Você ajustou a amostra, mas nada mudou — porque o problema não era "
            "a amostra, e sim a escala manipulada. A ilusão persiste intacta."
        ),
        "correta": False
    },
    {
        "conceito": "Olho do Equilíbrio Gráfico",
        "descricao": "Corrige escalas distorcidas e revela a verdadeira relação entre variáveis.",
        "descricao_completa": (
            "Uma habilidade completa que detecta e corrige manipulações nos eixos, restaurando a proporção verdadeira do gráfico. Ao ajustar a escala, a suposta correlação desaparece e o padrão real dos dados é revelado."
        ),
        "preco": 3,
        "feedback": (
            "Você corrige a escala e devolve o equilíbrio ao gráfico."
            "Com os eixos proporcionais, percebe que não há tendência real"
            "a ilusão criada por Erradon se desfaz instantaneamente."
        ),
        "imagem": image_path + "grafico_dispersao_feedback_fase5.png",
        "correta": True
    }
]
        
        self.loja = LojaSimples(self.hero.sprite, self.displaySurface, self.npcloja.sprite , dicas_estatisticas_fase5, pos=(100, 50))

        self.pergunta = PerguntaGrafico(
        displaySurface=self.displaySurface,
        hero=self.hero.sprite,
        npc=self.samuraigirl.sprite,
        pergunta=(
            "Rosa acredita que o vento faz as flores crescerem mais rápido, "
            "mas algo parece errado neste gráfico... "
            "Qual é o verdadeiro problema que você enxerga?"
        ),
        grafico_path = graficos_path + "grafico_dispersao_feedback_fase5.png",
        loja=self.loja,
        correta_conceito ="Olho do Equilíbrio Gráfico"
    )



        # Recria inimigos
        
        self.samuraixamom.add(Samuraixamom((900,240), moveRight=True,limit_left= 700, limit_right= 950))

        self.samuraixamom.add(Samuraixamom((900,240), moveRight=True,limit_left= 710, limit_right= 950))

        self.samuraixamom.add(Samuraixamom((900,485), moveRight=True,limit_left= 690, limit_right= 980))

        self.samuraixamom.add(Samuraixamom((900,485), moveRight=True,limit_left= 700, limit_right= 950))


        self.samuraixamom.add(Samuraixamom((200,290), moveRight=True,limit_left= 180, limit_right= 400))

        self.samuraixamom.add(Samuraixamom((1200,370), moveRight=True,limit_left= 1100, limit_right= 1350))

        self.samuraixamom.add(Samuraixamom((1600,495), moveRight=True,limit_left= 1600, limit_right= 1850))

        self.samuraixamom.add(Samuraixamom((1500,495), moveRight=True,limit_left= 1400, limit_right= 1650))

        self.samuraixamom.add(Samuraixamom((900,240), moveRight=True,limit_left= 700, limit_right= 950))

        self.samuraixamom.add(Samuraixamom((900,240), moveRight=True,limit_left= 700, limit_right= 950))

        self.samuraigirl.add(SamuraigirlNpc((173,481) , faceRight= False))

        self.npcloja.add(LojaNpc((1800,265) , faceRight= False))
       
        self.Coin.add(Coin((120,145)))
        self.Coin.add(Coin((150,145)))
        
        self.Coin.add(Coin((80,370)))
        self.Coin.add(Coin((50,370)))
        
        
        self.Coin.add(Coin((540,300)))
        self.Coin.add(Coin((510,300)))
        
        self.Coin.add(Coin((1040,300)))
        self.Coin.add(Coin((1010,300)))


        self.Coin.add(Coin((1250,280)))
        self.Coin.add(Coin((1280,280)))

        self.potion.add(Potion((1800,490)))

        self.potion.add(Potion((1600,490)))

        self.potion.add(Potion((225,385)))
    
        self.hero.add(Hero((185, 400), faceRight=True))
       

        # Recria zona de teleporte
        self.teleport_zone = pygame.Rect(
            self.samuraigirl.sprite.hitbox.rect.x - 50,
            self.samuraigirl.sprite.hitbox.rect.y - 100,
            self.samuraigirl.sprite.hitbox.rect.width + 100,
            self.samuraigirl.sprite.hitbox.rect.height + 100
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
                    self.portal.add(Portal((0,130)))
                
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

                    self.Coin.update()
                    self.potion.update()
                    self.samuraixamom.update(self)
                    
                # Atualiza NPCs e loja sempre, se existirem
            if self.samuraigirl.sprite:
                    self.samuraigirl.update(self)
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
                       
                    self.ja_teletransportou = True
                    # Reseta o erro para não teletransportar várias vezes
                    self.pergunta.errou = False


                # Resetar o teleporte caso ele saia da área
            if self.ja_teletransportou and not self.hero.sprite.hitbox.colliderect(self.teleport_zone):
                    self.ja_teletransportou = False
                                   
    def draw(self):
        if self.cutscene_active:
            self.cutscene.draw5()
        else:          # Desenha o fundo         
            self.background.draw1(self.displaySurface)
            

            for tile in self.other3sprites:
                pos = self.camera.apply(tile)
                self.displaySurface.blit(tile.image, pos)

            for tile in self.other2sprites:
                pos = self.camera.apply(tile)
                self.displaySurface.blit(tile.image, pos)

            
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
            for samurai in self.samuraixamom:
                pos = self.camera.apply(samurai)
                self.displaySurface.blit(samurai.image, pos)


            pos = self.camera.apply(self.samuraigirl.sprite)
            self.displaySurface.blit(self.samuraigirl.sprite.image, pos)
            self.samuraigirl.sprite.draw(self.displaySurface, self.camera)

            
         
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

            
            self.quest_system.draw()



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



class Level6():
    def __init__(self, displaySurface, fase_id=3):
       
        self.ja_teletransportou = False

        self.verificar_prox_fase = None
        
        self.displaySurface = displaySurface
        
        self.fase_id = fase_id

        self.cutscene_active = True

        self.cutscene_final_active = False

        self.cutscene = Cutscene(self.displaySurface, font_path , multi_stage=False)

        self.cutscene_final = Cutscene_final(self.displaySurface, font_path , multi_stage=True)

        self.font = pygame.font.Font(font_path, 40)
        self.phase_text = AnimatedText("Fase 6: Batalha final", self.font, (255, 255, 255), surface=self.displaySurface)

        dicas_estatisticas = [
    {
        "conceito": "Golpe da Precisão Cega",
        "descricao": "Ataque rápido e repetitivo, sempre no mesmo ponto.",
        "descricao_completa": (
            "Um golpe com alta consistência, mas pouca flexibilidade. "
            "Acerta sempre o mesmo ponto, mesmo que o alvo mude. "
            "É previsível e tende ao erro sistemático — o viés. "
            "Ideal para quem busca estabilidade, mas arrisca a verdade."
        ),
        "preco": 0,
        "feedback": (
            "Seu ataque é estável, mas previsível. "
            "Erradon se alimenta da rigidez — cuidado com o viés!"
        )
    },
    {
        "conceito": "Golpe da Incerteza Selvagem",
        "descricao": "Ataque imprevisível, muda de direção a cada instante.",
        "descricao_completa": (
            "Um golpe caótico e instável. Às vezes acerta em cheio, "
            "outras vezes erra completamente. Tem baixa consistência, "
            "mas grande alcance de possibilidades. "
            "É dominado pela variância — energia sem controle."
        ),
        "preco": 0,
        "feedback": (
            "Ataques cheios de energia, mas sem foco. "
            "Erradon se confunde, mas você também — cuidado com a variância!"
        )
    },
    {
        "conceito": "Golpe do Ajuste Perfeito",
        "descricao": "Golpe que tenta compensar todo erro anterior.",
        "descricao_completa": (
            "Um golpe refinado e calculado para corrigir cada falha passada. "
            "No entanto, ao tentar se adaptar a tudo, perde a generalidade. "
            "Funciona bem contra um inimigo conhecido, mas falha em outros. "
            "Representa o superajuste — aprender demais com o ruído."
        ),
        "preco": 0,
        "feedback": (
            "Você se adapta bem, mas talvez demais. "
            "Erradon muda o padrão e o golpe perde sua força."
        )
    },
    {
        "conceito": "Golpe do Equilíbrio",
        "descricao": "Combinação precisa entre constância e adaptação.",
        "descricao_completa": (
            "Um golpe que busca o ponto de menor erro possível. "
            "Nem rígido demais, nem aleatório. "
            "Cada movimento considera tanto o viés quanto a variância. "
            "É o único ataque capaz de atingir o núcleo de Erradon."
        ),
        "preco": 0,
        "feedback": (
            "Perfeito equilíbrio! O golpe flui como um modelo ideal. "
            "Erradon treme — este é o ataque certo para derrotá-lo!"
        )
    }
]

        quests = [
            {"id": 1, "text": "Fale com erradon", "done": False},
            {"id": 2, "text": "Encontre o mercador", "done": False},
            {"id": 3 , "text": "Derrote erradon" , "done" : False},
        ]
        
        self.quest_system = QuestSystem(quests, self.displaySurface )
         # Carregar o arquivo TMX

        self.levelData = load_pygame(LEVELS_PATH + "Level1/level6.tmx")


        # Instanciar classes
        self.background = Background()

        # Criar grupos de sprites
        self.hero = pygame.sprite.GroupSingle()
        self.platformTiles = pygame.sprite.Group()
        self.othersprites = pygame.sprite.Group()
        self.other2sprites = pygame.sprite.Group()
        self.other3sprites = pygame.sprite.Group()
        self.paredesprites = pygame.sprite.Group()
        self.bees = pygame.sprite.Group()
        self.robot = pygame.sprite.Group()
        self.Coin = pygame.sprite.Group()
        self.potion = pygame.sprite.Group()
        self.npcrobot = pygame.sprite.GroupSingle()
        self.npcloja = pygame.sprite.GroupSingle()
        self.portal = pygame.sprite.GroupSingle()
        self.skeleton = pygame.sprite.Group()
        self.crow = pygame.sprite.GroupSingle()
        self.zombie =  pygame.sprite.Group()
        self.reaper = pygame.sprite.GroupSingle()
        self.erradon = pygame.sprite.GroupSingle()
        self.samuraixamom = pygame.sprite.Group()
        self.samuraigirl = pygame.sprite.GroupSingle()
      
        layer = self.levelData.get_layer_by_name('Platforms')
        for x, y, tileSurface in layer.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.platformTiles.add(tile)
        
        other = self.levelData.get_layer_by_name('Background')
        for x, y, tileSurface in other.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.othersprites.add(tile)

        other2 = self.levelData.get_layer_by_name('Background2')
        for x, y, tileSurface in  other2.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self. other2sprites.add(tile)

        other3 = self.levelData.get_layer_by_name('Arvores')
        for x, y, tileSurface in  other3.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self. other3sprites.add(tile)

        
        parede = self.levelData.get_layer_by_name('Parede')
        for x, y, tileSurface in parede.tiles():
            tile = Tile((x * TILESIZE, y * TILESIZE), tileSurface)
            self.paredesprites.add(tile)

        self.dialogue_box = AppearingTextBox(repositorio.dialogo_fase(fase_id), self.displaySurface)
       
     
        
        self.erradon.add(ErradonNpc((735,498) , faceRight= False))

        self.npcloja.add(LojaNpc((400,505) , faceRight= True))
       

    
        self.hero.add(Hero((185, 400), faceRight=True))
       

        self.loja = LojaSimples(self.hero.sprite, self.displaySurface, self.npcloja.sprite , dicas_estatisticas, pos=(100, 50))
  
        self.pergunta = PerguntaResposta1(
        displaySurface=self.displaySurface,
        hero=self.hero.sprite,
        npc=self.erradon.sprite,
        pergunta=(
            "Jack percebe que seus golpes são firmes, mas sempre erram o centro. "
            "Ele tenta variar seus ataques, mas agora acerta de forma inconsistente. "
            "O que ele deve fazer para derrotar Erradon?"
        ),
        loja=self.loja,
        correta_conceito="Golpe do Equilíbrio",
        pos=(100, 100)
    )
       

        vida_rect = (0, 0, 12, 12)
        self.hud = HUD(self.hero.sprite, hud_path + "vida_icon.png",vida_rect,contorno_path = hud_path + "vida_hud.png")

        # Configura a câmera
        self.camera = Camera(self.levelData.width * TILESIZE, self.levelData.height * TILESIZE)

        self.teleport_zone = pygame.Rect(
        self.erradon.sprite.hitbox.rect.x - 50,   # aumenta para esquerda
        self.erradon.sprite.hitbox.rect.y -100,   # aumenta para cima
        self.erradon.sprite.hitbox.rect.width + 100,  # aumenta largura
        self.erradon.sprite.hitbox.rect.height + 100  # aumenta altura
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

        other2 = self.levelData.get_layer_by_name('Background2')
        for x, y, tileSurface in other2.tiles():
            self.other2sprites.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))

        parede = self.levelData.get_layer_by_name('Parede')
        for x, y, tileSurface in parede.tiles():
            self.paredesprites.add(Tile((x * TILESIZE, y * TILESIZE), tileSurface))

       
        # Recria inimigos
        
        
       
    

      

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
        self.pergunta = PerguntaResposta1(
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


        
        
        if self.cutscene_final_active:
            if self.cutscene_final.finished:
                self.cutscene_final_active = False
                
            return

        if self.cutscene_active:
            if self.cutscene.finished:
                self.cutscene_active = False  # agora a fase 1 começa
            return
        else:
        
       
            if self.pergunta.acertou and not self.cutscene_final_active:
                self.cutscene_final_active = True
           
           
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

                    self.Coin.update()
                    self.potion.update()
                    self.zombie.update(self)

                    
                # Atualiza NPCs e loja sempre, se existirem
            if self.erradon.sprite:
                    self.erradon.update(self)
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
                    self.robot.add(Robot((800, 255), moveRight=True, limit_left=700, limit_right=900))
                    self.robot.add(Robot((900, 445), moveRight=True, limit_left=1000, limit_right=1100))
                    self.ja_teletransportou = True
                    # Reseta o erro para não teletransportar várias vezes
                    self.pergunta.errou = False


                # Resetar o teleporte caso ele saia da área
            if self.ja_teletransportou and not self.hero.sprite.hitbox.colliderect(self.teleport_zone):
                    self.ja_teletransportou = False
                                    
    def draw(self):
       
        if self.cutscene_final_active:
            self.cutscene_final.draw()
            return


        elif self.cutscene_active:
            self.cutscene.draw6()
        else:            # Desenha o fundo         
            self.background.draw1(self.displaySurface)
            

            for tile in self.other3sprites:
                pos = self.camera.apply(tile)
                self.displaySurface.blit(tile.image, pos)

            for tile in self.other2sprites:
                pos = self.camera.apply(tile)
                self.displaySurface.blit(tile.image, pos)

            
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
            for zombie in self.zombie:
                pos = self.camera.apply(zombie)
                self.displaySurface.blit(zombie.image, pos)


            pos = self.camera.apply(self.erradon.sprite)
            self.displaySurface.blit(self.erradon.sprite.image, pos)
            self.erradon.sprite.draw(self.displaySurface, self.camera)

            
         
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

            
            self.quest_system.draw()



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

