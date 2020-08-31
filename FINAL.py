import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('player.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('background.png')

# background sound
mixer.music.load('Space Trip.mp3')
mixer.music.play(-1)

# player
playerImg = pygame.image.load('player.png')
player_x = 368
player_y = 472
player_x_change = 0

# Enemy
enemyImg = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemy_x.append(random.randint(0, 734))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(3)
    enemy_y_change.append(40)

# Bullet

# ready - you can;t see the bullet on the screen
# fire - bullet is currentlu moving

bulletImg = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 15
bullet_state = 'ready'

# count score
score = 0
font = pygame.font.Font('aAlloyInk.ttf', 32)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('aAlloyInk.ttf', 64)


# golden color : (255,215,0)
def show_score(x, y):
    final_score = font.render('score : ' + str(score), True, (251, 181, 64))
    screen.blit(final_score, (x, y))


def game_over_text():
    over_score = over_font.render('GAME OVER', True, (251, 181, 64))
    screen.blit(over_score, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def iscollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True

while running:
    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))

    # Background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if key pressed check whether its right or left !
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player_x_change = -5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                player_x_change = 0

    # move the direction of the spaceship
    player_x += player_x_change
    # setting border
    if player_x <= -64 :
        player_x = 736
    elif player_x >= 800:
        player_x = 0

    # move the direction of the  enemy

    for i in range(num_of_enemies):

        # game over

        if enemy_y[i] > 400:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        # setting border
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 4
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]

            # collision

        collision = iscollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            collision_sound = mixer.Sound('blast.wav')
            collision_sound.play()
            bullet_y = 480
            bullet_state = 'ready'
            score += 1
            print(score)
            enemy_x[i] = random.randint(0, 734)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    # bullet movement

    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(textX, textY)
    pygame.display.update()
