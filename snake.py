import pygame
import sys
import random
import os

pygame.init()
pygame.mixer.init()

# ------------------ SCREEN ------------------
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game 🐍")

# ------------------ CONSTANTS ------------------
BLOCK = 40
CRYSTALS_PER_LEVEL = 4
FPS = 12  # constant speed for all levels

# ------------------ FILE PATHS ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

background = pygame.image.load(os.path.join(BASE_DIR, "background.png")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

snake_head = pygame.image.load(os.path.join(BASE_DIR, "snake_head.png")).convert_alpha()
snake_head = pygame.transform.scale(snake_head, (BLOCK, BLOCK))

snake_body = pygame.Surface((BLOCK, BLOCK))
snake_body.fill((0, 180, 0))

crystal_img = pygame.image.load(os.path.join(BASE_DIR, "crystal.png")).convert_alpha()
crystal_img = pygame.transform.scale(crystal_img, (BLOCK, BLOCK))

# ------------------ SOUNDS ------------------
eat_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "ting.mp3"))
game_over_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "game-over.mp3"))
pygame.mixer.music.load(os.path.join(BASE_DIR, "background-music.mp3"))
pygame.mixer.music.play(-1)

# ------------------ FONT ------------------
font_path = os.path.join(BASE_DIR, "super_mario_256", "SuperMario256.ttf")
font = pygame.font.Font(font_path, 40)
level_font = pygame.font.Font(font_path, 60)
message_font = pygame.font.Font(font_path, 50)

# ------------------ CLOCK ------------------
clock = pygame.time.Clock()

# ------------------ LEVEL MESSAGES ------------------
level_messages = {
    1: "Great!", 2: "Good!", 3: "Nice!", 4: "WOW!", 5: "Awesome!",
    6: "BRAVO!", 8: "Incredible!"
}
for i in range(7, 101):
    if i not in level_messages:
        level_messages[i] = random.choice(["Good!", "Nice!", "WOW!", "Awesome!", "BRAVO!", "Incredible!"])

# ------------------ GAME VARIABLES ------------------
game_over_start_time = None  # for game-over music
paused = False
show_level = False
level_alpha = 0
level_timer = 0
current_level_display = 1
level_message = ""

# ------------------ FUNCTIONS ------------------
def spawn_food(snake):
    while True:
        pos = (
            random.randrange(0, WIDTH, BLOCK),
            random.randrange(0, HEIGHT, BLOCK)
        )
        if pos not in snake:
            return pos

def reset_game():
    global show_level, level_alpha, level_timer, current_level_display, level_message
    snake = [(200, 200), (160, 200), (120, 200)]
    direction = (BLOCK, 0)
    next_direction = direction
    food = spawn_food(snake)
    score = 0
    level = 1
    show_level = True
    level_alpha = 0
    level_timer = pygame.time.get_ticks()
    current_level_display = 1
    level_message = ""
    return snake, direction, next_direction, food, score, level

