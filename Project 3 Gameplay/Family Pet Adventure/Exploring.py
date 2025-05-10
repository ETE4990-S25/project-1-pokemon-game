# Exploring
# how players interact with the world

class Exploring(object):
    """Moving around the space."""
    def __init__(self, jump = 1, sneak = 1):
        """ Initialize jump, and sneak."""
        self.jump = 1.0
        self.sneak = 1.0
    
    def jump_up(self):
        """Allows player to jump. The more the player jumps, the stronger they become."""

        print(f"You jump {self.jump} units.")  ###Learned to use f and {} instead of + here since a float is being passed from the internet. 
        
        
        self.jump+= 0.25

        
    def get_stats(self):
        """Displays the stats of the player on the console."""
        print("Your general stats are as follows: ")
        print(f"Jump stat: {self.jump} units.")
        # print(f"Sneak stat: {self.sneak} units.")
        
# Child classes      
class CatMoves(Exploring):
    """Represents the actions a cat can do."""
    def __init__(self, jump, sneak):
        """Sets up basic actions and specific actions."""
        super().__init__(jump, sneak)
        self.high_leap = True
        self.climb = True
        
    def furniture_leap(self):
        if self.high_leap == True: 
            print("You jump onto the furniture.")
        else:
            print("Your attempt failed.")

    def climb_up(self):
        print("You climb up the stucture.")

class DogMoves(Exploring):
    """Represents the  actions a dog can do"""
    def __init__(self, jump, sneak):
        """sets up basic actions"""
        super().__init__(jump, sneak)

    def jump_up(self):
        """Allows player to jump. The more the player jumps, the stronger they become."""

        print(f"You jump {self.jump} units.")  ###Learned to use f and {} instead of + here since a float is being passed from the internet. 
        
        
        self.jump+= 0.25

    def sprint(self):
        print("You sprint.")

    def paw_stand(self):
        print("You stand.")

    def dog_walking_and_obstacles(self): #added function name and took while from gameplay section
        """Mechanic for walking around the game and discovering things."""
        import Items
        import random
        brick= Items.Brick(name="Brick", uses=1)
        shoes = Items.Shoes("Shoes", 5)
        food_bowl = Items.FoodBowl("Food Bowl", 5)
        
        x = 0
        
        while x != 3: # to keep the player in a playing loop, looking around the room
            print("You walk around the room, searching for the key . . .\n")
            print("You find a pile of sticks. Does this have the key? Use your inventory.\n")
            print("You have 4 options to explore: \n1:Sprint \n2:Get_stats \n3:Jump Up\n4:Paw Stand.")
            print("=============")
            print("You have 4 items to use to find your key: \n1:Brick \n2:Laptop \n3:Shoes \n4:Food_Bowl.")
            print("=============")
            
            move_choice= input("Choose an action (1-4):")
            item_choice= input("chosee an object(1-4):")
            moves={ "1": self.sprint,
                    "2": self.get_stats,
                    "3": self.jump_up,
                    "4": self.paw_stand}
            if move_choice in moves:
                moves[move_choice]()
            else:
                print("invalid move choice.")
            
            
            objects={"1":brick.throw, 
                    "2":Items.Laptop, 
                    "3":shoes.super_jump, 
                    "4":Items.FoodBowl}
            if item_choice in objects:
                objects[item_choice]()
            else:
                print("Invalid object choice.")

            x = random.randint(1,3)