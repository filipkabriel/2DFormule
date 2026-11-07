import pygame
import math
import settings

def create_map():
    map_w, map_h = 2400, 1600
    world_map = pygame.Surface((map_w, map_h))

    track = pygame.Rect(200, 200, 2000, 1200)
    inner_grass = pygame.Rect(450, 450, 1500, 700)

    line = pygame.Rect(1100, 1150, 20, 250)
    checkpoint = pygame.Rect(1100, 200, 50, 250)

    world_map.fill(settings.colour.Green)
    pygame.draw.rect(world_map, settings.colour.LightGray, track, border_radius=120)
    pygame.draw.rect(world_map, settings.colour.White, track, width=6, border_radius=120)
    pygame.draw.rect(world_map, settings.colour.Green, inner_grass, border_radius=80)
    pygame.draw.rect(world_map, settings.colour.White, inner_grass, width=6, border_radius=80)
    pygame.draw.rect(world_map, settings.colour.White, line)
    return world_map, line, checkpoint

def run(player):
    world_map, line, checkpoint = create_map()

    font_hud = pygame.font.SysFont("Arial", 32)
    font_big = pygame.font.SysFont("Arial", 64, bold=True)

    cam_size = 900
    camera_view = pygame.Surface((cam_size, cam_size))

    race_started = False
    race_finished = False
    start_ticks = 0
    elapsed_time = 0.0

    current_lap = 1
    total_laps = 3
    checkpoint_passed = False
    reward_coins = 0

    gameStatus = True
    while gameStatus:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT", 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU", 0

                if event.key == pygame.K_SPACE and not race_started:
                    race_started = True
                    start_ticks = pygame.time.get_ticks()
                elif race_finished or player.formule_list[player.formule_index].dnf_status:
                    if event.key == pygame.K_SPACE:
                        return "MENU", reward_coins

        if race_started and not race_finished:
            key = pygame.key.get_pressed()
            player.formule_list[player.formule_index].control(key)
            player.formule_list[player.formule_index].move(world_map)

            if not player.formule_list[player.formule_index].dnf_status:
                elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000.0

                if checkpoint.collidepoint(player.formule_list[player.formule_index].x, player.formule_list[player.formule_index].y):
                    checkpoint_passed = True
                if line.collidepoint(player.formule_list[player.formule_index].x, player.formule_list[player.formule_index].y) and checkpoint_passed:
                    checkpoint_passed = False
                    if current_lap < total_laps:
                        current_lap += 1
                    else:
                        race_finished = True
                        reward_coins = 300

        camera_view.fill(settings.colour.Green)

        offset_x = (cam_size // 2) - int(player.formule_list[player.formule_index].x)
        offset_y = (cam_size // 2) - int(player.formule_list[player.formule_index].y)
        camera_view.blit(world_map, (offset_x, offset_y))

        zoomed_view = pygame.transform.scale(camera_view, (cam_size * 2, cam_size * 2))

        rotated_world = pygame.transform.rotate(zoomed_view, player.formule_list[player.formule_index].angle + 90)

        world_rect = rotated_world.get_rect(center=(settings.width // 2, settings.height // 2))
        settings.screen.blit(rotated_world, world_rect)

        player.formule_list[player.formule_index].render()
        hud(player.formule_list[player.formule_index], elapsed_time, current_lap, total_laps, font_hud)

        if not race_started:
            draw_panel(settings.screen, font_big, "STISKNI MEZERNIK PRO START", (255, 255, 0))
        elif race_finished:
            draw_panel(settings.screen, font_big, f"CIL! Vyhra: +{reward_coins} Coins (Stiskni SPACE)", (50, 255, 50))
        elif player.formule_list[player.formule_index].dnf_status:
            draw_panel(settings.screen, font_big, "DNF - AUTO ZNICENO! (Stiskni SPACE)", (255, 50, 50))
        pygame.display.flip()
        settings.time.tick(settings.fps)
def draw_panel(screen, font, text, colour):
    screen_w, screen_h = screen.get_size()
    text_surf = font.render(text, True, colour)
    text_rect = text_surf.get_rect(center=(screen_w // 2, screen_h // 2 - 120))
    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(40, 20), border_radius=10)
    screen.blit(text_surf, text_rect)
def hud(formule, elapsed_time,current_lap, total_laps, font_hud):
    font_hud = pygame.font.SysFont("Arial", 36)

    kmh = int(abs(formule.speed) * 45)

    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    hundredths = int((elapsed_time * 100) % 100)

    time_string = f"{minutes:02d}:{seconds:02d}.{hundredths:02d}"

    stats = [
        f"Lap: {current_lap} / {total_laps}",
        f"Time: {time_string}",
        f"Speed: {kmh} km/h",
        f"Tires ({formule.tires}): {int(formule.tire_status)} %",
        f"Brakes: {int(formule.brakes_status)} %",
        f"Engine: {int(formule.engine_status)} %",
        f"Body: {int(formule.body_status)} %"
    ]

    if formule.dnf_status:
        stats.append("STAV: DNF (Zniceno!)")

    for i, radek in enumerate(stats):
        text_surf = font_hud.render(radek, True, (255, 255, 255))
        settings.screen.blit(text_surf, (20, 15 + i * 25))