from Items.item import Item


class Inventory:
    def __init__(self):
        self._item_list = []

    def add_item(self, item: Item):
        self._item_list.append(item)

    def remove_item(self, item: Item):
        self._item_list.remove(item)

    def get_item_list_by_type(self, item_type: type):
        result_list = []
        for item in self._item_list:
            if isinstance(item, item_type):
                result_list.append(item)
        return result_list

    def find_item_by_id(self, item_id: int):
        for item in self._item_list:
            if item.id == item_id:
                return item
        return None
