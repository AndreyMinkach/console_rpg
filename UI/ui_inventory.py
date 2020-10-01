from pyglet.graphics import OrderedGroup

from Items.Weapons.weapon import Weapon
from UI.ui_base import *

from Gameplay.inventory import Inventory
from Helpers.color_helper import ColorHelper
from Items.items_loader import ItemLoader
from UI.ui_base import UIBase
from UI.ui_scrollable_container import ScrollableContainer
from UI.ui_text import UIText


class UIInventory(UIBase):
    def __init__(self, position: Vector2, size: Vector2):
        super().__init__(position, size)

        all_items = ItemLoader()
        # print(all_items._items)
        invent = Inventory()
        weapon = all_items.get_item_by_id(1)
        outfit = all_items.get_item_by_id(50)
        invent.add_item(weapon)
        invent.add_item(outfit)
        # print(invent.get_item_list_by_type("Weapon"))
        self._child_group = OrderedGroup(self.group.order + 1)

        my_inv_button = UIBase(Vector2(position.x + 10, position.y + size.y - 60), Vector2(185, 50),
                               color=ColorHelper.GRAY)
        my_inv_button.group = self._child_group
        someone_inv_button = UIBase(Vector2(position.x + size.x - 195, position.y + size.y - 60), Vector2(185, 50),
                                    color=ColorHelper.GRAY)
        someone_inv_text = UIText("Someone", Vector2(position.x + size.x - 195, position.y + size.y - 120),
                                  Vector2(185, 50), 20, ColorHelper.PINK)
        print(someone_inv_button.size, someone_inv_button.position)
        print(someone_inv_text.size, someone_inv_text.position)
        someone_inv_button.group = self._child_group
        someone_inv_text.group = self._child_group

        item_lit_container = ScrollableContainer(Vector2(position.x + 10, position.y + 10), Vector2(size.x - 20, 150))
        item_lit_container.color = ColorHelper.GREEN[:3]
        item_lit_container.children_margin = Vector2(5, 5)
        item_lit_container.group = self._child_group

        for item in invent.get_item_list_by_type("Outfit"):
            item_text = UIText(item.name, Vector2.zero, Vector2(item_lit_container.size.x - 5, 2), 20, ColorHelper.PINK)
            item_lit_container.add_child(item_text)
            item_text.group = self._child_group

    def update_logic(self, **kwargs):
        super().update_logic()
        # for ui_element in self.children:
        #     if isinstance(ui_element, ScrollableContainer):
        #         ui_element.update_logic()
        #     else:
        #         ui_element.draw()
