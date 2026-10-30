
import pygame

pygame.init()

width, height  = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Formule")

colourBlack = (0, 0, 0)
colourGray = (80, 80, 80)
colourRed = (255, 0, 0)
colourLightGray = (130, 130, 130)
colourWhite = (255, 255, 255)

fontButton = pygame.font.SysFont("Arial", 36)
fontTitle = pygame.font.SysFont("Arial", 80)

buttonPlay = pygame.Rect(300, 250, 200, 60)
buttonEnd = pygame.Rect(300, 340, 200, 60)

state = "MENU"

game = True

time = pygame.time.Clock()
fps = 60

while game:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == "MENU":
                if buttonPlay.collidepoint(mouse_pos):
                    state = "PLAY"
                elif buttonEnd.collidepoint(mouse_pos):
                    game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and state == "PLAY":
                state = "MENU"

    if state == "MENU":
        screen.fill(colourBlack)

        title_surf = fontTitle.render("2D Formule", True, colourWhite)
        title_rect = title_surf.get_rect(center=(width // 2, 130))
        screen.blit(title_surf, title_rect)

        if buttonPlay.collidepoint(mouse_pos):
            pygame.draw.rect(screen, colourLightGray, buttonPlay, border_radius = 10)
        else:
            pygame.draw.rect(screen, colourGray, buttonPlay, border_radius=10)

        textGame = fontButton.render("PLAY", True, colourWhite)
        screen.blit(textGame, textGame.get_rect(center=buttonPlay.center))
        if buttonEnd.collidepoint(mouse_pos):
            pygame.draw.rect(screen, colourLightGray, buttonEnd, border_radius=10)
        else:
            pygame.draw.rect(screen, colourGray, buttonEnd, border_radius=10)

        textQuit = (fontButton.render("QUIT", True, colourWhite))
        screen.blit(textQuit, textQuit.get_rect(center=buttonEnd.center))

    elif state == "PLAY":
        screen.fill((20, 50, 80))
        info = fontButton.render("G", True, colourWhite)
        screen.blit(info, info.get_rect(center=(width // 2, height // 2)))

    pygame.display.flip()
    time.tick(fps)

pygame.quit()