import PokemonGame as PG
import PokemonAndItems as PI
import json
import time
import os

DATA = "Data.json" ## The file
global GameData      ## What is being saves to the file
GameData = {}
global player_pokemon_list
player_pokemon_list = []
global player_inventory
player_inventory = []

def load_data():
    if os.path.exists(DATA) and os.path.getsize(DATA) > 0:
        with open(DATA, 'r') as file:
            return json.load(file)
    return {}

def save_data(data):
    with open(DATA, 'w') as file:
        json.dump(data, file, indent=4)

def Start():
    print("\n1. New\n2. Load")
    if input() == '2':
        Load()
    else:
        Open()


def Open():        ## Need to check save to see how many slots available
    global GameData
    global SaveSlot ##Global variables called inside function to be modified
    global player_pokemon_list
    print("\n---Welcome to Pokemon---  \n---Do you have what it takes to be a trainer?---\n")

    Name = input("What is your name?").strip().capitalize()
    Gender = input("Are you a boy or a girl?") ##Never used in the game, player can enter whatever they want because we are inclusive :) (also just here because its asked in pokemon)
    
    print("Choose from the following:\n")
    temp = []
    for i in range(len(PI.chosen_pokemon)): ## For me chosen_pokemon is a variable/list
        print(PI.chosen_pokemon[i].name)
        temp.append(PI.chosen_pokemon[i].name) ## temp list of pokemon names to compare later

    FirstPokemon = input("Choose a pokemon from the list:")

    while FirstPokemon not in temp:     ## Verify a valid pokemon was selected, Have to compare with temp, not wild_pokemon_list because comparing names or pokemon class instances
        FirstPokemon = input("\nPokemon not available, please choose another")

    for i in range(len(PI.chosen_pokemon)):
        if FirstPokemon == PI.chosen_pokemon[i].name:
            PokemonClassInstance = PI.chosen_pokemon[i]      ## assign class instance of chosen pokemon 
            player_pokemon_list.append(PokemonClassInstance)       ## Players dictionary of pokemon class instances  ## First pokemon

    Player = PI.Player(Name, Gender, pokemon=[PokemonClassInstance]) ## initialize player

    GameData = load_data()    ## Load already saved data

    if len(GameData) < 3:
        
        SaveSlot = len(GameData) +1
        GameData[SaveSlot] = Player.to_dict()
        save_data(GameData) ## Write data to json
        print(f"\nGame started in slot #{SaveSlot}")
        Menu(Player)

    else:
        print("All save slots are full.\nOverwrite data to which slot?")
        flag = True
        while(flag):
            choice = int(input("1, 2, or 3"))
            if 1 <= choice <= 3:
                GameData[choice] = Player.to_dict()  ## Should reassign old Save # 
                save_data(GameData)
                print(f"\nSlot:{choice} has been overwritten\n")
                SaveSlot = choice
                Menu(Player)

            else:
                print("Invalid Option")
    

def Load():
    global GameData
    global SaveSlot
    global player_pokemon_list
    global player_inventory
    
    GameData = load_data()

    if GameData == {}:          ## check if empty dictionary or empty space? " " {}?
        print("No saved data available")
        return
    
    print("\n---Welcome Back---")
    print("Choose a file to load: ")

    for Slot, Data in GameData.items():   ## Key, value in json
        print(f"{Slot} : {Data['name']}")

    flag = True

    while(flag):
        SaveSlot = input().strip()       ## choose which to open  ## GameData carries string saveslots '1', '2' ect.
        if SaveSlot in GameData: 
            print(f"\nLoading {GameData[SaveSlot]['name']}'s save")

            player_pokemon_list = []
            player_inventory = []
            
            CurrentPlayer = PI.Player(
                GameData[SaveSlot]['name'], 
                GameData[SaveSlot]['gender'], 
                GameData[SaveSlot]['bag'], 
                GameData[SaveSlot]['team']
                )  ##reinnit player class (name, gender, inventory, pokemon)
            
            for i in range(len(GameData[SaveSlot]["team"])): ##Length of team list ## How many pokemon to innitialize

                player_pokemon_list.append(PI.Pokemon(   ## A dictionary of all player pokemon reinnitialized
                    
                    GameData[SaveSlot]["team"][i]['name'],
                    GameData[SaveSlot]["team"][i]['health'],
                    GameData[SaveSlot]["team"][i]['health_cap'],
                    GameData[SaveSlot]["team"][i]['moves'],
                    GameData[SaveSlot]["team"][i]['element']
                ))

            for i in range(len(GameData[SaveSlot]["bag"])): 
                
                if GameData[SaveSlot]["bag"][i]['name'] in PI.Pokeball_list:

                    player_inventory.append(PI.PokeBalls(

                        GameData[SaveSlot]["bag"][i]['name'],
                        GameData[SaveSlot]["bag"][i]['effect'],
                        GameData[SaveSlot]["bag"][i]['stack'],
                        GameData[SaveSlot]["bag"][i]['amount']
                    ))
                elif GameData[SaveSlot]["bag"][i]['name'] in PI.Potion_names:
                    
                     player_inventory.append(PI.Heal_Items(

                        GameData[SaveSlot]["bag"][i]['name'],
                        GameData[SaveSlot]["bag"][i]['effect'],
                        GameData[SaveSlot]["bag"][i]['stack'],
                        GameData[SaveSlot]["bag"][i]['amount']
                    ))

            CurrentPlayer.pokemon = player_pokemon_list ## assign pokemon to player
            CurrentPlayer.inventory = player_inventory ## assign inventory 
            flag = False
            Menu(CurrentPlayer)  ## Call to start Game
        else:
            print("Incorrect file number")
        


    ### Read how many files in JSON and ouput names and numbers

def Save(Player):
    global GameData
    global SaveSlot

    print("\n---Saving Game---")
    GameData[SaveSlot] = Player.to_dict()
    save_data(GameData)
    time.sleep(2)
    print("---Game Saved---")
    time.sleep(1)

def Menu(CurrentPlayer):      ## Show what attacks available, option to run, check inventory, switch pokemon, Pokemon on field
    global GameData
    global SaveSlot
    global player_pokemon_list

    if not PG.CheckPokemonAlive(CurrentPlayer):
        player_pokemon_list = PG.PokeCenter(player_pokemon_list)

    MainPokemon = player_pokemon_list[0] ## First pokemon in team list by default
    Play = True
    while(Play):
        print("\n\n\n--------------------------------------")
        print("1. Walk into grass       2. Check Bag")
        print("3. Go to PokeCenter      4. Swap Main Pokemon")
        print("5. Save Game             6. Exit Game")
        option = int(input())

        if option not in range(7):
            print("\nInvalid option")

        elif option == 1:
            if PG.CheckPokemonAlive(CurrentPlayer):
                PG.TallGrass(CurrentPlayer, MainPokemon)
            else:
                print("\nYou shouldn't go into the grass without any pokemon to fight\nHead to the pokecenter first!")

        elif option == 2:
            CurrentPlayer.display_inventory()

        elif option == 3:
            player_pokemon_list = PG.PokeCenter(player_pokemon_list)
            print("Your Pokemon have been fully healed!!\n")

        elif option == 4:
            MainPokemon = PG.SwapPokemon(player_pokemon_list)

        elif option == 5:
            Save(CurrentPlayer)

        elif option == 6:
            Play = False
            Save(CurrentPlayer)   ##Just in case 
            print("Thanks for playing!")

        time.sleep(1.5)