from pyglet.graphics import OrderedGroup, Batch


class Renderer:
    _instance: 'Renderer' = None

    def __init__(self):
        self.__class__._instance = self
        self.batch = Batch()
        self.group = OrderedGroup(0)
        self._object_list: list = []

    @classmethod
    def group(cls):
        return cls._instance.group

    @classmethod
    def batch(cls):
        return cls._instance.batch

    @classmethod
    def add_scene_object_to_render_loop(cls, scene_object):
        cls._instance._object_list.append(scene_object)

    @classmethod
    def remove_scene_object_from_render_loop(cls, scene_object):
        cls._instance._object_list.remove(scene_object)

    @classmethod
    def draw(cls):
        self = cls._instance
        self.batch.invalidate()
        self.batch.draw()
