from pyglet.gl import *

from Helpers.color_helper import ColorHelper
from Helpers.input_helper import InputHelper
from UI.renderer import Renderer


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)
        self.clear_color = ColorHelper.DARK
        self.total_ticks = 0

    def on_activate(self):
        glClearColor(*[i / 255.0 for i in self.clear_color])
        glEnable(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    def on_draw(self):
        self.clear()
        Renderer.draw()

    def update(self, dt):
        Renderer.update_logic()

        # input helper should be updated after all other logic
        InputHelper.update()
        self.total_ticks += 1
        if self.total_ticks > 1000:
            self.total_ticks -= 1000
