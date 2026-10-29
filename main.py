import pygame

pygame.init()

width, height  = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2DFormule")

colourBlack = (0, 0, 0)
colourRed = (255, 50, 50)

time = pygame.time.Clock()
fps = 60

player_x = 375
player_y = 275
size = 50
speed = 5

game = True
while game:
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

    pygame.display.flip()

    time.tick(fps)

pygame.quit()