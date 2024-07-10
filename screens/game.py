import pygame
from random import shuffle, randrange
from settings import screen, BLACK, WHITE, GRAY, RED, GAME_FONT, NANUM_FONT, SCREEN_WIDTH, SCREEN_HEIGHT

level = 1
display_time = 5.0
number_groups = []
hidden = False
start_ticks = None
current_group = None
wrong_click = False
showing_wrong = False

def setup_game():
    global display_time, number_groups, hidden, start_ticks, current_group, wrong_click, showing_wrong
    number_groups = shuffle_grid(3)
    hidden = False
    start_ticks = pygame.time.get_ticks()
    current_group = None
    wrong_click = False
    showing_wrong = False
    if display_time > 3:
        display_time -= 0.5

def shuffle_grid(number_count):
    rows, columns = 5, 9
    cell_size = 130
    button_size = 110
    screen_left_margin = 55
    screen_top_margin = 20

    grid = [[0 for _ in range(columns)] for _ in range(rows)]
    number_buttons = []
    numbers = [num for num in range(1, number_count + 1) for _ in range(3)]
    shuffle(numbers)

    for number in numbers:
        placed = False
        while not placed:
            row_idx = randrange(rows)
            col_idx = randrange(columns)
            if grid[row_idx][col_idx] == 0:
                grid[row_idx][col_idx] = number
                placed = True

                center_x = screen_left_margin + (col_idx * cell_size) + (cell_size / 2)
                center_y = screen_top_margin + (row_idx * cell_size) + (cell_size / 2)
                button = pygame.Rect(0, 0, button_size, button_size)
                button.center = (center_x, center_y)
                number_buttons.append((button, number))
    groups = {num: [] for num in range(1, number_count + 1)}
    for button, number in number_buttons:
        groups[number].append(button)

    final_groups = [group for group in groups.values()]
    return final_groups

def display_game_screen():
    global hidden, wrong_click, showing_wrong, back_button, display_time, level
    screen.fill(BLACK)
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

    if not hidden and elapsed_time > display_time:
        hidden = True

    if 0 < elapsed_time <= display_time:
        time_text = NANUM_FONT.render(f"Time: {display_time - elapsed_time:.1f}", True, WHITE)
        screen.blit(time_text, (SCREEN_WIDTH - 150, 20))

    all_cleared = all(len(group) == 0 for group in number_groups)
    if all_cleared:
        if display_time > 3:
            display_time -= 0.5
            message = f"축하합니다. 숫자를 모두 맞추셨습니다. 다음 레벨로 넘어갑니다"
            level += 1
        else:
            message = "축하합니다. 당신은 기억력 챔피언입니다."
            current_screen = 'menu'
        message_text = NANUM_FONT.render(message, True, WHITE)
        screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        setup_game()
        return

    if elapsed_time > 0:
        for group in number_groups:
            for rect in group:
                if hidden:
                    pygame.draw.rect(screen, GRAY, rect)
                else:
                    number = number_groups.index(group) + 1
                    cell_text = GAME_FONT.render(str(number), True, WHITE)
                    text_rect = cell_text.get_rect(center=rect.center)
                    screen.blit(cell_text, text_rect)

    if showing_wrong:
        wrong_text = NANUM_FONT.render("Wrong", True, RED)
        screen.blit(wrong_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

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

def check_click(pos):
    global current_group, wrong_click, showing_wrong
    if current_group is None:
        for i, group in enumerate(number_groups):
            for rect in group:
                if rect.collidepoint(pos):
                    current_group = i
                    number_groups[current_group].remove(rect)
                    if not number_groups[current_group]:
                        current_group = None
                    return True
        wrong_click = True
        showing_wrong = True
        return False
    else:
        for rect in number_groups[current_group]:
            if rect.collidepoint(pos):
                number_groups[current_group].remove(rect)
                if not number_groups[current_group]:
                    current_group = None
                return True
        wrong_click = True
        showing_wrong = True
        return False