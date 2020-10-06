from pyglet import font
from pyglet.font.ttf import TruetypeInfo
from typing import Tuple

from pyglet.graphics import Batch, Group, OrderedGroup
from pyglet.text import Label
from UI.ui_base import *


def load_font(path):
    p = TruetypeInfo(path)
    p.close()
    font.add_file(path)


load_font('Static/Fonts/DisposableDroidBB.ttf')


class UIText(UIBase):
    def __init__(self, text: str, position: Vector2, size: Vector2, font_size: int,
                 color: Tuple[int, int, int, int] = ColorHelper.GREEN, anchor_x: str = 'left'):
        size.y = max(1, size.y)
        super().__init__(position, size, transparent=True)

        self.my_label = Label(text, font_name='DisposableDroid BB', font_size=font_size, color=color, x=position.x,
                              y=position.y, width=size.x, height=1, multiline=True, anchor_x=anchor_x,
                              anchor_y='bottom', batch=self.batch, group=OrderedGroup(self.group.order + 2))
        self.my_label.content_valign = 'center'
        self.size.y = self.my_label.content_height
        self.my_label.height = self.my_label.content_height

    def set_text(self, text: str):
        self.my_label.text = text
        self.size.y = self.my_label.content_height
        self.my_label.height = self.my_label.content_height

    @UIBase.batch.setter
    def batch(self, value: Batch):
        UIBase.batch.fset(self, value)
        self.my_label.batch = value

    @UIBase.group.setter
    def group(self, value: Group):
        UIBase.group.fset(self, value)
        self.my_label.group = value

    @UIBase.position.setter
    def position(self, value: Vector2):
        UIBase.position.fset(self, value)
        self.my_label.x = value.x
        self.my_label.y = value.y

    def update_logic(self, **kwargs):
        super().update_logic()
        self.my_label.draw()
