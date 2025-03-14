#inventory management (backpack)
    #items that stack
    #single use items
    #multi use items
#inventory display
#item details
#player selection
#game play main function
#save menu w/ json files (allow progress to be kept when file is closed)

import random
import itertools

# Define Elements (powers for characters)
ELECTRIC = "electric"
WATER = "water"
FIRE = "fire"
GRASS = "grass"
NORMAL = "normal"

# Element effectiveness against other elements
element_effectiveness = {
    # Elemental strengths (Amplifiers)
    (ELECTRIC, WATER): 1.4,  # Electric is strong against Water
    (WATER, FIRE): 1.4,      # Water is strong against Fire
    (FIRE, GRASS): 1.4,      # Fire is strong against Grass
    (GRASS, WATER): 1.4,     # Grass is strong against Water

    # Elemental weaknesses (Reducers)
    (WATER, GRASS): 0.7,     # Water is weak against Grass
    (FIRE, WATER): 0.7,      # Fire is weak against Water
    (GRASS, FIRE): 0.7       # Grass is weak against Fire
}

# Define Item class
class Item:
    def __init__(self, name, effect_type, effect_value, stackable=False, quantity=1):
        self.name = name
        self.effect_type = effect_type  # For example, 'heal', 'boost_attack', etc.
        self.effect_value = effect_value
        self.stackable = stackable
        self.quantity = quantity

    def use(self, pokemon):
        if self.stackable:
            if self.quantity > 0:
                self.apply_effect(pokemon)
                self.quantity -= 1
                print(f"{pokemon.name} used {self.name}!")
                if self.quantity == 0:
                    print(f"There's no {self.name} left.")
            else:
                print(f"{self.name} is no longer available.")
        else:
            self.apply_effect(pokemon)
            print(f"{pokemon.name} used {self.name}!")

    def apply_effect(self, pokemon):

        if self.effect_type == 'heal':
            pokemon.health += self.effect_value

            if pokemon.health > pokemon.health_cap:
                pokemon.health = pokemon.health_cap  # Prevent health from exceeding the max limit.
            print(f"{pokemon.name} healed for {self.effect_value} health!")


        elif self.effect_type == 'boost_attack':
            pokemon.damage += self.effect_value
            print(f"{pokemon.name}'s attack increased by {self.effect_value}!")


        elif self.effect_type == 'catch':
            if pokemon in Player.pokemon:        ## Check if player already has that pokemon
                print(f"You already have a {pokemon.name}")

            elif self.effect_value > random.random():  ## PokeBall effectiveness
                Player.pokemon.append(pokemon)
                print(f"You caught a wild {pokemon.name}!")

            else:
                print(f"The wild {pokemon.name} broke free!")

##innit some items
PokeBall = Item("Poke Ball", "catch", 0.6, stackable=True, quantity=10)
GreatBall = Item("Great Ball", "catch", 0.7, stackable=True, quantity=10)
UltraBall = Item("Ultra Ball", "catch", 0.8, stackable=True, quantity=10)
MasterBall = Item("Master Ball", "catch", 1, stackable=True, quantity=10)

Potion = Item("Potion", "heal", 20, stackable=True, quantity=10)
SuperPotion = Item("Super Potion", "heal", 40, stackable=True, quantity=10)
HyperPotion = Item("Hyper Potion", "heal", 60, stackable=True, quantity=10)
MaxPotion = Item("Max Potion", "heal", 100, stackable=True, quantity=10)

XAttack = Item("X Attack", "boost_attack", 10)
# Define Player class
class Player():

    def __init__(self, name, gender, inventory = [], pokemon = []):
        self.name = name
        self.gender = gender
        self.inventory = inventory
        self.pokemon = pokemon

    def to_dict(self):      ## In order to save data, Cannot save class instance itself to json
        return {
            "name": self.name,
            "gender": self.gender,
            "bag": self.inventory,
            "team": self.pokemon
        }
    
    def add_item(self, item):
        self.inventory.append(item)
        print(f"{item.name} has been added to your backpack.")

    def use_item(self, item_name, pokemon):
        for item in self.inventory:
            if item.name == item_name:
                item.use(pokemon)
                return
        print(f"{item_name} is not in your backpack.")

    def display_inventory(self):
        if not self.inventory:
            print("Your backpack is empty.")
        else:
            print("Backpack:")
            for item in self.inventory:
                print(f"{item.name} - Quantity: {item.quantity}")
    
