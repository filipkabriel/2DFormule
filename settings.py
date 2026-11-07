import pygame

def setcreen():
    width, height = 1600,900
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("2D Formule")
    return screen
def gameinit():
    nie = 5

class colour:
    Black = (0, 0, 0)
    Gray = (80, 80, 80)
    Red = (255, 0, 0)
    LightGray = (130, 130, 130)
    White = (255, 255, 255)
    Yellow = (255, 255, 0)
