from Helpers.color_helper import ColorHelper
from UI.ui_base import *


def trunc_line(text, font, max_width):
    real = len(text)
    s_text = text
    l = font.size(text)[0]
    cut = 0
    a = 0
    done = 1
    old = None
    while l > max_width:
        a = a + 1
        n = text.rsplit(None, a)[0]
        if s_text == n:
            cut += 1
            s_text = n[:-cut]
        else:
            s_text = n
        l = font.size(s_text)[0]
        real = len(s_text)
        done = 0
    return real, done, s_text


def wrap_line(text, font, max_width):
    done = 0
    wrapped = []

    while not done:
        nl, done, s_text = trunc_line(text, font, max_width)
        wrapped.append(s_text.strip())
        text = text[nl:]
    return wrapped


class UIText(UIBase):
    def __init__(self, position: Vector2,
                 size: Vector2,
                 text: str,
                 foreground: (int, int, int),
                 font_size: int = 25,
                 font_name: str = None):
        self.font_name = font_name
        self.font_obj = pygame.font.SysFont(self.font_name, font_size)
        line_list = wrap_line(text, self.font_obj, size.x)
        super().__init__(position, Vector2(size.x, len(line_list) * font_size))
        self.font_size = font_size
        self.foreground = foreground
        self._text = text
        for line in line_list:
            self.children.append(self.font_obj.render(line, 0, self.foreground))

    def update(self, display_canvas: UIBase):
        for i in range(len(self.children)):
            self.blit(self.children[i], (0, i * self.font_size))
        display_canvas.blit(self, (self.position.x, self.position.y))
