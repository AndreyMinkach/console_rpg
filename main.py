from pyglet import font
from pyglet.gl import *

import configs
from Helpers.location_helper import Vector2
from UI.renderer import Renderer
from UI.ui_base import UIBase
from UI.ui_text import UIText

renderer = Renderer()


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)

    def on_activate(self):
        glClearColor(0.2, 0.2, 0.2, 0)
        glEnable(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    def on_key_press(self, symbol, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        print(f"{x, y}: {button}")

    def on_draw(self):
        self.clear()
        renderer.update()

    def update(self, dt):
        pass


if __name__ == '__main__':
    window = MyWindow(configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT, caption=configs.WINDOW_TITLE, resizable=True,
                      vsync=True)

    temp_ui_text1 = UIText("Updates the callingpdates the calling abject and all its  Updates the calling abject "
                           "and all itspdates the calling abject and all its  Updates the calling abject and all "
                           "itspdates the calling abject and all its  Updates the calling abject and all its abject "
                           "and all its  Updates the calling abject and all its ",
                           Vector2(400, 200), Vector2(200, 0))


    temp_base1 = UIBase(Vector2(100, 100), Vector2(300, 200))
    renderer.add_ui_object(temp_ui_text1)
    renderer.add_ui_object(temp_base1)
    pyglet.clock.schedule_interval(window.update, 1.0 / float(configs.DESIRED_FPS))
    pyglet.app.run()
