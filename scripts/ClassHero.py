import pygame
from scripts.Config import *
from scripts.ClassSpriteSheet import SpriteSheet
import random
from scripts.Classtext import *
from scripts.ClassPerguntaResposta1 import *
from scripts.Musicmanager import *

music = MusicManager()


# RUN SPRITES
runSprites = [(x, 48, 65, 65) for x in range(32, 993, 128)]

# IDLE SPRITES
idleSprites = [(x, 48, 65, 65) for x in range(32, 1312, 128)]

# ATTACK SPRITES (último quadro com largura menor, precisa ser tratado separadamente)
attackSprites = [(x, 48, 90, 65) for x in range(32, 815, 128)] 

# DEATH SPRITES (último quadro com largura menor)
deathSprites = [(x, 48, 65, 65) for x in range(32, 1072, 128)] 

# JUMP SPRITES
jumpSprites = [(x, 48, 65, 65) for x in [32, 162, 288]]

# FALL SPRITES
fallSprites = [(x, 48, 65, 65) for x in [32, 162, 288]]

# HURT SPRITES
HurtSprites = [(x, 47, 65, 66) for x in [32,128,336]]

jumptransitionSprites = [(x, 48, 65, 65) for x in [32, 162, 288]]

HealingSprites = [(x, 48, 65, 65) for x in range(32, 1568, 128)]




class Hero(pygame.sprite.Sprite):

    def __init__(self, position, faceRight):
        super().__init__()

        # Load spritesheets
        #idleSpriteSheet = SpriteSheet(SPRITESHEET_PATH + "Character/Idle/Idle-Sheet.png", idleSprites)
        #runSpriteSheet = SpriteSheet(SPRITESHEET_PATH + "Character/Run/Run-Sheet.png", runSprites)
        #attackSpriteSheet = SpriteSheet(SPRITESHEET_PATH + "Character/Attack-01/Attack-01-Sheet.png", attackSprites)
        #deathSpriteSheet = SpriteSheet(SPRITESHEET_PATH + "Character/Dead/Dead-Sheet.png", deathSprites)
        
        jumpSpriteSheet = SpriteSheet(samurai_path + "/JUMP-START.png", jumpSprites)
        fallSpriteSheet = SpriteSheet(samurai_path  + "/JUMP-FALL.png", fallSprites)
        jumptransitionSpriteSheet = SpriteSheet(samurai_path  + "/JUMP-TRANSITION.png",jumptransitionSprites)
        #idleSpriteSheet = SpriteSheet(samurai_path  + "/Idle-sheet.png", idleSprites)
        #runSpriteSheet = SpriteSheet(samurai_path  + "/Run-Sheet.png", runSprites)
        idleSpriteSheet = SpriteSheet(samurai_path  + "/IDLE.png", idleSprites)
        runSpriteSheet = SpriteSheet(samurai_path  + "/RUN.png", runSprites)
        attackSpriteSheet = SpriteSheet(samurai_path  + "/ATTACK1.png", attackSprites)
        deathSpriteSheet = SpriteSheet(samurai_path  + "/DEATH.png", deathSprites)
        hurtSpriteSheet = SpriteSheet(samurai_path  + "/HURT.png", HurtSprites)
        healingSpriteSheet = SpriteSheet(samurai_path + "/HEALING.png", HealingSprites)

    
        self.spriteSheets = {
            'IDLE'   : idleSpriteSheet,
            'RUN'    : runSpriteSheet,
            'ATTACK' : attackSpriteSheet,
            'DIE'    : deathSpriteSheet,
            'JUMP'   : jumpSpriteSheet,
            'FALL'   : fallSpriteSheet,
            'HURT'   : hurtSpriteSheet,
            'JUMPTRANS' : jumptransitionSpriteSheet,
            'HEALING': healingSpriteSheet
        }

        self.animationIndex = 0
        self.facingRight = faceRight
        self.currentState = 'IDLE'
        self.xDir = 0
        self.yDir = 0
        self.speed = SPEED_HERO
        self.xPos = position[0]
        self.yPos = position[1]
        self.position_initial = position[0],position[1]
        self.y_collision = False
        self.isJumping = False
        self.lives = LIVES 
        self.coins_count = 0
        self.isInvincible = False
        self.invincibleTimer = 0
        self.attack_hitbox = None
        self.attack_hitbox1 = None
        self.down_pressed = False
        self.prev_down_key = False
        self.health = False
        self.contato_dialogo = False
        self.debug_platform_rects = []
        self.falou_com_npc = False
        self.passou_portal = False
        self.respondeu_certo = False

   
    def create_hitbox(self, x_center, y_bottom, width, height, scale_x=0.6, scale_y=0.7, offset_y=50, offset_x = 5):
        """Cria hitbox proporcional à sprite."""
        new_width = int(width * scale_x)
        new_height = int(height * scale_y)
         
       
        x = x_center - new_width // 2 + offset_x
        y = y_bottom - new_height + offset_y
        
        return pygame.Rect(x, y, new_width, new_height)


