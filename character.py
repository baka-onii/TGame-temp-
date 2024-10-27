import random

class Character:
    def __init__(self, name, HP, STR, MP, MANA, SPD, DEF ) -> None:
        self.name = name
        self.maxHP = HP
        self.HP = HP
        self.STR = STR
        self.MP = MP
        self.maxMP = MP
        self.MANA = MANA
        self.SPD = SPD
        self.DEF = DEF
        self.status = None
        self.status_duration = 0
        self.danger = 0
        self.cooldowns = {}
        self.preparation = {}
    
    def is_alive(self):
        return self.HP > 0
    
    def take_damage(self, dmg, penetration = 0):
        """penetration = ratio of defense ignore"""
        actual_dmg = max(0, dmg - round(0.8 * (self.DEF - penetration * self.DEF)))
        self.HP -= actual_dmg
        print(f"{self.name} took {actual_dmg} damage! Remaining HP = {self.HP}")

    def attack(self, target):
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def calculate_dmg(self, fixed, scaling, is_phy):
        """Physical Damage = True
        Magic Damage = False"""
        if is_phy:
            return fixed + (scaling * self.STR)
        else:
            return fixed + (scaling * self.MP)

    def prepare_skill(self, ability, time):
        self.preparation[ability] = time
    
    def check_and_execute_skill(self):
        """Checks for Skill Casting time and returns codes for following:
        0: No skill casting
        1: Skill ready to execute
        2: Skill is still casting"""

        if(self.preparation):
            if(next(iter(self.preparation.values())) == 0):
                return 1
            return 2
        return 0


    def check_mana(self, req):
        if(self.MANA < req):
            print(f"You don't have enough mana to use this skill")
            return 0
        else:
            return 1

    def deduct_MANA(self, req):
        self.MP -= req

    def set_danger(self, level):
        """set danger level in int"""
        self.danger = level

    def set_status(self, type, duration, damage = 0):
        """type: Status Effect = stun/prepare/poison
        duration: duration of effect = int"""
        if (type == "stun"):
            self.status = "stun"
            self.status_duration = duration

        elif(type == "prepare"):
            self.status = "prepare"
            self.duration = duration
        
        elif(type == "poison"):
            self.status = "poison"
            self.status_duration = duration


    def check_status(self):
        if(self.status == "stun"):
            print(f"Stunned. Skipping this turn.")
            self.status_duration -= 1
            return "stun"

        elif(self.status == "prepare"):
            self.status_duration -= 1
            return "prepare"

        elif(self.status == "poison"):
            self.take_damage(0.4 * self.maxHP)
            self.status_duration -= 1
            return "poison"

    def check_cooldowns(self, ability_name):
        """Check Cooldowns"""
        if ability_name in self.cooldowns and self.cooldowns[ability_name] > 0:
            print(f"{ability_name} is on cooldown for {self.cooldowns[ability_name]} more turns!")
            return False
        return True

    def reduce_cooldowns(self):
        """Reduce Cooldowns by 1 at the end of the turn"""
        for ability, cooldown in self.cooldowns.items():
            if cooldown[ability] > 0:
                cooldown[ability] -= 1

    def set_cooldown(self, ability, cooldown):
        """Set cooldown for an ability"""
        self.cooldowns[ability] = cooldown


#------------------------------------------------------------------------Players--------------------------------------------------------------------------------------------

class Duelist(Character):
    def __init__(self, name) -> None:
        super().__init__(name, HP = 100, STR = 20, MP = 0, MANA = 0, SPD = 30, DEF = 10)
        self.cooldowns = {
            "Random Slashes" : 0,
            "Thrust" : 0
            } 

    def first_strike(self, targets):
        """First Strike will always hit first"""
        desc = f"This skill will always hit the enemy first and deal damage equal to 20 + 60% STR to the enemy."
        print(f"{self.name} used First Strike on {targets[0].name}!")

        targets[0].take_damage(self.calculate_dmg(20, 0.6, True))

    def random_slashes(self, targets):
        """Randomly slash the target for 2-6 times"""
        desc = f"This skill will randomly hit the target 2-6 times dealing 15 + 40% STR damage to the enemy with every strike."
        if(self.check_cooldowns("Random Slashes")):
            slashes = random.randint(2, 6)
            print(f"{self.name} used Random Slashes on {targets[0].name}! ({slashes} slashes!)")

            for _ in range(slashes):
                targets[0].take_damage(self.calculate_dmg(15, 0.4, True))
            self.set_cooldown("Random Slashes", 2)

    def thrust(self, targets):
        """A high damage penetrating attack which ignores enemies' DEF completely"""
        if(self.check_cooldowns("Thrust")):
            desc = f"This skill completely ignores enemies' defense and deals damage equal to 50 + 80% STR to the enemy."
            print(f"{self.name} used Thrust on {targets[0].name}!")

            targets[0].take_damage(self.calculate_dmg(50, 0.8, True), 1)

            self.set_cooldown("Thrust", 3)


