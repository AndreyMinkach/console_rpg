from Helpers.location_helper import Vector2


def _get_last_list_element(some_list):
    return some_list[len(some_list) - 1] if len(some_list) != 0 else -1


class InputHelper:
    _instance: 'InputHelper' = None

    def __init__(self, window):
        self.__class__._instance = self
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
                             self.on_mouse_scroll, self.on_mouse_motion, self.on_mouse_drag)

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

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self._mouse_pos = Vector2(x, y)
        self._mouse_pos_delta = Vector2(dx, dy)
        # print(x, y)

    @classmethod
    def get_mouse_scroll(cls) -> int:
        return cls._instance._mouse_scroll

    @classmethod
    def is_key_pressed(cls, key) -> bool:
        return key in cls._instance._keys_pressed

    @classmethod
    def is_key_down(cls, key) -> bool:
        return key in cls._instance._keys_down

    @classmethod
    def is_key_up(cls, key) -> bool:
        return key in cls._instance._keys_up

    @classmethod
    def is_mouse_pressed(cls, button) -> bool:
        return button in cls._instance._mouse_pressed_buttons

    @classmethod
    def is_mouse_down(cls, button) -> bool:
        return button in cls._instance._mouse_down_buttons

    @classmethod
    def is_mouse_up(cls, button) -> bool:
        return button in cls._instance._mouse_up_buttons

    @classmethod
    def get_last_mouse_pressed_button(cls):
        return _get_last_list_element(cls._instance._mouse_pressed_buttons)

    @classmethod
    def get_last_mouse_button_down(cls):
        return _get_last_list_element(cls._instance._mouse_down_buttons)

    @classmethod
    def get_last_mouse_button_up(cls):
        return _get_last_list_element(cls._instance._mouse_up_buttons)

    @classmethod
    def get_last_pressed_key(cls):
        return _get_last_list_element(cls._instance._keys_pressed)

    @classmethod
    def get_mouse_pos(cls) -> Vector2:
        return cls._instance._mouse_pos

    @classmethod
    def get_mouse_pos_delta(cls) -> Vector2:
        return cls._instance._mouse_pos_delta

    @classmethod
    def update(cls):
        # if self._key_down_ticks != self.window.total_ticks:
        cls._instance._keys_down.clear()
        # if self._key_up_ticks != self.window.total_ticks:
        cls._instance._keys_up.clear()

        # if self._mouse_down_ticks != self.window.total_ticks:
        cls._instance._mouse_down_buttons.clear()
        # if self._mouse_up_ticks != self.window.total_ticks:
        cls._instance._mouse_up_buttons.clear()
        if cls._instance._scroll_ticks != cls._instance.window.total_ticks:
            cls._instance._mouse_scroll = 0.0

        cls._instance._mouse_pos_delta = Vector2.zero
