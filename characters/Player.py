import turtle
from .Character import Character
# from item.HealthPotion import HealthPotion
from items.Equipment import WeaponType

class Player(Character):
    def __init__(self, current_hp, max_hp, start_x, start_y, startingInventory, startingEquipment, t, offset, tile_size=24):
        # initializing character for hp and inventory
        Character.__init__(self, current_hp, max_hp, start_x, start_y, startingInventory, startingEquipment, t, offset)
        
        # player position and settings
        self.tile_size = tile_size
        self.color = "green"
        self._draw_self()
    
    # Override from parent class
    def _draw_self(self):
        self.t.clear()
        xDestination = self.position[1] * self.tile_size - self.offset[0] + self.tile_size // 2
        yDestination = self.position[0] * self.tile_size - self.offset[1] + self.tile_size // 4
        self.t.goto(xDestination, yDestination)
        self.t.pendown()
        self.t.fillcolor(self.color)
        self.t.begin_fill()
        self.t.circle(20)
        self.t.end_fill()
        self.t.penup()
    
    def get_strength(self):
        return self.equipment[WeaponType.SWORD]
    
    def add_to_inventory(self, item):
        # TODO: edit later when items
        if len(self.inventory) < 9:
            self.inventory.append(item)
    
    # def use_item(self, item_index):
    #     if 0 <= item_index < len(self.inventory["items"]):
    #         item = self.inventory["items"][item_index]
    #         if isinstance(item, HealthPotion):
    #             healed = self.heal()
    #             if healed > 0:
    #                 return "Healed " + str(healed) + " HP!"
    #     return "Invalid item!"

    
    # move methods (board 'isOut' method will do error handling)
    def move_up(self):
        new_x = self.position[0] + 1
        new_y = self.position[1]
        self.set_position(new_x, new_y)
    
    def move_down(self):
        new_x = self.position[0] - 1
        new_y = self.position[1]
        self.set_position(new_x, new_y)
    
    def move_left(self):
        new_x = self.position[0]
        new_y = self.position[1] - 1
        self.set_position(new_x, new_y)
    
    def move_right(self):
        new_x = self.position[0]
        new_y = self.position[1] + 1
        self.set_position(new_x, new_y)

if __name__ == "__main__":
    p = Player(7, 10, 1, 1, [], [])
    print(p)
