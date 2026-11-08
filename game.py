import pygame
import math
import os
import settings

TRACKS = [
    {
        "name": "Track 1",
        "top_svg": "tracks/track1_top.svg",
        "bottom_svg": "tracks/track1_bottom.svg",
        "start_pos": (1150, 1275),
        "start_angle": 180,
        "laps": 3,
        "reward": 300
    },
    {
        "name": "Track 2",
        "top_svg": "tracks/track2_top.svg",
        "bottom_svg": "tracks/track2_bottom.svg",
        "start_pos": (900, 925),
        "start_angle": 180,
        "laps": 5,
        "reward": 250
    },
    {
        "name": "Track 3",
        "top_svg": "tracks/track3_top.svg",
        "bottom_svg": "tracks/track3_bottom.svg",
        "start_pos": (1560, 1650),
        "start_angle": 180,
        "laps": 2,
        "reward": 500
    }
]

def get_start_pos(track_index):
    return TRACKS[track_index]["start_pos"]

def load_track_layers(track_index):
    t = TRACKS[track_index]
    top_path = t["top_svg"]
    bottom_path = t["bottom_svg"]

    if os.path.exists(top_path) and os.path.exists(bottom_path):
        visual_map = pygame.image.load(top_path).convert()
        logic_map = pygame.image.load(bottom_path).convert()
    else:
        print(f"Upozorneni: Soubory {top_path} nebo {bottom_path} nenalezeny, generuji nahradni trat.")
        map_w, map_h = 2400, 1600
        visual_map = pygame.Surface((map_w, map_h))
        logic_map = pygame.Surface((map_w, map_h))

        track_rect = pygame.Rect(200, 200, 2000, 1200)
        inner_rect = pygame.Rect(450, 450, 1500, 700)
        line_rect = pygame.Rect(1100, 1150, 20, 250)
        cp_rect = pygame.Rect(1100, 200, 50, 250)

        logic_map.fill((0, 153, 0))
        pygame.draw.rect(logic_map, (130, 130, 130), track_rect, border_radius=120)
        pygame.draw.rect(logic_map, (0, 153, 0), inner_rect, border_radius=80)
        pygame.draw.rect(logic_map, (0, 0, 255), cp_rect)
        pygame.draw.rect(logic_map, (255, 255, 255), line_rect)

        visual_map.fill((0, 153, 0))
        pygame.draw.rect(visual_map, (130, 130, 130), track_rect, border_radius=120)
        pygame.draw.rect(visual_map, (255, 255, 255), track_rect, width=6, border_radius=120)
        pygame.draw.rect(visual_map, (0, 153, 0), inner_rect, border_radius=80)
        pygame.draw.rect(visual_map, (255, 255, 255), inner_rect, width=6, border_radius=80)
        pygame.draw.rect(visual_map, (255, 255, 255), line_rect)

    return visual_map, logic_map, t["laps"], t["reward"]

