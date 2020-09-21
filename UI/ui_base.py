import types

import pygame
from pygame import Surface

from Animation.number_field_animation import NumberFieldAnimation
from Animation.storyboard import Storyboard
from Helpers.input_helper import InputHelper
from Helpers.location_helper import Vector2


class UIBase(Surface):
    def __init__(self, position: Vector2, size: Vector2):
        super().__init__((size.x, size.y))
        self.position = position
        self.size = size
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

    def update(self, display_canvas: Surface):
        """
        Updates the calling abject and all its children
        :param display_canvas:
        :return:
        """
        if self.enabled:
            for child in self.children:
                if child is UIBase:
                    self.blit(child, (child.position.x, child.position.y))
            display_canvas.blit(self, (self.position.x, self.position.y))

            # update mouse events
            mouse_pos = InputHelper.instance.mouse_position
            if self.on_mouse_enter is not None and isinstance(self.on_mouse_enter, types.LambdaType):
                if not self._is_mouse_inside and self.is_point_inside(mouse_pos):
                    self._is_mouse_inside = True
                    self.on_mouse_enter(self)

            if self.on_mouse_leave is not None and isinstance(self.on_mouse_leave, types.LambdaType):
                if self._is_mouse_inside and not self.is_point_inside(mouse_pos):
                    self._is_mouse_inside = False
                    self.on_mouse_leave(self)

            self.update_click_event(self.on_click_down, pygame.MOUSEBUTTONDOWN)
            self.update_click_event(self.on_click_up, pygame.MOUSEBUTTONUP)

    def update_click_event(self, click_lambda, click_type):
        if click_lambda is not None and isinstance(click_lambda, types.LambdaType):
            button = InputHelper.instance.current_mouse_button
            current_click_type = InputHelper.instance.current_click_type
            if button != -1 and current_click_type == click_type:
                click_lambda(self, button)

    def is_point_inside(self, point: Vector2):
        lu_corner = self.position if self.parent is None else self.position - self.parent.position
        rb_corner = lu_corner + self.size
        return lu_corner.x <= point.x <= rb_corner.x and lu_corner.y <= point.y <= rb_corner.y

    def fade_in(self, duration: float):
        Storyboard.instance.begin_animation(NumberFieldAnimation(self, 'opacity', 0, 255, duration))

    def fade_out(self, duration: float):
        Storyboard.instance.begin_animation(NumberFieldAnimation(self, 'opacity', 0, 255, duration))
