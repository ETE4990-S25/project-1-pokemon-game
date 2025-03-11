import PokemonGame as PG
import ##inventory system
import json
import itertools

SAVE = "Data.json" ## The file
GameData = {}      ## What is being saves to the file

def Start():
    if input(print("1. New\n2. Load")) == '2':
        Load()
    else:
        Open()


def Open():        ## Need to check save to see how many slots available
    print("---Welcome to Pokemon---")
    Name = input("What is your name?")
    Gender = input("Are you a boy or a girl?")
    Player = PG.Player(Name, Gender)
    GameData["PlayerClass"] = Player     ## New Save Data

def Load():
    Temp = {}
    print("---Welcome Back---")
    print("Choose a file to load: ")

    with open(SAVE, 'r'):
        for "PlayerClass" in SAVE:

            print(f"{itertools.count(start=1)}. {json.load(SAVE["PlayerClass"].Name)}\n")   ## count(). PlayerName       1. Ash 
            Temp[itertools.count(start=1)] = json.load(SAVE[  .........  ])         ## Make a temporary dictionary of numbers and Saved Data???

        option = input()       ## choose which to open
        if option in Temp: 
            GameData = SAVE[Temp[option]]   ## Temp[option] is ????
        

    ### Read how many files in JSON and ouput names and numbers

def Save(CurrentPlayer):
    print("---Save Game---")
    if CurrentPlayer in SAVE["PlayerClass"]:
        SAVE["PlayerClass"] = GameData

def Menu(CurrentPlayer):      ## Show what attacks available, option to run, check inventory, switch pokemon, Pokemon on field

    print("\n--------------------------------------")
    print("1. Walk into grass       2. Check Bag")
    print("3. Go to PokeCenter      4. Save Game")
    option = int(input())
    if option == 1:
        PG.TallGrass(CurrentPlayer)
