class FieldAnimation:
    def __init__(self, object_to_animate, field_name: str, duration_in_secs: float):
        self._object_to_animate = object_to_animate
        self._field_name = field_name
        self.duration = duration_in_secs
        self.start_time = None

    def check_source(self, animated_object, field_name: str):
        return self._object_to_animate == animated_object and self._field_name == field_name