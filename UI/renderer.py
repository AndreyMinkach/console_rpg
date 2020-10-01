from pyglet.graphics import Batch, OrderedGroup
from pyglet.sprite import Sprite


class Renderer:
    instance: 'Renderer' = None

    def __init__(self):
        self.__class__.instance = self
        self._main_batch = Batch()
        self._main_group = OrderedGroup(0)
        self._ui_object_list = []
        self._ui_that_use_scissor_list = []  # stores ui objects that use scissor buffer and must be updated in draw method

    def get_batch(self) -> Batch:
        return self._main_batch

    def get_main_group(self) -> OrderedGroup:
        return self._main_group

    def draw(self):
        self._main_batch.draw()
        [i.update_logic() for i in self._ui_that_use_scissor_list if i is not None]

    def add_ui_object(self, ui_object: Sprite):
        self._ui_object_list.append(ui_object)

    def remove_ui_object(self, ui_object: Sprite):
        self._ui_object_list.remove(ui_object)

    def add_ui_object_scissor(self, ui_object: Sprite):
        self._ui_that_use_scissor_list.append(ui_object)

    def remove_ui_object_scissor(self, ui_object: Sprite):
        self._ui_that_use_scissor_list.remove(ui_object)

    def update_logic(self):
        [i.update_logic() for i in self._ui_object_list if i is not None]
