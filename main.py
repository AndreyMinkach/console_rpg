from pyglet import font
from pyglet.gl import *

import configs
from Animation.storyboard import Storyboard
from Helpers.color_helper import ColorHelper
from Helpers.input_helper import InputHelper
from Helpers.location_helper import Vector2
from UI.renderer import Renderer
from UI.ui_base import UIBase
from UI.ui_scrollable_container import ScrollableContainer
from UI.ui_text import UIText

renderer = Renderer()
storyboard = Storyboard()


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)
        self.counter = 0
        self.some_bool = False

    def on_activate(self):
        glClearColor(*[i / 255.0 for i in ColorHelper.DARK])
        glEnable(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    def on_draw(self):
        self.clear()
        renderer.update()

    def update(self, dt):
        self.counter += dt

        if self.counter >= 2 and not self.some_bool:
            renderer._ui_objects_list[2].add_child(UIBase(Vector2.zero, Vector2(50, 60), color=ColorHelper.GRAY))
            self.some_bool = True

        # input helper should be updated after all other logic
        InputHelper.instance.update()


if __name__ == '__main__':
    window = MyWindow(configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT, caption=configs.WINDOW_TITLE, resizable=True,
                      vsync=True)

    input_helper = InputHelper(window)

    temp_ui_text1 = UIText("Updates the callingpdates the calling abject ",
                           Vector2(400, 200), Vector2(200, 0))
    temp_base1 = UIBase(Vector2(100, 100), Vector2(300, 200), color=ColorHelper.GRAY)

    temp_v = Vector2(10, 20) + Vector2(5, 6)
    print(temp_v)
    temp_container1 = ScrollableContainer(Vector2(600, 100), Vector2(100, 200))
    temp_container1.color = ColorHelper.GREEN[:3]
    temp_container1.children_margin = Vector2(10, 10)
    temp_container1.add_child(UIBase(Vector2.zero, Vector2(50, 60), color=ColorHelper.BLACK))
    temp_container1.add_child(UIBase(Vector2.zero, Vector2(50, 50), color=ColorHelper.PINK))
    temp_container1.add_child(UIBase(Vector2.zero, Vector2(50, 60), color=ColorHelper.LIGHT_BLUE))
    temp_container1.add_child(UIBase(Vector2.zero, Vector2(50, 40), color=ColorHelper.YELLOW))

    renderer.add_ui_object(temp_ui_text1)
    renderer.add_ui_object(temp_base1)
    renderer.add_ui_object(temp_container1)

    pyglet.clock.schedule_interval(window.update, 1.0 / float(configs.DESIRED_FPS))
    pyglet.app.run()
