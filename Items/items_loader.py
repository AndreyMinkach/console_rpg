import json
from pydoc import locate

from Items.Outfits.outfit import Outfit
from Items.Weapons.weapon import Weapon


class LoadJson:
    ITEM_TYPE_LIST = ['Items.Weapons.weapon.Weapon', 'Items.Outfits.outfit.Outfit']

    def __init__(self):
        static_folder_path = 'Static/Items/'
        json_files = ["weapons.json", "outfits.json"]
        items = {}
        for json_file in json_files:
            with open(static_folder_path + json_file) as f:
                temp_json = json.load(f)
            for value_item in temp_json:
                items[value_item['id']] = value_item
        self._items = items

    def get_item_by_id(self, item_id: int):
        if item_id not in list(self._items.keys()):
            return None

        temp_dict = self._items[item_id]
        item_type = temp_dict['item_type']
        for i in LoadJson.ITEM_TYPE_LIST:
            if item_type in i:
                item_type = i
                break

        item = locate(item_type)
        instance_item = item()
        instance_item.__dict__.update(temp_dict)
        return instance_item
