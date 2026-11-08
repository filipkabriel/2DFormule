import math
import pygame
import settings

class Formule:
    def __init__(self, ai, name, colour, engine, transmission, steering, brakes, weight, tires):
        self.ai = ai
        self.name = name
        self.x = 0
        self.y = 0
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
            ride_dir = 1 if self.speed > 0 else -1

            if key[pygame.K_a]:
                self.angle -= steer_speed * ride_dir
                self.tire_status = max(0.0, self.tire_status - 0.001 * abs(self.speed))
                self.steering_status = max(0.0, self.steering_status - 0.002)

            if key[pygame.K_d]:
                self.angle += steer_speed * ride_dir
                self.tire_status = max(0.0, self.tire_status - 0.001 * abs(self.speed))
                self.steering_status = max(0.0, self.steering_status - 0.002)

    def move(self, logic_map):
        map_w, map_h = logic_map.get_size()

        old_x, old_y = self.x, self.y

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
        detected_colour = logic_map.get_at(pos_pixel)[:3]

        if detected_colour == (0, 153, 0):
            self.speed *= 0.90
            self.tire_status = max(0.0, self.tire_status - 0.03 * abs(self.speed))

        elif detected_colour == (255, 0, 0):
            if abs(self.speed) > 1.0:
                self.body_status = max(0.0, self.body_status - abs(self.speed) * 3)
            self.x, self.y = old_x, old_y
            self.speed = -self.speed * 0.4

        if self.engine_status <= 0 or self.transmission_status <= 0 or self.body_status <= 0:
            self.dnf_status = True

        return detected_colour

    def render(self):
        shape = pygame.Surface((20, 40), pygame.SRCALPHA)

        pygame.draw.rect(shape, self.colour, (3, 0, 14, 40), border_radius=4)
        pygame.draw.rect(shape, (0, 0, 0), (0, 5, 20, 8))
        pygame.draw.rect(shape, (0, 0, 0), (0, 28, 20, 8))

        zoomed_car = pygame.transform.scale(shape, (40, 80))

        pos = zoomed_car.get_rect(center=(settings.width // 2, settings.height // 2))
        settings.screen.blit(zoomed_car, pos)