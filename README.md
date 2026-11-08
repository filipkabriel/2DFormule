# 2D Formula Racing

A 2D top-down racing game built with Python and Pygame[cite: 1, 2]. Take control of a formula car, manage component wear during the race, earn coins, and upgrade your vehicle in the garage[cite: 1, 2].

## Features

* **Dynamic Rotating Camera:** The camera follows and rotates around the player's car, keeping the vehicle centered while the track moves dynamically.
* **Realistic Wear & Damage System:** Pushing your car to the limit wears down the engine, transmission, brakes, steering, and tires[cite: 2]. Hitting the map boundaries damages the car's body, and driving off-track on the grass slows you down and degrades your tires rapidly[cite: 2]. If critical components reach 0%, the race ends in a DNF (Did Not Finish)[cite: 2].
* **Garage & Upgrades:** Win races to earn coins and spend them in the garage to upgrade your Engine, Transmission, Steering, and Brakes, or switch between Soft, Medium, and Hard tire compounds.
* **Automatic Save System:** Your coins and car upgrades are automatically saved to `save.json` upon exiting the game.
* **Dual-Layer SVG Tracks:** Uses separate visual and collision `.svg` layers for accurate off-track grass slowdown, wall impacts, and checkpoint validation.

## Controls

| Key / Input | Action |
| :--- | :--- |
| **Mouse (Left Click)** | Navigate menus and buy upgrades in the Garage[cite: 1] |
| **SPACE** | Start the race / Return to menu after finishing or DNF[cite: 2] |
| **W** | Accelerate[cite: 2] |
| **S** | Brake / Reverse[cite: 2] |
| **A / D** | Steer Left / Right[cite: 2] |
| **R (Hold while stopped near Start/Finish line)** | Pit Stop Repair |
| **M** | Toggle Debug View (switches between visual and collision SVG layers) |
| **ESC** | Return to Main Menu (from Garage or Race)[cite: 1, 2] |

## Prerequisites

* Python 3.x
* Pygame library[cite: 1, 2]

## How to Play (Windows `.exe`)
1. Download `2DFormule_v0.2.zip` from the **Assets** section below.
2. Extract the `.zip` archive to any folder on your computer.
3. Run `2DFormule.exe` (make sure the `tracks` folder stays in the same directory as the `.exe`!).