# CRIANDO PARA O DIALOGO
    def handle_input(self,level):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_e] and not self.e_pressed_last_frame and self.contato_dialogo == True:
            if not level.dialogue_box.text_active:
                level.dialogue_box.start()

        if keys[pygame.K_a] and not self.a_pressed_last_frame:
            if level.dialogue_box.text_active:
                level.dialogue_box.advance_text()
            else:
                level.dialogue_box.reset()

        self.e_pressed_last_frame = keys[pygame.K_e]
        self.a_pressed_last_frame = keys[pygame.K_a]

    def update(self, level):

        self.handle_input(level)
        self.previousState = self.currentState
        self.xDir = 0
        
        if self.isInvincible:
            
            self.invincibleTimer -= 1
       
        if self.invincibleTimer <= 0:
            self.isInvincible = False

        # get key status
       
        # criar um key status para quando o personagem não estiver colidindo com o chão!
    
        if level.dialogue_box.text_active == False  and  level.loja.active == False and not level.loja.mostrar_compradas and level.pergunta.active == False:
            if self.currentState not in ['ATTACK', 'DIE', 'HURT', 'HEALING']:

                keys = pygame.key.get_pressed()
                self.down_pressed = keys[pygame.K_DOWN] 

                # ATAQUE
                if keys[pygame.K_SPACE] and not self.isJumping:
                    self.currentState = 'ATTACK'

                # MOVIMENTO PARA ESQUERDA OU DIREITA
                elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                    if keys[pygame.K_LEFT]:
                        self.xDir = -1
                        self.facingRight = False
                    elif keys[pygame.K_RIGHT]:
                        self.xDir = 1
                        self.facingRight = True
                    self.currentState = 'RUN'
                    
                
                    if self.yDir > 0.2:
                            self.currentState = 'FALL'
                           

                    # PULO COM MOVIMENTO
                    if keys[pygame.K_UP] and self.y_collision:
                        self.yDir = JUMP_WITH_RUN
                        self.isJumping = True
                        

                    # Transição aérea durante movimento
                    if self.isJumping:
                        if self.yDir < -1:
                            self.currentState = 'JUMP'
                            
                    
                        elif -1 <= self.yDir <= 1:
                                self.currentState = 'JUMPTRANS' 
                            
                        elif self.yDir > 1:
                            self.currentState = 'FALL'
                            
                    
                    
                # PULO PARADO
                elif keys[pygame.K_UP] and self.y_collision:
                    self.yDir = JUMP_NORMAL
                    self.isJumping = True
                    self.currentState = 'JUMP'
                    

                # DESCIDA FORÇADA
                elif keys[pygame.K_DOWN] and  self.y_collision:
                        self.yDir = 2
                        self.y_collision = False
                        self.isJumping = True
                        self.down_pressed = True
                        self.currentState = 'FALL'
                        

                elif keys[pygame.K_v] and self.health and self.lives < 4:
                    self.currentState = 'HEALING'
                    self.health = False
                    self.lives += 1
                    

                # SEM TECLAS PRESSIONADAS: IDLE OU ESTADO AÉREO
                else:
                    if self.y_collision:
                        if self.currentState == 'FALL' and self.yDir == 0:
                            self.currentState = 'IDLE'
                    else:
                        if self.isJumping:
                            if self.yDir < -1:
                                self.currentState = 'JUMP'

                            elif -1 <= self.yDir <= 1:
                                self.currentState = 'JUMPTRANS' 

                            elif self.yDir > 1:
                                self.currentState = 'FALL'
                        
                        elif self.yDir > 0.2:
                            self.currentState = 'FALL'
            
            # Select animation for current player action (idle, run, jump, fall, etc.)
            self.selectAnimation()

            # Start from beginning of a new animation
            if self.previousState != self.currentState:
                self.animationIndex = 0
                self.selectAnimation()
                self.image = self.currentAnimation[int(self.animationIndex)]
            else:
                self.selectAnimation()
                self.image = self.currentAnimation[int(self.animationIndex)]


        # Selecionando o tamanho do rect dependendo da animação certa
        # (xPos, yPos) = bottom-center posição do sprite

        if self.currentState == 'IDLE':
            self.rect = pygame.Rect(self.xPos - 22, self.yPos - 52, 44, 52)
            self.attack_hitbox = None

        elif self.currentState == 'RUN':
            self.rect = pygame.Rect(self.xPos - 22, self.yPos - 52, 44, 52)
            self.attack_hitbox = None
            
        elif self.currentState == 'HEALING':
            self.rect = pygame.Rect(self.xPos - 22, self.yPos - 52, 44, 52)
       
        elif self.currentState == 'ATTACK':
             self.rect = pygame.Rect(self.xPos - 22, self.yPos -8, 44, 52)
            
             if self.animationIndex >= 3:
                if self.facingRight:
                    self.attack_hitbox = pygame.Rect(self.rect.x + 55, self.rect.y + 15, 40, 35)
                else:
                    self.attack_hitbox = pygame.Rect(self.rect.x - 5, self.rect.y + 15, 40, 35)
        
        elif self.currentState == 'DIE':
            self.rect = pygame.Rect(self.xPos - 40, self.yPos - 30, 80, 60)
            self.attack_hitbox = None
        
        elif self.currentState == 'JUMP':
             self.rect = pygame.Rect(self.xPos - 22, self.yPos - 52, 44, 52) 
             self.attack_hitbox = None

        elif self.currentState == 'FALL':
            self.rect = pygame.Rect(self.xPos - 22, self.yPos - 52, 44, 52) 
            self.attack_hitbox = None
            
        
        # Play animation until end of current animation is reached
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.currentAnimation):
            if self.currentState == 'DIE':
                self.animationIndex = len(self.currentAnimation) - 1
            else:
                self.animationIndex = 0
                self.currentState = 'IDLE'



        ### Criando a Hitbox do personagem ###

        elif self.facingRight == True and self.currentState == "RUN":
         self.hitbox = self.create_hitbox(self.rect.centerx, self.rect.bottom, 20, 42, offset_x = 12)
         
        elif self.facingRight == False and self.currentState == "RUN":
          self.hitbox = self.create_hitbox(self.rect.centerx, self.rect.bottom, 20, 42 )

        elif self.facingRight == True :
           self.hitbox = self.create_hitbox(self.rect.centerx, self.rect.bottom, 20, 42)

        else : 
         self.hitbox = self.create_hitbox(self.rect.centerx, self.rect.bottom, 20, 42 , offset_x = 12)
        
        self.moveHorizontal(level)

        self.updateFootRect()
        
        self.applyGravity(level)

        # colisão com novos inimigos ou antigos inimigos
        self.checkEnemyCollisions(level.bees)

        self.checkEnemyCollisions(level.robot)

        self.checkEnemyCollisions(level.zombie)

        self.checkEnemyCollisions(level.skeleton)

        self.checkEnemyCollisions(level.samuraixamom)

        self.checkNpcCollisions(level.npcrobot)

        self.checkNpcCollisions(level.reaper)

        self.checkNpcCollisions(level.crow)

        self.checkNpcCollisions(level.erradon)

        self.checkNpcCollisions(level.samuraigirl)

        self.checkpower_apps(level.Coin)

        self.checkpower_apps_health(level.potion)

        self.checkportalcontato(level.portal)

       # print(self.xPos,self.yPos)


        if self.previousState != self.currentState:
            if self.currentState == 'JUMP':
                music.animations_sounds("jump")
            elif self.currentState == 'FALL':
                music.animations_sounds("jump_end")
            elif self.currentState == 'ATTACK':
                music.animations_sounds("ataquesemhit")
            elif self.currentState == 'HEALING':
                music.animations_sounds("curar_vida")
            elif self.currentState == 'RUN':
                music.animations_sounds("run")
       
        

    def selectAnimation(self):
    
        if self.currentState == 'IDLE':
            self.animationSpeed = ANIMSPEED_HERO_IDLE
    
        elif self.currentState in ['JUMP','FALL','JUMPTRANS']:
            self.animationSpeed = ANIMSPEED_HERO_JUMP_FALL

        elif self.currentState in ['ATTACK']:
            self.animationSpeed = ANIMSPEED_HERO_ATTACK

        elif self.currentState in ['HURT']:
           self.animationSpeed =  ANIMSPEED_HERO_HURT
        
        
        elif self.currentState in ['DIE']:
           self.animationSpeed =  ANIMSPEED_HERO_DIE
        

        else:
                self.animationSpeed = ANIMSPEED_HERO_DEFAULT

        spriteSheet = self.spriteSheets[self.currentState]
        self.currentAnimation = spriteSheet.getSprites(flipped = not self.facingRight)

        

    def teleport(self, posx , posy):
        self.xPos = posx
        self.yPos = posy

    def moveHorizontal(self, level):
    # Atualiza a hitbox dependendo do lado
        if self.facingRight == True:
            self.hitbox_parede = self.create_hitbox(self.rect.centerx, self.rect.centery, 10, 30, offset_x = 15, offset_y=70)
        else:
            self.hitbox_parede = self.create_hitbox(self.rect.centerx, self.rect.centery, 10, 30 ,offset_y = 70)

        # Salva posição original
        original_x = self.xPos

        # Calcula tentativa de movimento
        new_xPos = self.xPos + self.xDir * self.speed
        delta = new_xPos - original_x

        # Move a hitbox de teste
        self.hitbox_parede.x += delta

        # Verifica colisões com paredes
        for parede in level.paredesprites:
            if self.hitbox_parede.colliderect(parede.rect):

                if self.xDir > 0 :
                    self.hitbox_parede.right = parede.rect.left
                elif self.xDir < 0:
                    self.hitbox_parede.left = parede.rect.right

                # Zera movimento
                delta = 0
                self.xDir = 0

        # Aplica movimento apenas se não saiu da tela
        if self.hitbox_parede.left + delta < 0:
            delta = -self.hitbox_parede.left
        elif self.hitbox_parede.right + delta > level.camera.world_size[0] - 10:
            delta = (level.camera.world_size[0] - 10) - self.hitbox_parede.right

        # Aplica movimento ao personagem
        self.xPos += delta
        self.rect.centerx = round(self.xPos)


    def updateFootRect(self):
    # Ajuste horizontal padrão
        if not self.facingRight:
            offset_x = 10   # desloca um pouco para a direita
        else:
            offset_x = 0  # desloca um pouco para a esquerda

        if self.currentState == 'DIE':
            self.foot_rect = pygame.Rect(self.rect.centerx + offset_x, self.rect.bottom - 5, 40, 40)

        elif self.currentState == 'RUN':
            # Ajuste maior no pé da frente quando correndo
            if self.facingRight:
                run_offset_x = 10
            else:
                run_offset_x = 0
            
            self.foot_rect = pygame.Rect(self.rect.centerx + run_offset_x, self.rect.bottom + 50, 10, 5)

        elif  self.currentState == 'HEALING':
            self.foot_rect = pygame.Rect(self.rect.centerx , self.rect.bottom + 50 , 20, 10)

        elif self.currentState == 'HURT':
            self.foot_rect = pygame.Rect(self.rect.centerx + offset_x, self.rect.bottom - 5, 40, 40)

        elif self.currentState == 'FALL' and self.down_pressed:
            # Alonga o foot_rect verticalmente para encontrar plataformas abaixo
            self.foot_rect = pygame.Rect(self.rect.centerx + offset_x - 10, self.rect.bottom + 500, 20, 10)

        elif self.currentState == 'FALL':
            self.foot_rect = pygame.Rect(self.rect.centerx + offset_x, self.rect.bottom + 45, 20, 10)

        else:
            self.foot_rect = pygame.Rect(self.rect.centerx + offset_x, self.rect.bottom + 50, 10, 5)
            # print(self.foot_rect)
    
    def applyGravity(self, level):
        # Assume que está no ar até verificar o contrário
        self.y_collision = False
        
        if self.currentState in ['ATTACK']:
            return
     
        if not self.y_collision:
            self.yDir += GRAVITY_Player
            self.yPos += self.yDir
            self.rect.y = self.yPos
            
        # print(self.currentState)

        # Verifica colisão com plataformas
        self.debug_platform_rects = []
        for platform in level.platformTiles:
            top_rect = pygame.Rect(
            platform.rect.x,
            platform.rect.y,
            platform.rect.width,
            10  
        )
            self.debug_platform_rects.append(top_rect)
            if self.foot_rect.colliderect(top_rect) and self.yDir >= 0:
                self.rect.bottom = platform.rect.top
                self.yPos = self.rect.y
                self.yDir = 0
                self.y_collision = True
                self.isJumping = False
                       
        if self.rect.top > WINDOW_HEIGHT:
            self.get_hit()
            if self.lives > 0:
                self.xPos, self.yPos = self.position_initial
                self.rect.centerx = self.xPos
                self.rect.y = self.yPos
                self.yDir = 0
                self.animationIndex = 0
                

    def die(self):
        if self.currentState != 'DIE':
            self.currentState = 'DIE'
            self.animationIndex = 0 
            self.rect = None
            
    def get_hit(self):
        
        if self.lives > 0 and not self.isInvincible:
            self.lives -= 1
            self.currentState = 'HURT'
            self.animationIndex = 0
            self.isInvincible = True
            self.invincibleTimer = invicible_time
            music.animations_sounds("hurt1")  # duração da invencibilidade em frames (1 segundo, se fps=60)

        if self.lives <= 0:
           self.currentState = 'DIE'
           self.animationIndex = 0
           self.invincibleTimer = 0


        
    def checkEnemyCollisions(self, enemies):
        # Check for collisions between hero and all enemies in the spritegroup
        collidedSprites = pygame.sprite.spritecollide(self, enemies, False)
        for enemy in collidedSprites:
            if self.currentState == 'ATTACK'and self.attack_hitbox and self.attack_hitbox.colliderect(enemy.hitbox):
                music.animations_sounds("ataquecomhit")
                enemy.die()
                
            else:
                if enemy.currentState == 'ATTACK' and self.currentState != 'DIE':
                    if enemy.attack_hitbox.colliderect(self.hitbox):
                        self.get_hit()

                if enemy.currentState != 'DYING' and self.currentState != 'DIE':
                    if self.hitbox.colliderect(enemy.hitbox):
                        self.get_hit()

    def checkNpcCollisions(self, npc):
        # Check for collisions between hero and all enemies in the spritegroup
        collidedSprites = pygame.sprite.spritecollide(self, npc, False)
        for npc in collidedSprites:
                    if self.hitbox.colliderect(npc.hitbox):
                        npc.show_interaction = True # aparecer o texto de interação do npc da loja
                        self.contato_dialogo = True # aparecer o texto de interação do npc da pergunta
                        self.falou_com_npc = True 
                    else:
                        self.contato_dialogo = False
                        npc.show_interaction = False


    def checkpower_apps(self, apps):
        collided_apps_Sprites = pygame.sprite.spritecollide(self, apps, False)
        for apps in collided_apps_Sprites:
            if self.hitbox.colliderect(apps.hitbox):
                music.animations_sounds("pegar_moeda")
                self.coins_count += 1
                apps.die()

    def checkportalcontato(self,portal):
        collided_portal_Sprites = pygame.sprite.spritecollide(self, portal, False)
        for portal in collided_portal_Sprites:
            if self.hitbox.colliderect(portal.hitbox):
                portal.portal_show_interaction = True
            else:
                portal.portal_show_interaction = False

    def checkpower_apps_health(self, health):
        collided_health_Sprites = pygame.sprite.spritecollide(self, health, False)
        for health in collided_health_Sprites:
          
          if self.health == False:
            if self.hitbox.colliderect(health.hitbox):
                music.animations_sounds("pegar_moeda")
                self.health = True
                health.die()
    
        
         

        
