import warnings

import pyglet
from pyglet.gl import glTexParameteri, GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST, GL_TEXTURE_MAG_FILTER
from pyglet.image import AbstractImage, TextureRegion
from pyglet.image.atlas import TextureBin


class TextureAtlas:
    _texture_atlas = TextureBin()
    _textures = {}

    @classmethod
    def add_texture(cls, texture: AbstractImage, border: int = 0) -> TextureRegion:
        texture_region = cls._texture_atlas.add(texture, border)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return texture_region

    @classmethod
    def load_image(cls, image_path: str, folder: str = 'Static/Images/', border=0) -> TextureRegion:
        full_path = folder + image_path
        if full_path not in cls._textures:
            texture = cls.add_texture(pyglet.image.load(full_path), border)
            cls._textures[full_path] = texture
            return texture
        return cls._textures[full_path]

    @classmethod
    def get_texture(cls, image_path: str, folder: str = 'Static/Images/') -> TextureRegion:
        full_path = folder + image_path
        if full_path in cls._textures:
            return cls._textures[full_path]
        warnings.warn(f"There is no texture assigned to the '{full_path}' file!")
        return None


TextureAtlas.load_image('default_sprite.png')
