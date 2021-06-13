from Helpers.location_helper import Vector2
from Scene.PostProcessing.post_effect import PostEffect


class Light:
    __slots__ = ['position', 'intensity', 'color']

    def __init__(self, position: Vector2, intensity: float, color: (float, float, float) = (1.0, 1.0, 1.0)):
        self.position = position
        self.intensity = intensity
        self.color = color


class Lighting:
    _instance: 'Lighting' = None
    __slots__ = ['lights', 'casters', 'polar_transform_effect', 'shadows_effect', 'inverse_polar_effect']

    def __init__(self, screen_width: int, screen_height: int):
        self.__class__._instance = self
        self.lights = []
        self.casters = []
        self.polar_transform_effect: PostEffect = PostEffect(screen_width, screen_height, 'polar_transform_pps')
        self.shadows_effect: PostEffect = PostEffect(screen_width, screen_height, 'shadows_pps')
        self.inverse_polar_effect: PostEffect = PostEffect(screen_width, screen_height, 'inverse_polar_pps')

    @classmethod
    def add_light(cls, light: Light):
        self = cls._instance
        if isinstance(light, Light):
            self.lights.append(light)
        else:
            print('WARNING: The light object was not added to the lights list!')

    @classmethod
    def add_caster(cls, caster):
        self = cls._instance
        if caster.__class__ == 'HitBox':  # cannot use isinstance method because of circular imports with HitBox class
            if caster.light_caster is True:
                self.casters.append(caster)
        else:
            print('WARNING: The light caster object was not added to the casters list!')
