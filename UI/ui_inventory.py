import pygame
from pygame import Vector2
from UI.ui_base import *

from Gameplay.inventory import Inventory
from Helpers.color_helper import ColorHelper
from Items.items_loader import ItemLoader
from UI.ui_base import UIBase
from UI.ui_text import UIText


class UIInventory(UIBase):
    def __init__(self, position: Vector2, size: Vector2):
        super().__init__(position, size)

        my_invent_btn = UIBase(Vector2(10, 10), Vector2(185, 50))
        my_invent_btn.fill(ColorHelper.YELLOW)

        someone_invent_btn = UIBase(Vector2(205, 10), Vector2(185, 50))
        someone_invent_btn.fill(ColorHelper.YELLOW)

        q = UIBase(Vector2(100, 100), Vector2(100, 100))
        q.fill(ColorHelper.YELLOW)

        temp_text = UIText(Vector2(600, 100), Vector2(100, 10), "Hello")
        font_obj = pygame.font.Font(None, 30)

        print(font_obj)

        self.children.append(font_obj.render("asasdadasdadsd", 1, ColorHelper.YELLOW))
        self.children.append(temp_text)

        # main_window.children.append(my_invent_btn)
        #

    def update(self, display_canvas: UIBase):
        for ui_element in self.children:
            print(ui_element)
            self.blit(ui_element, (10, 10))
        display_canvas.blit(self, (self.position.x, self.position.y))
