from pyglet.gl import *
from pyglet.graphics import OrderedGroup

import configs
from Animation.storyboard import Storyboard
from Gameplay.Location.location_manager import LocationManager
from Gameplay.Quests.quest_manager import QuestManager
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
quest_manager = QuestManager()
location_manager = LocationManager()

temp_location = LocationManager.instance.get_location_by_name("The Deepest Hole")
print('location: ', temp_location.__dict__)
temp_point = temp_location.get_location_point("0")
print('point: ', temp_point)


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
        renderer._ui_object_list[0].children_batch.draw()

    def update(self, dt):
        renderer.update_logic()

        # input helper should be updated after all other logic
        InputHelper.instance.update()
        self.total_ticks += 1
        if self.total_ticks > 1000:
            self.total_ticks -= 1000


if __name__ == '__main__':
    window = MyWindow(configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT, caption=configs.WINDOW_TITLE, resizable=False,
                      vsync=True)
    input_helper = InputHelper(window)

    temp_ui1 = UIBase(Vector2(100, 100), Vector2(600, 500))
    temp_ui2 = UIBase(Vector2(300, 150), Vector2(50, 50))
    temp_ui2.color = (255, 0, 0)
    temp_ui3 = UIBase(Vector2(450, 300), Vector2(50, 50))
    temp_ui3.color = (255, 50, 200)

    temp_ui1.add_child(temp_ui2)
    temp_ui1.add_child(temp_ui3)

    pyglet.clock.schedule_interval(window.update, 1.0 / float(configs.DESIRED_FPS))
    pyglet.app.run()
