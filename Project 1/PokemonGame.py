import random
import itertools
import time

## David Long and Jacob Juarez

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
    def __init__(self, name, effect_value, stackable=False, quantity=1):
        self.name = name
        self.effect_value = effect_value
        self.stackable = stackable
        self.quantity = quantity

    def to_dict(self):
        return {
            "name": self.name,
            "effect": self.effect_value,
            "stack": self.stackable,
            "amount": self.quantity
        }

    def use(self, pokemon, player = None):

        if self.stackable:

            if self.quantity > 0:
                time.sleep(1.5)
                print(f"You used a {self.name} on {pokemon.name}!")
                if player: 
                    self.apply_effect(pokemon, player) ## only for pokeballs since we need to add captured pokemon to player list
                else: 
                    self.apply_effect(pokemon)
                self.quantity -= 1
                
                if self.quantity == 0:
                    time.sleep(1.5)
                    print(f"That was your last {self.name}!")
                    return True
            else:
                time.sleep(1.5)
                print(f"{self.name} is no longer available.")
                return False
        else:
            self.apply_effect(pokemon)
            time.sleep(1.5)
            print(f"{pokemon.name} used {self.name}!")
            return True

class HealItems(Item):
    def __init__(self, name, effect_value, stackable, quantity):
        super().__init__(name, effect_value, stackable, quantity)

    def apply_effect(self, pokemon):

        pokemon.health += self.effect_value
        if pokemon.health > pokemon.health_cap:
            pokemon.health = pokemon.health_cap  # Prevent health from exceeding the max limit.
        time.sleep(1.5)
        print(f"{pokemon.name} healed for {self.effect_value} health!")


class PokeBalls(Item):
    def __init__(self, name, effect_value, stackable, quantity):
        super().__init__(name, effect_value, stackable, quantity)

    def apply_effect(self, pokemon, player): ## Must pass wild pokemon

        if self.effect_value > random.random():  ## PokeBall effectiveness
            Count()
            convert_to_player_pokemon = Pokemon(pokemon.name, pokemon.health, pokemon.health_cap, pokemon.moves, pokemon.element)  ## in order to choose moves of pokemon
            player.pokemon.append(convert_to_player_pokemon)
            print(f"You caught a wild {pokemon.name}!")

        else:
            Count()
            print(f"The wild {pokemon.name} broke free!")

def Count():
    for i in range(3):
        print("*shake*")
        time.sleep(2)


##innit some items
PokeBall = PokeBalls("Poke Ball", 0.6, stackable=True, quantity=1)
GreatBall = PokeBalls("Great Ball", 0.7, stackable=True, quantity=1)
UltraBall = PokeBalls("Ultra Ball", 0.8, stackable=True, quantity=1)
MasterBall = PokeBalls("Master Ball", 1, stackable=True, quantity=1)

Potion = HealItems("Potion", 20, stackable=True, quantity=1)
SuperPotion = HealItems("Super Potion", 40, stackable=True, quantity=1)
HyperPotion = HealItems("Hyper Potion", 60, stackable=True, quantity=1)
MaxPotion = HealItems("Max Potion", 100, stackable=True, quantity=1)

