###Gives option to the player to choose a pet character and their name.
##Two characters in our game are a dog or a cat.
class Player_Choice(object):
    """Creates a class to choose a player and a pet."""

    def __init__(self, pet_name=None, pet_type=None):
        self.pet_name = pet_name
        self.pet_type= pet_type
        self.inventory= []
        self.jump= 1.0
        self.sneak=1.0
        """For player's item collection."""

    def Select_pet(self, pet_choice=None):
        self.pet_choice= pet_choice
        """Allow the player to select their pet and pet's name."""
        pet_choice= ["Dog", "Cat"]

        self.pet_name= input ("Please enter your pet's name: ")
        self.pet_type=input("Please choose your pet type dog or cat?: ")

        if self.pet_type not in pet_choice:  ###For player to pick their pet's name and pet type. 
                print ("Invalid choice, defaulting to a dog.") 
                self.pet_type= "Dog"
        """For invalid pet type from player 1, this will deafult the selection to a dog."""

    def display_players(self):
        """Display the players info with their names and pet's name."""
        print("\nPlayer: " + self.pet_name + ":" + self.pet_type)

class Exploring(object):
    """Moving around the space."""
    def __init__(self, jump=1.0, sneak=1.0):
        """ Initialize jump, and sneak."""
        self.jump = jump
        self.sneak = sneak
    
    def jump_up(self):
        """Allows player to jump. The more the player jumps, the stronger they become."""

        print(f"You jump {self.jump} units.")  ###Learned to use f and {} instead of + here since a float is being passed from the internet. 
        self.jump+= 0.25

    def sneaking(self):
        """Allows player to sneak around. The more the player does so, the stronger they become."""
        print("You decide to sneak.")
        self.sneak+= 0.25
        
    def get_stats(self):
        """Displays the stats of the player on the console."""
        print("Your general stats are as follows: ")
        print(f"Jump stat: {self.jump} units.")
        print(f"Sneak stat: {self.sneak} units.")

class Items:
      """Represents collectible and usuable items."""

      def __init__(self, name, uses, description):
           """Initialize the item."""
           self.name= name
           self.uses= uses
           self.description= description

      def use_item(self):
           """Uses an item if available."""
           if self.uses >0:
                self.uses -=1
                print ("Used " + self.name + ". Use left: " + str(self.uses))
           else:
                print(self.name + "has no uses left.")

      def display_item(self):
           """Displays item information."""
           print("Item: " + self.name + ":" + self.description + "(Uses:" +str(self.uses)+")")

player = Player_Choice()
player.Select_pet()
player.display_players()


explore= Exploring ()

explore.jump_up()
explore.sneaking()
explore.get_stats()

stick= Items("Stick", 3, "A simple stick to poke things.")
player.inventory.append(stick)

stick.display_item()
stick.use_item()
stick.use_item()

    

            
        
    
        
     

Family_Pet_Adventure= Player_Choice()

Family_Pet_Adventure.Select_pet()
"""Allow the player to choose their pets"""

Family_Pet_Adventure.display_players()
"""Displays the selected choice for the player."""






import json

def save_game(player):
    """Save the game details to a json file."""
    game_data= {
        "pet_name": player.pet_name,
        "pet_type": player.pet_type,
        "jump_stat": player.jump,
        "sneak_stat": player.sneak,
        "inventory": [{"name": Items.name, "uses": Items.uses, "description": Items.description} for item in player.inventory]
    }

    with open("save_game.josn", "w") as save_file:
        json.dump(game_data, save_file, indent=4)

    print("Game saved successfully!")

def menu():
    """""Creates a menu players can access."""

    options = ["Exit Menu", "Display Inventory","Save Game"]
    print("Options: \n")
    
    for i in enumerate(options, start = 1):
        print(i)

    choice = int(input("Enter the number of the chosen option: "))

    if choice == 1:
        return 
    elif choice == 2:
        for item in player.inventory:
            print(f"Item: {item.name}, Uses: {item.uses}, Description: {item.description}") 
        return

    elif choice == 3:
        save_game(player)
        return
    else:
        print("Invalid choice.")

player.Select_pet()
menu()
       
   