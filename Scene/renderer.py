class Renderer:
    _instance: 'Renderer' = None

    def __init__(self):
        self.__class__._instance = self

        self._object_list: list = []

    @classmethod
    def add_scene_object_to_render_loop(cls, scene_object):
        cls._instance._object_list.append(scene_object)

    @classmethod
    def remove_scene_object_to_render_loop(cls, scene_object):
        cls._instance._object_list.remove(scene_object)

    @classmethod
    def draw(cls):
        for scene_object in cls._instance._object_list:
            scene_object.draw()
