import pygame

from UI.ui_base import *


class UIText(UIBase):
    def __init__(self, position: Vector2, size: Vector2, text: str, font_size: int = 30, rgb=(int, int, int)):
        super().__init__(position, size)
        self.font = None
        self.font_size = font_size
        self.temp_font_opj = pygame.font.Font(self.font, self.font_size)
        self._text = text
        self.rgb = rgb
        self.text_obj = self.temp_font_opj.render(self._text, 0, self.rgb)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.text_obj = self.temp_font_opj.render(self._text, 0, self.rgb)

    def update(self, display_canvas: UIBase):
        super().update(display_canvas)
        display_canvas.blit(self.text_obj, (self.position.x, self.position.y))
