import pygame
import settings
import formule

btnTabUpgrades = pygame.Rect(500, 160, 280, 50)
btnTabShop = pygame.Rect(820, 160, 280, 50)

btnPrevCar = pygame.Rect(350, 240, 70, 50)
btnNextCar = pygame.Rect(1180, 240, 70, 50)

btnBuyEngine = pygame.Rect(980, 340, 220, 50)
btnBuyTrans = pygame.Rect(980, 410, 220, 50)
btnBuySteer = pygame.Rect(980, 480, 220, 50)
btnBuyBrakes = pygame.Rect(980, 550, 220, 50)
btnChangeTires = pygame.Rect(980, 620, 220, 50)

btnShopPrev = pygame.Rect(350, 420, 70, 60)
btnShopNext = pygame.Rect(1180, 420, 70, 60)
btnBuyCar = pygame.Rect(650, 630, 300, 60)

btnBack = pygame.Rect(700, 770, 200, 60)

tires_list = ["soft", "medium", "hard"]
tire_index = 0

garage_tab = "UPGRADES"
shop_index = 0

TYPE_CONFIG = {
    "Rookie": {"cost": 150, "step": 5},
    "Pro": {"cost": 300, "step": 8},
    "Hyper": {"cost": 550, "step": 10}
}

CAR_CATALOG = [
    {
        "name": "Red Arrow F3",
        "car_type": "Rookie",
        "price": 0,
        "colour": settings.colour.Red,
        "engine": 60,
        "transmission": 60,
        "steering": 60,
        "brakes": 60,
        "weight": 720,
        "max_engine": 90,
        "max_transmission": 90,
        "max_steering": 90,
        "max_brakes": 90
    },
    {
        "name": "Yellow Hornet F2",
        "car_type": "Pro",
        "price": 800,
        "colour": settings.colour.Yellow,
        "engine": 80,
        "transmission": 80,
        "steering": 85,
        "brakes": 80,
        "weight": 660,
        "max_engine": 120,
        "max_transmission": 120,
        "max_steering": 125,
        "max_brakes": 120
    },
    {
        "name": "Emerald Apex F1",
        "car_type": "Hyper",
        "price": 1800,
        "colour": settings.colour.Green,
        "engine": 105,
        "transmission": 105,
        "steering": 110,
        "brakes": 105,
        "weight": 600,
        "max_engine": 160,
        "max_transmission": 160,
        "max_steering": 165,
        "max_brakes": 160
    },
    {
        "name": "Phantom Ghost X",
        "car_type": "Hyper",
        "price": 2500,
        "colour": settings.colour.White,
        "engine": 115,
        "transmission": 110,
        "steering": 115,
        "brakes": 115,
        "weight": 580,
        "max_engine": 175,
        "max_transmission": 170,
        "max_steering": 175,
        "max_brakes": 175
    }
]

def get_upgrade_info(car):
    cfg = TYPE_CONFIG.get(car.car_type, {"cost": 200, "step": 10})
    return cfg["cost"], cfg["step"]

def is_car_owned(player, car_name):
    for auto in player.formule_list:
        if auto.name == car_name:
            return True
    return False

