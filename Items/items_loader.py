from pydoc import locate

from Helpers.json_loader import JsonLoader


class ItemLoader(JsonLoader):
    instance = None
    ITEM_TYPE_LIST = ['Items.Weapons.weapon.Weapon', 'Items.Outfits.outfit.Outfit']

    def __init__(self):
        self.__class__.instance = self
        super().__init__('Static/Items/')
        self._items = {}
        self.load_items()

    def load_items(self):
        for value_item in self.loaded_element_list:
            self._items[value_item['id']] = value_item

    def get_item_by_id(self, item_id: int):
        if item_id not in list(self._items.keys()):
            return None

        temp_dict = self._items[item_id]
        item_type = temp_dict['item_type']
        for i in ItemLoader.ITEM_TYPE_LIST:
            if item_type in i:
                item_type = i
                break

        located_item_class = locate(item_type)
        item_instance = located_item_class()  # call constructor of class to get its instance
        item_instance.__dict__.update(temp_dict)
        return item_instance
