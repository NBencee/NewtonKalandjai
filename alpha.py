import pygame
import random
import json
import math
import datetime

pygame.init()

WIDTH = 1920
HEIGHT = 1080

# Load images and double their sizes
NEWTON_IMAGE = pygame.transform.scale(pygame.image.load("newton.png"), (150, 150))
APPLE_IMAGE = pygame.transform.scale(pygame.image.load("apple.png"), (100, 100))

BKG_COLOR = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load game background
game_bg = pygame.image.load("game_bg.png")
game_bg = pygame.transform.scale(game_bg, (WIDTH, HEIGHT))

player_size = 150
player_pos = [WIDTH / 2, HEIGHT - 2 * player_size]

enemy_size = 100
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]
SPEED = 10

score = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

clock = pygame.time.Clock()

# Load font
FONT = pygame.font.Font("level-up.otf", 72)

# Function to save scores to a JSON file
def save_scores(scores):
    with open('scores.json', 'w') as file:
        json.dump(scores, file)

# Function to load scores from a JSON file
def load_scores():
    try:
        with open('scores.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {}


# At the beginning of your script or where you handle initialization, load scores
scores = load_scores()

import datetime

def draw_menu():
    screen.fill(BKG_COLOR)
    
    # Load menu background
    menu_bg = pygame.image.load("wp.png")
    menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))
    screen.blit(menu_bg, (0, 0))  # Menu Background
    
    # Display big title with breathing effect and shadow
    title_text = "NEWTON GAME"
    title_label = FONT.render(title_text, True, YELLOW)
    title_rect = title_label.get_rect(center=(WIDTH / 2, HEIGHT / 4))
    
    # Calculate breathing effect for the title text
    breathing = int(5 * (1 + math.sin(pygame.time.get_ticks() / 300)))
    
    # Create white shadow text for the title
    shadow_label = FONT.render(title_text, True, WHITE)
    shadow_rect = shadow_label.get_rect(center=(title_rect.centerx + breathing, title_rect.centery + breathing))
    
    # Draw shadow text for the title
    screen.blit(shadow_label, shadow_rect)
    
    # Draw title text with black stroke
    outline_label = FONT.render(title_text, True, BLACK)
    outline_rect = outline_label.get_rect(center=(title_rect.centerx + 2, title_rect.centery + 2))
    screen.blit(outline_label, outline_rect)
    
    # Draw the "NEWTON GAME" message
    screen.blit(title_label, title_rect)

    # Display instruction to play with breathing 3D effect
    text_play = "Press SPACE to play"
    label_play = FONT.render(text_play, True, WHITE)
    
    # Calculate scaling for the 3D effect
    scale_factor = 1 + 0.1 * math.sin(pygame.time.get_ticks() / 300)
    
    # Create a scaled version of the text surface
    scaled_text = pygame.transform.scale(label_play, (int(label_play.get_width() * scale_factor), int(label_play.get_height() * scale_factor)))
    
    # Get the rect for the scaled text and center it on the screen
    text_rect = scaled_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    
    # Draw the scaled text
    screen.blit(scaled_text, text_rect)

    # Display developer credits on the bottom left with black outline
    developer_text = "Developers: H. Andris, N. Bence, Z. Botond (10)"
    developer_label = pygame.font.Font("level-up.otf", 28).render(developer_text, True, WHITE)
    developer_rect = developer_label.get_rect(bottomleft=(20, HEIGHT - 20))
    
    # Draw developer text with black outline
    outline_thickness = 2
    outline_rect = developer_rect.inflate(outline_thickness * 2, outline_thickness * 2)
    pygame.draw.rect(screen, BLACK, outline_rect)
    screen.blit(developer_label, developer_rect)

    # Display copyright notice on the bottom right with black outline
    copyright_text = "Copyright Kenyer CO. Do not distribute! v0.91"
    copyright_label = pygame.font.Font("level-up.otf", 20).render(copyright_text, True, WHITE)
    copyright_rect = copyright_label.get_rect(bottomright=(WIDTH - 20, HEIGHT - 20))
    
    # Draw copyright text with black outline
    outline_rect = copyright_rect.inflate(outline_thickness * 2, outline_thickness * 2)
    pygame.draw.rect(screen, BLACK, outline_rect)
    screen.blit(copyright_label, copyright_rect)

    # Display current time in the top right corner
    current_time = datetime.datetime.now().strftime("UTC+1: %H:%M:%S")
    time_label = pygame.font.Font("level-up.otf", 30).render(current_time, True, WHITE)
    time_rect = time_label.get_rect(topright=(WIDTH - 20, 20))
    screen.blit(time_label, time_rect)

    pygame.display.update()

