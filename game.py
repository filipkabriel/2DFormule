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

        self.body_status = 100
        self.engine_status = 100
        self.transmission_status = 100
        self.steering_status = 100
        self.tire_status = 100
        self.brakes_status = 100

        self.angle = 180
        self.speed = 0
        self.distance = 0
    def move(self, screen):
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed

        self.x = pygame.math.clamp(self.x, 20, screen.width - 20)
        self.y = pygame.math.clamp(self.y, 20, screen.height - 20)
    def render(self, screen):
        shape = pygame.Surface((40, 20), pygame.SRCALPHA)

        pygame.draw.rect(shape, self.colour, (0, 3, 40, 14), border_radius=4)
        pygame.draw.rect(shape, (0, 0, 0), (5, 0, 8, 20))
        pygame.draw.rect(shape, (0, 0, 0), (28, 0, 8, 20))

        turned_formule = pygame.transform.rotate(shape, -self.angle)
        pos = turned_formule.get_rect(center=(self.x, self.y))

        screen.blit(turned_formule, pos)
def run(screen, fps, time):
    width, height = screen.get_size()

    colourBlack = (0, 0, 0)
    colourPath = (80, 80, 80)
    colourGrass = (0, 153, 0)
    colourRed = (255, 0, 0)
    colourLightGray = (130, 130, 130)
    colourWhite = (255, 255, 255)

    testformule = Formule(False, "GOAT", 375, 275, colourRed, 100 , 100 , 100, 100, 100, "soft")

    speed = 1
    font = pygame.font.SysFont("Arial", 24)

    gameStatus = True
    while gameStatus:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"
        key = pygame.key.get_pressed()
        if testformule.speed != speed:
            if key[pygame.K_a]:
                testformule.angle -= 2
            if key[pygame.K_d]:
                testformule.angle += 2
        if key[pygame.K_w]:
            testformule.speed += speed
        if key[pygame.K_s]:
            testformule.speed -= speed

        testformule.move(screen)
        screen.fill(colourGrass)
        testformule.render(screen)
        pygame.display.flip()
        time.tick(fps)
