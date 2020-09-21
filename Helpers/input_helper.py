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
        self.current_mouse_button = -1
        self.current_click_type = -1

    def reset_input_fields(self):
        self.mouse_wheel_delta = 0
        self.current_mouse_button = -1
        self.current_click_type = -1

    def update(self, event: Event):
        if event is not None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_wheel_delta = 1 if event.button == 4 else -1 if event.button == 5 else 0
                self.current_click_type = event.type
                self.current_mouse_button = event.button
            if event.type == pygame.MOUSEBUTTONUP:
                self.current_click_type = event.type
                self.current_mouse_button = event.button
