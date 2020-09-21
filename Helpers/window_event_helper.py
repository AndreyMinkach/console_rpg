import pygame

from Helpers.input_helper import InputHelper
from Helpers.location_helper import Vector2


class EventHelper:
    instance = None

    def __init__(self):
        self.__class__.instance = self
        self.input_helper = InputHelper()
        self.should_quit = False

    def update(self):
        self.input_helper.reset_input_fields()
        self.input_helper.mouse_position = Vector2(*pygame.mouse.get_pos())

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.should_quit = True
            if e.type == pygame.KEYDOWN or e.type == pygame.KEYUP or e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
                self.input_helper.update(e)

