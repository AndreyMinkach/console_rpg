import types

import pyglet
from pyglet.sprite import Sprite

from Animation.number_field_animation import NumberFieldAnimation
from Animation.storyboard import Storyboard
from Helpers.color_helper import ColorHelper
from Helpers.location_helper import Vector2


class UIBase(Sprite):
    def __init__(self, position: Vector2, size: Vector2, transparent=False, color=ColorHelper.WHITE):
        image = pyglet.image.SolidColorImagePattern(
            color if not transparent else ColorHelper.TRANSPARENT).create_image(size.x, size.y)
        super().__init__(image, x=position.x, y=position.y)
        self.enabled = True
        self.children = []
        self.children.append(self)
        self._position = position
        self._size = size
        self.parent = None
        self._is_mouse_inside = False

        # event handlers
        self.on_click_down = None
        self.on_click_up = None
        self.on_mouse_enter = None
        self.on_mouse_leave = None

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: Vector2):
        self._position = value
        self.x = value.x
        self.y = value.y

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value: Vector2):
        self._size = value
        # TODO: Implement object scaling

    def update_and_draw(self, **kwargs):
        if self.enabled:
            for child in self.children:
                if isinstance(child, UIBase):
                    child.draw()
            self.draw()

            # update mouse events
            # mouse_pos = InputHelper.instance.mouse_position
            # if self.on_mouse_enter is not None and isinstance(self.on_mouse_enter, types.LambdaType):
            #     if not self._is_mouse_inside and self.is_point_inside(mouse_pos):
            #         self._is_mouse_inside = True
            #         self.on_mouse_enter(self)
            #
            # if self.on_mouse_leave is not None and isinstance(self.on_mouse_leave, types.LambdaType):
            #     if self._is_mouse_inside and not self.is_point_inside(mouse_pos):
            #         self._is_mouse_inside = False
            #         self.on_mouse_leave(self)
            #
            # self.update_click_event(self.on_click_down, pygame.MOUSEBUTTONDOWN, mouse_pos)
            # self.update_click_event(self.on_click_up, pygame.MOUSEBUTTONUP, mouse_pos)

    def is_point_inside(self, point: Vector2):
        lb_corner = self.position if self.parent is None else self.position - self.parent.position
        ru_corner = lb_corner + self.size
        return lb_corner.x <= point.x <= ru_corner.x and lb_corner.y <= point.y <= ru_corner.y

    def fade_in(self, duration: float):
        Storyboard.instance.begin_animation(NumberFieldAnimation(self, 'opacity', 0, 255, duration))

    def fade_out(self, duration: float):
        Storyboard.instance.begin_animation(NumberFieldAnimation(self, 'opacity', 0, 255, duration))
