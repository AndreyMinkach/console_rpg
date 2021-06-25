from ctypes import byref

from pyglet.gl import *
from pyglet.image import Animation, AnimationFrame, Texture


def get_animation(images: list, durations: list) -> Animation:
    return Animation([AnimationFrame(images[i], durations[i]) for i in range(len(images))])


def create_texture(width: int, height: int, target: int = GL_TEXTURE_2D, internal_format: int = GL_RGBA,
                   min_filter: int = GL_LINEAR, mag_filter: int = GL_LINEAR, tex_wrapping: int = GL_REPEAT,
                   data_type: int = GL_UNSIGNED_BYTE, allocate_memory: bool = True,
                   bytes_per_pixel: int = 4) -> Texture:
    """
    Creates a new texture with specified parameters. In most cases it is enough to use the pyglet.image.Texture.create
    method, but if you want to control more texture parameters you should use this method.

    :param width: Texture width
    :param height: Texture height
    :param target: Texture target, GL_TEXTURE_2D,
    :param internal_format: Internal format of the texture, for example GL_RGBA or GL_DEPTH_COMPONENT
    :param min_filter: Min filter of the texture, for example GL_LINEAR
    :param mag_filter: Mag filter of the texture, for example GL_LINEAR
    :param tex_wrapping: Texture wrapping method, for example GL_CLAMP_TO_EDGE or GL_REPEAT
    :param data_type: Texture data type, GL_UNSIGNED_BYTE, GL_FLOAT and etc.
    :param allocate_memory: Determines whether some RAM memory should be allocated for the new texture
    :param bytes_per_pixel: Bytes per pixel, default is 4
    :return: New pyglet.image.Texture instance
    """
    texture_id = GLuint()
    glGenTextures(1, byref(texture_id))
    glBindTexture(target, texture_id)
    glTexParameteri(target, GL_TEXTURE_MIN_FILTER, min_filter)
    glTexParameteri(target, GL_TEXTURE_MAG_FILTER, mag_filter)
    glTexParameteri(target, GL_TEXTURE_WRAP_S, tex_wrapping)
    glTexParameteri(target, GL_TEXTURE_WRAP_T, tex_wrapping)

    if allocate_memory is True:
        blank = (GLubyte * (width * height * bytes_per_pixel))()
    else:
        blank = None
    glTexImage2D(target, 0, internal_format, width, height, 0, internal_format, data_type, blank)
    texture = Texture(width, height, target, texture_id.value)
    texture.min_filter = min_filter
    texture.mag_filter = mag_filter

    return texture
