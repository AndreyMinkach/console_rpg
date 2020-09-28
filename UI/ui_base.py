import types

import pyglet
from pyglet.sprite import Sprite

from Helpers.location_helper import Vector2


class UIBase(Sprite):
    def __init__(self, position: Vector2, size: Vector2):
        image = pyglet.image.SolidColorImagePattern((255, 255, 255, 255)).create_image(size.x, size.y)
        image.height = size.x
        image.width = size.y
        super().__init__(image, x=position.x, y=position.y)
        self.enabled = True
        self.children = []
        self.parent = None
        self._opacity = 255
        self._is_mouse_inside = False

        # event handlers
        self.on_click_down = None
        self.on_click_up = None
        self.on_mouse_enter = None
        self.on_mouse_leave = None

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value: int):
        self._opacity = value
        self.set_alpha(value)

    def update(self):
        self.draw()
