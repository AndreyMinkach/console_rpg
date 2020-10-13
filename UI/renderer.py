from pyglet.graphics import Batch, OrderedGroup
from pyglet.image import AbstractImage, TextureRegion
from pyglet.image.atlas import TextureBin
from pyglet.sprite import Sprite

from Helpers.hit_test import HitTest


class Renderer:
    _instance: 'Renderer' = None

    def __init__(self):
        self.__class__._instance = self
        self._main_batch = Batch()
        self._main_group = OrderedGroup(0)
        self._texture_atlas = TextureBin()
        self._ui_object_list = []
        self._ui_that_use_scissor_list = []  # stores ui objects that use scissor buffer and must be updated in draw method

    @classmethod
    def get_main_batch(cls) -> Batch:
        return cls._instance._main_batch

    @classmethod
    def get_main_group(cls) -> OrderedGroup:
        return cls._instance._main_group

    @classmethod
    def add_texture(cls, texture: AbstractImage, border: int = 0) -> TextureRegion:
        return cls._instance._texture_atlas.add(texture, border)

    @classmethod
    def draw(cls):
        HitTest.instance.draw()
        cls._instance._main_batch.draw()
        [i.update_logic() for i in cls._instance._ui_that_use_scissor_list if i is not None]

    @classmethod
    def add_ui_object(cls, ui_object: Sprite):
        cls._instance._ui_object_list.append(ui_object)

    @classmethod
    def remove_ui_object(cls, ui_object: Sprite):
        cls._instance._ui_object_list.remove(ui_object)

    @classmethod
    def add_ui_object_scissor(cls, ui_object: Sprite):
        cls._instance._ui_that_use_scissor_list.append(ui_object)

    @classmethod
    def remove_ui_object_scissor(cls, ui_object: Sprite):
        cls._instance._ui_that_use_scissor_list.remove(ui_object)

    @classmethod
    def update_logic(cls):
        HitTest.instance.update()
        [i.update_logic() for i in cls._instance._ui_object_list if i is not None]
