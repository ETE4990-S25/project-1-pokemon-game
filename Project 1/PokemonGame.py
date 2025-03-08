import random

# Define Elements (powers for characters)
ELECTRIC = "electric"
WATER = "water"
FIRE = "fire"
GRASS = "grass"
NORMAL = "normal"

# Element Effectiveness against other elements
Element_Effectivness = {
    # Elemental Strengths (Amplifiers)
    (ELECTRIC, WATER): 1.4,  # Electric is strong against Water
    (WATER, FIRE): 1.4,      # Water is strong against Fire
    (FIRE, GRASS): 1.4,      # Fire is strong against Grass
    (GRASS, WATER): 1.4,     # Grass is strong against Water

    # Elemental Weaknesses (Reducers)
    (WATER, GRASS): 0.7,     # Water is weak against Grass
    (FIRE, WATER): 0.7,      # Fire is weak against Water
    (GRASS, FIRE): 0.7       # Grass is weak against Fire
}

# Base Character Class (for all characters)
class Character:
    def __init__(self, name, health, health_cap, damage, element):
        self.name = name
        self.health = health
        self.health_cap = health_cap          ## To avoid over healing and for calculations (run)
        self.damage = damage
        self.element = element

    def get_elemental_multiplier(self, target_element):
        if (self.element, target_element) in Element_Effectivness:
            return Element_Effectivness[(self.element, target_element)]
        elif (target_element, self.element) in Element_Effectivness:
            return 1 / Element_Effectivness[(target_element, self.element)]
        return 1

    def Attack(self, target):
        # Get the elemental multiplier (either amplifier or reducer)
        multiplier = self.get_elemental_multiplier(target.element)
        total_damage = self.damage * multiplier  # Calculate damage based on the multiplier
        target.health -= total_damage  # Subtract the damage from target's health

        # Print out the results of the Attack
        print(f"{self.name} Attacks {target.name} for: {total_damage:.2f} damage.")

        # Determine if there is an elemental advantage or disadvantage
        if multiplier > 1:
            print("It's super effective!")
        elif multiplier < 1:
            print("It's not very effective...")

        # Print the health of the target and the Attacker after the Attack
        print(f"{target.name}'s health is now {target.health:.2f}.")
        print(f"{self.name}'s health is {self.health:.2f}.")

    def Run(self):                                                        ## Random chance to get away
        Probability = (self.health_cap - self.health) / self.health_cap   ## The less health, the better chance to get away    Between 1 and 0       

        if Probability > random.random():                                 ## random.random() returns random float between 1 and 0
            print("Got away safely\n")
            return True
        else:
            print("Couldn't get away\n")
            return False
    
    def Fainted(self):
        if self.health <= 0:                           ## Easily check if character fainted
            self.health = 0
            print(f"{self.name} fainted")
            return True
        
# Define Player Classes - Inherits from Character
class Player(Character):
    def __init__(self, name, health, health_cap, damage, element):
        super().__init__(name, health, health_cap, damage, element)

# Define playable pokemon - Inherits from Player
class Pikachu(Player):
    def __init__(self, name):
        super().__init__(name, 60, 60, 35, ELECTRIC)

class Squirtle(Player):
    def __init__(self, name):
        super().__init__(name, 70, 70, 20, WATER)

class Charmander(Player):
    def __init__(self, name):
        super().__init__(name, 70, 70, 20, FIRE)

class Bulbasaur(Player):
    def __init__(self, name):
        super().__init__(name, 70, 70, 20, GRASS)

# Define Enemy Classes - Inherits from Character
class Enemy(Character):
    def __init__(self, name, health, health_cap, damage, element):
        super().__init__(name, health, health_cap, damage, element)

    def Run(self):                                                         ## Overwrite Run function for enemies to not print anything
        Probability = (self.health_cap - self.health) / self.health_cap

        if Probability > random.random():
            return True
        else:
            return False
        
#Define enemy Pokemon - Inherits from Enemy
class Rattatta(Enemy):
    def __init__(self, name):
        super().__init__(name, 50, 50, 35, NORMAL)

class Poliwhirl(Enemy):
    def __init__(self, name):
        super().__init__(name, 65, 50, 20, WATER)

class Rapidash(Enemy):
    def __init__(self, name):
        super().__init__(name, 65, 65, 20, FIRE)

class Victoreebel(Enemy):
    def __init__(self, name):
        super().__init__(name, 65, 65, 20, GRASS)


def Battle(Player, Enemy):
    flag = True
    Turn = 1
    while flag:
        Decision = input("Attack or Run?")     ## Decide wheather to fight or run

        if Decision.capitalize == "Attack":
            Player.Attack(Enemy)               ## Use Attack from parent Character class
            if Enemy.Fainted():
                flag = False
            else:
                Turn = 0

        elif Decision.capitalize == "Run":     ## Use Run from parent Character class
            if Player.Run():
                flag = False
            else:
                Turn = 0

        else:
            print("Incorrect Input, Try again")
        
        if Turn == 0:                          ## Enemies turn
            enemy_choice = random.random()     ##Random chance for enemy to Attack or run

            if enemy_choice > 0.90:            ## 10% chance to decide to run
                if Enemy.Run():
                    flag = False
            else:
                Enemy.Attack(Player)           ## 90% chance to attack
                if Player.Fainted():
                    flag = False



def TallGrass(Player):
    flag = True
    while flag:

        Walk = input("Walk into the tall grass? (yes/no)")

        if Walk.capitalize() == "Yes":

            if random.random() > 0.9:            ## 10% chance per grass square to find pokemon
                ##Pick random pokemon and battle