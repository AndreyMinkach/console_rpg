from Items.item import Item


class Outfit(Item):
    def __init__(self, **entries):
        super().__init__()
        self.__dict__.update(dict(entries))

    def __init__(self, item_id: int = 0, sub_type="No sub type", name="No name", defence=0):
        super().__init__(item_id)
        self.sub_type = sub_type
        self.defence = defence
        self.name = name
