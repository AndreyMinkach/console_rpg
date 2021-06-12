from pyglet.gl import *

from Helpers.color_helper import ColorHelper
from Helpers.input_helper import InputHelper
from Helpers.shader_manager import ShaderManager
from Scene.PostProcessing.post_effect import PostEffect
from Scene.renderer import Renderer
from UI.ui_renderer import UIRenderer


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)
        self.set_location((self.screen.width - self.width) // 2, (self.screen.height - self.height) // 2)
        self.clear_color = ColorHelper.DARK
        self.total_ticks = 0
        UIRenderer.set_window_size((self.width, self.height))
        glClearColor(*[i / 255.0 for i in self.clear_color])
        glEnable(GL_TEXTURE_2D and GL_BLEND and GL_ALPHA_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBlendEquationSeparate(GL_FUNC_ADD, GL_MAX)
        glAlphaFunc(GL_GREATER, 0.5)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        self.polar_trs_effect = PostEffect(1280, 680, 'polar_transform_pps')
        self.shadows_effect = PostEffect(1280, 680, 'shadows_pps')
        self.inverse_polar_effect = PostEffect(1280, 680, 'inverse_polar_pps')

    def on_draw(self):
        self.clear()

        self.polar_trs_effect.bind()
        Renderer.draw()
        UIRenderer.draw()
        self.polar_trs_effect.unbind()

        self.shadows_effect.bind()
        self.polar_trs_effect.render()
        self.shadows_effect.unbind()

        self.inverse_polar_effect.bind()
        self.shadows_effect.render()
        self.inverse_polar_effect.unbind()

        self.inverse_polar_effect.render()

        self.invalid = False

    def update(self, dt):
        UIRenderer.update_logic()

        # input helper should be updated after all other logic
        InputHelper.update()
        self.total_ticks += 1
        if self.total_ticks > 1000:
            self.total_ticks -= 1000

    def on_close(self):
        ShaderManager.close()
        self.close()

    def get_aspect_ratio(self) -> float:
        return self.width / self.height
