from Helpers.location_helper import Vector2


class Light:
    __slots__ = ['position', 'intensity', 'color']

    def __init__(self, position: Vector2, intensity: float, color: (float, float, float) = (1.0, 1.0, 1.0)):
        self.position = position
        self.intensity = intensity
        self.color = color


class Lighting:
    pass
