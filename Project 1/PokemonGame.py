import random
import time
import itertools
import PokemonAndItems as PI


## David Long and Jacob Juarez


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
            options = [ "1) Attack", "2) Use Item", "3) Run", "4) Swap Pokemon"]
            for option in options:
                time.sleep(0.2)
                print(option)

        
        
            
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
                    pairs = list(zip(itertools.count(start=1), Player.inventory))
                    valid_numbers = [num for num, _ in pairs]

                    try:
                        item_num = int(input("Which item do you want to use ").strip())

                        if item_num not in valid_numbers: ##Check the count values and compare
                            print("Invalid input")

                        else:
                            for num, item in pairs:
                                if num == item_num:
                                    chosen_item = item
                                    break
                            
                        if chosen_item.name in PI.Pokeball_names:
                            player_pokemon_count = len(Player.pokemon)
                            Player.use_item(chosen_item.name, Enemy) ## use on enemy if pokeball

                            if player_pokemon_count != len(Player.pokemon): ##Check if player caught another pokemon / if pokeball was successful
                                Turn = True
                                flag = False  ## Wild pokemon is caught so it doesnt fight and we leave battle functino
                            else:
                                Turn = False  ## Not caught, continue battle
                                
                        elif chosen_item.name in PI.Potion_names:
                            Player.use_item(chosen_item.name, Pokemon) ## use on players pokemon if heal item
                            Turn = False
                    
                    except ValueError:
                        print("Invalid Input, please enter a number")
                    
            
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


def Walks(Player, Pokemon):

    if random.random() < 0.1:  # 10% chance to encounter a Pokémon
        # Randomly select a wild Pokémon
        PokeCenter(PI.wild_pokemon_list) ## Confirm enemies have full health
        wild_pokemon = random.choice(PI.wild_pokemon_list)
        time.sleep(1.5)
        print(f"\nA wild {wild_pokemon.name} appeared!")

                # Start a battle with the selected wild Pokémon
        Battle(Player, Pokemon, wild_pokemon)

    elif random.random() < 0.25:  # 25% to find item
        k = random.choices([1,2], weights = [85,15])[0] ##Chance to find two items
        found_item = random.choices(PI.item_list, weights = PI.item_chance, k = k)[0]  ## random item depending on how rare
        time.sleep(1.5)
        print(f"\nYou found {k} {found_item.name}")
        Player.add_item(found_item, k)     ## add to inventory


def TallGrass(Player, Pokemon):
    """Pass in the Player and the active pokemon
    here you can walk in tall grass and find items or battle wild pokemon"""
    flag = True
    while flag:

        Walk = input("\n1. Walk once\n2.Walk 10 times\n3.Exit walk\n")

        if Walk == '1':
            Walks(Player, Pokemon)

        elif Walk == '2':
            for i in range(10):
                Walks(Player, Pokemon)

        elif Walk == '3':
            time.sleep(1)
            print("You chose not to walk into the tall grass.")
            break  # Exit the loop if the player doesn't want to walk into the grass
        else:
            print("Invalid input")


def PokeCenter(pokemon_list):

    for i in range(len(pokemon_list)):
        pokemon_list[i].health = pokemon_list[i].health_cap ##Set all pokemon health to max
    
    return pokemon_list


def SwapPokemon(pokemon_list):
    print("\nThe pokemon you have right now are:")

    for i in range(len(pokemon_list)):
                time.sleep(0.2)
                print(f"{i+1}. {pokemon_list[i].name}. health: {pokemon_list[i].health}")
    while(True):
        try:
            choice = int(input("\nChoose a pokemon to pick as your main one")) - 1
            if choice < 0 or choice >= len(pokemon_list):
                print("invalid input")
            else:
                return pokemon_list[choice]
        except ValueError:
            time.sleep(1)
            print("invalid input")
        
def CheckPokemonAlive(player):
    return any(pokemon.health > 0 for pokemon in player.pokemon)