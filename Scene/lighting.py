import copy
import time
from typing import List

from pyglet.gl import glViewport
from pyglet.graphics import Batch

from Helpers.location_helper import Vector2
from Scene.PostProcessing.post_effect import PostEffect
from Scene.camera import Camera


class Light:
    __slots__ = ['position', 'size', 'intensity', 'color', 'polar_transform_effect', 'shadows_effect',
                 'inverse_polar_effect', '_previous_center']

    def __init__(self, position: Vector2, intensity: float = 1.0, color: (float, float, float) = (1.0, 1.0, 1.0)):
        """
        Initializes a new Light object

        :param position: Position of the light source in world space
        :param intensity: The intensity of the light source
        :param color: The color of the light source
        """
        self.position = position
        self.intensity = intensity
        self.color = color
        # Size of the lighting effects in screen space
        size = Lighting.get_light_size()
        size = Vector2(*size)
        self.size = size

        self.polar_transform_effect: PostEffect = PostEffect(size.x, size.y, 'polar_transform_pps')
        self.shadows_effect: PostEffect = PostEffect(size.x, size.y, 'shadows_pps')
        self.inverse_polar_effect: PostEffect = PostEffect(size.x, size.y, 'inverse_polar_pps')

        self._previous_center: tuple = (None, None)

        self.set_resolution(*Lighting.get_light_resolution())
        Lighting.add_light(self)

    def set_size(self, width: int, height: int):
        """
        Sets a new size for the lighting effects rectangle

        :param width: New lighting effects rectangle width
        :param height: New lighting effects rectangle height
        """
        self.size = Vector2(width, height)
        self.polar_transform_effect.set_size(width, height)
        self.shadows_effect.set_size(width, height)
        self.inverse_polar_effect.set_size(width, height)

    def set_resolution(self, width: int, height: int):
        """
        Sets a new resolution for the lighting effects

        :param width: New FBO textures width
        :param height: New FBO textures height
        """
        self.polar_transform_effect.set_resolution(width, height)
        self.shadows_effect.set_resolution(width, height)
        self.inverse_polar_effect.set_resolution(width, height)

    def set_position_by_center(self, center_x, center_y):
        """
        Places rectangles of lighting effects so that their center is located in the specified center

        :param center_x: X coordinate of a new center
        :param center_y: Y coordinate of a new center
        """
        # if self._previous_center[0] == center_x and self._previous_center[1] == center_y:
        #     return
        new_size = self.size * Lighting.get_zoom_divisor()
        x = center_x - new_size.x * 0.5
        y = center_y - new_size.y * 0.5
        # self._previous_center = (center_x, center_y)
        self.inverse_polar_effect.set_boundaries(x, y, new_size.x, new_size.y)
        self.inverse_polar_effect.uniforms.set_uniform('light_offset', (x, y))
        self.inverse_polar_effect.uniforms.set_uniform('texture_scale', Lighting.get_zoom_divisor())

    def draw(self):
        """
        Draws lighting and shadows of the light source
        """
        self.polar_transform_effect.bind()
        Lighting.render_shadow_casters()
        self.polar_transform_effect.unbind()

        self.shadows_effect.bind()
        self.polar_transform_effect.render()
        self.shadows_effect.unbind()

        self.inverse_polar_effect.bind()
        self.shadows_effect.render()
        self.inverse_polar_effect.unbind()

        self.inverse_polar_effect.render()


class Lighting:
    _instance: 'Lighting' = None
    __slots__ = ['lights', 'shadow_casters', '_batch', '_camera_lighting_zoom', '_zoom_divisor', '_light_size',
                 '_light_resolution']

    def __init__(self, window_width: int, window_height: int, camera_lighting_zoom: float = 30,
                 light_resolution: Vector2 = Vector2(256, 256)):
        self.__class__._instance = self
        self.lights: List[Light] = []
        self._batch = Batch()
        self._camera_lighting_zoom = camera_lighting_zoom
        self._zoom_divisor = camera_lighting_zoom / Camera.get_zoom()
        self._light_size = Vector2(window_width, window_height)
        self._light_resolution = light_resolution

        self.set_lights_size(window_width, window_height)

    @classmethod
    def get_zoom_divisor(cls) -> float:
        """
        Returns the result of camera_lighting_zoom / camera_default_zoom
        """
        return cls._instance._zoom_divisor

    @classmethod
    def get_light_size(cls) -> (int, int):
        """
        Returns lighting effects rectangle size
        """
        return cls._instance._light_size.tuple()

    @classmethod
    def get_light_resolution(cls) -> (int, int):
        """
        Returns lighting effects FBO resolution
        """
        return cls._instance._light_resolution.tuple()

    @classmethod
    def set_resolution(cls, width: int, height: int):
        """
        Sets a new resolution for the lighting effects

        :param width: New FBO textures width
        :param height: New FBO textures height
        """
        self = cls._instance
        self._light_resolution = Vector2(width, height)

        for light in self.lights:
            light.set_resolution(width, height)

    @classmethod
    def set_lights_size(cls, width: int, height: int):
        """
        Sets a new size for the lighting effects rectangle

        :param width: New lighting effects rectangle width
        :param height: New lighting effects rectangle height
        """
        self = cls._instance

        for light in self.lights:
            light.set_size(width, height)

    @classmethod
    def get_batch(cls) -> Batch:
        """
        Returns the batch object for shadow casters
        """
        return cls._instance._batch

    @classmethod
    def add_light(cls, light: Light):
        self = cls._instance
        if isinstance(light, Light):
            self.lights.append(light)
        else:
            print('WARNING: The light object was not added to the lights list!')

    @classmethod
    def render_shadow_casters(cls):
        cls._instance._batch.draw()

    @classmethod
    def draw(cls):
        self = cls._instance

        start = time.time()

        # glViewport(0, 0, 256, 256)

        current_camera_zoom = Camera.get_zoom()
        current_camera_pos = Camera.get_position()

        Camera.set_zoom(self._camera_lighting_zoom)
        for light in self.lights:
            Camera.set_position(light.position.x, light.position.y)
            light.draw()

        Camera.set_zoom(current_camera_zoom)
        Camera.set_position(*current_camera_pos)
        for light in self.lights:
            light_effects_center_pos = Camera.world_to_screen(light.position.x, light.position.y)
            light.set_position_by_center(*light_effects_center_pos)

        # glViewport(0, 0, 1280, 680)

        print((time.time() - start) * 1000)
