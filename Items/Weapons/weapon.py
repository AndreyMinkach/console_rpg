from Items.item import Item


class Weapon(Item):
    def __init__(self, damage=0, name="No name", weapon_type="No type"):
        self.weapon_type = weapon_type
        self.damage = damage
        self.name = name
