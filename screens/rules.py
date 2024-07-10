import pygame
from settings import screen, BLACK, WHITE, NANUM_FONT, SCREEN_WIDTH, SCREEN_HEIGHT

def display_rules():
    screen.fill(BLACK)
    rules_text = [
        "이 게임은 짝 맞추기 게임의 응용버전입니다.",
        "Mode1은 같은 숫자 3개를 맞추어야 하고 Mode2는 4개입니다.",
        "다 맞춘다면, 다음 레벨로 진행되는데 레벨이 높아질수록 시간이 짧아집니다.",
        "그럼 좋은 시간 되십시오."
    ]
    for i, text in enumerate(rules_text):
        text_surface = NANUM_FONT.render(text, True, WHITE)
        screen.blit(text_surface, (100, 50 + i * 50))

    back_button = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 60, 100, 50)
    pos = pygame.mouse.get_pos()

    if back_button.collidepoint(pos):
        pygame.draw.rect(screen, BLACK, back_button)
        back_text = NANUM_FONT.render('Back', True, WHITE)
    else:
        pygame.draw.rect(screen, WHITE, back_button)
        back_text = NANUM_FONT.render('Back', True, BLACK)

    back_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_rect)
    return back_button