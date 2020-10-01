import types

import pyglet
from pyglet.sprite import Sprite

from Animation.number_field_animation import NumberFieldAnimation
from Animation.storyboard import Storyboard
from Helpers.color_helper import ColorHelper
from Helpers.input_helper import InputHelper
from Helpers.location_helper import Vector2
from UI.renderer import Renderer


class UIBase(Sprite):
    def __init__(self, position: Vector2, size: Vector2, transparent=False, color=ColorHelper.WHITE):
        image = pyglet.image.SolidColorImagePattern(
            color if not transparent else ColorHelper.TRANSPARENT).create_image(size.x, size.y)
        super().__init__(image, x=position.x, y=position.y, batch=Renderer.instance.get_batch(),
                         group=Renderer.instance.get_main_group())

        self.enabled = True
        self.children = []
        self.children.append(self)
        self._position = position
        self._size = size
        self.parent = None
        self._opacity = 255
        self._is_mouse_inside = False
        Renderer.instance.add_ui_object(self)

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

    def update_logic(self, **kwargs):
        if self.enabled:
            # for child in self.children:
            #     if isinstance(child, UIBase):
            #         child.draw()
            # self.draw()

            # update mouse events
            mouse_pos = InputHelper.instance.get_mouse_pos()
            if self.on_mouse_enter is not None and isinstance(self.on_mouse_enter, types.LambdaType):
                if not self._is_mouse_inside and self.is_point_inside(mouse_pos):
                    self._is_mouse_inside = True
                    self.on_mouse_enter(self)

            if self.on_mouse_leave is not None and isinstance(self.on_mouse_leave, types.LambdaType):
                if self._is_mouse_inside and not self.is_point_inside(mouse_pos):
                    self._is_mouse_inside = False
                    self.on_mouse_leave(self)

            self._update_click_event(self.on_click_down, 1, mouse_pos)
            self._update_click_event(self.on_click_up, 0, mouse_pos)

    def _update_click_event(self, click_lambda, click_type: int, mouse_pos: Vector2):
        """
        :param click_lambda: lambda which is called when user clicks on ui object
        :param click_type: 1 - user pressed down mouse button, 0 - user releases mouse button
        :param mouse_pos: position of the cursor relative to the window
        """
        if click_lambda is not None and isinstance(click_lambda, types.LambdaType):
            button = InputHelper.instance.get_last_mouse_button_down() if click_type == 1\
                else InputHelper.instance.get_last_mouse_button_up() if click_type == 0 else -1
            if button != -1 and self.is_point_inside(mouse_pos):
                click_lambda(self, button)

    def is_point_inside(self, point: Vector2):
        lb_corner = self.position if self.parent is None else self.position - self.parent.position
        ru_corner = lb_corner + self.size
        return lb_corner.x <= point.x <= ru_corner.x and lb_corner.y <= point.y <= ru_corner.y

    def fade_in(self, duration: float):
        Storyboard.instance.begin_animation(NumberFieldAnimation(self, 'opacity', 0, 255, duration))

    def fade_out(self, duration: float):
        Storyboard.instance.begin_animation(NumberFieldAnimation(self, 'opacity', 0, 255, duration))
