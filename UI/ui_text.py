from pyglet import font
from pyglet.font.ttf import TruetypeInfo
from typing import Tuple
from pyglet.text import Label
from UI.ui_base import *


def load_font(path):
    p = TruetypeInfo(path)
    p.close()
    font.add_file(path)


load_font('Static/Fonts/DisposableDroidBB.ttf')


class UIText(UIBase):
    def __init__(self, text: str, position: Vector2, size: Vector2, font_size: int,
                 color: Tuple[int, int, int, int] = ColorHelper.GREEN):
        super().__init__(position, size, transparent=True)
        self.text = Label(text, font_name='DisposableDroid BB', font_size=font_size, color=color, x=position.x,
                          y=position.y, width=size.x, height=size.y, multiline=True)

    def update_logic(self, **kwargs):
        super().update_logic()
        self.text.draw()
