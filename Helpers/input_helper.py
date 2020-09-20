import pygame
from pygame.event import Event

from Helpers.location_helper import Vector2


class InputHelper:
    instance = None

    def __init__(self):
        self.__class__.instance = self
        self.mouse_wheel_delta = 0
        self.mouse_position = Vector2.zero
        self.should_quit = False

    def update(self, event: Event):
        if event is not None and event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_wheel_delta = 1 if event.button == 4 else -1 if event.button == 5 else 0
