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
    def __init__(self, name, health, attack, element):
        self.name = name
        self.health = health
        self.attack = attack
        self.element = element

    def get_elemental_multiplier(self, target_element):
        if (self.element, target_element) in Element_Effectivness:
            return Element_Effectivness[(self.element, target_element)]
        elif (target_element, self.element) in Element_Effectivness:
            return 1 / Element_Effectivness[(target_element, self.element)]
        return 1

    def attack(self, target):
        # Get the elemental multiplier (either amplifier or reducer)
        multiplier = self.get_elemental_multiplier(target.element)
        total_damage = self.attack * multiplier  # Calculate damage based on the multiplier
        target.health -= total_damage  # Subtract the damage from target's health

        # Print out the results of the attack
        print(f"{self.name} attacks {target.name} for: {total_damage:.2f} damage.")

        # Determine if there is an elemental advantage or disadvantage
        if multiplier > 1:
            print("It's super effective!")
        elif multiplier < 1:
            print("It's not very effective...")

        # Print the health of the target and the attacker after the attack
        print(f"{target.name}'s health is now {target.health:.2f}.")
        print(f"{self.name}'s health is {self.health:.2f}.")

# Define Player Classes - Inherits from Character
class Player(Character):
    def __init__(self, name, health, attack, element):
        super().__init__(name, health, attack, element)

# Define playable pokemon - Inherits from Player
class Pikachu(Player):
    def __init__(self, name):
        super().__init__(name, 60, 35, ELECTRIC)

class Squirtle(Player):
    def __init__(self, name):
        super().__init__(name, 70, 20, WATER)

class Charmander(Player):
    def __init__(self, name):
        super().__init__(name, 70, 20, FIRE)

class Bulbasaur(Player):
    def __init__(self, name):
        super().__init__(name, 70, 20, GRASS)

# Define Enemy Classes - Inherits from Character
class Enemy(Character):
    def __init__(self, name, health, attack, element):
        super().__init__(name, health, attack, element)

#Define enemy Pokemon - Inherits from Enemy
class Rattatta(Enemy):
    def __init__(self, name):
        super().__init__(name, 50, 35, NORMAL)

class Poliwhirl(Enemy):
    def __init__(self, name):
        super().__init__(name, 65, 20, WATER)

class Rapidash(Enemy):
    def __init__(self, name):
        super().__init__(name, 65, 20, FIRE)

class Victoreebel(Enemy):
    def __init__(self, name):
        super().__init__(name, 65, 20, GRASS)