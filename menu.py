import pygame
import game
import garage
import settings



buttonPlay = pygame.Rect(700, 300, 200, 60)
buttonGarage = pygame.Rect(700, 400, 200, 60)
buttonEnd = pygame.Rect(700, 500, 200, 60)

def reset_car_for_race(car):
    # Nastaví auto na startovní čáru a opraví opotřebení před závodem
    car.x = 1150
    car.y = 1275
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
                    settings.state = "PLAY"
                elif buttonGarage.collidepoint(mouse_pos):
                    settings.state = "GARAGE"
                elif buttonEnd.collidepoint(mouse_pos):
                    settings.menuStatus = False
            elif settings.state == "GARAGE":
                garage.handle_click(player, mouse_pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and settings.state == "GARAGE":
                settings.state = "MENU"

    if settings.state == "MENU":
        settings.screen.fill(settings.colour.Black)

        title_surf = settings.fontTitle.render("2D Formule", True, settings.colour.White)
        settings.screen.blit(title_surf, title_surf.get_rect(center=(settings.width // 2, 150)))

        settings.draw_button(buttonPlay, "PLAY", settings.fontButton, mouse_pos)
        settings.draw_button(buttonGarage, "GARAGE", settings.fontButton, mouse_pos)
        settings.draw_button(buttonEnd, "QUIT", settings.fontButton, mouse_pos)

    elif settings.state == "PLAY":
        reset_car_for_race(player.formule_list[player.formule_index])
        next_state, reward = game.run(player)
        player.coins += reward
        if next_state == "QUIT":
            settings.menuStatus = False
        else:
            settings.state = next_state

    elif settings.state == "GARAGE":
        garage.menu(player)
