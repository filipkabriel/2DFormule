import pygame

def run(screen, fps, time):
    width, height = screen.get_size()

    colourBlack = (0, 0, 0)
    colourGray = (80, 80, 80)
    colourRed = (255, 0, 0)
    colourLightGray = (130, 130, 130)
    colourWhite = (255, 255, 255)


    playerX = 375
    playerY = 275

    speed = 5
    font = pygame.font.SysFont("Arial", 24)

    gameStatus = True
    while gameStatus:
        player = pygame.Rect(playerX, playerY, 50, 50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            playerX -= speed
        if key[pygame.K_d]:
            playerX += speed
        if key[pygame.K_w]:
            playerY -= speed
        if key[pygame.K_s]:
            playerY += speed

        screen.fill(colourBlack)
        pygame.draw.rect(screen, colourRed, player)
        pygame.display.flip()
        time.tick(fps)
