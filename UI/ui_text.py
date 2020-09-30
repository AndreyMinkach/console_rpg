import time

from pyglet import font
from pyglet.font.ttf import TruetypeInfo
from typing import Tuple

from pyglet.text import Label

from Helpers.color_helper import ColorHelper
from UI.ui_base import *
from itertools import chain


def load_font(path):
    # load external font from file
    p = TruetypeInfo(path)
    name = p.get_name("name")
    p.close()
    font.add_file(path)
    # print("Loaded font " + name + " from " + path)


class UIText(UIBase):
    def __init__(self, text: str, position: Vector2, size: Vector2, font_size: int,
                 color: Tuple[int, int, int, int] = ColorHelper.GREEN):
        super().__init__(position, size, transparent=True)
        load_font('Static/Fonts/DisposableDroidBB.ttf')
        self.text = Label(text, font_name='DisposableDroid BB', font_size=font_size, color=color, x=position.x,
                          y=position.y, width=size.x, height=size.y, multiline=True)

    def update_and_draw(self, **kwargs):
        self.text.draw()