global item_list
global item_chance
item_list = [PokeBall, GreatBall, UltraBall, MasterBall, Potion, SuperPotion, HyperPotion, MaxPotion]
item_chance = [100, 80, 60, 5, 100, 70, 50, 20] ## Masterballs are rare while pokeballs and potions are common
Pokeball_list = [PokeBall, GreatBall, UltraBall, MasterBall]
Pokeball_names = ["Poke Ball", "Great Ball", "Ultra Ball", "Master Ball"]
Potion_names = ["Potion", "Super Potion", "Hyper Potion", "Max Potion"]
# Define Player class
class Player():

    def __init__(self, name, gender, inventory=None, pokemon=None):
        if inventory is None:
            inventory = [] ## key(item) value(quantity)
        if pokemon is None:
            pokemon = []

        self.name = name
        self.gender = gender
        self.inventory = inventory
        self.pokemon = pokemon

    def to_dict(self):      ## In order to save data, Cannot save class instance itself to json
        return {
            "name": self.name,
            "gender": self.gender,
            "bag": [item.to_dict() for item in self.inventory],
            "team": [pokemon.to_dict() for pokemon in self.pokemon]
        }
    
    def add_item(self, item, amount):
        for items in self.inventory:
            if item.name == items.name:
                item.quantity += amount
                break
        else:
            self.inventory.append(item)
    
        time.sleep(1.5)
        if amount > 1:
            print(f"{amount} {item.name}'s have been added to your backpack.")
        else:
            print(f"{item.name} has been added to your backpack.")

    def use_item(self, item_name, pokemon):
        while(True):
            item_found = False

            for item in self.inventory:
                if item.name.lower() == item_name.lower():
                    item_found = True
                    if item.name in Pokeball_names: ## if item is a pokeball, also pass in the player
                        if item.use(pokemon, self):
                            self.inventory.remove(item)
                            
                    else:
                        if item.use(pokemon):  ## Just pass pokemon for all other items
                            self.inventory.remove(item)
                    return
            if not item_found:
                item_name = input("Item not available, try another").strip()
                

    def display_inventory(self):
        if not self.inventory:
            print("\nYour backpack is empty.")
        else:
            print("\nBackpack:")
            counter = itertools.count(1)
            for item in self.inventory:
                time.sleep(0.2)
                print(f"{next(counter)}. {item.name} - Quantity: {item.quantity}")
    
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

        while(True):
            time.sleep(1.5)
            print("Choose a move:\n")
            for key, move in self.moves.items():
                time.sleep(0.2)
                print(f"{key}. {move[0]}: {move[1]}")   ## Prints dictionary key and move name and damage
                move_count = int(key)
            print("5. Exit")
            choice = input("Pick a move to use!").strip()

            if choice == '5':
                break
            try:
                if int(choice) not in range(move_count+1):
                    print("Invalid input")
                
                else:
                    damage = self.moves[choice][1] ## Damage value of move
                    break
            except ValueError:
                print("Invalid input")

        if choice == '5':
            return False
        # Get the elemental multiplier (either amplifier or reducer)
        multiplier = self.get_elemental_multiplier(target.element)
        total_damage = damage * multiplier  # Calculate damage based on the multiplier
        target.health -= total_damage  # Subtract the damage from target's health

        # Print out the results of the Attack
        time.sleep(1.5)
        print(f"\n{self.name} attacks {target.name} with {self.moves[choice][0]} for: {total_damage} damage.")
        # Determine if there is an elemental advantage or disadvantage
        if multiplier > 1:
            time.sleep(1.5)
            print("\nIt's super effective!")
        elif multiplier < 1:
            time.sleep(1.5)
            print("\nIt's not very effective...")

        # Print the health of the target and the Attacker after the Attack
        time.sleep(1.5)
        if not target.fainted():
            print(f"\n{target.name}'s health is now {target.health}.")
            time.sleep(1.5)
            print(f"\n{self.name}'s health is {self.health}.")
        else:
            print(f"\n{target.name}'s health is now 0.")
            time.sleep(1.5)
            print(f"\n{self.name}'s health is {self.health}.")
        return True

    def run(self):                                                        ## Random chance to get away
        Probability = (self.health_cap - self.health) / self.health_cap   ## The less health, the better chance to get away    

        if Probability > random.random():      
            time.sleep(1.5)                           ## random.random() returns random float between 1 and 0
            print(f"\n{self.name} got away safely\n")
            return True
        else:
            time.sleep(1.5)
            print(f"\n{self.name} couldn't get away\n")
            return False
    
    def fainted(self):
        if self.health <= 0:   ## Check if Pokemon fainted
            self.health = 0
            return True
        return False
    
class Wild(Pokemon):
    def attack(self, target):
        
        enemy_move_name = random.choice(list(self.moves.keys()))
        damage = self.moves[enemy_move_name][1]

        # Get the elemental multiplier (either amplifier or reducer)
        multiplier = self.get_elemental_multiplier(target.element)
        total_damage = damage * multiplier  # Calculate damage based on the multiplier
        target.health  -= total_damage  # Subtract the damage from target's health

        # Print out the results of the Attack
        time.sleep(1.5)
        print(f"\n{self.name} attacks {target.name} with {self.moves[enemy_move_name][0]} for: {total_damage} damage.")
        
        # Determine if there is an elemental advantage or disadvantage
        if multiplier > 1:
            time.sleep(1.5)
            print("\nIt's super effective!")
        elif multiplier < 1:
            time.sleep(1.5)
            print("\nIt's not very effective...")

        # Print the health of the target and the Attacker after the Attack
        time.sleep(1.5)
        if not target.fainted():
            print(f"\n{target.name}'s health is now {target.health}.")
            time.sleep(1.5)
            print(f"\n{self.name}'s health is {self.health}.")
        else:
            print(f"\n{target.name}'s health is now 0.")
            time.sleep(1.5)
            print(f"\n{self.name}'s health is {self.health}.")

