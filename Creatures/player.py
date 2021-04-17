from math import sqrt

from Helpers.input_helper import InputHelper
from Helpers.location_helper import Vector2
from Scene.scene_object import SceneObject
from pyglet.window import key


class Player(SceneObject):
    _instance: 'Player' = None

    def __init__(self, image):
        super().__init__(image)
        self.__class__._instance = self
        self.movement_speed = 10

    @classmethod
    def update(cls, dt):
        self = cls._instance
        self._update_movement(dt)

    def _update_movement(self, dt):
        vector = Vector2(
            -int(InputHelper.is_key_pressed(key.A)) + int(InputHelper.is_key_pressed(key.D)),
            -int(InputHelper.is_key_pressed(key.S)) + int(InputHelper.is_key_pressed(key.W))
        ).normalize() * dt * self.movement_speed

        current_position = Vector2(*self.position) + vector
        self.position = current_position.tuple()
