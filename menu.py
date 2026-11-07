import pygame
import game
import settings

fontButton = pygame.font.SysFont("Arial", 36)
fontTitle = pygame.font.SysFont("Arial", 80)

buttonPlay = pygame.Rect(700, 300, 200, 60)
buttonGarage = pygame.Rect(700, 400, 200, 60)
buttonEnd = pygame.Rect(700, 500, 200, 60)

def draw(player):
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            settings.menuStatus = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if settings.state == "MENU":
                if buttonPlay.collidepoint(mouse_pos):
                    settings.state = "PLAY"
                elif buttonGarage.collidepoint(mouse_pos):
                    settings.state = "GARAGE"
                elif buttonEnd.collidepoint(mouse_pos):
                    settings.menuStatus = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and settings.state == "GARAGE":
                settings.state = "MENU"
        if settings.state == "MENU":
            settings.screen.fill(settings.colour.Black)

            title_surf = fontTitle.render("2D Formule", True, settings.colour.White)
            settings.screen.blit(title_surf, title_surf.get_rect(center=(settings.width // 2, 150)))

            settings.draw_button(buttonPlay,  "PLAY",fontButton, mouse_pos)
            settings.draw_button(buttonGarage, "GARAGE",fontButton, mouse_pos)
            settings.draw_button(buttonEnd, "QUIT",fontButton, mouse_pos)
        elif settings.state == "PLAY":
            reward = game.run(player.formule_list[player.formule_index])
            player.coins += reward

        if settings.state == "QUIT":
            settings.menuStatus = False
