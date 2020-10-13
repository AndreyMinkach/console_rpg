from Animation.number_field_animation import NumberFieldAnimation


class Storyboard:
    _instance: 'Storyboard' = None

    def __init__(self):
        self.__class__._instance = self
        self._animations = []
        self._animations_to_remove = []

    @classmethod
    def begin_animation(cls, animation: NumberFieldAnimation):
        cls._instance._animations.append(animation)
        animation.start_animation()

    @classmethod
    def stop_animation(cls, animated_object, field_name: str):
        for a in cls._instance._animations:
            if a.check_source(animated_object, field_name):
                cls._instance._animations_to_remove.append(a)

    @classmethod
    def update(cls):
        for a in cls._instance._animations:
            if a.update_logic():
                cls._instance._animations_to_remove.append(a)

        for a in cls._instance._animations_to_remove:
            cls._instance._animations.remove(a)
        cls._instance._animations_to_remove.clear()
