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
            self.transmission_status = max(0.0, self.transmission_status - 0.008)

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
    def move(self, screen):
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed

        self.distance += abs(self.speed)

        if self.x < 20 or self.x > screen.width - 20 or self.y < 20 or self.y > screen.height - 20:
            if abs(self.speed) > 1.5:
                self.body_status = max(0.0, self.body_status - abs(self.speed) * 2)
            self.speed *= 0.5
            self.x = pygame.math.clamp(self.x, 20, screen.width - 20)
            self.y = pygame.math.clamp(self.y, 20, screen.height - 20)

        pos_pixel = (int(self.x), int(self.y))
        detected_colour = screen.get_at(pos_pixel)[:3]

        if detected_colour == (0, 153, 0):
            self.speed *= 0.90
            self.tire_status = max(0.0, self.tire_status - 0.03 * abs(self.speed))

        if self.engine_status <= 0 or self.transmission_status <= 0 or self.body_status <= 0:
            self.dnf_status = True
    def render(self, screen):
        shape = pygame.Surface((40, 20), pygame.SRCALPHA)

        pygame.draw.rect(shape, self.colour, (0, 3, 40, 14), border_radius=4)
        pygame.draw.rect(shape, (0, 0, 0), (5, 0, 8, 20))
        pygame.draw.rect(shape, (0, 0, 0), (28, 0, 8, 20))

        turned_formule = pygame.transform.rotate(shape, -self.angle)
        pos = turned_formule.get_rect(center=(self.x, self.y))

        screen.blit(turned_formule, pos)
def run(screen, fps, time, formule):

    colourBlack = (0, 0, 0)
    colourPath = (80, 80, 80)
    colourGrass = (0, 153, 0)
    colourRed = (255, 0, 0)
    colourLightGray = (130, 130, 130)
    colourWhite = (255, 255, 255)

    track = pygame.Rect(50, 50, 1500, 800)
    inner_grass = pygame.Rect(180, 180, 440, 240)
    line = pygame.Rect(400, 420, 10, 130)

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

    gameStatus = True
    while gameStatus:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"
        key = pygame.key.get_pressed()
        formule.control(key)

        screen.fill(colourGrass)
        pygame.draw.rect(screen, colourPath, track)
        pygame.draw.rect(screen, colourWhite, track, width=4, border_radius=80)
        pygame.draw.rect(screen, colourGrass, inner_grass, border_radius=40)
        pygame.draw.rect(screen, colourWhite, inner_grass, width=4, border_radius=40)
        pygame.draw.rect(screen, colourWhite, line)
        formule.move(screen)
        formule.render(screen)
        hud(screen, formule)
        pygame.display.flip()
        time.tick(fps)
def hud(screen, player):
    font = pygame.font.SysFont("Arial", 36)

    kmh = int(abs(player.speed) * 45)

    stats = [
        f"Speed: {kmh} km/h",
        f"Tires ({player.tires}): {int(player.tire_status)} %",
        f"Brakes: {int(player.brakes_status)} %",
        f"Engine: {int(player.engine_status)} %",
        f"Body: {int(player.body_status)} %"
    ]

    if player.dnf_status:
        stats.append("STAV: DNF (Zniceno!)")

    for i, radek in enumerate(stats):
        text_surf = font.render(radek, True, (255, 255, 255))
        screen.blit(text_surf, (20, 15 + i * 25))