##Initialize some Pokemon
WBulbasaur = Wild("Bulbasaur", 90, 90,     {'1':("Tackle", 30), '2':("Vine Whip", 40)}, GRASS)
WSquirtle = Wild("Squirtle", 85, 85,       {'1':("Tackle", 30), '2':("Water Jet", 40)}, WATER)
WCharmander = Wild("Charmander", 85, 85,   {'1':("Tackle", 30), '2':("Ember", 40)},     FIRE)
WPikachu = Wild("Pikachu", 80, 80,         {'1':("Tackle", 30), '2':("Spark", 40)},     ELECTRIC)
WJigglypuff = Wild("Jigglypuff", 95, 95,   {'1':("Tackle", 30), '2':("Body Slam", 40)}, NORMAL)
WMeowth = Wild("Meowth", 80, 80,           {'1':("Tackle", 30), '2':("Scratch", 40)}, NORMAL)
WPsyduck = Wild("Psyduck", 75, 75,         {'1':("Tackle", 30), '2':("Water Jet", 40)}, WATER)
WEevee = Wild("Eevee", 85, 85,             {'1':("Tackle", 30), '2':("Growl", 40)}, NORMAL)
WGrowlithe = Wild("Growlithe", 85, 85,     {'1':("Tackle", 30), '2':("Ember", 40)}, FIRE)
WOddish = Wild("Oddish", 90, 90,           {'1':("Tackle", 30), '2':("Vine Whip", 40)},  GRASS)
WBellsprout = Wild("Bellsprout", 75, 75,   {'1':("Tackle", 30), '2':("Vine Whip", 40)}, GRASS)

Bulbasaur = Pokemon("Bulbasaur", 90, 90,     {'1':("Tackle", 30), '2':("Vine Whip", 40), '3':("Razor Leaf", 45)}, GRASS)
Squirtle = Pokemon("Squirtle", 85, 85,       {'1':("Tackle", 30), '2':("Water Jet", 40), '3':("Shell Smash", 45)}, WATER)
Charmander = Pokemon("Charmander", 85, 85,   {'1':("Tackle", 30), '2':("Ember", 40),     '3':("Fire Spin", 45)},     FIRE)

# List of possible wild Pokemon that can appear
wild_pokemon_list = [WBulbasaur, WSquirtle, WCharmander, WPikachu, WJigglypuff, WMeowth, WPsyduck, WEevee, WGrowlithe, WOddish, WBellsprout]
chosen_pokemon = [Bulbasaur, Squirtle, Charmander]

