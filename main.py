import pygame
import game
import settings
import json
import os

pygame.init()

screen = settings.setcreen()


colourBlack = (0, 0, 0)
colourGray = (80, 80, 80)
colourRed = (255, 0, 0)
colourLightGray = (130, 130, 130)
colourWhite = (255, 255, 255)
colourYellow = (255, 255, 0)

fontButton = pygame.font.SysFont("Arial", 36)
fontTitle = pygame.font.SysFont("Arial", 80)

buttonPlay = pygame.Rect(700, 300, 200, 60)
buttonGarage = pygame.Rect(700, 400, 200, 60)
buttonEnd = pygame.Rect(700, 500, 200, 60)

btnBuyEngine = pygame.Rect(950, 250, 180, 50)
btnBuyTrans = pygame.Rect(950, 330, 180, 50)
btnBuySteer = pygame.Rect(950, 410, 180, 50)
btnBuyBrakes = pygame.Rect(950, 490, 180, 50)
btnChangeTires = pygame.Rect(950, 570, 180, 50)
btnBack = pygame.Rect(700, 750, 200, 60)

state = "MENU"

menuStatus = True

coins = 1000
upgrade_cost = 200


car_stats = formule_list[formule_index]

def draw_button(rect, text, mouse_pos):
    colour = colourLightGray if rect.collidepoint(mouse_pos) else colourGray
    pygame.draw.rect(screen, colour, rect, border_radius = 10)
    text_surface = fontButton.render(text, True, colourWhite)
    screen.blit(text_surface, text_surface.get_rect(center=rect.center))

SAVE_FILE = "save.json"
def save_game(coins, formule_list):
    data = {
        "coins": coins,
        "formule_list": formule_list
    }
    with open(SAVE_FILE, "w") as file:
        json.dump(data, file, indent=4)
def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            data = json.load(file)

            for auto in data["formule_list"]:
                auto["colour"] = tuple(auto["colour"])

            return data["coins"], data["formule_list"]

    return None, None
time = pygame.time.Clock()
fps = 60

loaded_coins, loaded_formule = load_game()
if loaded_coins is not None:
    coins = loaded_coins
    formule_list = loaded_formule

formule_index = 0
car_stats = formule_list[formule_index]

tire_index = tires_list.index(car_stats["tires"])
while menuStatus:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menuStatus = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == "MENU":
                if buttonPlay.collidepoint(mouse_pos):
                    state = "PLAY"
                elif buttonGarage.collidepoint(mouse_pos):
                    state = "GARAGE"
                elif buttonEnd.collidepoint(mouse_pos):
                    menuStatus = False
            elif state == "GARAGE":
                if btnBack.collidepoint(mouse_pos):
                    state = "MENU"
                    if state == "QUIT":
                        menuStatus = False

                elif btnBuyEngine.collidepoint(mouse_pos) and coins >= upgrade_cost:
                    coins -= upgrade_cost
                    car_stats["engine"] += 10

                elif btnBuyTrans.collidepoint(mouse_pos) and coins >= upgrade_cost:
                    coins -= upgrade_cost
                    car_stats["transmission"] += 10

                elif btnBuySteer.collidepoint(mouse_pos) and coins >= upgrade_cost:
                    coins -= upgrade_cost
                    car_stats["steering"] += 10

                elif btnBuyBrakes.collidepoint(mouse_pos) and coins >= upgrade_cost:
                    coins -= upgrade_cost
                    car_stats["brakes"] += 10

                elif btnChangeTires.collidepoint(mouse_pos):
                    tire_index = (tire_index + 1) % len(tires_list)
                    car_stats["tires"] = tires_list[tire_index]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and state == "GARAGE":
                state = "MENU"
    if state == "MENU":
        screen.fill(colourBlack)

        title_surf = fontTitle.render("2D Formule", True, colourWhite)
        screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 150)))

        draw_button(buttonPlay,  "PLAY", mouse_pos)
        draw_button(buttonGarage, "GARAGE", mouse_pos)
        draw_button(buttonEnd, "QUIT", mouse_pos)
    elif state == "PLAY":
        state, reward = game.run(screen, fps, time, car_stats)
        coins += reward

        if state == "QUIT":
            menuStatus = False
    elif state == "GARAGE":
        screen.fill((25, 25, 30))

        title_surf = fontTitle.render("GARAGE", True, colourWhite)
        screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 100)))

        coins_surf = fontButton.render(f"Coins: {coins}", True, colourYellow)
        screen.blit(coins_surf, (width - 250, 50))

        stats_texts = [
            (f"Engine: {car_stats['engine']}", 260),
            (f"Transmission: {car_stats['transmission']}", 340),
            (f"Steering: {car_stats['steering']}", 420),
            (f"Brakes: {car_stats['brakes']}", 500),
            (f"Tires: {car_stats['tires'].upper()}", 580)
        ]
        for text, y_pos in stats_texts:
            surf = fontButton.render(text, True, colourWhite)
            screen.blit(surf, (450, y_pos))

        draw_button(btnBuyEngine, f"+10 ({upgrade_cost}$)", mouse_pos)
        draw_button(btnBuyTrans, f"+10 ({upgrade_cost}$)", mouse_pos)
        draw_button(btnBuySteer, f"+10 ({upgrade_cost}$)", mouse_pos)
        draw_button(btnBuyBrakes, f"+10 ({upgrade_cost}$)", mouse_pos)
        draw_button(btnChangeTires, "CHANGE", mouse_pos)

        draw_button(btnBack, "BACK", mouse_pos)
    pygame.display.flip()
    time.tick(fps)
    save_game(coins, formule_list)

pygame.quit()