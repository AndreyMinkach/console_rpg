from UI.ui_base import *


class Renderer:
    instance = None

    def __init__(self):
        self.__class__.instance = self
        self._ui_objects_list = []

    def add_ui_object(self, ui_object: UIBase):
        self._ui_objects_list.append(ui_object)

    def remove_ui_object(self, ui_object: UIBase):
        self._ui_objects_list.remove(ui_object)

    def update(self):
        for child in self._ui_objects_list:
            child.update_and_draw()
