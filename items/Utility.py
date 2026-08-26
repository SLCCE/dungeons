import turtle
from abc import ABC, abstractmethod

class Utility(ABC):
    def __init__(self, name: str, quanity: int):
        self.name = name
        self.quantity = quanity
        turtle.Turtle.__init__(self)
    
    def getName(self): 
        return self.name
    
    def getQuanity(self):
        return self.quantity
    
    def setName(self, name):
        self.name = name
        return
    
    def setQuanity(self, quanity):
        self.quantity = quanity
        return
    
    @property
    @abstractmethod
    def use(self):
        pass

    @property
    @abstractmethod
    def draw(self, xpos: int, ypos:int, scale:int):
        pass
    
