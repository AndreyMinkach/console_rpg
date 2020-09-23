import json
import os
from pydoc import locate


class ItemLoader:
    ITEM_TYPE_LIST = ['Items.Weapons.weapon.Weapon', 'Items.Outfits.outfit.Outfit']

    def __init__(self):
        self._items = {}
        self.load_items()

    def load_items(self):
        folder_path = 'Static/Items/'
        file_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.json')]
        items = {}
        for file_path in file_list:
            with open(file_path, 'r') as f:
                temp_json = json.load(f)
                for value_item in temp_json:
                    items[value_item['id']] = value_item
        self._items = items

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
