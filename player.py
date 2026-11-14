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
        self.statistics = Statistics()
        self.formule_list = [
            formule.Formule(
                ai=False,
                name="Red Arrow F3",
                colour=settings.colour.Red,
                engine=60,
                transmission=60,
                steering=60,
                brakes=60,
                weight=720,
                tires=garage.tires_list[garage.tire_index],
                car_type="Rookie",
                max_engine=90,
                max_transmission=90,
                max_steering=90,
                max_brakes=90
            )
        ]
        self.load()

    def save(self):
        cars_data = []
        for auto in self.formule_list:
            cars_data.append({
                "ai": auto.ai,
                "name": auto.name,
                "car_type": auto.car_type,
                "colour": list(auto.colour),
                "engine": auto.engine,
                "transmission": auto.transmission,
                "steering": auto.steering,
                "brakes": auto.brakes,
                "weight": auto.weight,
                "tires": auto.tires,
                "max_engine": auto.max_engine,
                "max_transmission": auto.max_transmission,
                "max_steering": auto.max_steering,
                "max_brakes": auto.max_brakes
            })

        data = {
            "coins": self.coins,
            "formule_index": self.formule_index,
            "formule_list": cars_data,
            "statistics": self.statistics.to_dict()
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

                if "statistics" in data:
                    self.statistics.from_dict(data["statistics"])

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
                            tires=auto_dict["tires"],
                            car_type=auto_dict.get("car_type", "Rookie"),
                            max_engine=auto_dict.get("max_engine", 100),
                            max_transmission=auto_dict.get("max_transmission", 100),
                            max_steering=auto_dict.get("max_steering", 100),
                            max_brakes=auto_dict.get("max_brakes", 100)
                        )
                    )

                if loaded_cars:
                    self.formule_list = loaded_cars
                    if self.formule_index >= len(self.formule_list):
                        self.formule_index = 0
                    current_tires = self.formule_list[self.formule_index].tires
                    if current_tires in garage.tires_list:
                        garage.tire_index = garage.tires_list.index(current_tires)
            except Exception as e:
                print(f"Error while loading: {e}")


class Statistics:
    def __init__(self):
        self.races = 0
        self.wins = 0
        self.dnf_count = 0
        self.total_distance = 0.0
        self.track_stats = {}

    def get_track(self, track_name):
        if track_name not in self.track_stats:
            self.track_stats[track_name] = {
                "best_lap": 0.0,
                "best_race": 0.0,
                "avg_race": 0.0,
                "wins": 0
            }
        return self.track_stats[track_name]

    def record_race_start(self):
        self.races += 1

    def record_dnf(self):
        self.dnf_count += 1

    def record_lap(self, track_name, lap_time):
        if lap_time <= 0:
            return
        t = self.get_track(track_name)
        if t["best_lap"] == 0.0 or lap_time < t["best_lap"]:
            t["best_lap"] = lap_time

    def record_win(self, track_name, total_time, distance):
        self.wins += 1
        self.total_distance += distance
        t = self.get_track(track_name)
        t["wins"] += 1
        if total_time > 0:
            if t["best_race"] == 0.0 or total_time < t["best_lap"]:
                t["best_lap"] = total_time
            if t["best_lap"] == 0.0:
                t["best_lap"] = total_time
            else:
                t["best_lap"] = (t["best_lap"] + total_time) / 2.0

    def add_distance(self, distance):
        self.total_distance += distance

    def to_dict(self):
        return {
            "races": self.races,
            "wins": self.wins,
            "dnf_count": self.dnf_count,
            "total_distance": self.total_distance,
            "track_stats": self.track_stats
        }

    def from_dict(self, data):
        self.races = data.get("races", 0)
        self.wins = data.get("wins", 0)
        self.dnf_count = data.get("dnf_count", 0)
        self.total_distance = data.get("total_distance", 0.0)
        self.track_stats = data.get("track_stats", {})