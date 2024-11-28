import pygame as py
import random as r
import math as m
# To deal with sound...
from pygame import mixer
# Initialize pygame
py.init()

# Create the screen
screen = py.display.set_mode((800, 600))

# Caption and icon
py.display.set_caption("Space Invaders")
icon = py.image.load('rocket.png')
py.display.set_icon(icon)

# Background image
backgroundImg =py.image.load('background.png')

#background sound...
mixer.music.load('background.wav')
mixer.music.play(-1)

# Enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6
for i in range(num_of_enemies):
    enemyImg.append(py.image.load('enemy.png'))
    enemyX.append(r.randint(0, 736))
    enemyX_change.append(3)
    enemyY.append(r.randint(50, 150))
    enemyY_change.append(40)

# Bullet
bulletImg=py.image.load(r"C:\Users\sandi\PycharmProjects\PythonProject3\Bullet .png")
bulletX=0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# Player
playerImg = py.image.load('spaceship.png')
playerX = 370
playerX_change = 0
playerY = 500

#score
score=0
font=py.font.Font('freesansbold.ttf',32)
textX=10
textY=10

#Game over ...
over_font=py.font.Font('freesansbold.ttf',64)

def game_over():
    over_ =over_font.render("GAME OVER !" , True, (255, 255, 255))
    screen.blit(over_, (200, 250))

def show_score(x,y):
    score_=font.render("SCORE :"+str(score),True,(0,0,255))
    screen.blit(score_, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y + 20))

def check_collision(enemyX, enemyY, bulletX, bulletY):
    distance=m.sqrt(m.pow(enemyX-bulletX,2)+m.pow(enemyY-bulletY,2))
    if distance <27:
        return True
    else:
        return False
# Game loop
running = True
while running:
    # RGB background color
    screen.fill((0, 0, 0))
    screen.blit(backgroundImg, (0, 0))

    # Event handling
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_LEFT:
                playerX_change = -5
            if event.key == py.K_RIGHT:
                playerX_change = 5
            if event.key == py.K_SPACE and bullet_state == "ready":
                bullet_sound=mixer.Sound('laser.wav')
                bullet_sound.play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
        if event.type == py.KEYUP:
            if event.key == py.K_LEFT or event.key == py.K_RIGHT:
                playerX_change = 0

    # Player movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        #Game over...
        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=1500
            game_over()
            break
        enemyX[i]+= enemyX_change[i]
        if enemyX[i]<= 0:
            enemyX_change[i]= 2
            enemyY[i]+= enemyY_change[i]
        elif enemyX[i]>= 736:
            enemyX_change[i]= -2
            enemyY[i]+= enemyY_change[i]
        # Collision...
        collision = check_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            enemyX[i]=r.randint(0, 736)
            enemyY[i]=r.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Drawing the player and enemy
    player(playerX, playerY)

    #Displaying the score...
    show_score(textX,textY)

    # Update the screen
    py.display.update()
