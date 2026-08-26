# from item.HealthPotion import *
import turtle
from items.Equipment import Armor, Weapon, ArmorType, WeaponType

class Character:
    def __init__(self, current_hp, max_hp, initX, initY, startingInventory, startingEquipment, t: turtle.Turtle, offset):
        self.hp = [current_hp, max_hp]
        self.position = [initX, initY]
        # self.inventory = {"items": [HealthPotion(max_hp / 2, 1)]}
        self.inventory = []
        self.equipment = {ArmorType.HELMET: "", 
                          ArmorType.CHEST: "", 
                          ArmorType.LEGS: "", 
                          ArmorType.BOOTS: "", 
                          WeaponType.SWORD: 1}
        # (name, offense)
        for invEntry in startingInventory:
            print(invEntry)
            # TODO: determine weapon, potion, utility, etc. 
            self.add_item(invEntry)
        # (name, defense, armorType)
        for eqEntry in startingEquipment:
            armorObject = Armor(eqEntry[0], eqEntry[1], eqEntry[2])
            self.equip_item(ArmorType(int(eqEntry[2])), armorObject)
        self.t = t
        self.t.up()
        self.t.hideturtle()
        self.offset = offset
    
    def _draw_self(self, color):
        pass
    
    def die(self):
        self.t.clear()
    
    def __str__(self):
        return str(type(self)) + " " + str(self.hp)
    
    # hp getters and setters
    def get_hp(self):
        return self.hp[0]
    
    def set_hp(self, value):
        self.hp[0] = min(value, self.hp[1])
        if self.hp[0] < 0:
            self.hp[0] = 0
    
    def get_max_hp(self):
        return self.hp[1]
    
    def set_max_hp(self, value):
        self.hp[1] = value
    
    # position getters and setters
    def get_position(self):
        return self.position
    
    def set_position(self, x, y):
        self.position = [x, y]
    
    # equipment methods
    def equip_item(self, slot, item):
        self.equipment[slot] = item
    
    def unequip_item(self, slot):        
        self.equipment[slot] = None
    
    # inventory methods
    def add_item(self, item):
        self.inventory.append(item)
    
    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
    
    def set_offset(self, newOffset):
        self.offset = newOffset
    
    # Heals the Character if they have a HealthPotion in their inventory, upto their max health. Returns the amount of health healed
    # def heal(self):
    #     # Check for HealthPotions in character's inventory
    #     for item in self.inventory["items"]:
    #         if isinstance(item, HealthPotion):
    #             healedAmount = item.use()
    #             if healedAmount > -1:
    #                 # Prevent healing past the max hp of the character
    #                 healedAmount = min(healedAmount, self.hp[1] - self.hp[0])
    #                 self.hp[0] += healedAmount
    #                 return healedAmount
    #     return -1
