# -----------------------------------------------------------
# class representing a single bible-book
#
# short_name  abbreviated name of the book
# length      number of chaperts in the book 

class Book:

    def __init__(self, short_name, length):
        self.short_name = short_name
        self.length = length
        
    def __str__(self):
      return self.short_name + ", " + str(self.length)
