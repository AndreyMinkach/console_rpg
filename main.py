from pyglet.gl import *
from pyglet.graphics import OrderedGroup

import configs
from Animation.storyboard import Storyboard
from Gameplay.inventory import Inventory
from Helpers.color_helper import ColorHelper
from Helpers.input_helper import InputHelper
from Helpers.location_helper import Vector2
from Items.items_loader import ItemLoader
from UI.renderer import Renderer
from UI.ui_base import UIBase
from UI.ui_button import UIButton
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

    def on_activate(self):
        glClearColor(*[i / 255.0 for i in ColorHelper.DARK])
        glEnable(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    def on_draw(self):
        self.clear()
        renderer.draw()

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

    temp_ui_text1 = UIText("Death weeks early had ", Vector2.zero, Vector2(300, 270))

    temp_ui_button1 = UIButton("Instrument terminated of as astonished literature motionless admiration.",
                               Vector2(420, 350), Vector2(200, 60), color=(40, 50, 70, 255),
                               hover_color=(200, 50, 70, 150),
                               document_style=dict(color=(255, 255, 255, 255), align='center'))
    temp_ui_button1.size = Vector2(300, 80)

    temp_container1 = ScrollableContainer(Vector2(600, 100), Vector2(300, 200))
    temp_container1.color = ColorHelper.GREEN[:3]
    temp_container1.children_margin = Vector2(10, 10)
    temp_container1.add_child(UIBase(Vector2.zero, Vector2(50, 60), color=ColorHelper.BLACK))
    temp_container1.add_child(UIBase(Vector2.zero, Vector2(50, 50), color=ColorHelper.PINK))
    temp_container1.add_child(UIBase(Vector2.zero, Vector2(50, 60), color=ColorHelper.LIGHT_BLUE))
    temp_container1.add_child(UIBase(Vector2.zero, Vector2(50, 40), color=ColorHelper.YELLOW))

    temp_container1.add_child(temp_ui_text1)
    enemy_invent = Inventory()
    all_items = ItemLoader()
    weapon2 = all_items.get_item_by_id(2)
    weapon1 = all_items.get_item_by_id(1)

    outfit3 = all_items.get_item_by_id(52)
    enemy_invent.add_item(weapon1)
    enemy_invent.add_item(outfit3)
    enemy_invent.add_item(weapon2)
    enemy_invent.add_item(outfit3)

    ui_invent = UIInventory(Vector2(10, 100), Vector2(400, 300), enemy_invent)

    temp_sprite = UISprite("image.png", Vector2(610, 200), Vector2(120, 120), 3, 0, 8, Vector2(120, 120), 4, 8,
                           scale=1.0)
    temp_container1.add_child(temp_sprite)

    temp_base1 = UIBase(Vector2(0, 420), Vector2(120, 50), color=ColorHelper.GRAY)

    pyglet.clock.schedule_interval(window.update, 1.0 / float(configs.DESIRED_FPS))
    pyglet.app.run()
