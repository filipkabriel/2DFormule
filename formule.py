import math
import pygame
import settings

class Formule:
    def __init__(self, ai, name, colour, engine, transmission, steering, brakes, weight, tires, car_type="Rookie", max_engine=100, max_transmission=100, max_steering=100, max_brakes=100):
        self.ai = ai
        self.name = name
        self.car_type = car_type
        self.x = 0
        self.y = 0
        self.colour = colour
        self.engine = engine
        self.transmission = transmission
        self.steering = steering
        self.brakes = brakes
        self.weight = weight
        self.tires = tires

        self.max_engine = max_engine
        self.max_transmission = max_transmission
        self.max_steering = max_steering
        self.max_brakes = max_brakes

        self.dnf_status = False
        self.body_status = 100.0
        self.engine_status = 100.0
        self.transmission_status = 100.0
        self.steering_status = 100.0
        self.tire_status = 100.0
        self.brakes_status = 100.0

        self.angle = 180.0
        self.speed = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.angular_velocity = 0.0
        self.on_grass = False
        self.distance = 0.0
        self.slip_intensity = 0.0

    def get_tire_modifiers(self):
        if self.tires == "soft":
            return 1.22, 1.55
        elif self.tires == "hard":
            return 0.88, 0.55
        else:
            return 1.00, 1.00

    def get_tire_grip_curve(self):
        if self.tire_status > 30.0:
            return 0.80 + 0.20 * ((self.tire_status - 30.0) / 70.0)
        elif self.tire_status > 5.0:
            return 0.35 + 0.45 * ((self.tire_status - 5.0) / 25.0)
        else:
            return 0.20

    def control(self, key):
        if self.dnf_status:
            self.speed *= 0.95
            self.vx *= 0.95
            self.vy *= 0.95
            return

        ef_engine = 0.30 + 0.70 * ((self.engine_status / 100.0) ** 1.3)
        ef_transmission = 0.25 + 0.75 * (self.transmission_status / 100.0)
        ef_brakes = 0.20 + 0.80 * ((self.brakes_status / 100.0) ** 1.4)
        ef_tires = self.get_tire_grip_curve()
        ef_steering = 0.35 + 0.65 * (self.steering_status / 100.0)
        ef_aero = 0.60 + 0.40 * (self.body_status / 100.0)

        tire_grip, tire_wear_mult = self.get_tire_modifiers()
        total_grip = tire_grip * ef_tires
        if self.on_grass:
            total_grip *= 0.50

        weight_factor = 700.0 / max(400.0, self.weight)

        puncture_penalty = 0.55 if self.tire_status <= 5.0 else 1.0
        max_speed = (self.engine / 4.5) * ef_engine * ef_aero * puncture_penalty
        acc = (self.transmission / 650.0) * ef_transmission * weight_factor * (0.7 + 0.3 * total_grip)
        brake_power = (self.brakes / 550.0) * ef_brakes * (0.6 + 0.4 * total_grip)

        forward_input = key[pygame.K_w] or key[pygame.K_UP]
        brake_input = key[pygame.K_s] or key[pygame.K_DOWN]
        left_input = key[pygame.K_a] or key[pygame.K_LEFT]
        right_input = key[pygame.K_d] or key[pygame.K_RIGHT]

        speed_ratio = abs(self.speed) / max(1.0, max_speed)

        if forward_input:
            if self.speed < 0:
                self.speed += brake_power * 1.2
                self.transmission_status = max(0.0, self.transmission_status - 0.015)
            elif self.speed < max_speed:
                current_acc = acc * max(0.15, 1.0 - (speed_ratio ** 1.6))
                self.speed += current_acc

            rpm_stress = 0.001 + 0.008 * (speed_ratio ** 2.5)
            grass_engine_stress = 2.0 if self.on_grass else 1.0
            self.engine_status = max(0.0, self.engine_status - rpm_stress * grass_engine_stress)

            trans_stress = 0.002 + 0.005 * (1.0 - speed_ratio)
            self.transmission_status = max(0.0, self.transmission_status - trans_stress)

            if speed_ratio < 0.35:
                wheelspin_wear = 0.005 * (1.0 - speed_ratio) * tire_wear_mult
                self.tire_status = max(0.0, self.tire_status - wheelspin_wear)

        elif brake_input:
            if self.speed > 0.1:
                self.speed = max(0.0, self.speed - brake_power)

                heat_stress = 0.005 + 0.035 * (speed_ratio ** 1.8)
                self.brakes_status = max(0.0, self.brakes_status - heat_stress)

                brake_tire_wear = (0.004 + 0.015 * (speed_ratio ** 1.5)) * tire_wear_mult
                self.tire_status = max(0.0, self.tire_status - brake_tire_wear)
                self.transmission_status = max(0.0, self.transmission_status - 0.003 * speed_ratio)
            else:
                reverse_max = -2.5
                if self.speed > reverse_max:
                    self.speed -= acc * 0.6

        aero_drag_mult = 1.0 + (100.0 - self.body_status) * 0.01
        air_resistance = 0.0008 * aero_drag_mult * (self.speed ** 2)
        if self.speed > 0:
            self.speed = max(0.0, self.speed - air_resistance - 0.015)
        elif self.speed < 0:
            self.speed = min(0.0, self.speed + 0.02)

        if abs(self.speed) < 0.04 and not (forward_input or brake_input):
            self.speed = 0.0

        steer_input = 0
        if left_input:
            steer_input -= 1
        if right_input:
            steer_input += 1

        if abs(self.speed) > 0.05:
            ride_dir = 1 if self.speed > 0 else -1

            low_speed_factor = min(1.0, abs(self.speed) / 2.2)
            high_speed_understeer = max(0.55, 1.0 - (abs(self.speed) / (max_speed * 2.1)))

            max_turn_rate = (self.steering / 22.0) * ef_steering * total_grip * low_speed_factor * high_speed_understeer
            target_ang_vel = steer_input * max_turn_rate * ride_dir

            alignment_pull = 0.0
            if self.steering_status < 65.0:
                alignment_pull += (65.0 - self.steering_status) * 0.006 * speed_ratio
            if self.tire_status <= 5.0:
                alignment_pull -= 0.35 * speed_ratio

            steer_response = 0.28 if steer_input != 0 else 0.40
            self.angular_velocity += (target_ang_vel + alignment_pull - self.angular_velocity) * steer_response
            self.angle = (self.angle + self.angular_velocity) % 360

            if steer_input != 0:
                scrub = 1.0 - (0.0025 * abs(self.angular_velocity))
                self.speed *= max(0.98, scrub)

                lateral_g = abs(self.angular_velocity) * abs(self.speed)
                corner_tire_wear = 0.0005 * lateral_g * tire_wear_mult
                self.tire_status = max(0.0, self.tire_status - corner_tire_wear)

                steer_stress = 0.0015 * (1.0 + speed_ratio) * (2.5 if self.on_grass else 1.0)
                self.steering_status = max(0.0, self.steering_status - steer_stress)
        else:
            self.angular_velocity = 0.0

    def move(self, logic_map):
        map_w, map_h = logic_map.get_size()
        old_x, old_y = self.x, self.y

        if self.speed == 0.0 and math.hypot(self.vx, self.vy) > 2.0:
            self.vx, self.vy = 0.0, 0.0
            self.angular_velocity = 0.0

        rad = math.radians(self.angle)
        target_vx = math.cos(rad) * self.speed
        target_vy = math.sin(rad) * self.speed

        tire_grip, tire_wear_mult = self.get_tire_modifiers()
        ef_tires = self.get_tire_grip_curve()

        base_traction = 0.14 if self.on_grass else 0.32
        traction = min(0.65, base_traction * tire_grip * ef_tires)

        self.slip_intensity = math.hypot(target_vx - self.vx, target_vy - self.vy)
        if self.slip_intensity > 0.35:
            drift_wear = (self.slip_intensity - 0.35) * 0.012 * tire_wear_mult
            self.tire_status = max(0.0, self.tire_status - drift_wear)

        self.vx += (target_vx - self.vx) * traction
        self.vy += (target_vy - self.vy) * traction

        self.x += self.vx
        self.y += self.vy

        actual_move_speed = math.hypot(self.vx, self.vy)
        self.distance += actual_move_speed

        if self.x < 20 or self.x > map_w - 20 or self.y < 20 or self.y > map_h - 20:
            self.apply_crash_damage(actual_move_speed)
            self.speed *= 0.4
            self.vx *= -0.4
            self.vy *= -0.4
            self.x = pygame.math.clamp(self.x, 20, map_w - 20)
            self.y = pygame.math.clamp(self.y, 20, map_h - 20)

        pos_pixel = (int(self.x), int(self.y))
        detected_colour = logic_map.get_at(pos_pixel)[:3]

        if detected_colour == (0, 153, 0):
            self.on_grass = True
            if abs(self.speed) > 2.5:
                self.speed *= 0.94
            else:
                self.speed *= 0.98
            self.tire_status = max(0.0, self.tire_status - 0.018 * actual_move_speed * tire_wear_mult)
            self.steering_status = max(0.0, self.steering_status - 0.006 * actual_move_speed)
            if actual_move_speed > 3.5:
                self.body_status = max(0.0, self.body_status - 0.004 * actual_move_speed)
        else:
            self.on_grass = False

        if detected_colour == (255, 0, 0):
            self.apply_crash_damage(actual_move_speed)
            self.x, self.y = old_x, old_y
            self.speed = -self.speed * 0.35
            self.vx = -self.vx * 0.4
            self.vy = -self.vy * 0.4

        if self.engine_status <= 0 or self.transmission_status <= 0 or self.body_status <= 0:
            self.dnf_status = True

        return detected_colour

    def apply_crash_damage(self, impact_speed):
        if impact_speed > 0.8:
            self.body_status = max(0.0, self.body_status - (impact_speed ** 1.4) * 2.2)
            self.steering_status = max(0.0, self.steering_status - (impact_speed ** 1.3) * 1.8)
            if impact_speed > 3.0:
                self.transmission_status = max(0.0, self.transmission_status - impact_speed * 1.2)
                self.engine_status = max(0.0, self.engine_status - impact_speed * 0.8)

    def pit_stop_repair(self):
        self.tire_status = min(100.0, self.tire_status + 1.2)
        self.brakes_status = min(100.0, self.brakes_status + 0.8)
        self.body_status = min(100.0, self.body_status + 0.5)
        self.steering_status = min(100.0, self.steering_status + 0.6)
        self.engine_status = min(100.0, self.engine_status + 0.3)
        self.transmission_status = min(100.0, self.transmission_status + 0.3)

    def render(self):
        shape = pygame.Surface((20, 40), pygame.SRCALPHA)

        wheel_offset = int(pygame.math.clamp(self.angular_velocity * 0.8, -2, 2))

        pygame.draw.rect(shape, self.colour, (3, 0, 14, 40), border_radius=4)
        pygame.draw.rect(shape, (0, 0, 0), (0 + wheel_offset, 5, 20, 8))
        pygame.draw.rect(shape, (0, 0, 0), (0, 28, 20, 8))

        zoomed_car = pygame.transform.scale(shape, (40, 80))

        drift_visual_angle = -self.angular_velocity * 2.2
        rotated_car = pygame.transform.rotate(zoomed_car, drift_visual_angle)

        pos = rotated_car.get_rect(center=(settings.width // 2, settings.height // 2))
        settings.screen.blit(rotated_car, pos)