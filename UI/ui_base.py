from typing import List

import pyglet
from pyglet.graphics import Batch, OrderedGroup
from pyglet.image import AbstractImage
from pyglet.sprite import Sprite

from Animation.number_field_animation import NumberFieldAnimation
from Animation.storyboard import Storyboard
from Helpers.color_helper import ColorHelper
from Helpers.hit_test import HitTest
from Helpers.location_helper import Vector2
from UI.renderer import Renderer


class UIBase(Sprite):
    def __init__(self, position: Vector2, size: Vector2, texture: AbstractImage = None, transparent=False,
                 image_fill_color=ColorHelper.WHITE,
                 tint_color: (int, int, int) = ColorHelper.WHITE[:3]):
        if texture is None:
            texture = pyglet.image.SolidColorImagePattern(image_fill_color).create_image(1, 1)

        super().__init__(Renderer.add_texture(texture), x=position.x, y=position.y,
                         batch=Renderer.get_main_batch(),
                         group=Renderer.get_main_group())

        self.scale_x = size.x
        self.scale_y = size.y
        self.color = tint_color
        self._enabled = True
        self._current_batch = self.batch
        self.children: List[UIBase] = []
        self.children_batch = Batch()
        self.children_group = OrderedGroup(self.group.order + 1)
        self._position = position
        self._size = size
        self.custom_data = None  # can contain some data to simplify data transfer between scripts
        self.parent = None
        self.opacity = 255 if not transparent else 0
        self._opacity = 255
        self._is_mouse_inside = False
        self._hit_test_color = HitTest.instance.get_random_color(self)
        Renderer.add_ui_object(self)

        # event handlers
        self.on_click_down = lambda *args: None
        self.on_click_up = lambda *args: None
        self.on_mouse_enter = lambda *args: None
        self.on_mouse_leave = lambda *args: None

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: Vector2):
        self._position = value
        self.x = value.x
        self.y = value.y
        pos_difference = value - self.position
        for i in self.children:
            i.position = i.position + pos_difference
        self._position = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value: Vector2):
        self.scale_x = value.x / float(self._size.x)
        self.scale_y = value.y / float(self._size.y)
        self._size = value

    def delete_children(self):
        for child in self.children:
            child.batch = None
            child.group = None
        self.children.clear()
        del self.children[:]

    @Sprite.batch.setter
    def batch(self, value: Batch):
        Sprite.batch.fset(self, value)
        self._current_batch = value
        self.set_enabled(self._enabled)

    @Sprite.group.setter
    def group(self, value: OrderedGroup):
        Sprite.group.fset(self, value)
        self.children_group = OrderedGroup(value.order + 1)
        for i in self.children:
            i.group = self.children_group

    def set_enabled(self, enable: bool):
        self._enabled = enable
        Sprite.batch.fset(self, self._current_batch if enable else None)
        for i in self.children:
            i.batch = self.children_batch if enable else None

    def get_enabled(self) -> bool:
        return self._enabled

    def add_child(self, child: 'UIBase'):
        child.parent = self
        child.batch = self.children_batch if child.get_enabled() else None
        child.group = self.children_group
        self.children.append(child)

    def remove_child(self, child: 'UIBase'):
        self._remove_child(child)

    def _remove_child(self, child: 'UIBase', only_detach: bool = False):
        child.parent = None
        child.batch = Renderer.get_main_batch()
        child.group = Renderer.get_main_group()
        if not only_detach:
            self.children.remove(child)

    def clear_children(self):
        for child in self.children:
            self._remove_child(child, True)
        self.children.clear()

    def update_logic(self, **kwargs):
        pass

    def is_point_inside(self, point: Vector2):
        lb_corner = self.position
        ru_corner = lb_corner + self.size
        return lb_corner.x <= point.x <= ru_corner.x and lb_corner.y <= point.y <= ru_corner.y

    def fade_in(self, duration: float):
        Storyboard.begin_animation(NumberFieldAnimation(self, 'opacity', 0, 255, duration))

    def fade_out(self, duration: float):
        Storyboard.begin_animation(NumberFieldAnimation(self, 'opacity', 0, 255, duration))
