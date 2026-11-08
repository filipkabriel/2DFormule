import pygame
import game
import garage
import settings



buttonPlay = pygame.Rect(700, 300, 200, 60)
buttonGarage = pygame.Rect(700, 400, 200, 60)
buttonEnd = pygame.Rect(700, 500, 200, 60)

buttonTrack1 = pygame.Rect(600, 280, 400, 60)
buttonTrack2 = pygame.Rect(600, 380, 400, 60)
buttonTrack3 = pygame.Rect(600, 480, 400, 60)
buttonBackTrack = pygame.Rect(700, 620, 200, 60)

def reset_car_for_race(car, start_pos):
    # Nastaví auto na startovní čáru a opraví opotřebení před závodem
    car.x, car.y = start_pos
    car.angle = 180
    car.speed = 0
    car.dnf_status = False
    car.body_status = 100
    car.engine_status = 100
    car.transmission_status = 100
    car.steering_status = 100
    car.tire_status = 100
    car.brakes_status = 100
def draw(player):
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            settings.menuStatus = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if settings.state == "MENU":
                if buttonPlay.collidepoint(mouse_pos):
                    settings.state = "TRACK_SELECT"
                elif buttonGarage.collidepoint(mouse_pos):
                    settings.state = "GARAGE"
                elif buttonEnd.collidepoint(mouse_pos):
                    settings.menuStatus = False

            elif settings.state == "TRACK_SELECT":
                if buttonTrack1.collidepoint(mouse_pos):
                    settings.selected_track = 0
                    settings.state = "PLAY"
                elif buttonTrack2.collidepoint(mouse_pos):
                    settings.selected_track = 1
                    settings.state = "PLAY"
                elif buttonTrack3.collidepoint(mouse_pos):
                    settings.selected_track = 2
                    settings.state = "PLAY"
                elif buttonBackTrack.collidepoint(mouse_pos):
                    settings.state = "MENU"

            elif settings.state == "GARAGE":
                garage.handle_click(player, mouse_pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and settings.state in ["GARAGE", "TRACK_SELECT"]:
                settings.state = "MENU"

    # Vykreslování jednotlivých obrazovek
    if settings.state == "MENU":
        settings.screen.fill(settings.colour.Black)

        title_surf = settings.fontTitle.render("2D Formule", True, settings.colour.White)
        settings.screen.blit(title_surf, title_surf.get_rect(center=(settings.width // 2, 150)))

        settings.draw_button(buttonPlay, "PLAY", settings.fontButton, mouse_pos)
        settings.draw_button(buttonGarage, "GARAGE", settings.fontButton, mouse_pos)
        settings.draw_button(buttonEnd, "QUIT", settings.fontButton, mouse_pos)

    elif settings.state == "TRACK_SELECT":
        settings.screen.fill((20, 30, 20))

        title_surf = settings.fontTitle.render("VYBER TRAT", True, settings.colour.White)
        settings.screen.blit(title_surf, title_surf.get_rect(center=(settings.width // 2, 150)))

        settings.draw_button(buttonTrack1, "1. Standard Oval (3 kola)", settings.fontButton, mouse_pos)
        settings.draw_button(buttonTrack2, "2. Short Sprint (5 kol)", settings.fontButton, mouse_pos)
        settings.draw_button(buttonTrack3, "3. Grand Prix (2 kola)", settings.fontButton, mouse_pos)
        settings.draw_button(buttonBackTrack, "BACK", settings.fontButton, mouse_pos)

    elif settings.state == "PLAY":
        start_pos = game.get_start_pos(settings.selected_track)
        reset_car_for_race(player.formule_list[player.formule_index], start_pos)
        next_state, reward = game.run(player, settings.selected_track)
        player.coins += reward
        if next_state == "QUIT":
            settings.menuStatus = False
        else:
            settings.state = next_state

    elif settings.state == "GARAGE":
        garage.menu(player)