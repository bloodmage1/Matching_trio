import pygame
from random import shuffle, randrange

pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Number Match Game')
game_font = pygame.font.Font(None, 120)
나눔고딕_path = "C:/nanum/nanumgo/NanumFontSetup_OTF_GOTHIC/NanumGothic.otf"


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255,0,0)

menu_buttons = {}
def create_menu_buttons():
    global menu_buttons
    button_size = 120
    menu_buttons['rule'] = pygame.Rect(0, 0, button_size, button_size)
    menu_buttons['rule'].center = (120, screen_height - 540)
    menu_buttons['mode1'] = pygame.Rect(0, 0, button_size, button_size)  
    menu_buttons['mode1'].center = (120, screen_height - 360)
    menu_buttons['mode2'] = pygame.Rect(0, 0, button_size, button_size)  
    menu_buttons['mode2'].center = (120, screen_height - 180)

create_menu_buttons()

number_buttons = [] 
display_time = None
start_ticks = None
hidden = False
curr_level = 1
current_group = None
showing_wrong = False

current_screen = 'menu'

def display_menu():
    screen.fill(BLACK)
    labels = ['Rule', 'Mode1', 'Mode2']
    font = pygame.font.Font(나눔고딕_path, 30)
    for idx, (key, button) in enumerate(menu_buttons.items()):
        pos = pygame.mouse.get_pos()
        if button.collidepoint(pos):
            pygame.draw.circle(screen, WHITE, button.center, button.width // 2 - 10, 5)
            pygame.draw.circle(screen, WHITE, button.center, button.width // 2 - 10)
        else:
            pygame.draw.circle(screen, WHITE, button.center, button.width // 2, 5)

        text_surface = font.render(labels[idx], True, BLACK if button.collidepoint(pos) else WHITE)
        text_rect = text_surface.get_rect(center=button.center)
        screen.blit(text_surface, text_rect)

def display_rules():
    screen.fill(BLACK)
    font = pygame.font.Font(나눔고딕_path, 32)
    rules_text = [
        "이 게임은 짝 맞추기 게임의 응용버전입니다.",
        "Mode1은 같은 숫자 3개를 맞추어야 하고 Mode2는 4개입니다.",
        "다 맞춘다면, 다음 레벨로 진행되는데 레벨이 높아질수록 시간이 짧아집니다.",
        "그럼 좋은 시간 되십시오."
    ]
    for i, text in enumerate(rules_text):
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (100, 50 + i * 50))

    back_button = pygame.Rect(screen_width - 120, screen_height - 60, 100, 50)
    pos = pygame.mouse.get_pos() 

    if back_button.collidepoint(pos):
        pygame.draw.rect(screen, BLACK, back_button)
        back_text = font.render('Back', True, WHITE)
    else:
        pygame.draw.rect(screen, WHITE, back_button)
        back_text = font.render('Back', True, BLACK)

    back_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_rect)
    return back_button

level = 1  
display_time = 5.0 

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
        display_time -= 1

def shuffle_grid(number_count):
    rows, columns = 5, 9
    cell_size = 130
    button_size = 110
    screen_left_margin = 55
    screen_top_margin = 20

    # [[0,0,0,0,0,0,0,0,0]
    # [0,0,0,0,0,0,0,0,0]
    # [0,0,0,0,0,0,0,0,0]
    # [0,0,0,0,0,0,0,0,0]
    # [0,0,0,0,0,0,0,0,0]]

    grid = [[0 for _ in range(columns)] for _ in range(rows)]
    number_buttons = []
    # numbers = list(range(1, number_count + 1)) # [1,2,3,4,5,6]
    # shuffle(numbers)
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
    print('final_groups:',final_groups)
    print('final_groups[0]:',final_groups[0])
    print('final_groups[0][0]:',final_groups[0][0])
    return final_groups

wrong_click = False

def display_game_screen():
    global hidden, wrong_click, showing_wrong, back_button, display_time, level
    screen.fill(BLACK)
    font = pygame.font.Font(나눔고딕_path, 30)
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

    if not hidden and elapsed_time > display_time: 
        hidden = True

    if 0 < elapsed_time <= display_time:  
        time_text = font.render(f"Time: {display_time - elapsed_time:.1f}", True, WHITE)
        screen.blit(time_text, (screen_width - 150, 20)) 

    all_cleared = all(len(group) == 0 for group in number_groups)  
    if all_cleared:
        if display_time > 3:
            display_time -= 0.5
            message = f"축하합니다. 숫자를 모두 맞추셨습니다. 다음 레벨로 넘어갑니다"
            level += 1
        else:
            message = "축하합니다. 당신은 기억력 챔피언입니다."
            current_screen = 'menu'  # 메뉴 화면으로 돌아가는 게 맞나?
        message_text = font.render(message, True, WHITE)
        screen.blit(message_text, (screen_width // 2 - message_text.get_width() // 2, screen_height // 2))
        pygame.display.update()
        pygame.time.delay(3000)  # 3초 
        setup_game()  
        return

    if elapsed_time > 0: 
        for group in number_groups:
            for rect in group:
                if hidden:
                    pygame.draw.rect(screen, GRAY, rect)  
                else:
                    number = number_groups.index(group) + 1
                    cell_text = game_font.render(str(number), True, WHITE)
                    text_rect = cell_text.get_rect(center=rect.center)
                    screen.blit(cell_text, text_rect) 

    if showing_wrong:
        wrong_text = font.render("Wrong", True, RED)
        screen.blit(wrong_text, (screen_width // 2 - 50, screen_height // 2))

    back_button = pygame.Rect(screen_width - 120, screen_height - 60, 100, 50)
    pos = pygame.mouse.get_pos()

    if back_button.collidepoint(pos):
        pygame.draw.rect(screen, BLACK, back_button)
        back_text = font.render('Back', True, WHITE)
    else:
        pygame.draw.rect(screen, WHITE, back_button)
        back_text = font.render('Back', True, BLACK)

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
running = True
back_button = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONUP:  # 사용자가 마우스 클릭하는 경우
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
            elif current_screen == 'game_3' and back_button and back_button.collidepoint(pos):
                current_screen = 'menu'
            elif current_screen == 'game_4' and back_button and back_button.collidepoint(pos):
                current_screen = 'menu'
            elif current_screen in ['game_3', 'game_4']:
                if showing_wrong:  
                    showing_wrong = False
                    current_screen = 'menu'
                else:
                    if not check_click(pos):
                        wrong_click = True

    if current_screen == 'menu':
        display_menu()
    elif current_screen == 'rule':
        back_button = display_rules()
    elif current_screen == 'game_3':
        back_button = display_game_screen()
    elif current_screen == 'game_4':
        back_button = display_game_screen()

    pygame.display.update()

    if wrong_click:
        pygame.time.delay(1000)
        wrong_click = False

pygame.quit()
