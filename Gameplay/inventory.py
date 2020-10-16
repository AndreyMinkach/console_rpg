from Items.item import Item


class Inventory:
    def __init__(self):
        self._item_dict = {}

    def add_item(self, item: Item):
        if item.id in self._item_dict is True:
            self._item_dict[item.id].count += item.count
        else:
            self._item_dict[item.id] = item

    def _remove_item(self, item: Item):
        del self._item_dict[item.id]

    def remove_item(self, item_id: str, item_count: int) -> int:
        if item_id in self._item_dict:
            current_item = self._item_dict[item_id]
            if item_count >= current_item.count:
                item_count = current_item.count
            current_item.count -= item_count
            if current_item.count <= 0:
                self._remove_item(current_item)
            return current_item.count
        else:
            return -1

    def get_item_list_by_type(self, item_type: str):
        result_list = []
        for key_id, item in self._item_dict.items():
            if item.item_type == item_type:
                result_list.append(item)
        return result_list

    def find_item_by_id(self, item_id: int):
        if item_id in self._item_dict:
            return self._item_dict[item_id]
        return None
