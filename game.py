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
from routes import *
from character import *

class Game():
    def __init__(self, players):
        self.day = 1
        self.boss_strength = 1
        self.players = players
        self.enemies = []
        self.route = None
        self.routes = [FirstRoute(), SecondRoute(), ThirdRoute()]
        self.cleared_areas = 0
        self.traveller_present = any(isinstance(p, Traveller) for p in self.players)
        self.day = 1



    def start_battle(self, route, area, isBoss=False, isGuardian=False):

        if isGuardian == True:
            self.enemies = [route.guardian]
        else:
            # Spawn enemies or boss if last area
            self.enemies = list(route.spawn_enemies()) if not isBoss else [route.boss]
            # Debugging step: print self.enemies to verify it's a list of enemy objects, not generators
            for enemy in self.enemies:
                print("Enemies:", enemy)
        
        # Combine all active players and enemies in a list
        participants = [character for character in self.players if character.is_alive() and not character.is_kidnapped]
        # participants.extend(self.enemies)
        participants.extend(
            enemy for sublist in self.enemies 
            for enemy in (sublist if isinstance(sublist, list) else [sublist])  # If sublist is a list, iterate; else, treat as a single item
            if hasattr(enemy, 'is_alive') and enemy.is_alive()
        )
        
        # Main battle loop
        while any(enemy.is_alive() for enemy in self.enemies) and any(character.is_alive() for character in participants):
            # Sort participants by SPD in descending order
            participants = sorted(participants, key=lambda x: x.SPD, reverse=True)
            
            for participant in participants:
                if not participant.is_alive():
                    continue

                if isinstance(participant, Character) and not isinstance(participant, Enemy):
                    print(f"{participant.name}'s turn:")
                    
                    # Display available skills based on cooldowns
                    available_abilities = [ability for ability in participant.skills if participant.cooldowns.get(ability, 0) == 0]
                    
                    if available_abilities:
                        print("Available skills:")
                        for i, ability in enumerate(available_abilities):
                            print(f"{i + 1}. {ability}")
                            #  - {participant.skills[ability]['description']}

                        # Ask for input to select an ability
                        while True:
                            try:
                                selected_index = int(input(f"Select an ability for {participant.name} (1-{len(available_abilities)}): ")) - 1
                                if 0 <= selected_index < len(available_abilities):
                                    selected_ability = str(available_abilities[selected_index])
                                    print(f"{participant.name} uses {selected_ability}!")
                                    # getattr(participant, participant.skills[selected_ability]['method'])(self.enemies)
                                    getattr(participant, participant.skills[selected_ability])(self.enemies)
                                    # participant.cooldowns[selected_ability] = participant.skills[selected_ability]['cooldown']
                                    break
                                else:
                                    print("Invalid choice. Please select a valid ability number.")
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                    else:
                        print(f"{participant.name} has no abilities available due to cooldowns.")
                else:
                    # Enemy's turn
                    # target = random.choice([c for c in participants if (isinstance(c, Character) and not isinstance(c, Enemy) and c.is_alive())])
                    print(f"{participant.name} attacks!")
                    participant.attack(players)

        # End of battle check
        if all(not enemy.is_alive() for enemy in self.enemies):
            print("Players have won!")
        else:
            print("Enemies have won!")



    def choose_route(self):
        """Prompt players to select a route."""

        print("Choose a route:")

        for i, route in enumerate(self.routes, start=1):
            print(f"{i}. {route.name}")

        choice = int(input("Enter the route number: ")) - 1

        if 0 <= choice < len(self.routes):
            self.route = self.routes[choice]
            print(f"Chosen route: {self.route.name}")
        else:
            print("Invalid choice. Please select again.")
            self.choose_route()


    def explore_area(self):
        """Explore the current chosen area."""

        print(f"Exploring {self.route}'s Patch {(self.cleared_areas + 1)}")
        event = random.randint(0,100)
        print(event)
        if event <= 15:
            event = "trap"
        elif event <= 30 and event > 15:
            event = "guardian"
        elif event > 30:
            event = "enemy"

        if event == "enemy":
            self.start_battle(self.route, self.cleared_areas + 1)

        elif event == "trap":
            self.trap()

        else:
            print(f"You encountered the Guardian of the current Route")
            self.start_battle(self.route, self.cleared_areas + 1, isGuardian = True)

        if self.traveller_present:
            self.day += 0.5
        else:
            self.day += 1

        self.cleared_areas += 1
        if self.cleared_areas >= 5:
            self.start_battle(isBoss=True)
        else:
            self.vote()


    def vote(self):
        votes = {}
        options = ["progress", "face boss"]

        print("Vote to proceed:")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option.capitalize()}")

        for player in self.players:     # Collect votes from each player
            while True:
                try:
                    choice = int(input(f"{player.name}, cast your vote (1 for Progress, 2 to Face Boss): "))
                    if choice in [1, 2]:
                        votes[player] = options[choice - 1]
                        break
                    else:
                        print("Invalid choice. Please enter 1 or 2.")
                except ValueError:
                    print("Invalid input. Enter a number (1 or 2).")

        vote_count = {"progress": 0, "face boss": 0}        # Count votes

        for choice in votes.values():
            vote_count[choice] += 1

        # Determine majority decision
        if vote_count["progress"] > vote_count["face boss"]:
            print("The majority voted to progress to the next area.")
            self.explore_area()  # Proceed to the next area
        else:
            print("The majority voted to face the boss!")
            self.start_battle(self.route, self.cleared_areas + 1, isBoss=True)  # Trigger boss battle

            
    def trap(self):
        # Two types of traps: Kidnap and Stuck
        trap_type = random.choice(["Kidnap", "Stuck"])
        affected_player = random.choice([p for p in self.players if p.is_alive()])

        if trap_type == "Kidnap":
            print(f"Trap activated: {affected_player.name} has been kidnapped and cannot join the next fight!")
            affected_player.is_kidnapped = True  # Mark player as kidnapped

        elif trap_type == "Stuck":
            print("Trap activated: The whole party is stuck in a dungeon and will be delayed by 1 day!")
            self.day += 1  # Delay the current day by 1 for the entire party

        print(f"{affected_player.name if trap_type == 'Kidnap' else 'All players'} affected by the {trap_type} trap.")

    
    def game_loop(self):
        while self.cleared_areas < 4:
            self.choose_route()
            self.explore_area()
            self.progress_day()
        
        print("Final boss fight begins!")
        self.start_battle(self.route, self.cleared_areas, isBoss=True)



players = [
    Duelist(name="Aiden"),
    # Healer(name="Liora"),
    SpellCaster(name="Elara"),
    Archer(name="Finn")
]

# Create the Game instance
game = Game(players=players)

# Start the game loop
game.game_loop()