from math import sqrt


class Vector2:
    """
    This class is used only for ui objects to represent the size or coordinates in screen space
    """
    zero: 'Vector2' = None
    one: 'Vector2' = None

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def tuple(self) -> (float, float):
        return self.x, self.y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        other_type = type(other)
        if other_type != Vector2:
            raise ValueError(f'ERROR: Cannot compare Vector2 instance with {other_type} instance!')
        return self.x == other.x and self.y == other.y

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        length = self.length()
        if length == 0:
            return Vector2.zero
        return self * (1 / length)


Vector2.zero = Vector2(0, 0)
Vector2.one = Vector2(1, 1)
