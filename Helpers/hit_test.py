from random import randint

from pyglet.gl import *
from pyglet.graphics import Batch, Group
from pyglet.shapes import Rectangle, _ShapeGroup

from Helpers.input_helper import InputHelper


class HitTest:
    _instance: 'HitTest' = None
    _renderer_batch: Batch = None

    def __init__(self, window, renderer_batch: Batch):
        self.__class__._instance = self
        self.__class__._renderer_batch = renderer_batch
        self.window = window
        self._hit_test_batch: Batch = Batch()
        # the dictionary that contains an object's hash->object pairs
        self._hash_object_dict = {}
        # contains the pairs that represents which color have one or the other ui_object
        self._hash_color_dict = {}
        self._color_hash_dict = {}
        self._read_buffer = (GLubyte * 3)(0)
        self._current_ui_object = None

    @classmethod
    def _get_random_color(cls):
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        values = cls._instance._hash_color_dict.values()
        while color in values:
            color = (randint(0, 255), randint(0, 255), randint(0, 255))

        return color

    @classmethod
    def add_ui_object(cls, ui_object):
        color = cls._get_random_color()
        object_hash = hash(ui_object)
        cls._instance._hash_color_dict[object_hash] = color
        cls._instance._color_hash_dict[color] = object_hash
        rectangle = Rectangle(x=ui_object.position.x, y=ui_object.position.y, width=ui_object.size.x,
                              height=ui_object.size.y, batch=cls._instance._hit_test_batch, group=ui_object.group,
                              color=color)
        cls._instance._hash_object_dict[object_hash] = (rectangle, ui_object)

    @classmethod
    def remove_ui_object(cls, ui_object):
        object_hash = hash(ui_object)
        color = cls._instance._hash_color_dict[object_hash]
        del cls._instance._color_hash_dict[color]
        del cls._instance._hash_color_dict[object_hash]
        obj_tuple = cls._instance._hash_object_dict[object_hash]
        del cls._instance._hash_object_dict[object_hash]
        del obj_tuple

    @classmethod
    def update_batch(cls, ui_object):
        # note that this method will always delete the ui_object from the render process of HitTest
        # so as the result click or mouse events will be never handled on the ui_object
        object_tuple = cls._instance._hash_object_dict[hash(ui_object)]  # a tuple that contains rectangle and ui_object
        object_tuple[0]._batch = \
            None if object_tuple[1].batch is not cls._renderer_batch else cls._instance._hit_test_batch

    @classmethod
    def _set_rectangle_group(cls, rect: Rectangle, group: Group):
        rect._group = _ShapeGroup(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, group)
        if rect._batch is not None:
            rect._batch.migrate(rect._vertex_list, GL_TRIANGLES, rect._group, rect._batch)

    @classmethod
    def update_group(cls, ui_object):
        object_tuple = cls._instance._hash_object_dict[hash(ui_object)]  # a tuple that contains rectangle and ui_object
        cls._set_rectangle_group(object_tuple[0], object_tuple[1].group)

    @classmethod
    def update_position(cls, ui_object):
        object_tuple = cls._instance._hash_object_dict[hash(ui_object)]  # a tuple that contains rectangle and ui_object
        position = object_tuple[1].position.tuple()
        object_tuple[0].x, object_tuple[0].y = position

    @classmethod
    def update_size(cls, ui_object):
        object_tuple = cls._instance._hash_object_dict[hash(ui_object)]  # a tuple that contains rectangle and ui_object
        size = object_tuple[1].size.tuple()
        object_tuple[0].width, object_tuple[0].height = size

    @classmethod
    def draw(cls):
        cls._instance._hit_test_batch.invalidate()
        cls._instance._hit_test_batch.draw()

        mouse_pos = InputHelper.get_mouse_pos()
        glReadPixels(mouse_pos.x, mouse_pos.y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE, cls._instance._read_buffer)
        buffer_tuple = tuple(cls._instance._read_buffer)

        if buffer_tuple in cls._instance._color_hash_dict:
            ui_object_hash = cls._instance._color_hash_dict[buffer_tuple]
            ui_object = cls._instance._hash_object_dict[ui_object_hash][1]
            if cls._instance._current_ui_object != ui_object:
                if ui_object.get_enabled() is True:
                    ui_object.on_mouse_enter(ui_object)
                if cls._instance._current_ui_object is not None:
                    if cls._instance._current_ui_object.get_enabled() is True:
                        cls._instance._current_ui_object.on_mouse_leave(cls._instance._current_ui_object)
                cls._instance._current_ui_object = ui_object
        else:
            if cls._instance._current_ui_object is not None:
                if cls._instance._current_ui_object.get_enabled() is True:
                    cls._instance._current_ui_object.on_mouse_leave(cls._instance._current_ui_object)
                cls._instance._current_ui_object = None

        cls._instance.window.clear()

    @classmethod
    def update(cls):
        mouse_button_down = InputHelper.get_last_mouse_button_down()
        mouse_button_up = InputHelper.get_last_mouse_button_up()
        if cls._instance._current_ui_object is not None:
            if cls._instance._current_ui_object.get_enabled() is True:
                if mouse_button_down != -1:
                    cls._instance._current_ui_object.on_click_down(cls._instance._current_ui_object, mouse_button_down)
                if mouse_button_up != -1:
                    cls._instance._current_ui_object.on_click_up(cls._instance._current_ui_object, mouse_button_up)
