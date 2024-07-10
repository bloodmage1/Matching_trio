import pygame
from settings import screen, BLACK, WHITE, NANUM_FONT, SCREEN_HEIGHT

menu_buttons = {}

def create_menu_buttons():
    global menu_buttons
    button_size = 120
    menu_buttons['rule'] = pygame.Rect(0, 0, button_size, button_size)
    menu_buttons['rule'].center = (120, SCREEN_HEIGHT - 540)
    menu_buttons['mode1'] = pygame.Rect(0, 0, button_size, button_size)
    menu_buttons['mode1'].center = (120, SCREEN_HEIGHT - 360)
    menu_buttons['mode2'] = pygame.Rect(0, 0, button_size, button_size)
    menu_buttons['mode2'].center = (120, SCREEN_HEIGHT - 180)

create_menu_buttons()

def display_menu():
    screen.fill(BLACK)
    labels = ['Rule', 'Mode1', 'Mode2']
    for idx, (key, button) in enumerate(menu_buttons.items()):
        pos = pygame.mouse.get_pos()
        if button.collidepoint(pos):
            pygame.draw.circle(screen, WHITE, button.center, button.width // 2 - 10, 5)
            pygame.draw.circle(screen, WHITE, button.center, button.width // 2 - 10)
        else:
            pygame.draw.circle(screen, WHITE, button.center, button.width // 2, 5)

        text_surface = NANUM_FONT.render(labels[idx], True, BLACK if button.collidepoint(pos) else WHITE)
        text_rect = text_surface.get_rect(center=button.center)
        screen.blit(text_surface, text_rect)