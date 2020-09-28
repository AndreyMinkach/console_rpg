from Animation.number_field_animation import NumberFieldAnimation


class Storyboard:
    instance = None

    def __init__(self):
        self.__class__.instance = self
        self._animations = []
        self._animations_to_remove = []

    def begin_animation(self, animation: NumberFieldAnimation):
        self._animations.append(animation)
        animation.start_animation()

    def stop_animation(self, animated_object, field_name: str):
        for a in self._animations:
            if a.check_source(animated_object, field_name):
                self._animations_to_remove.append(a)

    def update(self):
        for a in self._animations:
            if a.update_and_draw():
                self._animations_to_remove.append(a)

        for a in self._animations_to_remove:
            self._animations.remove(a)
        self._animations_to_remove.clear()
