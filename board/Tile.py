from enum import Enum

class TileStatus(Enum):
    REGULAR = 0
    WALL = 1
    GOAL = 2

class Tile:
    def __init__(self, status: TileStatus, entity):
        self.status = status
        self.entity = entity

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status
    
    def getEntity(self):
        return self.entity
    
    def setEntity(self, entity):
        self.entity = entity

    def interaction(self):
        pass
