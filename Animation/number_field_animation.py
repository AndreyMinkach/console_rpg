import time


class NumberFieldAnimation:
    def __init__(self, object_to_animate, field_name: str, start_value: int, end_value: int, duration_in_secs: float):
        self._object_to_animate = object_to_animate
        self._field_name = field_name
        self._start_value = start_value
        self._end_value = end_value
        self._duration = duration_in_secs
        self.start_time = None

    def check_source(self, animated_object, field_name: str):
        return self._object_to_animate == animated_object and self._field_name == field_name

    def start_animation(self):
        self.start_time = time.time()

    def lerp(self, a: int, b: int, t: float) -> int:
        return int(a + t * (b - a))

    def update(self):
        """
        Updates animation
        :return: True if animation has completed, False if animation is still playing
        """
        current_time = time.time()
        current_difference = (self.start_time + self._duration) - current_time
        t_value = 1.0 - current_difference / self._duration
        t_value = max(0.0, min(t_value, 1.0))
        lerp_value = self._start_value + t_value * (self._end_value - self._start_value)
        setattr(self._object_to_animate, self._field_name, lerp_value)
        if 0.0 <= t_value < 1.0:
            return False
        else:
            setattr(self._object_to_animate, self._field_name, self._end_value)
            return True
