from pyglet import font
from pyglet.font.ttf import TruetypeInfo
from typing import Tuple
from pyglet.text import Label
from UI.ui_base import *


def load_font(path):
    p = TruetypeInfo(path)
    p.close()
    font.add_file(path)
    # print("Loaded font " + p.get_name("name") + " from " + path)


class UIText(UIBase):
    def __init__(self, text: str, position: Vector2, size: Vector2, font_size: int,
                 color: Tuple[int, int, int, int] = ColorHelper.GREEN):
        super().__init__(position, size, transparent=True)
        load_font('Static/Fonts/DisposableDroidBB.ttf')
        self.text = Label(text, font_name='DisposableDroid BB', font_size=font_size, color=color, x=position.x,
                          y=position.y, width=size.x, height=size.y, multiline=True)

    def update_and_draw(self, **kwargs):
        super().update_and_draw()
        self.text.draw()