def start_level(level):
    global enemy_size, SPEED
    if level == 1:
        enemy_size = 150
        SPEED = 6
    elif level == 2:
        enemy_size = 100
        SPEED = 10
    elif level == 3:
        enemy_size = 50
        SPEED = 15

def GAME_OVER(score):
    screen.fill(BKG_COLOR)
    
    # Draw game background
    screen.blit(game_bg, (0, 0))  # Game Background
    
    # Display "GAME OVER" message with stroke
    text = "GAME OVER!"
    label = FONT.render(text, True, YELLOW)
    label_rect = label.get_rect(center=(WIDTH / 2, HEIGHT / 3))
    
    # Double the font size for the "GAME OVER" message
    label = pygame.transform.scale(label, (label.get_width() * 2, label.get_height() * 2))
    label_rect = label.get_rect(center=(WIDTH / 2, HEIGHT / 3))
    
    # Render black stroke for the text
    outline_label = FONT.render(text, True, BLACK)
    outline_rect = outline_label.get_rect(center=(label_rect.centerx + 2, label_rect.centery + 2))
    
    # Double the font size for the stroke
    outline_label = pygame.transform.scale(outline_label, (outline_label.get_width() * 2, outline_label.get_height() * 2))
    outline_rect = outline_label.get_rect(center=(label_rect.centerx + 2, label_rect.centery + 2))
    
    # Draw black stroke text
    screen.blit(outline_label, outline_rect)
    
    # Draw the "GAME OVER" message
    screen.blit(label, label_rect)

    # Display the score with stroke
    text_score = "Your Score: " + str(score)
    label_score = FONT.render(text_score, True, YELLOW)
    label_score_rect = label_score.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 100))
    
    # Render black stroke for the score
    outline_label_score = FONT.render(text_score, True, BLACK)
    outline_rect_score = outline_label_score.get_rect(center=(label_score_rect.centerx + 2, label_score_rect.centery + 2))
    
    # Draw black stroke score
    screen.blit(outline_label_score, outline_rect_score)
    
    # Draw the score
    screen.blit(label_score, label_score_rect)

    # Display instructions to restart with stroke
    text_restart = "Press SPACE to restart."
    label_restart = FONT.render(text_restart, True, YELLOW)
    label_restart_rect = label_restart.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 200))
    
    # Render black stroke for the restart text
    outline_label_restart = FONT.render(text_restart, True, BLACK)
    outline_rect_restart = outline_label_restart.get_rect(center=(label_restart_rect.centerx + 2, label_restart_rect.centery + 2))
    
    # Draw black stroke restart text
    screen.blit(outline_label_restart, outline_rect_restart)
    
    # Draw the restart text
    screen.blit(label_restart, label_restart_rect)

    pygame.display.update()

