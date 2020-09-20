import pygame


class UIBase(pygame.Surface):
    def __init__(self, position_x, position_y, size_x, size_y):
        super(UIBase, self).__init__((size_x, size_y))
        self.position_x = position_x
        self.position_y = position_y
        self.size_x = size_x
        self.size_y = size_y
        self.enabled = True
        self.children = []

    def get_position(self):
        return self.position_x, self.position_y

    def get_size(self):
        return self.size_x, self.size_y

    def update(self, display_canvas: pygame.Surface):
        """
        Updates the calling abject and all its children
        :param display_canvas:
        :return:
        """
        if self.enabled:
            for child in self.children:
                if child is UIBase:
                    self.blit(child, (child.position_x, child.position_y))
            display_canvas.blit(self, (self.position_x, self.position_y))

    def fade_in(self):
        super().set_alpha(100)
