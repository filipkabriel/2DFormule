import pygame
import random

pygame.init()

width, height  = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2DFormule")

colourBlack = (0, 0, 0)
colourRed = (255, 50, 50)
colourWhite = (255, 255, 255)

font = pygame.font.SysFont("Arial", 20)

time = pygame.time.Clock()
fps = 60


player_x = 375
player_y = 275
size = 50
coinSize = 10
speed = 5
score = 0

coinX = random.randint(0, width - coinSize)
coinY = random.randint(0, height - coinSize)

game = True
while game:
    player_rect = pygame.Rect(player_x, player_y, size, size)
    coint_rect = pygame.Rect(coinX, coinY, coinSize, coinSize)
    if player_rect.colliderect(coint_rect):
        score += 1
        coinX = random.randint(0, width - coinSize)
        coinY = random.randint(0, height - coinSize)
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            game = False

    klavesy = pygame.key.get_pressed()
    if klavesy[pygame.K_a] and player_x > 0:
        player_x -= speed
    if klavesy[pygame.K_d] and player_x < width - size:
        player_x += speed
    if klavesy[pygame.K_w] and player_y > 0:
        player_y -= speed
    if klavesy[pygame.K_s] and player_y < height - size:
        player_y += speed

    screen.fill(colourBlack)
    pygame.draw.rect(screen, colourRed, (player_x, player_y, size, size))
    pygame.draw.circle(screen, colourWhite,(coinX, coinY), coinSize)

    coinScore = font.render(str(score), True, colourWhite)

    screen.blit(coinScore, (20, 20))
    pygame.display.flip()

    time.tick(fps)

pygame.quit()