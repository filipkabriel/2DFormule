import pygame
import game
import garage
import settings

buttonPlay = pygame.Rect(680, 280, 240, 60)
buttonGarage = pygame.Rect(680, 370, 240, 60)
buttonStats = pygame.Rect(680, 460, 240, 60)
buttonEnd = pygame.Rect(680, 550, 240, 60)

buttonTrack1 = pygame.Rect(600, 280, 400, 60)
buttonTrack2 = pygame.Rect(600, 380, 400, 60)
buttonTrack3 = pygame.Rect(600, 480, 400, 60)
buttonBackTrack = pygame.Rect(700, 620, 200, 60)

buttonBackStats = pygame.Rect(700, 760, 200, 60)
stats_scroll_y = 0

def reset_car_for_race(car, start_pos):
    car.x, car.y = start_pos
    car.angle = 180
    car.speed = 0
    car.vx = 0
    car.vy = 0
    car.angular_velocity = 0
    car.dnf_status = False
    car.body_status = 100
    car.engine_status = 100
    car.transmission_status = 100
    car.steering_status = 100
    car.tire_status = 100
    car.brakes_status = 100

def draw_stats(player, mouse_pos):
    global stats_scroll_y
    settings.screen.fill((22, 24, 32))

    title_surf = settings.fontTitle.render("STATISTICS", True, settings.colour.White)
    settings.screen.blit(title_surf, title_surf.get_rect(center=(settings.width // 2, 80)))

    stats = player.statistics
    win_rate = int((stats.wins / stats.races) * 100) if stats.races > 0 else 0
    total_km = round(stats.total_distance / 1000.0, 2)

    overview_rect = pygame.Rect(250, 150, 1100, 140)
    pygame.draw.rect(settings.screen, (38, 42, 54), overview_rect, border_radius=12)

    left_info = [
        f"Races: {stats.races}   |   Wins: {stats.wins} ({win_rate} %)",
        f"DNF: {stats.dnf_count}   |   Distance: {total_km} km"
    ]
    for i, text in enumerate(left_info):
        s = settings.fontButton.render(text, True, settings.colour.White)
        settings.screen.blit(s, (290, 175 + i * 50))

    list_border = pygame.Rect(250, 320, 1100, 410)
    pygame.draw.rect(settings.screen, (38, 42, 54), list_border, border_radius=12)
    pygame.draw.rect(settings.screen, settings.colour.LightGray, list_border, width=2, border_radius=12)

    row_height = 110
    content_height = len(game.TRACKS) * row_height + 20
    min_scroll = min(0, list_border.height - content_height)
    stats_scroll_y = max(min_scroll, min(0, stats_scroll_y))

    settings.screen.set_clip(list_border)

    for idx, track in enumerate(game.TRACKS):
        t_stat = stats.get_track(track.name)
        card_y = list_border.y + 15 + idx * row_height + stats_scroll_y
        card_rect = pygame.Rect(list_border.x + 20, card_y, list_border.width - 40, 95)

        pygame.draw.rect(settings.screen, (52, 56, 72), card_rect, border_radius=10)

        name_surf = settings.fontButton.render(f"{idx + 1}. {track.name}", True, settings.colour.Yellow)
        settings.screen.blit(name_surf, (card_rect.x + 20, card_rect.y + 10))

        times_text = (
            f"Best Lap: {game.format_time(t_stat['best_lap'])}   |   "
            f"Best Race: {game.format_time(t_stat['best_race'])}   |   "
            f"Avg: {game.format_time(t_stat['avg_race'])}"
        )
        times_surf = settings.fontButton.render(times_text, True, settings.colour.White)
        settings.screen.blit(times_surf, (card_rect.x + 20, card_rect.y + 52))

    settings.screen.set_clip(None)

    settings.draw_button(buttonBackStats, "BACK", settings.fontButton, mouse_pos)

def draw(player):
    mouse_pos = pygame.mouse.get_pos()
    stats_scroll_y = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            settings.menuStatus = False

        if event.type == pygame.MOUSEWHEEL and settings.state == "STATS":
            stats_scroll_y += event.y * 35

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if settings.state == "MENU":
                if buttonPlay.collidepoint(mouse_pos):
                    settings.state = "TRACK_SELECT"
                elif buttonGarage.collidepoint(mouse_pos):
                    settings.state = "GARAGE"
                elif buttonStats.collidepoint(mouse_pos):
                    settings.state = "STATS"
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

            elif settings.state == "STATS":
                if buttonBackStats.collidepoint(mouse_pos):
                    settings.state = "MENU"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and settings.state in ["GARAGE", "TRACK_SELECT", "STATS"]:
                settings.state = "MENU"

    if settings.state == "MENU":
        settings.screen.fill(settings.colour.Black)

        title_surf = settings.fontTitle.render("2D Formule", True, settings.colour.White)
        settings.screen.blit(title_surf, title_surf.get_rect(center=(settings.width // 2, 150)))

        settings.draw_button(buttonPlay, "PLAY", settings.fontButton, mouse_pos)
        settings.draw_button(buttonGarage, "GARAGE", settings.fontButton, mouse_pos)
        settings.draw_button(buttonStats, "STATISTICS", settings.fontButton, mouse_pos)
        settings.draw_button(buttonEnd, "QUIT", settings.fontButton, mouse_pos)

    elif settings.state == "TRACK_SELECT":
        settings.screen.fill((20, 30, 20))

        title_surf = settings.fontTitle.render("SELECT TRACK", True, settings.colour.White)
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

    elif settings.state == "STATS":
        draw_stats(player, mouse_pos)