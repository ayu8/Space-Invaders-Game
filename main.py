import pygame
import random

#initialize pygame module
pygame.init()

# creating the game window 
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('bg2.jpg')

# Title and icon of the window
pygame.display.set_caption("My First PyGame")
icon = pygame.image.load('car-icon.png')       # from flaticon website
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 368
# X coordinate of player; (800px - 64px) / 2; screen is 800px wide and picture is 64px wide
playerY = 500
playerY_change = 0
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('alien1.png')
enemyX = random.randint(0,800-64)
enemyY = random.randint(30,120)
enemyX_change = 0.5
enemyY_change = 40

def player(xPos, yPos):
    screen.blit(playerImg, (xPos, yPos))       # blit() means to draw


def enemy(xPos, yPos):
    screen.blit(enemyImg, (xPos, yPos))       # blit() means to draw

# game loop, window exits or stays
running = True
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
                playerX_change = -0.5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            elif event.key == pygame.K_UP:
                playerY_change = -0.4
            elif event.key == pygame.K_DOWN:
                playerY_change = 0.4
        
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
    enemyX += enemyX_change

    if enemyX <= 0:
        enemyX_change = 0.5
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -0.5
        enemyY += enemyY_change
    



    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.update()                         # necessary to update display everytime a change is made

