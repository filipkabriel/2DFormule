import pygame

time = pygame.time.Clock()
fps = 60
width, height = 1600, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Formule")
state = "MENU"
menuStatus = True
save_file = "save.json"

fontButton = pygame.font.SysFont("Arial", 36)
fontTitle = pygame.font.SysFont("Arial", 80)

class colour:
    Black = (0, 0, 0)
    Gray = (80, 80, 80)
    Red = (255, 0, 0)
    LightGray = (130, 130, 130)
    White = (255, 255, 255)
    Yellow = (255, 255, 0)
    Green = (0, 255, 0)

def draw_button(rect, text, font, mouse_pos):
    rectCol = colour.LightGray if rect.collidepoint(mouse_pos) else colour.Gray
    pygame.draw.rect(screen, rectCol, rect, border_radius = 10)
    text_surface = font.render(text, True, colour.White)
    screen.blit(text_surface, text_surface.get_rect(center=rect.center))
