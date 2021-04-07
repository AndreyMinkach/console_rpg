import pyglet
from pyglet.gl import *
from pyglet.graphics import Batch, OrderedGroup
from pyglet.image import AbstractImage, TextureRegion
from pyglet.image.atlas import TextureBin
from pyglet.sprite import Sprite

from Helpers.hit_test import HitTest


class UIRenderer:
    _instance: 'UIRenderer' = None

    def __init__(self):
        self.__class__._instance = self
        self._window_size: (int, int) = (0, 0)
        self._main_batch = Batch()
        self._main_group = OrderedGroup(0)
        self._texture_atlas = TextureBin()
        self._ui_object_list = []

    @classmethod
    def get_window_size(cls) -> (int, int):
        return cls._instance._window_size

    @classmethod
    def set_window_size(cls, value: (int, int)):
        cls._instance._window_size = value

    @classmethod
    def get_main_batch(cls) -> Batch:
        return cls._instance._main_batch

    @classmethod
    def get_main_group(cls) -> OrderedGroup:
        return cls._instance._main_group

    @classmethod
    def add_texture(cls, texture: AbstractImage, border: int = 0) -> TextureRegion:
        texture_region = cls._instance._texture_atlas.add(texture, border)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return texture_region

    @classmethod
    def load_image(cls, image_path: str, folder: str = 'Static/Images/', border=0) -> TextureRegion:
        return cls.add_texture(pyglet.image.load(folder + image_path), border)

    @classmethod
    def draw(cls):
        # TODO: Rewrite HitTest
        # HitTest.draw()
        cls._instance._main_batch.invalidate()
        cls._instance._main_batch.draw()

    @classmethod
    def add_ui_object(cls, ui_object: Sprite):
        cls._instance._ui_object_list.append(ui_object)

    @classmethod
    def remove_ui_object(cls, ui_object: Sprite):
        cls._instance._ui_object_list.remove(ui_object)

    @classmethod
    def update_logic(cls):
        HitTest.update()
        [i.update_logic() for i in cls._instance._ui_object_list if i is not None]
