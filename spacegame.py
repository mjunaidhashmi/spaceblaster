import random
import math
import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Blaster")
icon = pygame.image.load('Screenshot 2025-06-24 142836.png')
pygame.display.set_icon(icon)
mixer.music.load("background.wav")
mixer.music.play(-1)


score=0
font=pygame.font.Font('freesansbold.ttf',16)
font2=pygame.font.Font('freesansbold.ttf',32)
scorex=10
scorey=10


playerimg = pygame.image.load("spaceship.png")
playerx = 370
playery = 480
playerxchange = 0

enemyimg = []
enemyx = []
enemyy = []
enemyxchange = []
enemyychange=[]
numofenemies=6

gameoverx=200
gameovery=250

for i in range (numofenemies):
    enemyimg.append(pygame.image.load("alien.png"))
    enemyx.append (random.randint(0, 735))
    enemyy.append (random.randint(50, 150))
    enemyxchange.append (1.2)
    enemyychange.append (40)



bulletimg = pygame.image.load("bullet.png")
bulletx = 0
bullety = 480
bulletxchange = 0
bulletychange = 5
bulletstate = "ready"

background = pygame.image.load("background.png")

def game_over(x,y):
    gameovershow=font2.render("GAME OVER YOU LOSE",True,(255, 192, 203))
    screen.blit(gameovershow,(x,y))


def scoref(x,y):
    scoreshow=font.render("score:" + str(score),True,(255, 192, 203))
    screen.blit(scoreshow,(x,y))

def collision(bullety,bulletx,enemyy,enemyx):
    distance = math.sqrt(math.pow(enemyx - bulletx, 2) + (math.pow(enemyy - bullety, 2)))
    if distance <= 27:
        return True
    else:
        return False


def firebullet(x, y):
    global bulletstate
    bulletstate = "fire"
    screen.blit(bulletimg, (x + 15, y + 10))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


running = True
while running:
    screen.fill((255, 192, 203))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerxchange = -1.5
            if event.key == pygame.K_RIGHT:
                playerxchange = 1.5
            if event.key == pygame.K_SPACE:
                if bulletstate == "ready":
                    bulletx = playerx
                    firebullet(bulletx, bullety)
                    bulletsound=mixer.Sound("laser.wav")
                    bulletsound.play()

        if event.type == pygame.KEYUP:
            playerxchange = 0

    playerx += playerxchange
    if playerx < 0:
        playerx = 0
    if playerx > 740:
        playerx = 740

    for i in range(numofenemies):
        if enemyy[i] > 440:
            for j in range(numofenemies):
                enemyy[j]=2000
            game_over(gameoverx,gameovery)
            break
        enemyx[i] += enemyxchange[i]
        if enemyx[i] < 0:
            enemyxchange[i] = 1.2
            enemyy[i] += enemyychange[i]

        if enemyx[i] > 740  :
            enemyxchange[i] = -1.2
            enemyy[i] += enemyychange[i]

        collisionn = collision(bullety, bulletx, enemyy[i], enemyx[i])
        if collisionn == True:
            bulletstate = "ready"
            bullety = 480
            score = score + 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)
            enemysound=mixer.Sound("explosion.wav")
            enemysound.play()
        enemy(enemyx[i], enemyy[i],i)



    if bullety <= 0:
        bulletstate = "ready"
        bullety = 480
    if bulletstate == "fire":
        firebullet(bulletx, bullety)
        bullety = bullety - bulletychange

    scoref(scorex,scorey)








    player(playerx, playery)


    pygame.display.update()
