import pygame
import math
class Formule:
    def __init__(self, ai, name, x, y, colour, engine, transmission, steering, brakes, weight, tires):
        self.ai = ai
        self.name = name
        self.x = x
        self.y = y
        self.colour = colour
        self.engine = engine
        self.transmission = transmission
        self.steering = steering
        self.brakes = brakes
        self.weight = weight
        self.tires = tires

        self.dnf_status = False
        self.body_status = 100
        self.engine_status = 100
        self.transmission_status = 100
        self.steering_status = 100
        self.tire_status = 100
        self.brakes_status = 100

        self.angle = 180
        self.speed = 0
        self.distance = 0

    def control(self, key):
        if self.dnf_status:
            self.speed *= 0.95
            return

        ef_engine = max(0.2, self.engine_status / 100.0)
        ef_transmission = max(0.2, self.transmission_status / 100.0)
        ef_brakes = max(0.1, self.brakes_status / 100.0)
        ef_tires = max(0.3, self.tire_status / 100.0)
        ef_steering = max(0.3, self.steering_status / 100.0)

        max_speed = (self.engine / 5.0) * ef_engine
        acc = (self.transmission / 1000.0) * ef_transmission
        brake_power = (self.brakes / 1300.0) * ef_brakes
        steer_speed = (self.steering / 30.0) * ef_steering * ef_tires

        if key[pygame.K_w]:
            if self.speed < max_speed:
                self.speed += acc
            self.engine_status = max(0.0, self.engine_status - 0.0001)
            self.transmission_status = max(0.0, self.transmission_status - 0.0002)

        elif key[pygame.K_s]:
            if self.speed > 0:
                self.speed -= brake_power
                self.brakes_status = max(0.0, self.brakes_status - 0.03)
                self.tire_status = max(0.0, self.tire_status - 0.01)
            else:
                if self.speed > -2.0:
                    self.speed -= acc * 0.5

        self.speed *= 0.985

        if abs(self.speed) < 0.05 and not (key[pygame.K_w] or key[pygame.K_s]):
            self.speed = 0.0

        if abs(self.speed) > 0.1:
            ride_dir  = 1 if self.speed > 0 else -1

            if key[pygame.K_a]:
                self.angle -= steer_speed * ride_dir
                self.tire_status = max(0.0, self.tire_status - 0.001 * abs(self.speed))
                self.steering_status = max(0.0, self.steering_status - 0.002)

            if key[pygame.K_d]:
                self.angle += steer_speed * ride_dir
                self.tire_status = max(0.0, self.tire_status - 0.001 * abs(self.speed))
                self.steering_status = max(0.0, self.steering_status - 0.002)
    def move(self, screen, world_map):
        map_w, map_h = world_map.get_size()

        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed

        self.distance += abs(self.speed)

        if self.x < 20 or self.x > map_w - 20 or self.y < 20 or self.y > map_h - 20:
            if abs(self.speed) > 1.5:
                self.body_status = max(0.0, self.body_status - abs(self.speed) * 2)
            self.speed *= 0.5
            self.x = pygame.math.clamp(self.x, 20, map_w - 20)
            self.y = pygame.math.clamp(self.y, 20, map_h - 20)

        pos_pixel = (int(self.x), int(self.y))
        detected_colour = world_map.get_at(pos_pixel)[:3]

        if detected_colour == (0, 153, 0):
            self.speed *= 0.90
            self.tire_status = max(0.0, self.tire_status - 0.03 * abs(self.speed))

        if self.engine_status <= 0 or self.transmission_status <= 0 or self.body_status <= 0:
            self.dnf_status = True
    def render(self, screen):
        shape = pygame.Surface((20, 40), pygame.SRCALPHA)

        pygame.draw.rect(shape, self.colour, (3, 0, 14, 40), border_radius=4)
        pygame.draw.rect(shape, (0, 0, 0), (0, 5, 20, 8))
        pygame.draw.rect(shape, (0, 0, 0), (0, 28, 20, 8))

        zoomed_car = pygame.transform.scale(shape, (40, 80))

        screen_w, screen_h = screen.get_size()
        pos = zoomed_car.get_rect(center=(screen_w // 2, screen_h // 2))
        screen.blit(zoomed_car, pos)
def run(screen, fps, time, formule):
    screen_w, screen_h = screen.get_size()
    colourBlack = (0, 0, 0)
    colourPath = (80, 80, 80)
    colourGrass = (0, 153, 0)
    colourRed = (255, 0, 0)
    colourLightGray = (130, 130, 130)
    colourWhite = (255, 255, 255)

    map_w, map_h = 2400, 1600
    world_map = pygame.Surface((map_w, map_h))

    track = pygame.Rect(200, 200, 2000, 1200)
    inner_grass = pygame.Rect(450, 450, 1500, 700)

    line = pygame.Rect(1100, 1150, 20, 250)
    checkpoint = pygame.Rect(1100, 200, 50, 250)

    world_map.fill(colourGrass)
    pygame.draw.rect(world_map, colourPath, track, border_radius=120)
    pygame.draw.rect(world_map, colourWhite, track, width=6, border_radius=120)
    pygame.draw.rect(world_map, colourGrass, inner_grass, border_radius=80)
    pygame.draw.rect(world_map, colourWhite, inner_grass, width=6, border_radius=80)
    pygame.draw.rect(world_map, colourWhite, line)

    formule = Formule(
        formule["ai"],
        formule["name"],
        430, 485,
        formule["colour"],
        formule["engine"],
        formule["transmission"],
        formule["steering"],
        formule["brakes"],
        formule["weight"],
        formule["tires"]
    )

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
                elif race_finished or formule.dnf_status:
                    if event.key == pygame.K_SPACE:
                        return "MENU", reward_coins

        if race_started and not race_finished:
            key = pygame.key.get_pressed()
            formule.control(key)
            formule.move(screen, world_map)

            if not formule.dnf_status:
                elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000.0

                if checkpoint.collidepoint(formule.x, formule.y):
                    checkpoint_passed = True
                if line.collidepoint(formule.x, formule.y) and checkpoint_passed:
                    checkpoint_passed = False
                    if current_lap < total_laps:
                        current_lap += 1
                    else:
                        race_finished = True
                        reward_coins = 300

        camera_view.fill(colourGrass)

        offset_x = (cam_size // 2) - int(formule.x)
        offset_y = (cam_size // 2) - int(formule.y)
        camera_view.blit(world_map, (offset_x, offset_y))

        zoomed_view = pygame.transform.scale(camera_view, (cam_size * 2, cam_size * 2))

        rotated_world = pygame.transform.rotate(zoomed_view, formule.angle + 90)

        world_rect = rotated_world.get_rect(center=(screen_w // 2, screen_h // 2))
        screen.blit(rotated_world, world_rect)

        formule.render(screen)
        hud(screen, formule, elapsed_time, current_lap, total_laps, font_hud)

        if not race_started:
            draw_panel(screen, font_big, "STISKNI MEZERNIK PRO START", (255, 255, 0))
        elif race_finished:
            draw_panel(screen, font_big, f"CIL! Vyhra: +{reward_coins} Coins (Stiskni SPACE)", (50, 255, 50))
        elif formule.dnf_status:
            draw_panel(screen, font_big, "DNF - AUTO ZNICENO! (Stiskni SPACE)", (255, 50, 50))
        pygame.display.flip()
        time.tick(fps)
def draw_panel(screen, font, text, colour):
    screen_w, screen_h = screen.get_size()
    text_surf = font.render(text, True, colour)
    text_rect = text_surf.get_rect(center=(screen_w // 2, screen_h // 2 - 120))
    pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(40, 20), border_radius=10)
    screen.blit(text_surf, text_rect)
def hud(screen, player, elapsed_time,current_lap, total_laps, font_hud):
    font_hud = pygame.font.SysFont("Arial", 36)

    kmh = int(abs(player.speed) * 45)

    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    hundredths = int((elapsed_time * 100) % 100)

    time_string = f"{minutes:02d}:{seconds:02d}.{hundredths:02d}"

    stats = [
        f"Lap: {current_lap} / {total_laps}",
        f"Time: {time_string}",
        f"Speed: {kmh} km/h",
        f"Tires ({player.tires}): {int(player.tire_status)} %",
        f"Brakes: {int(player.brakes_status)} %",
        f"Engine: {int(player.engine_status)} %",
        f"Body: {int(player.body_status)} %"
    ]

    if player.dnf_status:
        stats.append("STAV: DNF (Zniceno!)")

    for i, radek in enumerate(stats):
        text_surf = font_hud.render(radek, True, (255, 255, 255))
        screen.blit(text_surf, (20, 15 + i * 25))