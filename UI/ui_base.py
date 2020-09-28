import pyglet
from pyglet.sprite import Sprite

from Helpers.color_helper import ColorHelper
from Helpers.location_helper import Vector2


class UIBase(Sprite):
    def __init__(self, position: Vector2, size: Vector2):
        image = pyglet.image.SolidColorImagePattern(ColorHelper.WHITE).create_image(size.x, size.y)
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

    def render(self):
        if self.enabled:
            for child in self.children:
                if isinstance(child, UIBase):
                    self.blit(child, (child.position.x, child.position.y))
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
