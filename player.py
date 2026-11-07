import pygame
import settings
import garage
import formule


class Player():
        def __init__(self):
             self.coins = 0
             self.formule_index = 0
             self.formule_list = [
                formule.Formule(
                    ai=False,
                    name="Formule 1",
                    colour=settings.colour.Red,
                    engine=60,
                    transmission=60,
                    steering=60,
                    brakes=60,
                    weight=700,
                    tires=garage.tires_list[garage.tire_index]
                    )]
class Statistics():
        def __init__(self):
            self.races = 0
            self.wins = 0
            self.avg_times = 0
            self.best_time = 0

