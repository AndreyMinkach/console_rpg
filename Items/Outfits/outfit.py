from Items.item import Item


class Outfit(Item):
    def __init__(self, durability=0, name="No name"):
        self.durability = durability
        self.name = name
