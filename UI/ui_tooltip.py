import pygame
from pygame.surface import Surface

from Helpers.color_helper import ColorHelper
from Helpers.location_helper import Vector2


class UITooltip:
    instance = None

    def __init__(self):
        self.__class__.instance = self
        self.enabled = True
        self._source = {}
        self.size = Vector2(150, 300)
        self.background = Surface((100, 100))
        self.border = Surface((40, 40))
        self.border.fill(ColorHelper.GREEN)
        self.background.fill(ColorHelper.BLACK)

    def set_source(self, source_dict: dict):
        self._source = source_dict

    def update(self, display_canvas: Surface):
        self.background.blit(self.border, (10, 10))
        display_canvas.blit(self.background, (100, 30))
