import random
from character import *

class Route:
    def __init__(self, name, enemies, boss, guardian=None, guardian_spawned=False):
        self.name = name
        self.enemies = enemies  # List of enemies in this route
        self.boss = boss
        self.guardian = guardian 
        self.guardian_spawned = guardian_spawned
        self.cleared_areas = 0

    def spawn_enemies(self):
        # Flatten the list of enemies
        all_enemies = [enemy for sublist in self.enemies for enemy in sublist]
        
        if self.cleared_areas > 4:
            # Boss encounter
            return [self.boss]
        else:
            # Regular enemy spawns
            return random.choices(all_enemies, k=3)  # k = number of enemies



class FirstRoute(Route):
    def __init__(self):
        super().__init__(
            name="The Torment-Ravaged Womb of the Widow Who Bled in Vain",
            enemies=[
                list((FleshWeepers(name=f"Flesh Weeper-{i}") for i in range(1, random.randint(1,2)))), 
                list(Bloodspawn(name=f"Bloodspawn-{i}") for i in range(1, random.randint(1,2))), 
                list(GriefboundSpirits(name=f"Griefbound Spirits-{i}") for i in range(1, random.randint(1,2)))
                ],
            guardian=FirstGuardian(),
            boss=BloodStainedWidow(name="Blood Stained Widow")
        )


class SecondRoute(Route):
    def __init__(self):
        super().__init__(
            name="The Dreadweaver’s Forest of Perpetual Night",
            enemies=["Shadow Lurkers", "Night Crawlers", "Ethereal Banshee"],
            boss="Nightmare Weaver"
        )


class ThirdRoute(Route):
    def __init__(self):
        super().__init__(
            name="The Plantation Fields Soaked with Endless Slaughter",
            enemies=["Ghoul Warriors", "Lost Souls", "Battlefield Wraith"],
            boss="Eternal Reaper"
        )