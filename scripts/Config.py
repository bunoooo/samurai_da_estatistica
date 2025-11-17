import os
import sys

def resource_path(relative_path):
    """Permite que paths funcionem no .exe e no .py."""
    if hasattr(sys, '_MEIPASS'):  # Quando rodando no .exe
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)  # Quando rodando no .py


# ========== ASSETS ==========
SPRITESHEET_PATH = resource_path("SPRITES SAMURAI/background/")
LEVELS_PATH      = resource_path("Levels/")

samurai_path     = resource_path("SPRITES SAMURAI/oldsamurai/")
menu_path        = resource_path("SPRITES SAMURAI/menu_img/")
menu_path1       = resource_path("SPRITES SAMURAI/menu_img/sakura/")
font_path        = resource_path("SPRITES SAMURAI/menu_img/TrueType/go3v2.ttf")

hud_path         = resource_path("SPRITES SAMURAI/menu_img/HUD/")
robot_path       = resource_path("SPRITES SAMURAI/robot/")
loja_path        = resource_path("SPRITES SAMURAI/loja_sprites/")
image_path       = resource_path("SPRITES SAMURAI\\cutscenes\\")

portal_path      = resource_path("SPRITES SAMURAI/portal/")
crow_path        = resource_path("SPRITES SAMURAI/crow/")
reaper_path      = resource_path("SPRITES SAMURAI/reaper/")
erradon_path     = resource_path("SPRITES SAMURAI/Evil wizard (erradon)/")
samuraigirl_path = resource_path("SPRITES SAMURAI/samuraigirl/")

# ========== LEVEL-SPECIFIC ENEMIES ==========
skeleton_path     = resource_path("Levels/Tilesets/enemies_level2/")
zombie_path       = resource_path("Levels/Tilesets/enemies_level4/")
samuraixamom_path = resource_path("Levels/Tilesets/enemies_level5/")

# ========== MUSIC ==========
music_path = resource_path("Levels/Music_levels/")

# ========== GRÁFICOS ==========
graficos_path = resource_path("graficos/")


# ========== WINDOW SETTINGS ==========
WINDOW_WIDTH, WINDOW_HEIGHT = 960, 540

TILESIZE = 16
GRAVITY = 0.6
GRAVITY_Player = 0.2

SPEED_HERO = 4
ANIMSPEED_HERO_DEFAULT = 0.2
ANIMSPEED_HERO_IDLE = 0.1
ANIMSPEED_HERO_JUMP_FALL = 0.1
ANIMSPEED_HERO_HURT = 0.09
ANIMSPEED_HERO_DIE = 0.1
ANIMSPEED_HERO_ATTACK = 0.2

JUMP_NORMAL = -5
JUMP_WITH_RUN = -8

LIVES = 4
invicible_time = 300

SPEED_BEE = 2
ANIMSPEED_BEE = 0.2
ANIMSPEED_BEE_ATTACK = 0.5

SPEED_ROBOT = 1
