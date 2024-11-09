import random

class Character:
    def __init__(self, name, HP, STR, MP, MANA, SPD, DEF ) -> None:
        self.name = name
        self.maxHP = HP
        self.HP = HP
        self.STR = STR
        self.maxSTR = STR
        self.MP = MP
        self.maxMP = MP
        self.MANA = MANA
        self.maxMANA = MANA
        self.SPD = SPD
        self.maxSPD = SPD
        self.DEF = DEF
        self.maxDEF = DEF
        self.status = None
        self.status_duration = 0
        self.bleed_dmg = 0
        self.danger = 0
        self.cooldowns = {}
        self.preparation = {}
        self.is_kidnapped = False
    
    def is_alive(self):
        return self.HP > 0
    
    def take_damage(self, dmg, penetration = 0):
        """penetration = ratio of defense ignore"""
        actual_dmg = max(0, dmg - round(0.8 * (self.DEF - (penetration * self.DEF))))
        self.HP -= actual_dmg
        print(f"{self.name} took {actual_dmg} damage! Remaining HP = {self.HP}")

        if self.HP <= 0:
            self.alive = False
            print(f"{self.name} died!")

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
        return 1

    def deduct_MANA(self, req):
        self.MP -= req

    def set_danger(self, level):
        """set danger level in int"""
        self.danger = level

    def set_status(self, type, duration, effect = 0):
        """type: Status Effect = stun/prepare/poison
        duration: duration of effect = int"""
        if (type == "stun"):
            self.status = "stun"
            self.status_duration = duration

        elif(type == "prepare"):
            self.status = "prepare"
            self.duration = duration
        
        elif(type == "bleed"):
            self.status = "bleed"
            self.bleed_dmg = effect
            self.status_duration = duration

        elif(type == "weaken"):
            self.status = "weaken"
            self.STR -= effect
            self.status_duration = duration
            
        elif(type == "slow"):
            self.status = "slow"
            self.SPD -= effect
            self.status_duration = duration

        elif(type == "shred"):
            self.status = "shred"
            self.DEF -= effect
            self.status_duration = duration


    # def check_status(self):
    #     if(self.status == "stun"):
    #         print(f"Stunned. Skipping this turn.")
    #         self.status_duration -= 1
    #         return "stun"

    #     elif(self.status == "prepare"):
    #         self.status_duration -= 1
    #         return "prepare"

    #     elif(self.status == "bleed"):
    #         self.take_damage(self.bleed_dmg, 1)
    #         self.status_duration -= 1
    #         return "bleed"

    #     elif(self.status == "weaken"):
    #         self.status_duration -= 1
    #         return "weaken"

    #     elif(self.status == "slow"):
    #         self.status_duration -= 1
    #         return "slow"

    #     elif(self.status == "shred"):
    #         self.status_duration -= 1
    #         return "shred"

    def check_status(self):
        """Check and return the character's active status without modifying duration or applying effects."""
        return self.status


    def check_cooldowns(self, ability_name):
        """Check Cooldowns"""
        if ability_name in self.cooldowns and self.cooldowns[ability_name] > 0:
            print(f"{ability_name} is on cooldown for {self.cooldowns[ability_name]} more turns!")
            return False
        return True

    def reduce_cooldowns(self):
        """Reduce Cooldowns by 1 at the end of the turn"""
        for ability, cooldown in self.cooldowns.items():
            if self.cooldown[ability] > 0:
                self.cooldown[ability] -= 1

    def set_cooldown(self, ability, cooldown):
        """Set cooldown for an ability"""
        self.cooldowns[ability] = cooldown


#------------------------------------------------------------------------Players--------------------------------------------------------------------------------------------

