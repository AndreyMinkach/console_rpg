from random import randint
from pyglet.gl import *
from Helpers.input_helper import InputHelper


class HitTest:
    instance: 'HitTest' = None

    def __init__(self, window):
        self.__class__.instance = self
        self.window = window
        # contains the pairs that represents which color have one or the other ui_object
        self._color_object_dict = {}
        self._rectangle: pyglet.shapes.Rectangle = pyglet.shapes.Rectangle(0, 0, 1, 1)
        self._ui_object_list_sorted = []
        self._read_buffer = (GLubyte * 3)(0)
        self._current_ui_object = None

    def get_random_color(self, ui_object):
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        values = self._color_object_dict.keys()
        while color in values:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))

        self._color_object_dict[color] = ui_object
        return color

    def add_ui_object(self, color: (int, int, int), ui_object):
        self._color_object_dict[color] = ui_object
        self._ui_object_list_sorted = sorted(self._color_object_dict.values(), key=lambda o: o.group.order)

    def remove_ui_object(self, color: (int, int, int)):
        del self._color_object_dict[color]

    def insert_ui_object(self, ui_object):
        values = list(self._color_object_dict.values())
        insert_index = -1
        for i in range(len(values)):
            if values[i].group.order > ui_object.group.order:
                insert_index = i
                break
        if insert_index == -1:
            values.append(ui_object)
        else:
            values.insert(insert_index, ui_object)
        self._ui_object_list_sorted = values

    def draw_ui_object(self, ui_object):
        self._rectangle.x, self._rectangle.y = ui_object.position.tuple()
        self._rectangle.width, self._rectangle.height = ui_object.size.tuple()
        self._rectangle.color = ui_object._hit_test_color
        self._rectangle.draw()

    def _draw_container(self, ui_object):
        ui_object._enable_scissor_test()
        self.draw_ui_object(ui_object)
        for child in ui_object.children:
            if child.__class__.__name__ == 'ScrollableContainer':
                self._draw_container(child)
            else:
                self.draw_ui_object(child)
        ui_object._disable_scissor_test()

    def draw(self):
        for ui_object in self._ui_object_list_sorted:
            if ui_object.parent is not None:
                continue
            if ui_object.__class__.__name__ == 'ScrollableContainer':
                self._draw_container(ui_object)
            else:
                self.draw_ui_object(ui_object)

        mouse_pos = InputHelper.get_mouse_pos()
        glReadPixels(mouse_pos.x, mouse_pos.y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE, self._read_buffer)
        buffer_tuple = tuple(self._read_buffer)

        if buffer_tuple in self._color_object_dict:
            ui_object = self._color_object_dict[buffer_tuple]
            if self._current_ui_object != ui_object:
                ui_object.on_mouse_enter(ui_object)
                if self._current_ui_object is not None:
                    self._current_ui_object.on_mouse_leave(self._current_ui_object)
                self._current_ui_object = ui_object
        else:
            if self._current_ui_object is not None:
                self._current_ui_object.on_mouse_leave(self._current_ui_object)
                self._current_ui_object = None

        self.window.clear()

    def update(self):
        mouse_button_down = InputHelper.get_last_mouse_button_down()
        mouse_button_up = InputHelper.get_last_mouse_button_up()
        if self._current_ui_object is not None:
            if mouse_button_down != -1:
                self._current_ui_object.on_click_down(self._current_ui_object, mouse_button_down)
            if mouse_button_up != -1:
                self._current_ui_object.on_click_up(self._current_ui_object, mouse_button_up)
