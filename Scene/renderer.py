from Scene.scene_object import SceneObject


class Renderer:
    _instance: 'Renderer' = None

    def __init__(self):
        self.__class__._instance = self
        self.triangle = SceneObject("some_fractal.png")
        self.triangle.set_position(-2, 0)
        self.triangle.set_anchor(0.5, 0.5)
        self.triangle1 = SceneObject("some_fractal.png")
        self.triangle1.set_position(2, 0)

    @classmethod
    def draw(cls):
        from math import sin, radians

        cls._instance.triangle.test_angle += 1
        cls._instance.triangle.set_rotation(cls._instance.triangle.test_angle)
        cls._instance.triangle.set_position(-2, sin(radians(cls._instance.triangle.test_angle * 5)))
        cls._instance.triangle.draw()

        cls._instance.triangle1.test_angle -= 1
        cls._instance.triangle1.set_rotation(cls._instance.triangle1.test_angle)
        cls._instance.triangle1.draw()