class Barbarian(Character):
    def __init__(self) -> None:
        super().__init__(HP = 150, STR = 40, MP = 0, MANA = 0, SPD = 15, DEF = 20)
        self.cooldowns = {
            "I don't care I paint the town Red" : 0,
            "Random Slashes" : 0
            } 

    def slash(self, targets):
        """Slashes upto 2 enemies"""
        desc = f"This skill hits upto 2 enemies and deal damage equal to 35 + 10% of the target's Current HP"
        print(f"{self.name} used Slash on {targets[0].name}.")

        for target in targets[:2]:  # Take the first two targets
            if target.is_alive():
                print(f"{self.name} used Slash on {target.name}!")
                target.take_damage(20 + 0.1 * target.HP)

    def rage(self, targets):
        """Blindly rages through the terrain and hits the enemy for 60% of their Max Health and suffers 15% of Max Health as damage."""
        desc = f"This skill will cause the player to blindly rage through and hit 1 enemy for 60% of their Max Health while suffering 15% of Max Health as Damage. Cooldown: 3"
        if(self.check_cooldowns("I don't care I paint the town Red")):
            targets[0].take_damage(0.6 * targets[0].maxHP)
            print(f"Barbarian suffered {0.15 * self.maxHP}")
            self.HP -= 0.15 * self.maxHP
            self.set_cooldown("I don't care I paint the town Red", 4)


    def random_slashes(self, targets):
        """Randomly slash the target for 4-7 times"""
        desc = f"This skill will randomly hit the target 4-7 times dealing 25 + 30% STR damage to the enemy with each strike. Cooldown: 1"
        if(self.check_cooldowns("Random Slashes")):
            slashes = random.randint(2, 6)
            print(f"{self.name} used Random Slashes on {targets[0].name}! ({slashes} slashes!)")

            for _ in range(slashes):
                targets[0].take_damage(self.calculate_dmg(25, 0.3, True))
            self.set_cooldown("Random Slashes", 2)

class SpellCaster(Character):
    def __init__(self) -> None:
        super().__init__(HP = 70, STR = 10, MP = 100, MANA = 200, SPD = 20, DEF = 5)
        self.cooldowns = {
            "Chains of Slavery" : 0,
            "World Ender" : 0
            } 

    def fireball(self, targets):
        """This skill creates a fireball and hurls it at the enemies"""
        desc = f"This skill hits a single target for damage equal to 20 + 50% of MP. There is a slight chance to hit all the targets."
        cost = 30

        if (self.check_mana(cost)):

            print(f"{self.name} used Fireball.")

            rng = random.randint(0,10)

            if (rng > 8):
                print(f"Lucky! Fireball hit all the enemies.")
                for target in targets:
                    target.take_damage(self.calculate_dmg(20, 0.5, False))
            else:
                targets[0].take_damage(self.calculate_dmg(20, 0.5, False))

            self.deduct_MANA(cost)

    def chains(self, targets):
        """Chains of Slavery binds the enemy with steel vines and restrict the enemy's movements"""
        desc = "This skill binds the enemy and makes them skip 1 turn. Mana Cost: 100. Cooldown: 2"
        cost = 100
        if(self.check_cooldowns("Chains of Slavery")):
            if(self.check_mana(cost)):
                print(f"{self.name} used Chains of Slavery on {targets[0].name}")
                targets[0].set_status(type="stun", duration=1)
                self.deduct_MANA(cost)
                self.set_cooldown("Chains of Slavery", 3)
        

    def ender(self, targets):
        """Starts chanting a forbidden spell in ancient language for 2 turns, creating 3 spell circles above the enemies each turn, then unleashes an ultimate spell detonating all the magic circles dealing a great amount of damage to all the enemies. It has a slight chance of hitting melee party members too."""
        
        desc = f"This skill will deal damage equal to 50 + 100% of MP + 20% of Max HP of enemies. Slight chance to hit melee teammates. Mana Cost: 200. Cooldown: 4"
        cost = 200

        if(self.check_and_execute_skill()) == 0:
            if(self.check_cooldowns("World Ender")):
                if(self.check_mana(cost)):
                    print(f"{self.name} used World Ender!")
                    print(f"{self.name} starts chanting the forbidden spell! Needs protection for 2 turns!")
                    self.deduct_MANA(cost)
                    self.set_danger(10)         # todo : important, dont forget about this
                    self.preparation("World Ender", 2)
                    self.set_status("prepare", 2)       # todo

        elif(self.check_and_execute_skill() == 1):
            print(f"Finished chanting the spell, detonates all the magic circles! There is a big explosion around the enemies!")
            for target in targets:
                self.take_damage(self.calculate_dmg(50, 1, False) + 0.2 * self.maxHP)
            
            # todo : Add friendly fire in here

            self.set_danger(0)      # i didn't forget about it ;)

        else:
            print(f"{self.name} is still chanting the spell. 3 Magic Circles appeared above the enemies!")
            
            # todo : might need some cooldown shii here


