from pyglet.gl import *

import configs
from Animation.storyboard import Storyboard
from Helpers.color_helper import ColorHelper
from Helpers.input_helper import InputHelper
from Helpers.location_helper import Vector2
from UI.renderer import Renderer
from UI.shadered_rectangle import UIRectangle
from UI.ui_base import UIBase
from UI.ui_inventory import UIInventory
from UI.ui_scrollable_container import ScrollableContainer
from UI.ui_sprite import UISprite
from UI.ui_text import UIText

renderer = Renderer()
storyboard = Storyboard()


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)
        self.total_ticks = 0
        self.some_shaded_object: UIRectangle = None

    def on_activate(self):
        glClearColor(*[i / 255.0 for i in ColorHelper.DARK])
        glEnable(GL_TEXTURE_2D and GL_BLEND and GL_ALPHA_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBlendEquationSeparate(GL_FUNC_ADD, GL_MAX)
        glAlphaFunc(GL_GREATER, 0.5)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        self.some_shaded_object = UIRectangle('some_fractal.png', Vector2(400, 100), Vector2(400, 300))

    def on_draw(self):
        self.clear()
        renderer.draw()
        self.some_shaded_object.draw()

    def update(self, dt):
        renderer.update_logic()

        # input helper should be updated after all other logic
        InputHelper.instance.update()
        self.total_ticks += 1
        if self.total_ticks > 1000:
            self.total_ticks -= 1000


if __name__ == '__main__':
    window = MyWindow(configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT, caption=configs.WINDOW_TITLE, resizable=True,
                      vsync=True)

    input_helper = InputHelper(window)

    temp_ui_text1 = UIText("Death weeks early had their and folly timed put. Hearted forbade on an village ye i"
                           "n fifteen. Age attended betrayed her man raptures la",
                           Vector2.zero, Vector2(300, 270), font_size=20, color=ColorHelper.BLACK)


    def change_text(o):
        o.set_text('Some other text')


    temp_ui_text2 = UIText("Instrument terminated of as astonished literature motionless admiration. ",
                           Vector2.zero, Vector2(400, 0), font_size=20, color=ColorHelper.WHITE)
    temp_ui_text2.on_click_down = lambda o, b: change_text(o)


    def test(o, color):
        o.color = color


    temp_base1 = UIBase(Vector2(100, 100), Vector2(300, 200), color=ColorHelper.GRAY)
    temp_base1.on_click_down = lambda o, b: test(o, ColorHelper.GREEN[:3])
    temp_base1.on_click_up = lambda o, b: test(o, ColorHelper.LIGHT_BLUE[:3])

    temp_container1 = ScrollableContainer(Vector2(600, 100), Vector2(300, 200))
    temp_container1.on_click_down = lambda o, b: (test(o, ColorHelper.LIGHT_BLUE[:3]), temp_container1.clear_children())
    temp_container1.color = ColorHelper.GREEN[:3]
    temp_container1.children_margin = Vector2(10, 10)
    temp_container1.add_child(UIBase(Vector2.zero, Vector2(50, 60), color=ColorHelper.BLACK))
    temp_container1.add_child(UIBase(Vector2.zero, Vector2(50, 50), color=ColorHelper.PINK))
    temp_container1.add_child(UIBase(Vector2.zero, Vector2(50, 60), color=ColorHelper.LIGHT_BLUE))
    temp_container1.add_child(UIBase(Vector2.zero, Vector2(50, 40), color=ColorHelper.YELLOW))

    temp_container1.add_child(temp_ui_text1)

    ui_invent = UIInventory(Vector2(0, 100), Vector2(400, 300))

    temp_sprite = UISprite("image.png", Vector2(610, 200), Vector2(120, 120), 3, 0, 8, Vector2(120, 120))
    temp_container1.add_child(temp_sprite)

    pyglet.clock.schedule_interval(window.update, 1.0 / float(configs.DESIRED_FPS))
    pyglet.app.run()
