from pyglet.gl import *

from Helpers.color_helper import ColorHelper
from Helpers.input_helper import InputHelper
from Helpers.shader_manager import ShaderManager
from UI.renderer import Renderer


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)
        self.set_location((self.screen.width - self.width) // 2, (self.screen.height - self.height) // 2)
        self.clear_color = ColorHelper.DARK
        self.total_ticks = 0
        Renderer.set_window_size((self.width, self.height))
        glClearColor(*[i / 255.0 for i in self.clear_color])
        glEnable(GL_TEXTURE_2D and GL_BLEND and GL_ALPHA_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBlendEquationSeparate(GL_FUNC_ADD, GL_MAX)
        glAlphaFunc(GL_GREATER, 0.5)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
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

    def on_close(self):
        ShaderManager.close()
        self.close()
