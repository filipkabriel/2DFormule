import pygame
import player

btnBuyEngine = pygame.Rect(950, 250, 180, 50)
btnBuyTrans = pygame.Rect(950, 330, 180, 50)
btnBuySteer = pygame.Rect(950, 410, 180, 50)
btnBuyBrakes = pygame.Rect(950, 490, 180, 50)
btnChangeTires = pygame.Rect(950, 570, 180, 50)
btnBack = pygame.Rect(700, 750, 200, 60)

tires_list = ["soft", "medium", "hard"]
tire_index = 0

def menu():
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
    screen.fill((25, 25, 30))

    title_surf = fontTitle.render("GARAGE", True, colourWhite)
    screen.blit(title_surf, title_surf.get_rect(center=(settings.width // 2, 100)))

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