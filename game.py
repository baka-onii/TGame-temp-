'''
game():
character selection ()
voting map()
explore()
Vote map()
battle()
progress day()
reduce cd()
check prepare()
check danger()


map:
The Torment-Ravaged Womb of the Widow Who Bled in Vain
The Dreadweaver’s Forest of Perpetual Night
The Culling Fields of Endless Slaughter


game loop()
while self.areas cleared < 5:
    choose route() 
    explore()
    progress day()
    areas cleared()

print("final boss fight)
start battle (isBoss = true)

'''
import random

class Game():
    def __init__(self, players):
        self.day = 1
        self.boss_strength = 1
        self.players = players
        self.enemies = []
        self.route = None
        self.cleared_areas = 0
        self.traveller_present = any(isinstance(p, Traveller) for p in self.players)
        self.day = 1



    def start_battle(route, area, isBoss = False):
        pass

    def choose_route(self):
        route = input("Choose route:")

        if (route == "The Torment-Ravaged Womb of the Widow Who Bled in Vain"):
            self.route = 1      # todo


        elif(route == "The Dreadweaver’s Forest of Perpetual Night"):
            self.route = 2

        elif(route == "The Culling Fields of Endless Slaughter"):
            self.route = 3


    def explore_area(self):
        """Explore the current chosen area."""

        print(f"Exploring {self.route}'s Patch {(self.cleared_areas + 1)}")
        event = random.choice(["enemy", "trap", "boss"])

        if event == "enemy":
            self.start_battle(self.route, self.cleared_areas + 1)

        elif event == "trap":
            self.trap()

        else:
            print(f"You encountered the boss of the current Route")
            self.start_battle(self.route, self.cleared_areas + 1, isBoss = True)

        if self.traveller_present:
            self.day += 0.5
        else:
            self.day += 1

        self.cleared_areas += 1
        if self.cleared_areas >= 5:
            self.bossBattle()
        else:
            self.vote()


    def vote(self):
        pass        # todo

    
        
