from pyglet.graphics import OrderedGroup

from UI.ui_base import *

from Gameplay.inventory import Inventory
from Helpers.color_helper import ColorHelper
from Items.items_loader import ItemLoader
from UI.ui_base import UIBase
from UI.ui_scrollable_container import ScrollableContainer
from UI.ui_sprite import UISprite
from UI.ui_text import UIText


class UIInventory(UIBase):
    def __init__(self, position: Vector2, size: Vector2, enemy_invent: Inventory = None):
        super().__init__(position, size)

        all_items = ItemLoader()
        hero_invent = Inventory()
        self._child_group = OrderedGroup(self.group.order + 1)

        weapon1 = all_items.get_item_by_id(1)
        outfit1 = all_items.get_item_by_id(50)
        weapon2 = all_items.get_item_by_id(2)
        outfit2 = all_items.get_item_by_id(51)

        hero_invent.add_item(weapon1)
        hero_invent.add_item(outfit1)
        hero_invent.add_item(weapon2)
        hero_invent.add_item(outfit2)

        button_size = Vector2(185, 60)
        indent = 10
        container_y_size_with_enemy = 170
        container_y_size_without_enemy = 230
        item_list_container = ScrollableContainer(Vector2(position.x + 10, position.y + 10),
                                                  Vector2(size.x - 20, container_y_size_without_enemy))
        item_list_container.scale_y = 1
        if enemy_invent:
            item_list_container.position = Vector2(item_list_container.position.x,
                                                   item_list_container.position.y + button_size.y)

            item_list_container.scale_y = container_y_size_with_enemy / container_y_size_without_enemy
            item_list_container.size.y = container_y_size_without_enemy * item_list_container.scale_y

            my_inv_button = UIBase(Vector2(position.x + indent, position.y + indent),
                                   Vector2(button_size.x, button_size.y - indent),
                                   color=ColorHelper.GRAY)

            my_inv_text = UIText("My inventory", Vector2(position.x + 27, position.y + button_size.y + indent - 45),
                                 Vector2(button_size.x, button_size.y - indent), 20,
                                 ColorHelper.BLACK)

            enemy_inv_button = UIBase(
                Vector2(position.x + size.x - button_size.x - indent, position.y + indent),
                Vector2(button_size.x, button_size.y - indent),
                color=ColorHelper.GRAY)

            enemy_inv_text = UIText("Someone inventory",
                                    Vector2(position.x + size.x - 150, position.y + button_size.y + indent - 57),
                                    Vector2(button_size.x, button_size.y - indent), 20, ColorHelper.BLACK)

            enemy_inv_button.group = self._child_group
            enemy_inv_button.custom_data = enemy_invent
            my_inv_button.group = self._child_group
            my_inv_button.custom_data = hero_invent

            enemy_inv_button.on_click_up = lambda o, b: self.change_inventory(self.chosen_invent, o,
                                                                              item_list_container)
            my_inv_button.on_click_up = lambda o, b: self.change_inventory(self.chosen_invent, o, item_list_container)

        self.chosen_invent = hero_invent

        item_list_container.color = ColorHelper.GREEN[:3]
        item_list_container.children_margin = Vector2(5, 5)
        item_list_container.group = self._child_group

        choose_item_type_sprite_pos = [Vector2(13, 1), Vector2(11, 7), Vector2(4, 1), Vector2(3, 9), Vector2(5, 5)]
        choose_item_type_name = ['Weapon', "Outfit", "heal", "Food", "Ore"]

        for i in range(len(choose_item_type_sprite_pos)):
            weapon_type_choose_sprite = UISprite("inventory_sprite_sheet.png",
                                                 Vector2(position.x + indent * 2 + i * 80, position.y + size.y - 50),
                                                 Vector2(40, 40), choose_item_type_sprite_pos[i].x,
                                                 choose_item_type_sprite_pos[i].y, 1, Vector2(32, 32), 20, 16, 1.25)
            weapon_type_choose_sprite.custom_data = i
            weapon_type_choose_sprite.group = self._child_group

            weapon_type_choose_sprite.on_click_down = lambda o, b: \
                self.show_one_type_items_in_scroll_container(
                    choose_item_type_name[o.custom_data], self.chosen_invent, item_list_container)

    def change_inventory(self, chosen_invent, o, item_list_container):
        item_list_container.delete_children()
        self.chosen_invent = o.custom_data
        return chosen_invent

    def show_one_type_items_in_scroll_container(self, items_type: str, invent, item_list_container):
        item_list_container.delete_children()
        for item in invent.get_item_list_by_type(items_type):
            item_text = UIText(item.name, Vector2.zero,
                               Vector2(item_list_container.size.x - 5, 2), 20,
                               ColorHelper.BLACK)
            item_list_container.add_child(item_text)
            print(item.name)
        item_list_container.group = self._child_group

    def update_logic(self, **kwargs):
        super().update_logic()
        # for ui_element in self.children:
        #     if isinstance(ui_element, ScrollableContainer):
        #         ui_element.update_logic()
        #     else:
        #         ui_element.draw()
