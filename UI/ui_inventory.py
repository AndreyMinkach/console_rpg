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

        my_invent_btn = UIBase(Vector2(position.x + 10, position.y + size.y - 60), Vector2(185, 50),
                               color=ColorHelper.GREEN)
        someone_invent_btn = UIBase(Vector2(position.x + 205, position.y + size.y - 60), Vector2(185, 50),
                                    color=ColorHelper.YELLOW)
        temp_ui_text1 = UIText("help1",
                               Vector2(200, 230), Vector2(300, 30), font_size=20, color=ColorHelper.BLACK)

        inventory_container = ScrollableContainer(Vector2(position.x + 10, position.y + 10), Vector2(380, 170))
        temp_container1 = ScrollableContainer(Vector2(position.x + 10, position.y + 10), Vector2(380, 170))
        temp_container1.color = ColorHelper.GREEN[:3]
        temp_container1.children_margin = Vector2(10, 10)

        # temp_container1.add_child(temp_ui_text1)
        temp_container1.add_child(someone_invent_btn)

        self.children.append(my_invent_btn)
        self.children.append(temp_ui_text1)
        self.children.append(someone_invent_btn)
        self.children.append(temp_container1)

        # main_window.children.append(my_invent_btn)

    def update_logic(self, **kwargs):
        super().update_logic()
        for ui_element in self.children:
            if isinstance(ui_element, ScrollableContainer):
                ui_element.update_logic()
            else:
                ui_element.draw()
