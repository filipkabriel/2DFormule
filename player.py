import pygame
import settings
import garage

class Player():
        def __init__(self):
             coins = 0
             formule_list = [{
                "ai": False,
                "name": "Formule 1",
                "colour": settings.colour.Red,
                "engine": 60,
                "transmission": 60,
                "steering": 60,
                "brakes": 60,
                "weight": 700,
                "tires": garage.tires_list[garage.tire_index]
                }]
             formule_index = 0
