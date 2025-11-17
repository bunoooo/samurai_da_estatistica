import pygame
from scripts.Config import *
from scripts.Musicmanager import *
from scripts.ClassMenu import Menu
from scripts.ClassLevel1 import *
from scripts.AnimatedText import *




# Lista de fases disponíveis
fases = [
    Tutorial,   
    Level1,     
    Level2,     
    Level3, 
    Level4, 
    Level5,
    Level6   
]

music = MusicManager()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Statisticsamurai")

    current_level = None
    show_menu = True
    confirm_exit = False
    
    result = None

    font = pygame.font.Font(font_path, 15)

    reset_msg = AnimatedText(
        text="Você morreu... Aperte R para reiniciar ou ESC para voltar ao menu",
        font=font,
        color=(255, 255, 255),
        surface=displaySurface,
        speed=0.5,
        duration=999999999999999999999999999999
    )

    exit_menu = ExitMenu(displaySurface, font)

    # Cria o menu principal
    menu = Menu(displaySurface, None, font_path, font_size=24)
    menu.id_fase = 0  # começa no tutorial

    def start_game(level_instance=None):
        """Função chamada pelo menu para iniciar o jogo."""
        nonlocal current_level, show_menu

        # Define a fase atual de acordo com o menu.id_fase
        if menu.id_fase < len(fases):
            current_level = fases[menu.id_fase](displaySurface, fase_id=menu.id_fase)
        else:
            current_level = fases[0](displaySurface, fase_id=0)

        show_menu = False

        music.tocar_musica(menu.id_fase)

    # Passa a função de início para o menu
    menu.start_game_callback = start_game

    isGameRunning = True

    while isGameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGameRunning = False

            elif event.type == pygame.KEYDOWN:
                # --- Confirmação de saída ---
                if confirm_exit:
                    result = exit_menu.handle_input(event)
                    if result == "SAIR":
                        music.tocar_musica(0)
                        show_menu = True
                        current_level = None
                        confirm_exit = False
                        menu.state = "principal"
                        menu.selected_index = 0
                        menu.buttons = [
                            ("entrar", menu.entrar_text_rect),
                            ("tutorial", menu.tutorial_rect),
                            ("fases", menu.fases_rect),
                            ("sair", menu.sair_rect),
                        ]
                    elif result == "NÃO":
                        confirm_exit = False
                    continue

                # --- ESC padrão ---
                if event.key == pygame.K_ESCAPE:
                    if show_menu and menu.state == "inicio":
                        isGameRunning = False
                    else:
                        if not show_menu:
                            confirm_exit = True
                        elif menu.state in ["tutorial_texto", "fases"]:
                            menu.state = "principal"
                            menu.selected_index = 0
                            menu.buttons = [
                                ("entrar", menu.entrar_text_rect),
                                ("tutorial", menu.tutorial_rect),
                                ("fases", menu.fases_rect),
                                ("sair", menu.sair_rect),
                            ]

                # --- Passa eventos para cutscene ---
                if current_level is not None and hasattr(current_level, "cutscene_active") :
                    if current_level.cutscene_active:
                        current_level.cutscene.handle_input(event)
                    
                    if hasattr(current_level , "cutscene_final_active"):
                            if current_level.cutscene_final_active:
                                current_level.cutscene_final.handle_input(event)
                                if current_level.cutscene_final.finished:
                                
                                    show_menu = True
                                    current_level = None
                                    menu.state = "principal"
                                    menu.selected_index = 0
                                    menu.buttons = [
                                        ("entrar", menu.entrar_text_rect),
                                        ("tutorial", menu.tutorial_rect),
                                        ("fases", menu.fases_rect),
                                        ("sair", menu.sair_rect),
                                    ]
                                    music.tocar_musica(0)  # música do menu

                # --- Eventos do menu ---
                if show_menu and not confirm_exit:
                    menu.handle_input(event)

        # --- Lógica principal ---
        if show_menu:
            menu.draw()
            if not pygame.mixer.music.get_busy() :
                 music.tocar_musica(0)
            
        else:
            if current_level is not None:
                current_level.update(confirm_exit=confirm_exit)
                current_level.draw()

                # --- TROCA DE FASE ---
                if current_level.verificar_prox_fase == "next_level":
                    menu.id_fase += 1  # avança para a próxima fase
                    if menu.id_fase < len(fases):
                        current_level = fases[menu.id_fase](displaySurface, fase_id=menu.id_fase)
                        music.tocar_musica(menu.id_fase) 
                    else:
                        # Todas as fases concluídas → volta ao menu
                        current_level = None
                        show_menu = True
                        menu.id_fase = 0
                        music.tocar_musica(menu.id_fase) 
                        
                # --- Morte do jogador ---
                keys = pygame.key.get_pressed()
                if hasattr(current_level.hero.sprite, "lives") and current_level.hero.sprite.lives <= 0:
                    reset_msg.draw()
                    reset_msg.update()
                    if keys[pygame.K_r]:
                        current_level.reset()
                        music.tocar_musica(menu.id_fase)

        # --- Confirmação de saída ---
        if confirm_exit:
            exit_menu.draw()

        pygame.display.flip()
        clock.tick(60)
        

    pygame.quit()

if __name__ == "__main__":
    main()
