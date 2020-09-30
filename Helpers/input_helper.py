import time

from Helpers.location_helper import Vector2


class InputHelper:
    instance = None

    def __init__(self, window):
        self.__class__.instance = self
        self.window = window
        self._keys = []
        self._mouse_keys = []
        self._mouse_scroll = 0
        self._mouse_pos = Vector2.zero
        self._mouse_pos_delta = Vector2.zero
        self._mouse_event_frame_number = 0

        window.push_handlers(self.on_key_press, self.on_key_release, self.on_mouse_press, self.on_mouse_release,
                             self.on_mouse_scroll, self.on_mouse_motion)

    def on_key_press(self, symbol, modifiers):
        self._add_key(symbol)

    def on_key_release(self, symbol, modifiers):
        self._remove_key(symbol)

    def on_mouse_press(self, x, y, button, modifiers):
        self._add_mouse_button(button)

    def on_mouse_release(self, x, y, button, modifiers):
        self._remove_mouse_button(button)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self._mouse_event_frame_number = self.window.total_frame_count
        self._set_mouse_scroll(scroll_y)

    def on_mouse_motion(self, x, y, dx, dy):
        self._mouse_pos = Vector2(x, y)
        self._mouse_pos_delta = Vector2(dx, dy)

    def _add_key(self, key):
        self._keys.append(key)

    def _remove_key(self, key):
        if key in self._keys:
            self._keys.remove(key)

    def _add_mouse_button(self, key):
        self._mouse_keys.append(key)

    def _remove_mouse_button(self, key):
        if key in self._mouse_keys:
            self._mouse_keys.remove(key)

    def _set_mouse_scroll(self, value):
        self._mouse_scroll = value

    def _set_mouse_pos(self, x: int, y: int):
        self._mouse_pos = Vector2(x, y)

    def get_mouse_scroll(self):
        return self._mouse_scroll

    def is_key_pressed(self, key):
        return key in self._keys

    def is_mouse_pressed(self, button):
        return button in self._mouse_keys

    def get_mouse_pos(self):
        return self._mouse_pos

    def get_mouse_pos_delta(self):
        return self._mouse_pos_delta

    def update(self):
        if self._mouse_event_frame_number != self.window.total_frame_count:
            self._mouse_scroll = 0.0

        self._mouse_pos_delta = Vector2.zero
