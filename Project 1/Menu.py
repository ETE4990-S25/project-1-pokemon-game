import PokemonGame as PG
import json
import itertools
import os

DATA = "Data.json" ## The file
global GameData      ## What is being saves to the file
GameData = {}

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
    print("\n---Welcome to Pokemon---\n")

    Name = input("What is your name?").capitalize()
    Gender = input("Are you a boy or a girl?")
    
    print("Choose from the following:")
    temp = []
    for i in range(len(PG.wild_pokemon_list)):
        print(PG.wild_pokemon_list[i].name)
        temp.append(PG.wild_pokemon_list[i].name)

    FirstPokemon = input("Choose a pokemon from the list:")

    while FirstPokemon not in temp:     ## Verify a valid pokemon was selected, Have to compare with temp, not wild_pokemon_list because comparing names or pokemon class instances
        FirstPokemon = input("\nPokemon not available, please choose another")

    for i in range(len(PG.wild_pokemon_list)):
        if FirstPokemon == PG.wild_pokemon_list[i].name:
            PokemonClassInstance = PG.wild_pokemon_list[i]      ## assign class instance of chosen pokemon 
            PokemonDict = PokemonClassInstance.to_dict()        ## Change to dictionary so we have the ability to save

    Player = PG.Player(Name, Gender, pokemon=[PokemonDict]) ## initialize player

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
    GameData = LoadData()

    if GameData == {}:          ## check if empty dictionary or empty space? " " {}?
        print("No saved data available")
        return
    
    print("\n---Welcome Back---")
    print("Choose a file to load: ")

    for Slot, Data in GameData.items():   ## Key, value in json
        print(f"{Slot} : {Data['name']}")

        option = input()       ## choose which to open
        if option in GameData: 
            print(f"\nLoading {GameData[option]['name']}'s save")

            CurrentPlayer = PG.Player(
                GameData[option]['name'], 
                GameData[option]['gender'], 
                GameData[option]['bag'], 
                GameData[option]['team']
                )  ##reinnit player class (name, gender, inventory, pokemon)
            
            Menu(CurrentPlayer)  ## Call to start Game
        else:
            print("Incorrect file number")
        
        

    ### Read how many files in JSON and ouput names and numbers

def Save(Player):
    print("\n---Saving Game---")
    SaveData(Player)
    print("---Game Saved---")

def Menu(Player):      ## Show what attacks available, option to run, check inventory, switch pokemon, Pokemon on field
    global GameData
    global SaveSlot

    MainPokemon = GameData[SaveSlot]["team"][0] ## First pokemon in team list
    Play = True
    while(Play):
        print("\n\n\n--------------------------------------")
        print("1. Walk into grass       2. Check Bag")
        print("3. Go to PokeCenter      4. Swap Main Pokemon")
        print("5. Save Game             6. Exit Game")
        option = int(input())

        if option not in range(1,5):
            print("\nInvalid option")

        elif option == 1:
            PG.TallGrass(Player)

        elif option == 2:
            Player.display_inventory()

        elif option == 3:
            PG.PokeCenter(Player)

        elif option == 4:
            print("\nThe pokemon you have right now are:")

            for pokemon in GameData[SaveSlot]["team"]:
                print(f"{pokemon}. {pokemon['name']}")

            choice = int(input("Choose a pokemon to pick as your main one")) + 1
            MainPokemon = GameData[SaveSlot]["team"][choice]

        elif option == 5:
            Save()

        elif option == 6:
            Play = False
            Save()   ##Just in case 