################################################################################################################################################
# animação da tela de entrada do Jogo
    def update_dummy(self):
        # Inicializa contadores se não existirem
        if not hasattr(self, "dummy_timer"):
            self.dummy_timer = 0
            self.dummy_state_duration = 120  # duração do estado atual em frames (~2 segundos a 60 fps)
            self.dummy_action = 'IDLE'  # Estado inicial
            self.facingRight = True

        self.dummy_timer += 1

        # Alterna ações automaticamente após um tempo
        if self.dummy_timer > self.dummy_state_duration:
            self.dummy_timer = 0
            self.dummy_state_duration = random.randint(90, 180)  # próxima duração
            self.dummy_action = random.choice(['IDLE', 'RUN'])

        # Animações e movimentação
        self.previousState = self.currentState

        # Aplica a ação atual
        if self.dummy_action == 'IDLE':
            self.currentState = 'IDLE'
        elif self.dummy_action == 'RUN':
            self.currentState = 'RUN'
            self.xPos += 2 if self.facingRight else -2
            if self.xPos > 700:
                self.facingRight = False
            elif self.xPos < 200:
                self.facingRight = True
       
        # Atualiza animação
        self.selectAnimation()
        if self.previousState != self.currentState:
            self.animationIndex = 0

        self.image = self.currentAnimation[int(self.animationIndex)]
        self.animationIndex += self.animationSpeed
        if self.animationIndex >= len(self.currentAnimation):
            self.animationIndex = 0

        self.rect = pygame.Rect(self.xPos - 22, self.yPos - 52, 44, 52)


       
