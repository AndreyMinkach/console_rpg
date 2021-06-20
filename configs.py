import pyglet
from pyglet.gl import glViewport

from Helpers.location_helper import Vector2
from Scene.camera import Camera
from Scene.lighting import Lighting

WINDOW_TITLE = 'Not a console RPG'
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 680
DESIRED_FPS = 60
IMAGE_FOLDER = 'Static/Images/'

_window_size: Vector2 = Vector2(WINDOW_WIDTH, WINDOW_HEIGHT)
_window_object: pyglet.window.Window = None


def get_window() -> pyglet.window.Window:
    return _window_object


def set_window(window: pyglet.window.Window):
    global _window_object
    _window_object = window


def get_window_size() -> Vector2:
    return _window_size


def set_window_size(width: int, height: int):
    global WINDOW_WIDTH, WINDOW_HEIGHT, _window_size

    WINDOW_WIDTH = int(width)
    WINDOW_HEIGHT = int(height)
    _window_size = Vector2(WINDOW_WIDTH, WINDOW_HEIGHT)
    _window_object.set_size(WINDOW_WIDTH, WINDOW_HEIGHT)

    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    Camera.update_projection_matrix(width, height)
    Lighting.set_lights_size(width, height)
