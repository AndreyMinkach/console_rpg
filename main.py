from pyglet.gl import *

import configs
from Animation.storyboard import Storyboard
from Gameplay.Location.location_manager import LocationManager
from Gameplay.Quests.quest_manager import QuestManager
from Helpers.color_helper import ColorHelper
from Helpers.hit_test import HitTest
from Helpers.input_helper import InputHelper
from Helpers.location_helper import Vector2
from UI.renderer import Renderer
from UI.ui_button import UIButton
from UI.ui_scrollable_container import ScrollableContainer
from UI.ui_sprite import UISprite
from UI.ui_text import UIText
from UI.window import MyWindow

renderer = Renderer()
storyboard = Storyboard()
quest_manager = QuestManager()
location_manager = LocationManager()

if __name__ == '__main__':
    window = MyWindow(configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT, caption=configs.WINDOW_TITLE, resizable=False,
                      vsync=False)
    hit_test = HitTest(window, Renderer.get_main_batch())
    input_helper = InputHelper(window)

    image = Renderer.load_image('basic_white_image.png')

    some_text = UIText("Somebody once told me the world is gonna roll me...", Vector2(500, 100), Vector2(200, 250),
                       tint_color=ColorHelper.GREEN)
    some_button = UIButton("Somebody once told me the world is gonna roll me...", Vector2(100, 300), Vector2(200, 300),
                           tint_color=ColorHelper.PINK, hover_color=ColorHelper.RED)
    temp_sprite = UISprite("image.png", Vector2(610, 200), Vector2(120, 120), 3, 0, 8, Vector2(120, 120), 4, 8,
                           scale=1.0)

    some_container = ScrollableContainer(Vector2(100, 100), Vector2(300, 420), children_margin=Vector2(10, 10))
    some_container.add_child(some_text)
    some_container.add_child(some_button)
    some_container.add_child(temp_sprite)

    pyglet.clock.schedule_interval(window.update, 1.0 / float(configs.DESIRED_FPS))
    pyglet.app.run()
