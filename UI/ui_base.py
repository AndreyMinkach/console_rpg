from pygame import Surface
from Helpers.location_helper import Vector2


class UIBase(Surface):
    def __init__(self, position: Vector2, size: Vector2):
        super().__init__((size.x, size.y))
        self.position = position
        self.size = size
        self.enabled = True
        self.children = []
        self.parent = None

    def update(self, display_canvas: Surface):
        """
        Updates the calling abject and all its children
        :param display_canvas:
        :return:
        """
        if self.enabled:
            for child in self.children:
                if child is UIBase:
                    self.blit(child, (child.position.x, child.position.y))
            display_canvas.blit(self, (self.position.x, self.position.y))

    def is_point_inside(self, point: Vector2):
        lu_corner = self.position if self.parent is None else self.position - self.parent.position
        rb_corner = lu_corner + self.size
        return lu_corner.x <= point.x <= rb_corner.x and lu_corner.y <= point.y <= rb_corner.y

    def fade_in(self):
        super().set_alpha(100)