def draw_text_center(text, font_obj, color, y_pos):
    surf = font_obj.render(text, True, color)
    screen.blit(surf, (WIDTH//2 - surf.get_width()//2, y_pos))

# ------------------ MAIN MENU ------------------
def main_menu():
    while True:
        screen.fill((0, 0, 50))
        draw_text_center("Welcome to MR.Snaker", level_font, (255, 215, 0), HEIGHT//3)
        mx, my = pygame.mouse.get_pos()
        
        # Start Button hover effect
        start_text = "START"
        start_surf = font.render(start_text, True, (255, 255, 255))
        start_rect = start_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
        if start_rect.collidepoint((mx, my)):
            start_surf = font.render(start_text, True, (255, 215, 0))
        screen.blit(start_surf, start_rect)
        
        # Quit Button hover effect
        quit_text = "QUIT"
        quit_surf = font.render(quit_text, True, (255, 255, 255))
        quit_rect = quit_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
        if quit_rect.collidepoint((mx, my)):
            quit_surf = font.render(quit_text, True, (255, 215, 0))
        screen.blit(quit_surf, quit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint((mx, my)):
                    return
                if quit_rect.collidepoint((mx, my)):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)

# ------------------ GAME START ------------------
main_menu()
snake, direction, next_direction, food, score, level = reset_game()
game_over = False

# ------------------ MAIN LOOP ------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            if game_over and event.key == pygame.K_r:
                snake, direction, next_direction, food, score, level = reset_game()
                game_over = False
                paused = False
            if not game_over and not paused:
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, BLOCK):
                    next_direction = (0, -BLOCK)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -BLOCK):
                    next_direction = (0, BLOCK)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (BLOCK, 0):
                    next_direction = (-BLOCK, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-BLOCK, 0):
                    next_direction = (BLOCK, 0)

    # ------------------ GAME OVER BUTTON HOVER ------------------
    mx, my = pygame.mouse.get_pos()

    if not paused and not game_over:
        direction = next_direction
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            eat_sound.play()
            food = spawn_food(snake)
            new_level = (score // CRYSTALS_PER_LEVEL) + 1
            if new_level > level:
                level = new_level
                show_level = True
                level_alpha = 0
                level_timer = pygame.time.get_ticks()
                current_level_display = level
                level_message = level_messages.get(level, "")
        else:
            snake.pop()

        if (new_head in snake[1:] or new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT):
            if not game_over:
                pygame.mixer.music.stop()
                game_over_sound.play()
                game_over_start_time = pygame.time.get_ticks()
            game_over = True

    # ------------------ DRAW ------------------
    screen.blit(background, (0, 0))
    screen.blit(crystal_img, food)
    for i, seg in enumerate(snake):
        if i == 0:
            screen.blit(snake_head, seg)
        else:
            screen.blit(snake_body, seg)

    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (20, 20))

    if show_level:
        elapsed = pygame.time.get_ticks() - level_timer
        if elapsed < 800:
            level_alpha += 8
        elif elapsed < 1800:
            level_alpha = 255
        elif elapsed < 2600:
            level_alpha -= 8
        else:
            show_level = False
        surf = level_font.render(f"LEVEL {current_level_display}", True, (255, 215, 0))
        surf.set_alpha(max(0, min(255, level_alpha)))
        screen.blit(surf, (WIDTH//2 - 120, 50))
        if level_message != "":
            msg_surf = message_font.render(level_message, True, (255, 215, 0))
            msg_surf.set_alpha(max(0, min(255, level_alpha)))
            screen.blit(msg_surf, (WIDTH//2 - msg_surf.get_width()//2, 130))

    if paused:
        pause_surf = level_font.render("PAUSED", True, (255, 215, 0))
        screen.blit(pause_surf, (WIDTH//2 - pause_surf.get_width()//2, HEIGHT//2 - 50))

    if game_over:
        screen.blit(font.render("GAME OVER", True, (255, 0, 0)), (WIDTH//2 - 120, HEIGHT//2 - 60))
        screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (WIDTH//2 - 100, HEIGHT//2))
        screen.blit(font.render(f"Level Reached: {level}", True, (255, 255, 255)), (WIDTH//2 - 130, HEIGHT//2 + 50))
        screen.blit(font.render("Press R to Restart", True, (255, 255, 255)), (WIDTH//2 - 150, HEIGHT//2 + 100))

        # Main Menu Button hover effect
        main_menu_text = "MAIN MENU"
        text_surf = font.render(main_menu_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 180))
        if text_rect.collidepoint((mx, my)):
            text_surf = font.render(main_menu_text, True, (255, 215, 0))
        screen.blit(text_surf, text_rect)

        # Check click on Main Menu
        if pygame.mouse.get_pressed()[0]:
            if text_rect.collidepoint((mx, my)):
                main_menu()
                snake, direction, next_direction, food, score, level = reset_game()
                game_over = False
                paused = False
                pygame.mixer.music.play(-1)

    # Resume background music after game over music
    if game_over and game_over_start_time is not None:
        elapsed = (pygame.time.get_ticks() - game_over_start_time) / 1000
        if elapsed >= game_over_sound.get_length():
            pygame.mixer.music.play(-1)
            game_over_start_time = None

    pygame.display.update()
    clock.tick(FPS)