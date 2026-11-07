import pygame
pygame.init()
import game
import menu
import player
import settings
import json
import os


player = player.Player()

upgrade_cost = 200


def save_game(coins, formule_list):
    data = {
        "coins": coins,
        "formule_list": formule_list
    }
    with open(settings.save_file, "w") as file:
        json.dump(data, file, indent=4)
def load_game():
    if os.path.exists(settings.save_file):
        with open(settings.save_file, "r") as file:
            data = json.load(file)
            for auto in data["formule_list"]:
                auto["colour"] = tuple(auto["colour"])

            return data["coins"], data["formule_list"]
    return None, None

while settings.menuStatus:
    menu.draw(player)
    pygame.display.flip()
    settings.time.tick(settings.fps)

pygame.quit()