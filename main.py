import pygame
pygame.init()
import menu
import player
import settings

hrac = player.Player()

while settings.menuStatus:
    menu.draw(hrac)
    pygame.display.flip()
    settings.time.tick(settings.fps)

hrac.save()
pygame.quit()