class Duelist(Character):
    def __init__(self, name) -> None:
        super().__init__(name, HP = 100, STR = 20, MP = 0, MANA = 0, SPD = 30, DEF = 10)
        self.cooldowns = {
            "First Strike" : 0,
            "Random Slashes" : 0,
            "Thrust" : 0
            }
        self.skills = {
            "First Strike": "FirstStrike",
            "Random Slashes":"RandomSlashes",
            "Thrust":"Thrust"
        }

    def FirstStrike(self, targets):
        """First Strike will always hit first"""
        desc = f"This skill will always hit the enemy first and deal damage equal to 50 + 60% STR to the enemy."
        print(f"{self.name} used First Strike on {targets[0].name}!")

        targets[0].take_damage(self.calculate_dmg(50, 0.6, True))

    def RandomSlashes(self, targets):
        """Randomly slash the target for 2-6 times"""
        desc = f"This skill will randomly hit the target 2-6 times dealing 25 + 40% STR damage to the enemy with every strike."
        if(self.check_cooldowns("Random Slashes")):
            slashes = random.randint(2, 6)
            print(f"{self.name} used Random Slashes on {targets[0].name}! ({slashes} slashes!)")

            for _ in range(slashes):
                targets[0].take_damage(self.calculate_dmg(25, 0.4, True))
            self.set_cooldown("Random Slashes", 2)

    def Thrust(self, targets):
        """A high damage penetrating attack which ignores enemies' DEF completely"""
        if(self.check_cooldowns("Thrust")):
            desc = f"This skill completely ignores enemies' defense and deals damage equal to 50 + 80% STR to the enemy."
            print(f"{self.name} used Thrust on {targets[0].name}!")

            targets[0].take_damage(self.calculate_dmg(50, 0.8, True), 1)

            self.set_cooldown("Thrust", 3)


