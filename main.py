import pygame
import random
import math
from pygame import mixer

# mixer is for music and audios

#initialize pygame module
pygame.init()

# creating the game window 
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('Space/bg2.jpg')
mixer.music.load('Space/bgmusic.wav')
mixer.music.play(-1)                        # plays the sound on loop

# Title and icon of the window
pygame.display.set_caption("My First PyGame")
icon = pygame.image.load('Space/car-icon.png')       # from flaticon website
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('Space/spaceship.png')
playerX = 368
# X coordinate of player; (800px - 64px) / 2; screen is 800px wide and picture is 64px wide
playerY = 500
playerY_change = 0
playerX_change = 0

# Enemy
num_enemies = 6
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(num_enemies):
    enemyImg.append(pygame.image.load('Space/alien2.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(20, 100))
    enemyX_change.append(1)
    enemyY_change.append(45)

# for Bullet
bulletImg = pygame.image.load('Space/bullet1.png')
bulletX = 0
bulletY = playerY
bulletX_change = 0.5
bulletY_change = 2.5
bullet_state = "ready"

def player(xPos, yPos):
    screen.blit(playerImg, (xPos, yPos))       # blit() means to draw

def enemy(xPos, yPos, i):
    screen.blit(enemyImg[i], (xPos, yPos))       # blit() means to draw

def fire_bullet(xPos, yPos):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (xPos + 16, yPos + 10))      
    # x+16 so that it fires from the center and y+10 so that it fires not from the center of our spaceship but from its upper tip

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((bulletX - enemyX), 2) + math.pow((bulletY - enemyY), 2))

    if distance < 15:
        return True
    return False

# Score
current_score = 0
font = pygame.font.Font('Space/Squids.ttf', 32)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score: " + str(current_score), True, (255,255,255))
    screen.blit(score, (x, y))

gameOver_font = pygame.font.Font('Space/Squids.ttf', 48)
over = False
game_over_sound = mixer.Sound('Space/gameover.wav')

def gameOver():
    over_text = gameOver_font.render("Game Over :(", True, (240, 145, 78))
    screen.blit(over_text, (200, 250))
    global over
    over = True
        


# game loop, window exits or stays
running = True
count = 0
while running:

    screen.fill((0, 0, 0))                          # RGB background of screen
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    
        # keystroke events are pygame events and gets stored in "pygame.event.get()"
        # pygame.KEYDOWN means any key or button has been pressed on the keyboard
        # pygame.KEYUP is for the event when the pressed key is released

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            elif event.key == pygame.K_RIGHT:
                playerX_change = 1
            elif event.key == pygame.K_UP:
                playerY_change = -1
            elif event.key == pygame.K_DOWN:
                playerY_change = 1
            elif event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('Space/bullet.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change = 0
            elif event.key == pygame.K_RIGHT:
                playerX_change = 0
            elif event.key == pygame.K_UP:
                playerY_change = 0
            elif event.key == pygame.K_DOWN:
                playerY_change = 0


    playerX += playerX_change
    playerY += playerY_change

    # creating spaceship's allowed movement boundary
    if playerX <= 0 :
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    if playerY <= 0:
        playerY = 0
    elif playerY >= 500:
        playerY = 500
    
    # creating movement mechanics of enemies
    
    for i in range(num_enemies):
        
        if enemyY[i] > 450:
            for j in range(num_enemies):
                enemyY[j] = 2000                    # remove that from the viewable screen
            gameOver()
            mixer.music.stop()
            # print("game over", count)
            count+=1
            if count==1:
                game_over_sound.play()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        
        # Collision between bullet and enemy
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            bang_sound = mixer.Sound('Space/collision.wav')
            bang_sound.play()
            bullet_state = "ready"
            current_score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(30, 120)
        
        enemy(enemyX[i], enemyY[i], i)
    
    # creating movement mechanics of the bullets
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX, textY)
      

    pygame.display.update()                         # necessary to update display everytime a change is made
