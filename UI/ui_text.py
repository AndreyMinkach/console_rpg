import time

import pygame

from Helpers.color_helper import ColorHelper
from UI.ui_base import *
from itertools import chain


def truncline(text, font, maxwidth):
    real = len(text)
    stext = text
    l = font.size(text)[0]
    cut = 0
    a = 0
    done = 1
    old = None
    while l > maxwidth:
        a = a + 1
        n = text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext = n[:-cut]
        else:
            stext = n
        l = font.size(stext)[0]
        real = len(stext)
        done = 0
    return real, done, stext


def wrapline(text, font, maxwidth):
    done = 0
    wrapped = []

    while not done:
        nl, done, stext = truncline(text, font, maxwidth)
        wrapped.append(stext.strip())
        text = text[nl:]
    return wrapped


def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)


class UIText(UIBase):
    def __init__(self, position: Vector2, size: Vector2, text: str, foreground=(int, int, int), font_size: int = 20,
                 font_name: str = 'serif'):
        self.font = font_name
        self.font_obj = pygame.font.SysFont(self.font, font_size)
        line_list = wrapline(text, self.font_obj, size.x)
        super().__init__(position, Vector2(size.x, len(line_list) * font_size))

        self.set_colorkey(ColorHelper.BLACK)
        self.font_size = font_size
        self.foreground = foreground
        self._text = text
        for line in line_list:
            self.children.append(self.font_obj.render(line, 0, self.foreground))

    def update(self, display_canvas: UIBase):
        for i in range(len(self.children)):
            self.blit(self.children[i], (0, i * self.font_size))
        display_canvas.blit(self, (self.position.x, self.position.y))