# Pokemon Class (for all Pokemon)
class Pokemon():
    def __init__(self, name, health, health_cap, moves, element):
        self.name = name
        self.health = health
        self.health_cap = health_cap          ## To avoid over healing and used for calculations (run)
        self.moves = moves
        self.element = element

    def to_dict(self):
        return {
            "name": self.name,
            "health": self.health,
            "health_cap": self.health_cap,
            "moves": self.moves,
            "element": self.element
        }
    
    def get_elemental_multiplier(self, target_element):
        if (self.element, target_element) in element_effectiveness:
            return element_effectiveness[(self.element, target_element)]
        elif (target_element, self.element) in element_effectiveness:
            return 1 / element_effectiveness[(target_element, self.element)]
        return 1

    def attack(self, target):
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

    def run(self):                                                        ## Random chance to get away
        Probability = (self.health_cap - self.health) / self.health_cap   ## The less health, the better chance to get away    

        if Probability > random.random():                                 ## random.random() returns random float between 1 and 0
            print(f"{self.name} got away safely\n")
            return True
        else:
            print(f"{self.name} couldn't get away\n")
            return False
    
    def fainted(self):
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
Growlithe = Pokemon("Growlithe", 55, 55,     {1:("Tackle", 30), 2:("Growl", 40)}, FIRE)
Oddish = Pokemon("Oddish", 45, 45,           {1:("Tackle", 30), 2:("Vine Whip", 40)},  GRASS)
Bellsprout = Pokemon("Bellsprout", 50, 50,   {1:("Tackle", 30), 2:("Vine Whip", 40)}, GRASS)

# List of possible wild Pokemon that can appear
wild_pokemon_list = [Bulbasaur, Squirtle, Charmander, Pikachu, Jigglypuff, Meowth, Psyduck, Eevee, Growlithe, Oddish, Bellsprout]

def Battle(Player, Pokemon, Enemy):
    """The battle function between the player and enemy Pokémon."""
    flag = True
    Turn = True
    while flag:
        # Player's turn
        print("\nChoose an action:")
        print("1) Attack")
        print("2) Item")
        print("3) Run")
        
        try:
            decision = int(input("Enter the number of the action you desire:"))  # Get the player's choice as a number
        except ValueError:
            print("Not an option. Enter a number from 1-3.")
            continue
        
        if decision == 1:  # Attack
            Pokemon.attack(Enemy)  # Use Attack method from Player's Pokemon
            flag = not Enemy.Fainted()  # Check if the enemy has fainted
            Turn = False

        elif decision == 2:  # Item
            # Show the player inventory and let the player choose an item to use
            if not Player.inventory:
                print("Your backpack is empty!")
            else:
                Player.display_inventory()  # Display all items in inventory
                item_name = input("Which item do you want to use? ").capitalize()
                Player.use_item(item_name, Enemy)  # Use item on the enemy or player’s Pokémon
            Turn = False
        
        elif decision == 3:  # Run
            flag = Pokemon.Run()  # Use Run method from Player's Pokemon
            Turn = False
        
        else:
            print("Not an option, try again.")
        
        # Enemy's turn
        if Turn == False and flag == True:  # Enemy's turn to attack
            print(f"\n{Enemy.name}'s Turn:")
            enemy_choice = random.random()  # Random chance for enemy to attack or run
            
            if enemy_choice > 0.95:  # 10% chance to decide to run
                flag = not Enemy.Run()  # Enemy tries to run away
                Turn = True
            else:
                Enemy.Attack(Player)  # 90% chance for enemy to attack
                flag = not Pokemon.fainted()  # Check if player has fainted
                Turn = True

def TallGrass(Player, Pokemon):
    flag = True
    while flag:

        Walk = input("Walk into the tall grass? (yes/no)").capitalize().strip()

        if Walk == "Yes":
            if random.random() > 0.9:  # 10% chance to encounter a Pokémon
                # Randomly select a wild Pokémon
                wild_pokemon = random.choice(wild_pokemon_list)
                print(f"A wild {wild_pokemon.name} appeared!")

                # Start a battle with the selected wild Pokémon
                Battle(Player, Pokemon, wild_pokemon)

                # Break out of the loop after the battle
                break
            else:
                print("You didn't encounter any Pokémon this time.")
        elif Walk == "No":
            print("You chose not to walk into the tall grass.")
            break  # Exit the loop if the player doesn't want to walk into the grass
        else:
            print("Please answer with 'yes' or 'no'.")

def AutoWalk(Player):
    itertools.repeat(TallGrass(Player), 10) ##Walk in grass 10 times

def PokeCenter(Player):

    for pokemon in Player.pokemon:
        pokemon.health = pokemon.health_cap ##Set all pokemon health to max
