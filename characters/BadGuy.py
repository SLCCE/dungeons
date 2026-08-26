from .Character import Character
# from item.HealthPotion import HealthPotion

class BadGuy(Character):
    def __init__(self, current_hp, max_hp, start_x, start_y, startingInventory, startingEquipment, t, offset, tile_size=24, size=10):        
        # initializing character for hp and inventory
        Character.__init__(self, current_hp, max_hp, start_x, start_y, startingInventory, startingEquipment, t, offset)

        self.tile_size = tile_size
        # self.goto(start_x * tile_size, start_y * tile_size)
        self.strength = 1
        self.size = size
        self._draw_self("red")
    
    # Override from parent class
    def _draw_self(self, color):
        self.t.clear()
        xDestination = self.position[1] * self.tile_size - self.offset[0] + self.tile_size // 2
        yDestination = self.position[0] * self.tile_size - self.offset[1] + self.tile_size // 4
        self.t.goto(xDestination, yDestination)
        self.t.pendown()
        self.t.fillcolor(color)
        self.t.begin_fill()
        self.t.circle(self.size)
        self.t.end_fill()
        self.t.penup()
    
    # def use_item(self, item_index):
    #     if 0 <= item_index < len(self.inventory["items"]):
    #         item = self.inventory["items"][item_index]
    #         if isinstance(item, HealthPotion):
    #             healed = self.heal()
    #             if healed > 0:
    #                 return "Healed " + str(healed) + " HP!"
    #     return "Invalid item!"
    
    # # move methods
    # def move_up(self, board):
    #     new_x = self.position[0]
    #     new_y = self.position[1] + 1
    #     self.set_position(new_x, new_y)
    
    # def move_down(self, board):
    #     new_x = self.position[0]
    #     new_y = self.position[1] - 1
    #     self.set_position(new_x, new_y)
    
    # def move_left(self, board):
    #     new_x = self.position[0] - 1
    #     new_y = self.position[1]
    #     self.set_position(new_x, new_y)
    
    # def move_right(self, board):
    #     new_x = self.position[0] + 1
    #     new_y = self.position[1]
    #     self.set_position(new_x, new_y)

if __name__ == "__main__":
    p = BadGuy(7, 10, 1, 1, [], [])
    print(p)