def run(player, track_index=0):
    visual_map, logic_map, total_laps, track_reward = load_track_layers(track_index)
    start_x, start_y = TRACKS[track_index]["start_pos"]

    font_hud = pygame.font.SysFont("Arial", 28, bold=True)
    font_big = pygame.font.SysFont("Arial", 64, bold=True)

    cam_size = 900
    camera_view = pygame.Surface((cam_size, cam_size))

    race_started = False
    race_finished = False
    start_ticks = 0
    elapsed_time = 0.0

    current_lap = 1
    checkpoint_passed = False
    reward_coins = 0

    car = player.formule_list[player.formule_index]
    car.angle = TRACKS[track_index]["start_angle"]

    show_logic_map = False

    gameStatus = True
    while gameStatus:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT", 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU", 0

                if event.key == pygame.K_m:
                    show_logic_map = not show_logic_map

                if event.key == pygame.K_SPACE and not race_started:
                    race_started = True
                    start_ticks = pygame.time.get_ticks()
                elif race_finished or car.dnf_status:
                    if event.key == pygame.K_SPACE:
                        return "MENU", reward_coins

        in_pit_zone = math.hypot(car.x - start_x, car.y - start_y) < 180

        if race_started and not race_finished:
            key = pygame.key.get_pressed()
            car.control(key)
            under_car_colour = car.move(logic_map)

            if in_pit_zone and abs(car.speed) < 0.5 and key[pygame.K_r] and not car.dnf_status:
                car.pit_stop_repair()

            if not car.dnf_status:
                elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000.0

                if under_car_colour == (0, 0, 255):
                    checkpoint_passed = True
                elif under_car_colour == (255, 255, 255) and checkpoint_passed:
                    checkpoint_passed = False
                    if current_lap < total_laps:
                        current_lap += 1
                    else:
                        race_finished = True
                        reward_coins = track_reward

        camera_view.fill(settings.colour.Green)

        offset_x = (cam_size // 2) - int(car.x)
        offset_y = (cam_size // 2) - int(car.y)

        active_map = logic_map if show_logic_map else visual_map
        camera_view.blit(active_map, (offset_x, offset_y))

        zoomed_view = pygame.transform.scale(camera_view, (cam_size * 2, cam_size * 2))
        rotated_world = pygame.transform.rotate(zoomed_view, car.angle + 90)

        world_rect = rotated_world.get_rect(center=(settings.width // 2, settings.height // 2))
        settings.screen.blit(rotated_world, world_rect)

        car.render()
        hud(car, elapsed_time, current_lap, total_laps, font_hud, in_pit_zone)

        if not race_started:
            draw_panel(settings.screen, font_big, "Press SPACE to start", (255, 255, 0))
        elif race_finished:
            draw_panel(settings.screen, font_big, f"WIN: +{reward_coins} Coins (Press SPACE)", (50, 255, 50))
        elif car.dnf_status:
            draw_panel(settings.screen, font_big, "DNF - FORMULE - DESTROYED! (Press SPACE)", (255, 50, 50))

        pygame.display.flip()
        settings.time.tick(settings.fps)

def draw_panel(screen, font, text, colour):
    screen_w, screen_h = screen.get_size()
    text_surf = font.render(text, True, colour)
    text_rect = text_surf.get_rect(center=(screen_w // 2, screen_h // 2 - 120))
    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(40, 20), border_radius=10)
    screen.blit(text_surf, text_rect)

def get_status_colour(val):
    if val > 60:
        return (100, 255, 100)
    elif val > 25:
        return (255, 215, 0)
    else:
        return (255, 70, 70)

def hud(formule, elapsed_time, current_lap, total_laps, font_hud, in_pit_zone):
    kmh = int(abs(formule.speed) * 45)

    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    hundredths = int((elapsed_time * 100) % 100)
    time_string = f"{minutes:02d}:{seconds:02d}.{hundredths:02d}"

    hud_bg = pygame.Surface((330, 310), pygame.SRCALPHA)
    hud_bg.fill((0, 0, 0, 150))
    settings.screen.blit(hud_bg, (10, 10))

    basic_info = [
        (f"Lap: {current_lap} / {total_laps}", (255, 255, 255)),
        (f"Time: {time_string}", (255, 255, 255)),
        (f"Speed: {kmh} km/h", (200, 230, 255)),
    ]

    tire_note = " (DEFECT!)" if formule.tire_status <= 5.0 else ""
    component_info = [
        (f"Tires ({formule.tires.upper()}): {int(formule.tire_status)} %{tire_note}", get_status_colour(formule.tire_status)),
        (f"Brakes: {int(formule.brakes_status)} %", get_status_colour(formule.brakes_status)),
        (f"Engine: {int(formule.engine_status)} %", get_status_colour(formule.engine_status)),
        (f"Transmission: {int(formule.transmission_status)} %", get_status_colour(formule.transmission_status)),
        (f"Steering: {int(formule.steering_status)} %", get_status_colour(formule.steering_status)),
        (f"Body / Aero: {int(formule.body_status)} %", get_status_colour(formule.body_status)),
    ]

    all_rows = basic_info + component_info

    for i, (text, col) in enumerate(all_rows):
        text_surf = font_hud.render(text, True, col)
        settings.screen.blit(text_surf, (22, 18 + i * 30))

    if in_pit_zone and not formule.dnf_status:
        pit_surf = font_hud.render("PIT ZONE: Stop and hold [R] to repair", True, (255, 255, 0))
        settings.screen.blit(pit_surf, (20, 330))