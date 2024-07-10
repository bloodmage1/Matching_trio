import pygame
from settings import screen, SCREEN_WIDTH, SCREEN_HEIGHT
from screens.menu import display_menu, create_menu_buttons, menu_buttons
from screens.rules import display_rules
from screens.game import display_game_screen, setup_game, check_click

pygame.init()
current_screen = 'menu'
create_menu_buttons()
running = True
back_button = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if current_screen == 'menu':
                if menu_buttons['rule'].collidepoint(pos):
                    current_screen = 'rule'
                elif menu_buttons['mode1'].collidepoint(pos):
                    setup_game()
                    current_screen = 'game_3'
                elif menu_buttons['mode2'].collidepoint(pos):
                    setup_game()
                    current_screen = 'game_4'
            elif current_screen == 'rule' and back_button and back_button.collidepoint(pos):
                current_screen = 'menu'
            elif current_screen in ['game_3', 'game_4'] and back_button and back_button.collidepoint(pos):
                current_screen = 'menu'
            elif current_screen in ['game_3', 'game_4']:
                if not check_click(pos):
                    pass

    if current_screen == 'menu':
        display_menu()
    elif current_screen == 'rule':
        back_button = display_rules()
    elif current_screen in ['game_3', 'game_4']:
        back_button = display_game_screen()

    pygame.display.update()

pygame.quit()