def Battle(Player, Pokemon, Enemy):
    """The battle function between the player and enemy Pokémon."""
    flag = True
    Turn = True
    MainPokemon = Pokemon

     

    while flag:
        
    # Confirm player has pokemon to fight with
        if not CheckPokemonAlive(Player): # Check if any pokemon alive
            time.sleep(1.5)
            print("You can't fight! \nYou have no useable pokemon!")
            flag = False
            
        elif MainPokemon.fainted() and CheckPokemonAlive(Player): ## If we have pokemon alive but main pokemon is dead, switch
            time.sleep(1.5)
            print(f"{MainPokemon.name} is fainted, choose a different pokemon to fight")
            MainPokemon = SwapPokemon(Player.pokemon)

        if flag == True:
            # Player's turn
            time.sleep(1.5)
            print("\nChoose an action:")
            time.sleep(0.2)
            print("1) Attack")
            time.sleep(0.2)
            print("2) Use Item")
            time.sleep(0.2)
            print("3) Run")
            time.sleep(0.2)
            print("4) Swap Pokemon")

        
        
            
            try:
                decision = input("Enter the number of the action you desire:").strip()  # Get the player's choice as a number
            except ValueError:
                time.sleep(1)
                print("Not an option. Enter a number from 1-4.")
                continue
        
            if decision == '1':  # Attack
                if MainPokemon.attack(Enemy):  # Use Attack method from Player's Pokemon
                    flag = not Enemy.fainted()  # Check if the enemy has fainted
                    Turn = False

            elif decision == '2':  # Item
                # Show the player inventory and let the player choose an item to use
                if not Player.inventory:
                    time.sleep(1)
                    print("Your backpack is empty!")

                else:     
                    Player.display_inventory()  # Display all items in inventory
                    item_name = input("Name the item you want to use ")
                        
                    if item_name in Pokeball_names:
                        player_pokemon_count = len(Player.pokemon)
                        Player.use_item(item_name, Enemy) ## use on enemy if pokeball

                        if player_pokemon_count != len(Player.pokemon): ##Check if player caught another pokemon
                            Turn = True
                            flag = False  ## Wild pokemon doesnt fight and leave battle functino
                        else:
                            Turn = False  ## Not caught, continue battle
                            
                    elif item_name in Potion_names:
                        Player.use_item(item_name, Pokemon) ## use on players pokemon
                        Turn = False
                    
                    
            
            elif decision == '3':  # Run
                if Pokemon.run():  # Use Run method from Player's Pokemon
                    flag = False
                else:
                    Turn = False

            elif decision == '4': # Swap Pokemon
                MainPokemon = SwapPokemon(Player.pokemon)
            else:
                time.sleep(1)
                print("Not an option, try again.")
            
            # Enemy's turn
            if Turn == False and flag == True:  # Enemy's turn to attack
                time.sleep(1.5)
                print(f"\n{Enemy.name}'s Turn:")
                enemy_choice = random.random()  # Random chance for enemy to attack or run
                
                if enemy_choice > 0.90:  # 10% chance to decide to run
                    flag = not Enemy.run()  # Enemy tries to run away
                    Turn = True
                else:
                    Enemy.attack(MainPokemon)  # 90% chance for enemy to attack
                    Turn = True

def TallGrass(Player, Pokemon):
    flag = True
    while flag:

        Walk = input("\n1. Walk once\n2.Walk 10 times\n3.Exit walk\n")

        if Walk == '1':
            Walks(Player, Pokemon)

        elif Walk == '2':
            AutoWalk(Player, Pokemon)

        elif Walk == '3':
            time.sleep(1)
            print("You chose not to walk into the tall grass.")
            break  # Exit the loop if the player doesn't want to walk into the grass
        else:
            print("Invalid input")


def Walks(Player, Pokemon):

    if random.random() < 0.1:  # 10% chance to encounter a Pokémon
        # Randomly select a wild Pokémon
        PokeCenter(wild_pokemon_list) ## Confirm enemies have full health
        wild_pokemon = random.choice(wild_pokemon_list)
        time.sleep(1.5)
        print(f"\nA wild {wild_pokemon.name} appeared!")

                # Start a battle with the selected wild Pokémon
        Battle(Player, Pokemon, wild_pokemon)

    elif random.random() < 0.25:  # 25% to find item
        k = random.choices([1,2], weights = [85,15])[0] ##Chance to find two items
        found_item = random.choices(item_list, weights = item_chance, k = k)[0]  ## random item depending on how rare
        time.sleep(1.5)
        print(f"\nYou found {k} {found_item.name}")
        Player.add_item(found_item, k)     ## add to inventory


def AutoWalk(player, Pokemon):
    for i in range(10):
        Walks(player, Pokemon)

def PokeCenter(pokemon_list):

    for i in range(len(pokemon_list)):
        pokemon_list[i].health = pokemon_list[i].health_cap ##Set all pokemon health to max
    
    return pokemon_list


def SwapPokemon(pokemon_list):
    time.sleep(1.5)
    print("\nThe pokemon you have right now are:")

    for i in range(len(pokemon_list)):
                time.sleep(0.2)
                print(f"{i+1}. {pokemon_list[i].name}. health: {pokemon_list[i].health}")
    while(True):
        try:
            choice = int(input("\nChoose a pokemon to pick as your main one")) - 1
            if choice < 0 or choice >= len(pokemon_list):
                time.sleep(1)
                print("invalid input")
            else:
                return pokemon_list[choice]
        except ValueError:
            time.sleep(1)
            print("invalid input")
        
def CheckPokemonAlive(player):
    pokemon_alive = []
    for pokemon in player.pokemon:
        if pokemon.health > 0:
            pokemon_alive.append(True)
        else:
            pokemon_alive.append(False)

    if any(pokemon_alive): ## If any pokemon are alive
        return True
    else:
        return False