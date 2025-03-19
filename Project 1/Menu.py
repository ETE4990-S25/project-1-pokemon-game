import PokemonGame as PG
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

def LoadData():
    if os.path.exists(DATA) and os.path.getsize(DATA) > 0:
        with open(DATA, 'r') as file:
            return json.load(file)
    return {}

def SaveData(data):
    with open(DATA, 'w') as file:
        json.dump(data, file)

def Start():
    if input(print("\n1. New\n2. Load")) == '2':
        Load()
    else:
        Open()


def Open():        ## Need to check save to see how many slots available
    global GameData
    global SaveSlot
    global player_pokemon_list
    print("\n---Welcome to Pokemon---\n")

    Name = input("What is your name?").capitalize()
    Gender = input("Are you a boy or a girl?")
    
    print("Choose from the following:\n")
    temp = []
    for i in range(len(PG.chosen_pokemon)):
        print(PG.chosen_pokemon[i].name)
        temp.append(PG.chosen_pokemon[i].name) ## temp list of pokemon names to compare later

    FirstPokemon = input("Choose a pokemon from the list:")

    while FirstPokemon not in temp:     ## Verify a valid pokemon was selected, Have to compare with temp, not wild_pokemon_list because comparing names or pokemon class instances
        FirstPokemon = input("\nPokemon not available, please choose another")

    for i in range(len(PG.chosen_pokemon)):
        if FirstPokemon == PG.chosen_pokemon[i].name:
            PokemonClassInstance = PG.chosen_pokemon[i]      ## assign class instance of chosen pokemon 
            player_pokemon_list.append(PokemonClassInstance)       ## Players dictionary of pokemon class instances  ## First pokemon

    Player = PG.Player(Name, Gender, pokemon=[PokemonClassInstance]) ## initialize player

    GameData = LoadData()    ## Load already saved data

    if len(GameData) < 3:
        
        SaveSlot = len(GameData) +1
        GameData[SaveSlot] = Player.to_dict()
        SaveData(GameData) ## Write data to json
        print(f"\nGame started in slot #{SaveSlot}")
        Menu(Player)

    else:
        print("All save slots are full\nOverwrite Data to which slot?")
        choice = int(input("1, 2, or 3"))
        if choice in range(1,4):
            GameData[choice] = Player.to_dict()  ## Should reassign old Save # 
            SaveData(GameData)
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
    
    GameData = LoadData()

    if GameData == {}:          ## check if empty dictionary or empty space? " " {}?
        print("No saved data available")
        return
    
    print("\n---Welcome Back---")
    print("Choose a file to load: ")

    for Slot, Data in GameData.items():   ## Key, value in json
        print(f"{Slot} : {Data['name']}")

    flag = True

    while(flag):
        option = input()       ## choose which to open
        SaveSlot = option
        if option in GameData: 
            print(f"\nLoading {GameData[option]['name']}'s save")

            CurrentPlayer = PG.Player(
                GameData[option]['name'], 
                GameData[option]['gender'], 
                GameData[option]['bag'], 
                GameData[option]['team']
                )  ##reinnit player class (name, gender, inventory, pokemon)
            
            for i in range(len(GameData[option]["team"])): ##Length of team list ## How many pokemon to innitialize

                player_pokemon_list.append(PG.Pokemon(   ## A dictionary of all player pokemon reinnitialized
                    
                    GameData[option]["team"][i]['name'],
                    GameData[option]["team"][i]['health'],
                    GameData[option]["team"][i]['health_cap'],
                    GameData[option]["team"][i]['moves'],
                    GameData[option]["team"][i]['element']
                ))

            for i in range(len(GameData[option]["bag"])): 
                
                if GameData[option]["bag"][i]['name'] in ["Poke Ball", "Great Ball", "Ultra Ball", "Master Ball"]:

                    player_inventory.append(PG.PokeBalls(

                        GameData[option]["bag"][i]['name'],
                        GameData[option]["bag"][i]['effect'],
                        GameData[option]["bag"][i]['stack'],
                        GameData[option]["bag"][i]['amount']
                    ))
                else:
                    
                     player_inventory.append(PG.HealItems(

                        GameData[option]["bag"][i]['name'],
                        GameData[option]["bag"][i]['effect'],
                        GameData[option]["bag"][i]['stack'],
                        GameData[option]["bag"][i]['amount']
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
    time.sleep(2)
    SaveData(GameData)
    print("---Game Saved---")
    time.sleep(1)

def Menu(CurrentPlayer):      ## Show what attacks available, option to run, check inventory, switch pokemon, Pokemon on field
    global GameData
    global SaveSlot
    global player_pokemon_list

    MainPokemon = player_pokemon_list[0] ## First pokemon in team list by default
    Play = True
    while(Play):
        print("\n\n\n--------------------------------------")
        print("1. Walk into grass       2. Check Bag")
        print("3. Go to PokeCenter      4. Swap Main Pokemon")
        print("5. Save Game             6. Exit Game")
        option = input()

        if option not in ['1','2','3','4','5','6']:
            print("\nInvalid option")

        elif option == '1':
            if PG.CheckPokemonAlive(CurrentPlayer):
                PG.TallGrass(CurrentPlayer, MainPokemon)
            else:
                print("\nYou shouldn't go into the grass without any pokemon to fight\nHead to the pokecenter first!")

        elif option == '2':
            CurrentPlayer.display_inventory()

        elif option == '3':
            player_pokemon_list = PG.PokeCenter(player_pokemon_list)
            print("Your Pokemon have been fully healed!!\n")

        elif option == '4':
            MainPokemon = PG.SwapPokemon(player_pokemon_list)

        elif option == '5':
            Save(CurrentPlayer)

        elif option == '6':
            Play = False
            Save(CurrentPlayer)   ##Just in case 
            print("Thanks for playing!")

        time.sleep(1.5)