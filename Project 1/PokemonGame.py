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

# Define Player Class
class Player():
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender


# Pokemon Class (for all Pokemon)
class Pokemon():
    def __init__(self, name, health, health_cap, moves, element):
        self.name = name
        self.health = health
        self.health_cap = health_cap          ## To avoid over healing and used for calculations (run)
        self.damage = moves
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
        Probability = (self.health_cap - self.health) / self.health_cap   ## The less health, the better chance to get away    

        if Probability > random.random():                                 ## random.random() returns random float between 1 and 0
            print(f"{self.name} got away safely\n")
            return True
        else:
            print(f"{self.name} couldn't get away\n")
            return False
    
    def Fainted(self):
        if self.health <= 0:                           ## Check if Pokemon fainted
            self.health = 0
            print(f"{self.name} fainted")
            return True
        return False
    

##Initialize some Pokemon
Bulbasaur = Pokemon("Bulbasaur", 45, 45,     {1:("Tackle", 30), 2:("Vine Whip", 40)}, GRASS)
Squirtle = Pokemon("Squirtle", 44, 44,       {1:("Tackle", 30), 2:("Water Jet", 40)}, WATER)
Charmander = Pokemon("Charmander", 39, 39,   {1:("Tackle", 30), 2:("Ember", 40)},     FIRE)
Pikachu = Pokemon("Pikachu", 35, 35,         {1:("Tackle", 30), 2:("Spark", 40)},     ELECTRIC)
Jigglypuff = Pokemon("Jigglypuff", 115, 115, {1:("Tackle", 30), 2:("Something", 40)}, NORMAL)
Meowth = Pokemon("Meowth", 40, 40,           {1:("Tackle", 30), 2:("Scratch", 40)}, NORMAL)
Psyduck = Pokemon("Psyduck", 50, 50,         {1:("Tackle", 30), 2:("Water Jet", 40)}, WATER)
Eevee = Pokemon("Eevee", 55, 55,             {1:("Tackle", 30), 2:("Growl", 40)}, NORMAL)
Growlithe = Pokemon("Growlithe", 55,         {1:("Tackle", 30), 2:("Growl", 40)}, FIRE)
Oddish = Pokemon("Oddish", 45, 45,           {1:("Tackle", 30), 2:("Vine Whip", 40)},  GRASS)
Bellsprout = Pokemon("Bellsprout", 50, 50,   {1:("Tackle", 30), 2:("Vine Whip", 40)}, GRASS)


def Battle(Player, Enemy):   ### Rework to call class methods for 
    flag = True
    Turn = True
    while flag:
        Decision = input("Attack or Run?")     ## Decide wheather to fight or run

        if Decision.capitalize == "Attack":
            Player.Attack(Enemy)               ## Use Attack from parent Character class
            flag = not(Enemy.Fainted())
            Turn = False

        elif Decision.capitalize == "Run":     ## Use Run from parent Character class
            flag = Player.Run()
            Turn = False

        else:
            print("Incorrect Input, Try again")
        
        if Turn == False & flag == True:                          ## Enemies turn
            enemy_choice = random.random()     ##Random chance for enemy to Attack or run

            if enemy_choice > 0.90:            ## 10% chance to decide to run
                flag = not Enemy.Run()
                Turn = True
            else:
                Enemy.Attack(Player)           ## 90% chance to attack
                flag = not Player.Fainted()
                Turn = True



def TallGrass(Player):
    flag = True
    while flag:

        Walk = input("Walk into the tall grass? (yes/no)")

        if Walk.capitalize() == "Yes":

            if random.random() > 0.9:            ## 10% chance per grass square to find pokemon
                ##Pick random pokemon and battle