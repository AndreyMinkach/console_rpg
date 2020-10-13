from random import randint

from pyglet.gl import *

import configs
from Animation.storyboard import Storyboard
from Gameplay.Location.location_manager import LocationManager
from Gameplay.Quests.quest_manager import QuestManager
from Gameplay.inventory import Inventory
from Helpers.color_helper import ColorHelper
from Helpers.hit_test import HitTest
from Helpers.input_helper import InputHelper
from Helpers.location_helper import Vector2
from UI.renderer import Renderer
from UI.ui_base import UIBase
from UI.ui_button import UIButton
from UI.ui_inventory import UIInventory
from UI.ui_scrollable_container import ScrollableContainer
from UI.ui_sprite import UISprite
from UI.ui_text import UIText
from UI.window import MyWindow

renderer = Renderer()
storyboard = Storyboard()
quest_manager = QuestManager()
location_manager = LocationManager()

temp_location = LocationManager.instance.get_location_by_name("The Deepest Hole")
print('location: ', temp_location.__dict__)
temp_point = temp_location.get_location_point("0")
print('point: ', temp_point)

if __name__ == '__main__':
    window = MyWindow(configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT, caption=configs.WINDOW_TITLE, resizable=False,
                      vsync=True)
    hit_test = HitTest(window)
    input_helper = InputHelper(window)

    temp = UIBase(Vector2.one * 100, Vector2(900, 400), tint_color=(255, 100, 0))

    pyglet.clock.schedule(window.update)
    pyglet.app.run()
