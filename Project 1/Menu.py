import PokemonGame


def Start():        ## Need to check save to see how many slots available
    print("---Welcome to Pokemon---")
    Name = input("What is your name?")
    Gender = input("Are you a boy or a girl?")
    Player1 = PokemonGame.Player(Name, Gender)


def Menu():      ## Show what attacks available, option to run, check inventory, switch pokemon, Pokemon on field


