from enum import Enum

class ArmorType(Enum):
    HELMET = 1
    CHEST = 2
    LEGS = 3
    BOOTS = 4

class WeaponType (Enum):
    SWORD = "A"

class Armor():
    def __init__(self, name: str, defense: int, armorType: ArmorType):
        self.name = name
        self.defense = defense
        self.armorType = armorType

    def getName(self):
        return self.name
    
    def setName(self, name: str):
        self.name = name

    def getDefense(self):
        return self.defense

    def setDefense(self, defense: int):
        self.defense = defense
    
    def getArmorType(self):
        return self.armorType
    
    def setArmorType(self, armorType: ArmorType):
        self.armorType = armorType

class Weapon():
    def __init__(self, name: str, atkDmg: int, weaponType: WeaponType):
        self.name = name
        self.atkDmg = atkDmg
        self.weaponType = weaponType
    
    def getName(self):
        return self.name
    
    def setName(self, name: str):
        self.name = name

    def getDamage(self):
        return self.atkDmg

    def setDamage(self, atkDmg: int):
        self.atkDmg = atkDmg
    
    def getWeaponType(self):
        return self.weaponType
    
    def setWeaponType(self, weaponType: WeaponType):
        self.weaponType = weaponType

    