class Archer(Character):
    def __init__(self, name):
        super().__init__(HP = 90, STR = 25, MP = 0, MANA = 0, SPD = 30, DEF = 10)



    def quick_shots(self, targets):
        """Fires 4-6 arrows in quick succession."""
        desc = f"Fires 4-6 shots in quick succession to the first enemy. Deals 20 + 20% of STR damage."

        print(f"{self.name} used Quick Shots.")
        for _ in range(random.randint(4,6)):
            targets[0].take_damage(self.calculate_dmg(20, 0.2, True))

    def penetration(self, targets):
        """Fires a penetrating arrow that ignores part of the target's defense."""
        desc = f"Fires a penetrating arrow that deals 45 + 30% of STR as damage. Ignores defense."
        print(f"{self.name} used Penetration. Will hit all targets.")

        for target in targets:
            target.take_damage(self.calculate_dmg(35, 30, True), 1)

    def meditation(self):
        pass


class Healer(Character):
    def __init__(self, name) -> None:
        super().__init__(name, HP = 100, STR = 20, MP = 0, MANA = 0, SPD = 30, DEF = 10)

    def heal(self, allies):
        pass

    def sanctuary(self, allies):
        pass

    def orbital(self, targets):
        pass


class Alchemist(Character):
    def __init__(self, name) -> None:
        super().__init__(name, HP = 100, STR = 20, MP = 0, MANA = 0, SPD = 30, DEF = 10)

    def deep_breaths(self, targets):
        pass

    def sleep(self, targets):
        pass

    def nagasaki(self, targets):
        pass


class Traveller(Character):
    def __init__(self, name) -> None:
        super().__init__(name, HP = 100, STR = 20, MP = 0, MANA = 0, SPD = 30, DEF = 10)
        
    def defuse(self):
        pass

    def explore(self):
        pass

    def slash(self, targets):
        pass


class Succubus(Character):
    def __init__(self, name) -> None:
        super().__init__(name, HP = 100, STR = 20, MP = 0, MANA = 0, SPD = 30, DEF = 10)

    def seduce(self, targets):
        pass

    def lashes(self, targets):
        pass

    def drain(self, targets):
        pass


class Necromancer(Character):
    def __init__(self, name) -> None:
        super().__init__(name, HP = 100, STR = 20, MP = 0, MANA = 0, SPD = 30, DEF = 10)

    def summon(self):
        pass

    def doll(self, allies):
        pass

    def burn(self, targets):
        pass


class Elementalist(Character):
    def __init__(self, name) -> None:
        super().__init__(name, HP = 100, STR = 20, MP = 0, MANA = 0, SPD = 30, DEF = 10)

    def flame(self, targets):
        pass

    def lightning(self, targets):
        pass

    def wind(self, targets):
        pass



#--------------------------------------------------------------------Enemies---------------------------------------------------------------------------------------------

class blood_stained_widow(Character):
    def __init__(self, name, HP, STR, MP, MANA, SPD, DEF):
        super().__init__(name, HP = 1000, STR = 80, MP = 300, MANA = 550, SPD = 35, DEF = 70)

    desc = "You encountered the route boss of The 'Torment-Ravaged Womb of the Widow Who Bled in Vain', the spectral embodiment of the Widow herself. Her body is covered in wounds that constantly bleed, and she fights with a mixture of dark magic and unrelenting rage. She is sorrowful but vengeful, wielding her suffering as a weapon."

    def blood_vortex(self, players):
        """Creates a vortex of blood, damaging all players each turn and healing herself slightly."""
        desc = "Creates a vortex of blood, damaging all players each turn and healing herself slightly."

        for player in players:
            player.take_damage(self.calculate_dmg(30, 0.2, False))
            print(f"The Widow healed herself by 20 HP!")
            self.HP += 15

    def final_lament(self, players):
        desc = "Final Lament: Upon reaching low HP, she unleashes a powerful attack that deals massive damage to all party members and reduces their damage for the rest of the battle. She cannot heal herself after this attack."

        if self.HP < 0.3 * self.maxHP:
            if self.check_and_execute_skill() == 0:
                    print(f"{self.name} is using Final Lament! Charging Time 2 turns.")
                    self.prepare_skill("Final Lament", 2)
                    self.set_status("prepare", 2)

            if self.check_and_execute_skill() == 1:
                print(f"{self.name} finished charging.")
                for player in players:
                    player.take_damage(self.calculate_dmg(60, 0.6, 0))