# Exploring
# how players interact with the world

class Exploring(object):
    """Moving around the space."""
    def __init__(self, jump, sneak):
        """ Initialize jump, and sneak."""
        self.jump = jump
        self.sneak = sneak
    
    def jump_up(self, jump):
        """Allows player to jump. The more the player jumps, the stronger they become."""
        
        print("You jump "+ jump +"units.")
        jump = jump + 0.25

    def sneaking(self, sneak):
        """Allows player to sneak around. The more the player does so, the stronger they become."""
        print("You decide to sneak.")
        sneak = sneak + 0.25
        
    def get_stats(self):
        """Displays the stats of the player on the console."""
        print("Your general stats are as follows: ")
        print("Jump stat: "+ self.jump + "units.")
        print("Sneak stat: "+ self.sneak + "units.")


# Child classes      
class CatMoves(Exploring):
    """Represents the actions a cat can do."""
    def __init__(self, jump, sneak, high_leap, climb):
        """Sets up basic actions and specific actions."""
        super().__init__(jump, sneak)
        self.high_leap = True
        self.climb = True
        
    def furniture_leap(self):
        super().furniture_leap(self)
        if self.high_leap == True: 
            print("You jump onto the furniture.")
        else:
            print("Your attempt failed.")

    def climb_up(self):
        super().climb(self)
        print("You climb up the stucture.")

class DogMoves(Exploring):
    """Represents the  actions a dog can do"""
    def __init__(self, jump, sneak, spring, paw_stand):
        """sets up basic actions"""
        super().__init__(self, jump, sneak)
        
    def sprint(self):
        super().sprint(self)
        print("You sprint.")

    def paw_stand(self):
        super().paw_stand(self)
        print("You stand.")
