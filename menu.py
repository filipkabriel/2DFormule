import pygame
import game
import garage
import settings

buttonPlay = pygame.Rect(680, 280, 240, 60)
buttonGarage = pygame.Rect(680, 370, 240, 60)
buttonStats = pygame.Rect(680, 460, 240, 60)
buttonSettings = pygame.Rect(680, 550, 240, 60)
buttonEnd = pygame.Rect(680, 640, 240, 60)

track_list_area = pygame.Rect(450, 230, 700, 490)
buttonBackTrack = pygame.Rect(700, 760, 200, 60)
track_scroll_y = 0

buttonBackStats = pygame.Rect(700, 760, 200, 60)
stats_scroll_y = 0

btnToggleControls = pygame.Rect(860, 260, 280, 55)
btnToggleMinimap = pygame.Rect(860, 345, 280, 55)
btnToggleUnits = pygame.Rect(860, 430, 280, 55)
btnToggleFps = pygame.Rect(860, 515, 280, 55)
buttonBackSettings = pygame.Rect(700, 760, 200, 60)


def reset_car_for_race(car, track):
    car.x, car.y = track.start_pos
    car.angle = track.start_angle
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


def format_laps(laps):
    if laps == 1:
        return "1 kolo"
    elif 2 <= laps <= 4:
        return f"{laps} kola"
    return f"{laps} kol"


def update_track_scroll(delta_y=0):
    global track_scroll_y
    row_step = 85
    content_height = len(game.TRACKS) * row_step + 20
    min_scroll = min(0, track_list_area.height - content_height)
    track_scroll_y = max(min_scroll, min(0, track_scroll_y + delta_y))


def get_track_buttons():
    buttons = []
    row_step = 85
    for idx, track in enumerate(game.TRACKS):
        btn_y = track_list_area.y + 15 + idx * row_step + track_scroll_y
        rect = pygame.Rect(
            track_list_area.x + 30,
            btn_y,
            track_list_area.width - 60,
            65
        )
        label = f"{idx + 1}. {track.name} ({format_laps(track.laps)} | {track.reward}$)"
        buttons.append((idx, rect, label))
    return buttons


def draw_track_select(mouse_pos):
    settings.screen.fill((20, 30, 20))

    title_surf = settings.fontTitle.render("SELECT TRACK", True, settings.colour.White)
    settings.screen.blit(title_surf, title_surf.get_rect(center=(settings.width // 2, 140)))

    update_track_scroll(0)
    settings.screen.set_clip(track_list_area)

    for _, rect, label in get_track_buttons():
        if rect.bottom >= track_list_area.top and rect.top <= track_list_area.bottom:
            settings.draw_button(rect, label, settings.fontButton, mouse_pos)

    settings.screen.set_clip(None)
    settings.draw_button(buttonBackTrack, "BACK", settings.fontButton, mouse_pos)


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

def draw_settings(mouse_pos):
    settings.screen.fill((22, 24, 32))

    title_surf = settings.fontTitle.render("SETTINGS", True, settings.colour.White)
    settings.screen.blit(title_surf, title_surf.get_rect(center=(settings.width // 2, 110)))

    panel_rect = pygame.Rect(420, 220, 760, 390)
    pygame.draw.rect(settings.screen, (38, 42, 54), panel_rect, border_radius=14)

    controls_labels = {"BOTH": "WSAD" + "ARROWS", "WSAD": "ONLY WSAD", "ARROWS" : "ONLY ARROWS"}
    rows = [
        ("Controls", controls_labels[settings.control_scheme], btnToggleControls, 270),
        ("Minimap:", "ON" if settings.show_minimap else "OFF", btnToggleMinimap, 355),
        ("speed Unit", settings.speed_unit, btnToggleUnits, 440),
        ("FPS Limit", f"{settings.fps} FPS", btnToggleFps, 425),
    ]

    for label, btn_text, btn_rect, y_pos in rows:
        lbl_surf = settings.fontButton.render(label, True, settings.colour.White)
        settings.screen.blit(lbl_surf, (470, y_pos))
        settings.draw_button(btn_rect, btn_text, settings.fontButton, mouse_pos)
    settings.draw_button(buttonBackSettings, "BACK", settings.fontButton, mouse_pos)
def draw(player):
    global stats_scroll_y
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            settings.menuStatus = False

        if event.type == pygame.MOUSEWHEEL:
            if settings.state == "STATS":
                stats_scroll_y += event.y * 35
            elif settings.state == "TRACK_SELECT":
                update_track_scroll(event.y * 35)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if settings.state == "MENU":
                if buttonPlay.collidepoint(mouse_pos):
                    settings.state = "TRACK_SELECT"
                elif buttonGarage.collidepoint(mouse_pos):
                    settings.state = "GARAGE"
                elif buttonStats.collidepoint(mouse_pos):
                    settings.state = "STATS"
                elif buttonSettings.collidepoint(mouse_pos):
                    settings.state = "SETTINGS"
                elif buttonEnd.collidepoint(mouse_pos):
                    settings.menuStatus = False

            elif settings.state == "TRACK_SELECT":
                if buttonBackTrack.collidepoint(mouse_pos):
                    settings.state = "MENU"
                elif track_list_area.collidepoint(mouse_pos):
                    for idx, rect, _ in get_track_buttons():
                        if rect.collidepoint(mouse_pos):
                            settings.selected_track = idx
                            settings.state = "PLAY"
                            break
            elif settings.state == "SETTINGS":
                if btnToggleControls.collidepoint(mouse_pos):
                    order = ["BOTH", "WASD", "ARROWS"]
                    idx = (order.index(settings.control_scheme) + 1) % len(order)
                    settings.control_scheme = order[idx]
                elif btnToggleMinimap.collidepoint(mouse_pos):
                    settings.show_minimap = not settings.show_minimap
                elif btnToggleUnits.collidepoint(mouse_pos):
                    settings.speed_unit = "MPH" if settings.speed_unit == "KMH" else "KMH"
                elif btnToggleFps.collidepoint(mouse_pos):
                    settings.fps = 120 if settings.fps == 60 else 60
                elif buttonBackSettings.collidepoint(mouse_pos):
                    settings.state = "MENU"
            elif settings.state == "GARAGE":
                garage.handle_click(player, mouse_pos)

            elif settings.state == "STATS":
                if buttonBackStats.collidepoint(mouse_pos):
                    settings.state = "MENU"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and settings.state in ["GARAGE", "TRACK_SELECT", "STATS", "SETTINGS"]:
                settings.state = "MENU"

    if settings.state == "MENU":
        settings.screen.fill(settings.colour.Black)

        title_surf = settings.fontTitle.render("2D Formule", True, settings.colour.White)
        settings.screen.blit(title_surf, title_surf.get_rect(center=(settings.width // 2, 150)))

        settings.draw_button(buttonPlay, "PLAY", settings.fontButton, mouse_pos)
        settings.draw_button(buttonGarage, "GARAGE", settings.fontButton, mouse_pos)
        settings.draw_button(buttonStats, "STATISTICS", settings.fontButton, mouse_pos)
        settings.draw_button(buttonSettings, "SETTINGS", settings.fontButton, mouse_pos)
        settings.draw_button(buttonEnd, "QUIT", settings.fontButton, mouse_pos)

    elif settings.state == "TRACK_SELECT":
        draw_track_select(mouse_pos)

    elif settings.state == "PLAY":
        selected = game.TRACKS[settings.selected_track]
        reset_car_for_race(player.formule_list[player.formule_index], selected)
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
    elif settings.state == "SETTINGS":
        draw_settings(mouse_pos)