from Items.item import Item


class Weapon(Item):
    def __init__(self, damage=0, name="No name"):
        self.damage = damage
        self.name = name