def handle_click(player, mouse_pos):
    global tire_index, garage_tab, shop_index

    if btnBack.collidepoint(mouse_pos):
        settings.state = "MENU"
        return

    if btnTabUpgrades.collidepoint(mouse_pos):
        garage_tab = "UPGRADES"
        return
    elif btnTabShop.collidepoint(mouse_pos):
        garage_tab = "SHOP"
        return

    if garage_tab == "UPGRADES":
        if btnPrevCar.collidepoint(mouse_pos):
            player.formule_index = (player.formule_index - 1) % len(player.formule_list)
            car = player.formule_list[player.formule_index]
            if car.tires in tires_list:
                tire_index = tires_list.index(car.tires)
            return

        elif btnNextCar.collidepoint(mouse_pos):
            player.formule_index = (player.formule_index + 1) % len(player.formule_list)
            car = player.formule_list[player.formule_index]
            if car.tires in tires_list:
                tire_index = tires_list.index(car.tires)
            return

        car = player.formule_list[player.formule_index]
        cost, step = get_upgrade_info(car)

        if btnBuyEngine.collidepoint(mouse_pos) and player.coins >= cost and car.engine < car.max_engine:
            player.coins -= cost
            car.engine = min(car.max_engine, car.engine + step)

        elif btnBuyTrans.collidepoint(mouse_pos) and player.coins >= cost and car.transmission < car.max_transmission:
            player.coins -= cost
            car.transmission = min(car.max_transmission, car.transmission + step)

        elif btnBuySteer.collidepoint(mouse_pos) and player.coins >= cost and car.steering < car.max_steering:
            player.coins -= cost
            car.steering = min(car.max_steering, car.steering + step)

        elif btnBuyBrakes.collidepoint(mouse_pos) and player.coins >= cost and car.brakes < car.max_brakes:
            player.coins -= cost
            car.brakes = min(car.max_brakes, car.brakes + step)

        elif btnChangeTires.collidepoint(mouse_pos):
            tire_index = (tire_index + 1) % len(tires_list)
            car.tires = tires_list[tire_index]

    elif garage_tab == "SHOP":
        if btnShopPrev.collidepoint(mouse_pos):
            shop_index = (shop_index - 1) % len(CAR_CATALOG)
            return
        elif btnShopNext.collidepoint(mouse_pos):
            shop_index = (shop_index + 1) % len(CAR_CATALOG)
            return

        offer = CAR_CATALOG[shop_index]
        owned = is_car_owned(player, offer["name"])

        if btnBuyCar.collidepoint(mouse_pos):
            if owned:
                for i, auto in enumerate(player.formule_list):
                    if auto.name == offer["name"]:
                        player.formule_index = i
                        garage_tab = "UPGRADES"
                        break
            elif player.coins >= offer["price"]:
                player.coins -= offer["price"]
                new_car = formule.Formule(
                    ai=False,
                    name=offer["name"],
                    colour=offer["colour"],
                    engine=offer["engine"],
                    transmission=offer["transmission"],
                    steering=offer["steering"],
                    brakes=offer["brakes"],
                    weight=offer["weight"],
                    tires="medium",
                    car_type=offer["car_type"],
                    max_engine=offer["max_engine"],
                    max_transmission=offer["max_transmission"],
                    max_steering=offer["max_steering"],
                    max_brakes=offer["max_brakes"]
                )
                player.formule_list.append(new_car)
                player.formule_index = len(player.formule_list) - 1
                tire_index = tires_list.index("medium")

def draw_car_preview(car_colour, center_x, center_y):
    shape = pygame.Surface((20, 40), pygame.SRCALPHA)
    pygame.draw.rect(shape, car_colour, (3, 0, 14, 40), border_radius=4)
    pygame.draw.rect(shape, (0, 0, 0), (0, 5, 20, 8))
    pygame.draw.rect(shape, (0, 0, 0), (0, 28, 20, 8))
    scaled = pygame.transform.scale(shape, (60, 120))
    settings.screen.blit(scaled, scaled.get_rect(center=(center_x, center_y)))

def draw_tab_button(rect, text, active, mouse_pos):
    if active:
        col = (60, 140, 60)
    elif rect.collidepoint(mouse_pos):
        col = settings.colour.LightGray
    else:
        col = settings.colour.Gray
    pygame.draw.rect(settings.screen, col, rect, border_radius=10)
    surf = settings.fontButton.render(text, True, settings.colour.White)
    settings.screen.blit(surf, surf.get_rect(center=rect.center))

