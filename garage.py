import pygame
import settings

btnBuyEngine = pygame.Rect(950, 250, 180, 50)
btnBuyTrans = pygame.Rect(950, 330, 180, 50)
btnBuySteer = pygame.Rect(950, 410, 180, 50)
btnBuyBrakes = pygame.Rect(950, 490, 180, 50)
btnChangeTires = pygame.Rect(950, 570, 180, 50)
btnBack = pygame.Rect(700, 750, 200, 60)

upgrade_cost = 200

tires_list = ["soft", "medium", "hard"]
tire_index = 0

def menu(player):
    tire_index = 0
    mouse_pos = pygame.mouse.get_pos()
    if btnBack.collidepoint(mouse_pos):
        state = "MENU"
        if state == "QUIT":
            menuStatus = False

    elif btnBuyEngine.collidepoint(mouse_pos) and player.coins >= upgrade_cost:
        player.coins -= upgrade_cost
        player.formule_list[player.formule_index].engine += 10

    elif btnBuyTrans.collidepoint(mouse_pos) and player.coins >= upgrade_cost:
        player.coins -= upgrade_cost
        player.formule_list[player.formule_index].transmission += 10

    elif btnBuySteer.collidepoint(mouse_pos) and player.coins >= upgrade_cost:
        player.coins -= upgrade_cost
        player.formule_list[player.formule_index].steering += 10

    elif btnBuyBrakes.collidepoint(mouse_pos) and player.coins >= upgrade_cost:
        player.coins -= upgrade_cost
        player.formule_list[player.formule_index].brakes += 10

    elif btnChangeTires.collidepoint(mouse_pos):
        tire_index = (tire_index + 1) % len(tires_list)
        player.formule_list[player.formule_index].tires = tires_list[tire_index]
    settings.screen.fill((25, 25, 30))

    title_surf = settings.fontTitle.render("GARAGE", True, settings.colour.White)
    settings.screen.blit(title_surf, title_surf.get_rect(center=(settings.width // 2, 100)))

    coins_surf = settings.fontButton.render(f"Coins: {player.coins}", True, settings.colour.Yellow)
    settings.screen.blit(coins_surf, (settings.width - 250, 50))

    stats_texts = [
        (f"Engine: {player.formule_list[player.formule_index].engine}", 260),
        (f"Transmission: {player.formule_list[player.formule_index].transmission}", 340),
        (f"Steering: {player.formule_list[player.formule_index].steering}", 420),
        (f"Brakes: {player.formule_list[player.formule_index].brakes}", 500),
        (f"Tires: {player.formule_list[player.formule_index].tires .upper()}", 580)
    ]
    for text, y_pos in stats_texts:
        surf = settings.fontButton.render(text, True, settings.colour.White)
        settings.screen.blit(surf, (450, y_pos))

    settings.draw_button(btnBuyEngine, f"+10 ({upgrade_cost}$)", mouse_pos)
    settings.draw_button(btnBuyTrans, f"+10 ({upgrade_cost}$)", mouse_pos)
    settings.draw_button(btnBuySteer, f"+10 ({upgrade_cost}$)", mouse_pos)
    settings.draw_button(btnBuyBrakes, f"+10 ({upgrade_cost}$)", mouse_pos)
    settings.draw_button(btnChangeTires, "CHANGE", mouse_pos)

    settings.draw_button(btnBack, "BACK", mouse_pos)