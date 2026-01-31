import math
import random
import pygame
from pygame import mixer
import os
import asyncio

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))
fullscreen = False  # Track fullscreen state

# Backgrounds
background = pygame.image.load('background.png')
game_over_background = pygame.image.load('game_over_background.png')  # New background for game over screen

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score and Level
score_value = 0
level = 1
high_score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
small_font = pygame.font.Font('freesansbold.ttf', 24)
textX = 10
testY = 10

# Load high score from file
def load_high_score():
    try:
        with open('highscore.txt', 'r') as f:
            return int(f.read())
    except:
        return 0

# Save high score to file
def save_high_score(score):
    with open('highscore.txt', 'w') as f:
        f.write(str(score))

# Calculate level based on score
def calculate_level(score):
    if score < 20:
        return 1
    elif score < 70:
        return 2
    elif score < 150:
        return 3
    elif score < 250:
        return 4
    else:
        return 5 + (score - 250) // 120

# Get enemy speed based on level
def get_enemy_speed(level):
    return 3 + (level * 0.5)  # Gradually increase speed

high_score = load_high_score()

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
restart_font = pygame.font.Font('freesansbold.ttf', 32)

# Function to display the score, level, and high score
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
    
    level_text = small_font.render("Level: " + str(level), True, (255, 255, 0))
    screen.blit(level_text, (x, y + 40))
    
    high_score_text = small_font.render("High Score: " + str(high_score), True, (0, 255, 255))
    screen.blit(high_score_text, (x, y + 70))

# Function to draw the player
def player(x, y):
    screen.blit(playerImg, (x, y))

# Function to draw an enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Function to fire the bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Function to check for collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

# Function to reset the game
def reset_game():
    global playerX, playerY, playerX_change, bulletX, bulletY, bullet_state, score_value, game_over, level, high_score
    global enemyX, enemyY, enemyX_change, enemyY_change
    
    # Update and save high score if needed
    if score_value > high_score:
        high_score = score_value
        save_high_score(high_score)
    
    # Reset player
    playerX = 370
    playerY = 480
    playerX_change = 0
    
    # Reset bullet
    bulletX = 0
    bulletY = 480
    bullet_state = "ready"
    
    # Reset score and level
    score_value = 0
    level = 1
    
    # Reset game over flag
    game_over = False
    
    # Reset enemies
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 736)
        enemyY[i] = random.randint(50, 150)
        enemyX_change[i] = get_enemy_speed(level)
        enemyY_change[i] = 40

# Function to show restart message
def show_restart_message():
    restart_text = restart_font.render("Press ENTER to Play Again", True, (285, 285, 255))
    screen.blit(restart_text, (180, 350))
    fullscreen_text = restart_font.render("Press F to Toggle Fullscreen", True, (255, 255, 255))
    screen.blit(fullscreen_text, (150, 400))

# Game Loop
async def main():
    global playerX, playerY, playerX_change, bulletX, bulletY, bullet_state, score_value, game_over, level, high_score
    global enemyX, enemyY, enemyX_change, enemyY_change, fullscreen, screen
    
    running = True
    game_over = False  # Added flag to check if game is over

    while running:

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystroke events
        if event.type == pygame.KEYDOWN:
            # Toggle fullscreen with F key
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((800, 600))
            
            # Restart game if game over and Enter is pressed
            if event.key == pygame.K_RETURN and game_over:
                reset_game()
            
            if not game_over:
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if not game_over:
        # Background color and image
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        # Player movement boundaries
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy movement and game over condition
        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                game_over = True  # Set the game over flag to True
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            # Check for collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                
                # Update high score in real-time
                if score_value > high_score:
                    high_score = score_value
                    save_high_score(high_score)
                
                # Check for level progression
                new_level = calculate_level(score_value)
                if new_level > level:
                    level = new_level
                    # Update all enemy speeds for new level
                    for j in range(num_of_enemies):
                        speed = get_enemy_speed(level)
                        if enemyX_change[j] > 0:
                            enemyX_change[j] = speed
                        else:
                            enemyX_change[j] = -speed
                
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # Bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        # Draw player and show score
        player(playerX, playerY)
        show_score(textX, testY)

    else:
        # Game over screen without "GAME OVER" text
        screen.blit(game_over_background, (0, 0))  # Show game over background
        show_restart_message()  # Show restart instructions
        # You can remove or comment out the next line to avoid displaying the "GAME OVER" text
        # game_over_text()

    pygame.display.update()
    await asyncio.sleep(0)  # Required for pygbag

asyncio.run(main())