def menu(player):
    mouse_pos = pygame.mouse.get_pos()
    settings.screen.fill((25, 25, 30))

    title_surf = settings.fontTitle.render("GARAGE", True, settings.colour.White)
    settings.screen.blit(title_surf, title_surf.get_rect(center=(settings.width // 2, 80)))

    coins_surf = settings.fontButton.render(f"Coins: {player.coins}", True, settings.colour.Yellow)
    settings.screen.blit(coins_surf, (settings.width - 280, 50))

    draw_tab_button(btnTabUpgrades, "MY CARS", garage_tab == "UPGRADES", mouse_pos)
    draw_tab_button(btnTabShop, "CAR DEALER", garage_tab == "SHOP", mouse_pos)

    if garage_tab == "UPGRADES":
        car = player.formule_list[player.formule_index]
        cost, step = get_upgrade_info(car)

        panel_rect = pygame.Rect(330, 230, 940, 480)
        pygame.draw.rect(settings.screen, (40, 40, 48), panel_rect, border_radius=14)

        settings.draw_button(btnPrevCar, "<", settings.fontButton, mouse_pos)
        settings.draw_button(btnNextCar, ">", settings.fontButton, mouse_pos)

        header_text = f"{car.name}  [{car.car_type.upper()}]  ({player.formule_index + 1}/{len(player.formule_list)})"
        header_surf = settings.fontButton.render(header_text, True, settings.colour.Yellow)
        settings.screen.blit(header_surf, header_surf.get_rect(center=(settings.width // 2, 265)))

        draw_car_preview(car.colour, 430, 480)

        weight_surf = settings.fontButton.render(f"Weight: {car.weight} kg", True, settings.colour.LightGray)
        settings.screen.blit(weight_surf, weight_surf.get_rect(center=(430, 590)))

        stats_rows = [
            (f"Engine: {car.engine} / {car.max_engine}", 345, car.engine >= car.max_engine, btnBuyEngine),
            (f"Transmission: {car.transmission} / {car.max_transmission}", 415, car.transmission >= car.max_transmission, btnBuyTrans),
            (f"Steering: {car.steering} / {car.max_steering}", 485, car.steering >= car.max_steering, btnBuySteer),
            (f"Brakes: {car.brakes} / {car.max_brakes}", 555, car.brakes >= car.max_brakes, btnBuyBrakes),
        ]

        for text, y_pos, is_max, btn_rect in stats_rows:
            surf = settings.fontButton.render(text, True, settings.colour.White)
            settings.screen.blit(surf, (540, y_pos))
            btn_label = "MAX" if is_max else f"+{step} ({cost}$)"
            settings.draw_button(btn_rect, btn_label, settings.fontButton, mouse_pos)

        tire_surf = settings.fontButton.render(f"Tires: {car.tires.upper()}", True, settings.colour.White)
        settings.screen.blit(tire_surf, (540, 625))
        settings.draw_button(btnChangeTires, "CHANGE", settings.fontButton, mouse_pos)

    elif garage_tab == "SHOP":
        offer = CAR_CATALOG[shop_index]
        owned = is_car_owned(player, offer["name"])
        cfg = TYPE_CONFIG[offer["car_type"]]

        panel_rect = pygame.Rect(330, 230, 940, 480)
        pygame.draw.rect(settings.screen, (40, 40, 48), panel_rect, border_radius=14)

        settings.draw_button(btnShopPrev, "<", settings.fontButton, mouse_pos)
        settings.draw_button(btnShopNext, ">", settings.fontButton, mouse_pos)

        name_surf = settings.fontButton.render(f"{offer['name']}  -  Class: {offer['car_type'].upper()}", True, settings.colour.Yellow)
        settings.screen.blit(name_surf, name_surf.get_rect(center=(settings.width // 2, 275)))

        draw_car_preview(offer["colour"], 480, 440)

        specs = [
            f"Engine: {offer['engine']} (Max {offer['max_engine']})",
            f"Transmission: {offer['transmission']} (Max {offer['max_transmission']})",
            f"Steering: {offer['steering']} (Max {offer['max_steering']})",
            f"Brakes: {offer['brakes']} (Max {offer['max_brakes']})",
            f"Weight: {offer['weight']} kg  |  Upgrade: +{cfg['step']} ({cfg['cost']}$)"
        ]

        for i, line in enumerate(specs):
            s = settings.fontButton.render(line, True, settings.colour.White)
            settings.screen.blit(s, (630, 330 + i * 48))

        if owned:
            settings.draw_button(btnBuyCar, "OWNED (SELECT)", settings.fontButton, mouse_pos)
        else:
            settings.draw_button(btnBuyCar, f"BUY ({offer['price']}$)", settings.fontButton, mouse_pos)

    settings.draw_button(btnBack, "BACK", settings.fontButton, mouse_pos)