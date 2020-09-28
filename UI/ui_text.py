import time
from typing import Tuple

from pyglet.text import Label

from Helpers.color_helper import ColorHelper
from UI.ui_base import *
from itertools import chain


class UIText(UIBase):
    def __init__(self, text: str, position: Vector2, size: Vector2,
                 color: Tuple[int, int, int, int] = (255, 255, 255, 255)):
        text = Label(text, color=color, x=position.x, y=position.y, width=size.x, height=size.y, multiline=True)
        self.children = []
        self.children.append(text)

    def update_and_draw(self):
        for c in self.children:
            c.draw()
