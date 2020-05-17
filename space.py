import pygame
from pygame import  mixer
import math
import random

# initialize the pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))
running = True

# background
background = pygame.image.load("mountains.png")
#background sound
mixer.music.load("background.wav")
mixer.music.play(-1)
# title and icon
pygame.display.set_caption("space invadors")
icon = pygame.image.load("alien.png")
pygame.display.set_icon(icon)
# player
playerimg = pygame.image.load("space.png")
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):

    enemyimg.append(pygame.image.load("monster.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# bullet
# ready state  means you cant see the bullet
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#score
score_value =  0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("SCORE :"+ str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerimg, (playerX, playerY))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def firebullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop


def game_over_text():

    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


while running:

    # RGB= RED , GREEN , BLUE
    screen.fill((192, 192, 192))
    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        # if key stroke pressed check  whether its right or left
        if event.type == pygame.KEYDOWN:

            print("key is pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:

                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    firebullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # checking boundries
    playerX += playerX_change

    if playerX <= 0:

        playerX = 0
    elif playerX >= 736:

        playerX = 736
    for i in range(num_of_enemies):
        #game over
        if enemyY [i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
          enemyX_change[i] = 4
          enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
          enemyX_change[i] = -4
          enemyY[i] += enemyY_change[i]
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        firebullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)


    show_score(textX, textY)
    pygame.display.update()
