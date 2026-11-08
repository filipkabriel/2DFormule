import json
import os
import pygame
import settings
import garage
import formule


class Player:
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
            )
        ]
        self.load()

    def save(self):
        cars_data = []
        for auto in self.formule_list:
            cars_data.append({
                "ai": auto.ai,
                "name": auto.name,
                "colour": list(auto.colour),
                "engine": auto.engine,
                "transmission": auto.transmission,
                "steering": auto.steering,
                "brakes": auto.brakes,
                "weight": auto.weight,
                "tires": auto.tires
            })

        data = {
            "coins": self.coins,
            "formule_index": self.formule_index,
            "formule_list": cars_data
        }

        with open(settings.save_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load(self):
        if os.path.exists(settings.save_file):
            try:
                with open(settings.save_file, "r", encoding="utf-8") as file:
                    data = json.load(file)

                self.coins = data.get("coins", 0)
                self.formule_index = data.get("formule_index", 0)

                loaded_cars = []
                for auto_dict in data.get("formule_list", []):
                    loaded_cars.append(
                        formule.Formule(
                            ai=auto_dict["ai"],
                            name=auto_dict["name"],
                            colour=tuple(auto_dict["colour"]),
                            engine=auto_dict["engine"],
                            transmission=auto_dict["transmission"],
                            steering=auto_dict["steering"],
                            brakes=auto_dict["brakes"],
                            weight=auto_dict["weight"],
                            tires=auto_dict["tires"]
                        )
                    )

                if loaded_cars:
                    self.formule_list = loaded_cars
                    current_tires = self.formule_list[self.formule_index].tires
                    if current_tires in garage.tires_list:
                        garage.tire_index = garage.tires_list.index(current_tires)
            except Exception as e:
                print(f"Error while loading: {e}")


class Statistics:
    def __init__(self):
        self.races = 0
        self.wins = 0
        self.avg_times = 0
        self.best_time = 0