import math
import time
from abc import ABC

from pyglet.gl import *
from pyglet.shapes import Rectangle

from Helpers.color_helper import ColorHelper
from Helpers.input_helper import InputHelper
from Helpers.shader_manager import ShaderManager
from Scene.lighting import Lighting
from Scene.renderer import Renderer
from UI.ui_renderer import UIRenderer


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)
        self.set_location((self.screen.width - self.width) // 2, (self.screen.height - self.height) // 2)
        self.clear_color = tuple(i / 255.0 for i in ColorHelper.DARK)
        self.total_ticks = 0

        glEnable(GL_TEXTURE_2D and GL_BLEND and GL_ALPHA_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    def on_draw(self):
        glClearColor(*self.clear_color)
        self.clear()

        Lighting.draw()
        Renderer.draw()
        # UIRenderer.draw()

        self.invalid = False

    def update(self, dt):
        UIRenderer.update_logic()

        # for i in range(len(self.angle_list)):
        #     angle = self.angle_list[i] + 5 * dt
        #     angle_radians = math.radians(angle)
        #     x = math.cos(angle_radians) * 4
        #     y = math.sin(angle_radians) * 4
        #     self.object_list[i].position = (x, y)
        #     self.angle_list[i] = angle

        # value = time.time() * 2
        # self.light1.position.y = math.sin(value) * 4
        # self.light2.position.y = (1.0 - math.sin(value)) * 4

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
