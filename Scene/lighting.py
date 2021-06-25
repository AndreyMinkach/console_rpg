from typing import Set

from pyglet.gl import *
from pyglet.graphics import Batch
from pyglet.image import Texture

from Helpers.atlas_helper import TextureAtlas
from Helpers.location_helper import Vector2
from Scene.PostProcessing.post_effect import PostEffect
from Scene.camera import Camera


class Light:
    __slots__ = ['position', '_size', '_intensity', '_color', '_hard_shadows', '_shadow_bias', '_pixels_to_skip',
                 'polar_transform_effect', 'shadows_effect', 'inverse_polar_effect', '_previous_center']

    def __init__(self,
                 position: Vector2,
                 intensity: float = 1.0,
                 color: (float, float, float) = (1.0, 1.0, 1.0),
                 hard_shadows: bool = False,
                 shadow_bias: float = 1.0,
                 pixels_to_skip: float = 2.0):
        """
        Initializes a new Light object

        :param position: Position of the light source in world space
        :param intensity: The intensity of the light source
        :param color: The color of the light source
        :param hard_shadows: Determines whether the shadows will be hard if True or soft if False
        :param shadow_bias: Offset from the center of the light's origin in pixels
        :param pixels_to_skip: Pixels number to skip in the shadow shader loop. Higher values gives a better performance
        """
        self.position = position
        self._intensity = intensity
        self._color = color
        self._hard_shadows = hard_shadows
        self._shadow_bias = shadow_bias
        self._pixels_to_skip = pixels_to_skip
        # Size of the lighting effects in screen space
        size = Vector2(*Lighting.get_light_size())
        self._size = size
        # self._texture = None
        # self._shader = ShaderManager.get_shader_by_name(shader_name)
        # self.uniforms = UniformSetter(self._shader)
        # self._batch = Batch()
        # self._group = ShadedGroup(self._texture, self._shader, self.uniforms, None, blend_src, blend_dest)
        # self._create_vertex_list()

        self.polar_transform_effect: PostEffect = PostEffect(size.x, size.y, 'polar_transform_pps')
        self.shadows_effect: PostEffect = PostEffect(size.x, size.y, 'shadows_pps')
        self.inverse_polar_effect: PostEffect = PostEffect(size.x, size.y, 'inverse_polar_pps')
        # self.set_blend_func(GL_SRC_ALPHA, GL_ONE)

        self._previous_center: Vector2 = Vector2(None, None)

        self.set_resolution(*Lighting.get_light_resolution())
        self.color = color
        Lighting.add_light(self)

    def delete(self):
        """
        Deletes the light source object
        """
        Lighting.remove_light(self)
        del self.polar_transform_effect
        del self.shadows_effect
        del self.inverse_polar_effect

    @property
    def intensity(self) -> float:
        return self._intensity

    @intensity.setter
    def intensity(self, value: float):
        self._intensity = value
        self.inverse_polar_effect.uniforms.set_uniform('light_intensity', value)

    @property
    def color(self) -> (float, float, float):
        return self._color

    @color.setter
    def color(self, value: (float, float, float)):
        self._color = value
        self.inverse_polar_effect.uniforms.set_uniform('light_color', value)

    @property
    def hard_shadows(self) -> bool:
        return self._hard_shadows

    @hard_shadows.setter
    def hard_shadows(self, value: bool):
        self._hard_shadows = value
        self.inverse_polar_effect.uniforms.set_uniform('hard_shadows', value)

    @property
    def shadow_bias(self) -> float:
        return self._shadow_bias

    @shadow_bias.setter
    def shadow_bias(self, value: float):
        self._shadow_bias = value
        self.shadows_effect.uniforms.set_uniform('shadow_bias', value)

    @property
    def pixels_to_skip(self) -> float:
        return self._pixels_to_skip

    @pixels_to_skip.setter
    def pixels_to_skip(self, value: float):
        self._pixels_to_skip = value
        self.shadows_effect.uniforms.set_uniform('pixels_to_skip', value)

    def set_blend_func(self, blend_source: int, blend_destination: int):
        """
        Sets new blending functions for lighting effects
        """
        # set source blending func
        self.polar_transform_effect.group.blend_src = blend_source
        self.shadows_effect.group.blend_src = blend_source
        self.inverse_polar_effect.group.blend_src = blend_source
        # set destination blending func
        self.polar_transform_effect.group.blend_dest = blend_destination
        self.shadows_effect.group.blend_dest = blend_destination
        self.inverse_polar_effect.group.blend_dest = blend_destination

    def set_size(self, width: int, height: int):
        """
        Sets a new size for the lighting effects rectangle

        :param width: New lighting effects rectangle width
        :param height: New lighting effects rectangle height
        """
        self._size = Vector2(width, height)
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
        # if self._previous_center.x == center_x and self._previous_center.y == center_y:
        #     return
        new_size = self._size * Lighting.get_zoom_divisor()
        x = center_x - new_size.x * 0.5
        y = center_y - new_size.y * 0.5

        # self._previous_center.x, self._previous_center.y = center_x, center_y

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
                 '_light_resolution', '_light_cookie']

    def __init__(self, window_width: int, window_height: int, camera_lighting_zoom: float = 30,
                 light_resolution: Vector2 = Vector2(256, 256)):
        self.__class__._instance = self
        self.lights: Set[Light] = set()
        self._batch = Batch()
        self._camera_lighting_zoom = camera_lighting_zoom
        self._zoom_divisor = camera_lighting_zoom / Camera.get_zoom()
        self._light_size = Vector2(window_width, window_height)
        self._light_resolution = light_resolution
        self._light_cookie: Texture = TextureAtlas.load_image('light_cookie1.png', add_to_atlas=False,
                                                              tex_filter=GL_LINEAR)

        self.set_lights_size(window_width, window_height)

    @classmethod
    def get_light_cookie_texture(cls) -> Texture:
        """
        Returns the light cookie texture
        """
        return cls._instance._light_cookie

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
        """
        Adds the light object to the lighting system
        :param light: Light instance to add
        """
        self = cls._instance
        if isinstance(light, Light):
            self.lights.add(light)
        else:
            print('WARNING: The light object was not added to the lights list!')

    @classmethod
    def remove_light(cls, light: Light):
        """
        Removes the light object from the lighting system
        :param light: Light instance to remove
        """
        self = cls._instance
        if isinstance(light, Light):
            self.lights.remove(light)
        else:
            print('WARNING: The light object was not added to the lights list!')

    @classmethod
    def render_shadow_casters(cls):
        """
        Renders all the SceneObject instances that are registered in lighting system as the shadow casters
        """
        cls._instance._batch.draw()

    @classmethod
    def draw(cls):
        """
        Does all the lighting rendering
        """
        self = cls._instance

        # start = time.time()

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

        # print((time.time() - start) * 1000)