def set_level(score, SPEED):
    if score < 3:
        SPEED = 6
    elif score < 10:
        SPEED = 8
    elif score < 20:
        SPEED = 10
    elif score < 35:
        SPEED = 15
    elif score < 50:
        SPEED = 20
    else:
        SPEED = 25
    return SPEED

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 1 and delay < 1:
        x_pos = random.randint(0, WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        screen.blit(APPLE_IMAGE, (enemy_pos[0], enemy_pos[1]))

def update_enemy_positions(enemy_list, score):
    for i, enemy_pos in enumerate(enemy_list):
        # Updates Enemy Position
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(i)
            score += 1
    return score

def collision_check(enemy_list, player_pos):
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for enemy_pos in enemy_list:
        enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_size, enemy_size)
        if player_rect.colliderect(enemy_rect):
            enemy_list.remove(enemy_pos)
            return True
    return False

def draw_score(score, score_changed):
    # Display score
    text = "Score: " + str(score)

    # Render white text with slight offset for outline
    label_white = FONT.render(text, True, WHITE)
    label_black = FONT.render(text, True, BLACK)

    # Check if the score changed
    if score_changed:
        # Calculate scaling factor for the pumping effect
        scale_factor = 1.2

        # Create a scaled version of the text surface for the pumping effect
        scaled_text_white = pygame.transform.scale(label_white, (int(label_white.get_width() * scale_factor), int(label_white.get_height() * scale_factor)))
        scaled_text_black = pygame.transform.scale(label_black, (int(label_black.get_width() * scale_factor), int(label_black.get_height() * scale_factor)))

        # Get the rect for the scaled text and position it in the top left corner
        text_rect = scaled_text_white.get_rect(topleft=(10, 10))

        # Draw the scaled text
        screen.blit(scaled_text_black, (text_rect.x + 2, text_rect.y + 2))  # Offset for shadow
        screen.blit(scaled_text_white, text_rect)
    else:
        # Get the rect for the text and position it in the top left corner
        text_rect = label_white.get_rect(topleft=(10, 10))

        # Draw the text
        screen.blit(label_black, (text_rect.x + 2, text_rect.y + 2))  # Offset for shadow
        screen.blit(label_white, text_rect)

def restart_game():
    global player_pos, enemy_list, score, game_over
    player_pos = [WIDTH / 2, HEIGHT - 2 * player_size]
    enemy_list = [[random.randint(0, WIDTH - enemy_size), 0]]
    score = 0
    game_over = False

running = True
menu_active = True
current_level = 1
return_to_menu = False
score_changed = False

while running:
    if menu_active:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_active = False  # Start the game
                elif event.key == pygame.K_1:
                    # Show scoreboard (you can implement this functionality)
                    pass
    else:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_pos[0] -= player_size
                elif event.key == pygame.K_RIGHT:
                    player_pos[0] += player_size
                elif event.key == pygame.K_SPACE and game_over:
                    restart_game()
                elif event.key == pygame.K_ESCAPE:
                    return_to_menu = True
                elif event.key == pygame.K_SPACE and not game_over:
                    # Pause the game (you can implement this functionality)
                    pass

        if return_to_menu:
            menu_active = True
            return_to_menu = False
            continue  # Skip the game logic if returning to the menu

        # Draw background
        screen.blit(game_bg, (0, 0))  # Game Background

        # Handle game logic
        if not game_over:
            # Update enemies and score
            drop_enemies(enemy_list)
            score = update_enemy_positions(enemy_list, score)
            SPEED = set_level(score, SPEED)

            # Check for collisions
            if collision_check(enemy_list, player_pos) is True:
                score += 1  # Increase score on collision
                score_changed = True
            else:
                score_changed = False

            # Draw enemies and player
            draw_enemies(enemy_list)
            screen.blit(NEWTON_IMAGE, (player_pos[0], player_pos[1]))

        else:
            # Game over
            GAME_OVER(score)

        # Draw score with pumping effect
        draw_score(score, score_changed)

        # Check for enemy reaching bottom
        for enemy_pos in enemy_list:
            if enemy_pos[1] > HEIGHT - player_size:
                game_over = True
                break  # Exit loop after one enemy reaches bottom

        # Update display and clock
        pygame.display.update()
        clock.tick(30)

# Save scores before quitting
save_scores(scores)

pygame.quit()