class Barbarian(Character):
    def __init__(self, name) -> None:
        super().__init__(name = name, HP = 150, STR = 40, MP = 0, MANA = 0, SPD = 15, DEF = 20)
        self.cooldowns = {
            "Slash" : 0,
            "I don't care I paint the town Red" : 0,
            "Random Slashes" : 0
            } 
        
        self.skills = {
            "Slash" : "slash",
            "I don't care I paint the town Red" : "rage",
            "Random Slashes" : "random_slashes"
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
    def __init__(self, name) -> None:
        super().__init__(name = name, HP = 70, STR = 10, MP = 100, MANA = 200, SPD = 20, DEF = 5)
        self.cooldowns = {
            "Fireball" : 0,
            "Chains of Slavery" : 0,
            "World Ender" : 0
            }
        
        self.skills = {
            "Fireball" : "fireball",
            "Chains of Slavery" : "chains",
            "World Ender" : "ender"
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
        else:
            return 0

    def chains(self, targets):
        """Chains of Slavery binds the enemy with steel vines and restrict the enemy's movements"""
        desc = "This skill binds the enemy and makes them skip 1 turn. Mana Cost: 100. Cooldown: 2"
        cost = 100
        cooldown = 3

        if(self.check_cooldowns("Chains of Slavery")):
            if(self.check_mana(cost)):
                print(f"{self.name} used Chains of Slavery on {targets[0].name}")
                targets[0].set_status(type="stun", duration=1)
                self.deduct_MANA(cost)
                self.set_cooldown("Chains of Slavery", cooldown=cooldown)
            else:
                return 0
        

    def ender(self, targets):
        """Starts chanting a forbidden spell in ancient language for 2 turns, creating 3 spell circles above the enemies each turn, then unleashes an ultimate spell detonating all the magic circles dealing a great amount of damage to all the enemies. It has a slight chance of hitting melee party members too."""
        
        desc = f"This skill will deal damage equal to 50 + 100% of MP + 20% of Max HP of enemies. Slight chance to hit melee teammates. Mana Cost: 200. Cooldown: 4"
        cost = 200
        cooldown = 4

        if(self.check_and_execute_skill()) == 0:
            if(self.check_cooldowns("World Ender")):
                if(self.check_mana(cost)):
                    print(f"{self.name} used World Ender!")
                    print(f"{self.name} starts chanting the forbidden spell! Needs protection for 2 turns!")
                    self.deduct_MANA(cost)
                    self.set_danger(10)         # todo : important, dont forget about this
                    self.preparation("World Ender", 2)
                    self.set_status("prepare", 2)       # todo
                else:
                    return 0

        elif(self.check_and_execute_skill() == 1):
            print(f"Finished chanting the spell, detonates all the magic circles! There is a big explosion around the enemies!")
            for target in targets:
                self.take_damage(self.calculate_dmg(50, 1, False) + 0.2 * self.maxHP)
                self.set_cooldown("World Ender", cooldown=cooldown)
            
            # todo : Add friendly fire in here

            self.set_danger(0)      # i didn't forget about it ;)

        else:
            print(f"{self.name} is still chanting the spell. 3 Magic Circles appeared above the enemies!")
            
            # todo : might need some cooldown shii here


class Archer(Character):
    def __init__(self, name):
        super().__init__(name = name, HP = 90, STR = 25, MP = 0, MANA = 0, SPD = 30, DEF = 10)

        self.cooldowns = {
            "Quick Shots" : 0,
            "Penetration" : 0,
            "Focus" : 0
            }
        
        self.skills = {
            "Quick Shots" : "quick_shots",
            "Penetration" : "penetration",
            "Focus" : "Focus"
        }

    def quick_shots(self, targets):
        """Fires 4-6 arrows in quick succession."""
        desc = f"Fires 4-6 shots in quick succession to the first enemy. Deals 20 + 20% of STR damage."

        print(f"{self.name} used Quick Shots.")
        for _ in range(random.randint(4,6)):
            targets[0].take_damage(self.calculate_dmg(20, 0.2, True))

    def penetration(self, targets):
        """Fires a penetrating arrow that ignores part of the target's defense."""
        desc = f"Fires a penetrating arrow that deals 35 + 30% of STR as damage. Ignores defense."
        print(f"{self.name} used Penetration. Will hit all targets.")

        for target in targets:
            target.take_damage(self.calculate_dmg(35, 0.3, True), 1)

    def Focus(self):
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

class Enemy(Character):
    def __init__(self, name, HP, STR, MP, MANA, SPD, DEF):
        super().__init__(name, HP, STR, MP, MANA, SPD, DEF)
        self.name = name
        self.maxHP = HP
        self.HP = HP
        self.STR = STR
        self.maxSTR = STR
        self.MP = MP
        self.maxMP = MP
        self.MANA = MANA
        self.maxMANA = MANA
        self.SPD = SPD
        self.maxSPD = SPD
        self.DEF = DEF
        self.maxDEF = DEF
        self.status = None
        self.status_duration = 0
        self.cooldowns = {}
        self.preparation = {}

    def attack(self):
        pass



class BloodStainedWidow(Enemy):       #boss route 1
    def __init__(self, name):
        super().__init__(name, HP=1000, STR=80, MP=300, MANA=550, SPD=35, DEF=70)
        self.lament_used = False

        self.cooldowns = {
            "Blood Vortex" : 0,
            "Final Lament" : 0
            # "Focus" : 0
            }
        
        self.skills = {
            "Blood Vortex" : "blood_vortex",
            "Final Lament" : "final_lament"
            # "Focus" : self.Focus
        }

    def attack(self, players):
        if (self.HP <= 0.3 * self.maxHP) and self.lament_used == False:
            self.final_lament(players)
            self.lament_used = True
        
        else:
            abilities = [self.blood_vortex]
            chosen_ability = random.choice(abilities)
            chosen_ability(players)


    desc = "You encountered the route boss of The 'Torment-Ravaged Womb of the Widow Who Bled in Vain', the spectral embodiment of the Widow herself. Her body is covered in wounds that constantly bleed, and she fights with a mixture of dark magic and unrelenting rage. She is sorrowful but vengeful, wielding her suffering as a weapon."

    def blood_vortex(self, players):
        """Creates a vortex of blood, damaging all players each turn and healing herself slightly."""
        desc = "Creates a vortex of blood, damaging all players each turn and healing herself slightly."

        for player in players:
            player.take_damage(self.calculate_dmg(30, 0.2, False))
            if self.lament_used == False:
                self.HP += 15
                print(f"The Widow healed herself by 15 HP!")

    def final_lament(self, players):


        desc = "Final Lament: Upon reaching low HP, she unleashes a powerful attack that deals massive damage to all party members and reduces their damage for the rest of the battle. She cannot heal herself after this attack."

        if self.check_and_execute_skill() == 0:
                print(f"{self.name} is using Final Lament! Charging Time 2 turns.")
                self.prepare_skill("Final Lament", 2)
                self.set_status("prepare", 2)

        if self.check_and_execute_skill() == 1:
            print(f"{self.name} finished charging.")
            for player in players:
                player.take_damage(self.calculate_dmg(60, 0.6, 0))      # todo : balance her


class FleshWeepers(Enemy):
    def __init__(self, name):
        super().__init__(name, HP=200, STR=30, MP=0, MANA=0, SPD=25, DEF=30)

        self.cooldowns = {
            "Agonized Slash" : 0,
            "Weeping Wound" : 0,
            "Despairing Wail" : 0
            }
        
        self.skills = {
            "Agonized Slash" : "agonized_slash",
            "Weeping Wound" : "weeping_wound",
            "Despairing Wail" : "despairing_wail"
        }


    def attack(self, players):
        abilities = [self.agonized_slash, self.weeping_wound, self.despairing_wail] # List of possible abilities for random selection
        chosen_ability = random.choice(abilities)
        chosen_ability(players)  # Execute the randomly chosen attack

    def agonized_slash(self, players):
        """A slashing attack that deals moderate damage to a single player."""
        print(type(players))
        target = random.choice([p for p in players if p.is_alive()])
        print(f"{self.name} uses Agonized Slash on {target.name}!")
        damage = self.calculate_dmg(10, 0.3, False)
        target.take_damage(damage)

    def weeping_wound(self, players):
        """An attack that causes the target to bleed, taking damage over several turns."""
        print(type(players))
        target = random.choice([p for p in players if p.is_alive()])
        print(f"{self.name} inflicts Weeping Wound on {target.name}!")
        damage = self.calculate_dmg(8, 0.2, False)
        target.take_damage(damage)
        self.set_status(type="bleed", duration=3, effect=5)  # Bleeding effect: 5 damage per turn for 3 turns

    def despairing_wail(self, players):     # todo : weaken is not implemented yet
        print(type(players))
        """A despairing wail that reduces all players' attack power briefly."""
        print(f"{self.name} lets out a Despairing Wail, affecting all players!")
        for player in players:
            player.set_status(type="weaken", duration=1, effect=-5)  # Reduces attack power by 5 for 1 turn

    

class Bloodspawn(Enemy):
    def __init__(self, name):
        super().__init__(name, HP=250, STR=40, MP=0, MANA=0, SPD=20, DEF=35)

        self.cooldowns = {
            "Blood Frenzy" : 0,
            "Gore Strike" : 0,
            "Vampiric Thirst" : 0
            }
        
        self.skills = {
            "Blood Frenzy" : "blood_frenzy",
            "Gore Strike" : "gore_strike",
            "Vampiric Thirst" : "vampiric_thirst"
        }
        
    def attack(self, players):
        abilities = [self.blood_frenzy, self.gore_strike, self.vampiric_thirst]
        chosen_ability = random.choice(abilities)
        chosen_ability(players)

    def blood_frenzy(self, players):
        """Deals damage to a single target and slightly heals Bloodspawn."""
        print(type(players))
        target = random.choice([p for p in players if p.is_alive()])
        print(f"{self.name} uses Blood Frenzy on {target.name}!")
        damage = self.calculate_dmg(15, 0.3, False)
        target.take_damage(damage)
        heal_amount = 10
        self.HP += heal_amount
        print(f"{self.name} heals itself for {heal_amount} HP!")

    def gore_strike(self, players):
        """Heavy strike with a chance to cause bleeding on the target."""
        print(type(players))
        target = random.choice([p for p in players if p.is_alive()])
        print(f"{self.name} uses Gore Strike on {target.name}!")
        damage = self.calculate_dmg(20, 0.4, False)
        target.take_damage(damage)
        if random.random() < 0.3:  # 30% chance to apply bleed
            print(f"{target.name} is now bleeding!")
            target.set_status(type="bleed", duration=2, effect=5)

    def vampiric_thirst(self, players):
        """Deals damage to a target and absorbs some health from them."""
        target = random.choice([p for p in players if p.is_alive()])
        print(f"{self.name} uses Vampiric Thirst on {target.name}!")
        damage = self.calculate_dmg(25, 0.3, False)
        target.take_damage(damage)
        self.HP += int(damage * 0.2)  # Heal 20% of damage dealt
        print(f"{self.name} absorbs {int(damage * 0.2)} HP from {target.name}!")


class GriefboundSpirits(Enemy):
    def __init__(self, name):
        super().__init__(name, HP=180, STR=20, MP=50, MANA=50, SPD=30, DEF=25)

        self.cooldowns = {
            "Haunting Whisper" : 0,
            "Soul Drain" : 0,
            "Wail of Regret" : 0
            }
        
        self.skills = {
            "Haunting Whisper" : "haunting_whisper",
            "Soul Drain" : "soul_drain",
            "Wail of Regret" : "wail_of_regret"
        }

    def attack(self, players):
        abilities = [self.haunting_whisper, self.soul_drain, self.wail_of_regret]
        chosen_ability = random.choice(abilities)
        chosen_ability(players)

    def haunting_whisper(self, players):
        """Reduces the target's defense for a turn by instilling fear."""
        print(type(players))
        target = random.choice([p for p in players if p.is_alive()])
        print(f"{self.name} whispers hauntingly to {target.name}, instilling fear!")
        target.set_status(type="fear", duration=1, effect=-5)
        print(f"{target.name}'s DEF is reduced temporarily!")

    def soul_drain(self, players):
        """Drains a portion of the target's HP and transfers it to Griefbound Spirit."""
        print(type(players))
        target = random.choice([p for p in players if p.is_alive()])
        print(f"{self.name} uses Soul Drain on {target.name}!")
        damage = self.calculate_dmg(10, 0.3, False)
        target.take_damage(damage)
        self.HP += int(damage * 0.5)  # Heals 50% of damage dealt
        print(f"{self.name} drains {int(damage * 0.5)} HP from {target.name}!")

    def wail_of_regret(self, players):
        """Lowers all players' SPD slightly by instilling despair."""
        print(type(players))
        print(f"{self.name} lets out a Wail of Regret, filling the air with despair!")
        for player in players:
            player.set_status(type="despair", duration=1, effect=-3)
            print(f"{player.name}'s SPD is reduced temporarily!")

class FirstGuardian(Enemy):
    def __init__(self, name="The Widow’s Womb Guardian", HP=800, STR=60, MP=200, MANA=400, SPD=25, DEF=50):
        super().__init__(name, HP, STR, MP, MANA, SPD, DEF)
        self.skills = {
            "Web Trap": {"method": "web_trap", "cooldown": 3},
            "Poisonous Bite": {"method": "poisonous_bite", "cooldown": 4},
            "Guardian's Roar": {"method": "guardians_roar", "cooldown": 5}
        }
        self.cooldowns = {skill: 0 for skill in self.skills}

    def web_trap(self, players):
        """Stuns a randomly chosen target from the players for 1 turn."""
        target = random.choice([p for p in players if p.is_alive()])
        print(f"{self.name} uses Web Trap on {target.name}, stunning them!")
        target.set_status("stun", duration=1)
        self.cooldowns["Web Trap"] = self.skills["Web Trap"]["cooldown"]

    def poisonous_bite(self, players):
        """Applies poison damage to a randomly chosen target from the players over 3 turns."""
        target = random.choice([p for p in players if p.is_alive()])
        print(f"{self.name} uses Poisonous Bite on {target.name}, inflicting poison damage!")
        target.set_status("bleed", duration=3, effect=15)
        self.cooldowns["Poisonous Bite"] = self.skills["Poisonous Bite"]["cooldown"]

    def guardians_roar(self, players):
        """Reduces the STR of all players for 2 turns."""
        print(f"{self.name} uses Guardian's Roar, weakening all enemies!")
        for target in players:
            if target.is_alive():
                target.set_status("weaken", duration=2, effect=10)
        self.cooldowns["Guardian's Roar"] = self.skills["Guardian's Roar"]["cooldown"]

    def attack(self, players):
        """Chooses and executes an attack on players."""
        available_abilities = [ability for ability, cd in self.cooldowns.items() if cd == 0]
        if available_abilities:
            selected_ability = random.choice(available_abilities)
            print(f"{self.name} uses {selected_ability}!")
            if selected_ability == "Guardian's Roar":
                self.guardians_roar(players)
            else:
                getattr(self, self.skills[selected_ability]['method'])(players)
        else:
            # Basic attack if no skills are available
            target = random.choice([p for p in players if p.is_alive()])
            print(f"{self.name} uses a basic attack on {target.name}!")
            target.take_damage(self.STR)
