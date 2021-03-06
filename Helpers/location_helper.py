class Vector2:
    zero, one = None, None

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def tuple(self) -> (int, int):
        return self.x, self.y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, int):
            return Vector2(self.x * other, self.y * other)
        else:
            return self

    def __repr__(self):
        return f"({self.x}, {self.y})"


Vector2.zero = Vector2(0, 0)
Vector2.one = Vector2(1, 1)
