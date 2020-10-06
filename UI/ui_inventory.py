from pyglet.graphics import OrderedGroup

from UI.ui_base import *

from Gameplay.inventory import Inventory
from Helpers.color_helper import ColorHelper
from Items.items_loader import ItemLoader
from UI.ui_base import UIBase
from UI.ui_button import UIButton
from UI.ui_scrollable_container import ScrollableContainer
from UI.ui_sprite import UISprite
from UI.ui_text import UIText


class UIInventory(UIBase):
    def __init__(self, position: Vector2, size: Vector2, other_inventory: Inventory = None):
        super().__init__(position, size)

        all_items = ItemLoader()
        hero_invent = Inventory()
        self._child_group = OrderedGroup(self.group.order + 0.2)

        weapon1 = all_items.get_item_by_id(1)
        outfit1 = all_items.get_item_by_id(50)
        weapon2 = all_items.get_item_by_id(2)
        outfit2 = all_items.get_item_by_id(51)

        hero_invent.add_item(weapon1)
        hero_invent.add_item(outfit1)
        hero_invent.add_item(weapon2)
        hero_invent.add_item(outfit2)

        self.button_size = Vector2(185, 50)
        indent = 10
        sc_cnt_high_other_invent = 170
        sc_cnt_high_no_other_invent = 230
        self.item_list_container = ScrollableContainer(Vector2(position.x + indent, position.y + 2 * indent),
                                                       Vector2(size.x - indent * 2, sc_cnt_high_no_other_invent))
        self.item_list_container.group = self._child_group
        self.item_list_container.color = ColorHelper.GREEN[:3]
        self.item_list_container.children_margin = Vector2(5, 5)
        self.item_list_container.scale_y = 1

        if other_inventory:
            self.item_list_container.position = Vector2(self.item_list_container.position.x,
                                                        self.item_list_container.position.y + self.button_size.y)

            self.item_list_container.scale_y = sc_cnt_high_other_invent / sc_cnt_high_no_other_invent
            self.item_list_container.size.y = sc_cnt_high_no_other_invent * self.item_list_container.scale_y
            button_click_color = (125, 125, 125, 180)
            self.my_inv_button = UIButton("My inventory", Vector2(position.x + indent, position.y + indent),
                                          Vector2(self.button_size.x, self.button_size.y), font_size=20,
                                          color=ColorHelper.GRAY, hover_color=button_click_color,
                                          document_style=dict(align='center'))
            self.other_inv_button = UIButton("Someone\ninventory",
                                             Vector2(position.x + size.x - indent - self.button_size.x,
                                                     position.y + indent), self.button_size, font_size=20,
                                             color=ColorHelper.GRAY, hover_color=button_click_color,
                                             document_style=dict(align='center'))

            self.other_inv_button.group = self._child_group
            self.other_inv_button.custom_data = other_inventory
            self.my_inv_button.group = self._child_group
            self.my_inv_button.custom_data = hero_invent

            self.other_inv_button.on_click_up = lambda o, b: self.choose_inventory(o, self.item_list_container)
            self.my_inv_button.on_click_up = lambda o, b: self.choose_inventory(o, self.item_list_container)

        self.chosen_invent = hero_invent

        sprite_pos = [Vector2(13, 1), Vector2(11, 7), Vector2(4, 1), Vector2(3, 9), Vector2(5, 5)]
        item_type_name = ['Weapon', "Outfit", "Heal", "Food", "Ore"]
        sprite_size = Vector2(32, 32)
        step = 80
        for i in range(len(sprite_pos)):
            weapon_type_sprite = UISprite("inventory_sprite_sheet.png",
                                          Vector2(position.x + indent * 2 + i * step, position.y + size.y - 50),
                                          sprite_size, sprite_pos[i].x, sprite_pos[i].y, 1, sprite_size, 20, 16, 1.25)
            weapon_type_sprite.custom_data = i
            weapon_type_sprite.group = self._child_group

            weapon_type_sprite.on_click_down = lambda o, b: \
                self.show_items_by_type(item_type_name[o.custom_data], self.chosen_invent,
                                        self.item_list_container)

    def choose_inventory(self, o, item_list_container):
        item_list_container.delete_children()
        self.chosen_invent = o.custom_data

    def show_items_by_type(self, items_type: str, invent, item_list_container):
        item_list_container.delete_children()
        indent = 10
        one_line_high = 22
        for item in invent.get_item_list_by_type(items_type):
            item_text = UIText(item.name, Vector2.zero, Vector2(item_list_container.size.x - indent, one_line_high),
                               font_size=20, color=ColorHelper.GRAY, document_style=dict(color=ColorHelper.BLACK))
            item_list_container.add_child(item_text)
        item_list_container.group = self._child_group

    def update_logic(self, **kwargs):
        super().update_logic()
        # for ui_element in self.children:
        #     if isinstance(ui_element, ScrollableContainer):
        #         ui_element.update_logic()
        #     else:
        #         ui_element.draw()
