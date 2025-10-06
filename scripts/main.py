import pygame
from Config import *
from ClassLevel1 import *
from ClassMenu import Menu
from AnimatedText import *

def main():
    pygame.init()
    clock = pygame.time.Clock()
    displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Statistcsamurai")

    current_level = None
    show_menu = True
    confirm_exit = False

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

    def start_game(level_instance):
        nonlocal current_level, show_menu
        current_level = level_instance
        show_menu = False

    menu = Menu(displaySurface, start_game, font_path, font_size=24)

    isGameRunning = True

    while isGameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGameRunning = False

            elif event.type == pygame.KEYDOWN:
                # Confirmação de saída
                if confirm_exit:
                    result = exit_menu.handle_input(event)
                    if result == "SAIR":
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

                # ESC padrão
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

                #  Se estiver em cutscene, passa os eventos para ela
                if current_level is not None and hasattr(current_level, "cutscene_active"):
                    if current_level.cutscene_active:
                        current_level.cutscene.handle_input(event)

                # Eventos do menu
                if show_menu and not confirm_exit:
                    menu.handle_input(event)

        # --- Lógica e desenho ---
        if show_menu:
            menu.draw()
        else:
            if current_level is not None:
                current_level.update(confirm_exit=confirm_exit)
                current_level.draw()


                # Mensagem de morte
                keys = pygame.key.get_pressed()
                if hasattr(current_level.hero.sprite, "lives") and current_level.hero.sprite.lives <= 0:
                    reset_msg.draw()
                    reset_msg.update()
                    if keys[pygame.K_r]:
                        current_level.reset()

        # Confirmação de saída sobreposta
        if confirm_exit:
            exit_menu.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
