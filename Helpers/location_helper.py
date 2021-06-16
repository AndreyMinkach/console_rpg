import math
from math import sqrt

import numpy as np


class Vector2:
    """
    This class is used only for ui objects to represent the size or coordinates in screen space
    """
    zero: 'Vector2' = None
    one: 'Vector2' = None
    right: 'Vector2' = None

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

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        length = self.length()
        if length == 0:
            return Vector2.zero
        return self * (1 / length)

    @classmethod
    def angle_between(cls, v1: (float, float), v2: (float, float)):
        dot = v1[0] * v2[0] + v1[1] * v2[1]
        det = v1[0] * v2[1] - v1[1] * v2[0]
        angle = math.atan2(det, dot)
        return 360 - math.degrees(angle)


Vector2.zero = Vector2(0, 0)
Vector2.one = Vector2(1, 1)
Vector2.right = Vector2(1, 0)
