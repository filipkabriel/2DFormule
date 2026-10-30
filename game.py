import pygame

def run(screen, fps, time):
    width, height = screen.get_size()

    colourBlack = (0, 0, 0)
    colourGray = (80, 80, 80)
    colourRed = (255, 0, 0)
    colourLightGray = (130, 130, 130)
    colourWhite = (255, 255, 255)

    player = pygame.Rect(375, 275, 50, 50)
    speed = 5
    font = pygame.font.SysFont("Arial", 24)

    gameStatus = True
    while gameStatus:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"

        pygame.display.flip()
        time.tick(fps)
