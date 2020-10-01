import time

from Helpers.location_helper import Vector2


def _get_last_list_element(some_list):
    return some_list[len(some_list) - 1] if len(some_list) != 0 else -1


class InputHelper:
    instance: 'InputHelper' = None

    def __init__(self, window):
        self.__class__.instance = self
        self.window = window
        self._keys_pressed = []
        self._keys_down = []
        self._key_down_ticks = 0
        self._keys_up = []
        self._key_up_ticks = 0
        self._mouse_pressed_buttons = []
        self._mouse_down_buttons = []
        self._mouse_down_ticks = 0
        self._mouse_up_buttons = []
        self._mouse_up_ticks = 0
        self._mouse_scroll = 0
        self._mouse_pos = Vector2.zero
        self._mouse_pos_delta = Vector2.zero
        self._scroll_ticks = 0

        window.push_handlers(self.on_key_press, self.on_key_release, self.on_mouse_press, self.on_mouse_release,
                             self.on_mouse_scroll, self.on_mouse_motion)

    def on_key_press(self, symbol, modifiers):
        self._keys_pressed.append(symbol)
        self._keys_down.append(symbol)
        self._key_down_ticks = self.window.total_ticks

    def on_key_release(self, symbol, modifiers):
        if symbol in self._keys_pressed:
            self._keys_pressed.remove(symbol)
        self._keys_up.append(symbol)
        self._key_up_ticks = self.window.total_ticks

    def on_mouse_press(self, x, y, button, modifiers):
        self._mouse_pressed_buttons.append(button)
        self._mouse_down_buttons.append(button)
        self._mouse_down_ticks = self.window.total_ticks

    def on_mouse_release(self, x, y, button, modifiers):
        if button in self._mouse_pressed_buttons:
            self._mouse_pressed_buttons.remove(button)
        self._mouse_up_buttons.append(button)
        self._mouse_up_ticks = self.window.total_ticks

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self._scroll_ticks = self.window.total_ticks
        self._mouse_scroll = scroll_y

    def on_mouse_motion(self, x, y, dx, dy):
        self._mouse_pos = Vector2(x, y)
        self._mouse_pos_delta = Vector2(dx, dy)

    def get_mouse_scroll(self):
        return self._mouse_scroll

    def is_key_pressed(self, key):
        return key in self._keys_pressed

    def is_key_down(self, key):
        return key in self._keys_down

    def is_key_up(self, key):
        return key in self._keys_up

    def is_mouse_pressed(self, button):
        return button in self._mouse_pressed_buttons

    def is_mouse_down(self, button):
        return button in self._mouse_down_buttons

    def is_mouse_up(self, button):
        return button in self._mouse_up_buttons

    def get_last_mouse_pressed_button(self):
        return _get_last_list_element(self._mouse_pressed_buttons)

    def get_last_mouse_button_down(self):
        return _get_last_list_element(self._mouse_down_buttons)

    def get_last_mouse_button_up(self):
        return _get_last_list_element(self._mouse_up_buttons)

    def get_last_pressed_key(self):
        return _get_last_list_element(self._keys_pressed)

    def get_mouse_pos(self):
        return self._mouse_pos

    def get_mouse_pos_delta(self):
        return self._mouse_pos_delta

    def update(self):
        # if self._key_down_ticks != self.window.total_ticks:
        self._keys_down.clear()
        # if self._key_up_ticks != self.window.total_ticks:
        self._keys_up.clear()

        # if self._mouse_down_ticks != self.window.total_ticks:
        self._mouse_down_buttons.clear()
        # if self._mouse_up_ticks != self.window.total_ticks:
        self._mouse_up_buttons.clear()
        if self._scroll_ticks != self.window.total_ticks:
            self._mouse_scroll = 0.0

        self._mouse_pos_delta = Vector2.zero
