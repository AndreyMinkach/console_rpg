import time

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
    def __init__(self, position: Vector2, labaa123: str):
        document = pyglet.text.document.FormattedDocument(labaa123)
        document.set_style(0, len(document.text), dict(color=(255, 255, 255, 255)))
        text = pyglet.text.layout.TextLayout(document, 600, 200, multiline=True)
        self.children = []
        self.children.append(text)

    def update(self):
        for c in self.children:
            c.draw()
