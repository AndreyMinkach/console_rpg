import math
from math import sqrt
from pydoc import Helper

import numpy as numpy
from pyglet.image import TextureRegion

from Helpers import helper
from Helpers.atlas_helper import TextureAtlas
from Helpers.input_helper import InputHelper
from Helpers.location_helper import Vector2
from Scene.camera import Camera
from Scene.scene_object import SceneObject
from pyglet.window import key


class Player(SceneObject):
    _instance: 'Player' = None

    def __init__(self, image):
        animation = helper.get_animation_from_sprite_grid(
            TextureAtlas.load_image(image_path=image), sprite_row=2, frame_height=120, frame_width=120, frames_count=7
        )
        super().__init__(animation)
        self.__class__._instance = self
        self.movement_speed = 10
        self.weapon_holder = SceneObject(image=TextureAtlas.load_image('arrow.png'))
        self.basic_scale = Vector2(2, 2)  # scale the default texture to seems like a player
        self.scale = self.basic_scale.tuple()
        self.weapon_position = Vector2(0.3, 0.3)
        self.play_animation()

    def show_weapon(self, weapon_img):
        pass

    @classmethod
    def update(cls, dt):
        self = cls._instance
        self._update_movement(dt)

    def __update_weapon_movement(self, current_position):
        """Helper method to update weapon movement"""
        self.weapon_holder.position = [current_position.x + self.weapon_position.x,
                                       current_position.y + self.weapon_position.y]

    def _update_movement(self, dt):
        """Method tp update player and weapon movement"""
        movement_direction = Vector2(
            -int(InputHelper.is_key_pressed(key.A)) + int(InputHelper.is_key_pressed(key.D)),
            -int(InputHelper.is_key_pressed(key.S)) + int(InputHelper.is_key_pressed(key.W))
        ).normalize() * dt * self.movement_speed

        if movement_direction.x == 0:
            self.scale = self.scale
            # waiting movement animation
        else:
            self.scale = (self.basic_scale * Vector2(numpy.sign(movement_direction.x), 1)).tuple()

        current_position = Vector2(*self.position) + movement_direction
        self.position = current_position.tuple()
        self.__update_weapon_movement(current_position=current_position)
        mouse_pos = Camera.screen_to_world(*InputHelper.get_mouse_pos().tuple())
        self.weapon_holder.rotation = Vector2.angle_between(
            Vector2.right.tuple(),
            (mouse_pos[0] - self.position[0], mouse_pos[1] - self.position[1])
        )
