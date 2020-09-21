from Items.item import Item


class Weapon(Item):
    def __init__(self, **entries):
        super().__init__()
        self.__dict__.update(dict(entries))

    def __init__(self, item_id=0, sub_type="No sub type", name="No name", damage=0):
        super().__init__(item_id)
        self.sub_type = sub_type
        self.damage = damage
        self.name = name
