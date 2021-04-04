from pyglet.gl import *

import configs
from Animation.storyboard import Storyboard
from Gameplay.Location.location_manager import LocationManager
from Gameplay.Quests.quest_manager import QuestManager
from Helpers.color_helper import ColorHelper
from Helpers.hit_test import HitTest
from Helpers.input_helper import InputHelper
from Helpers.location_helper import Vector2
from Helpers.shader_manager import ShaderManager
from Scene.camera import Camera
from Scene.renderer import Renderer
from Scene.scene_object import SceneObject
from UI.ui_renderer import UIRenderer
from UI.ui_base import UIBase
from UI.ui_button import UIButton
from UI.ui_scrollable_container import ScrollableContainer
from UI.ui_sprite import UISprite
from UI.ui_text import UIText
from UI.window import MyWindow

ui_renderer = UIRenderer()
scene_renderer = Renderer()
storyboard = Storyboard()
quest_manager = QuestManager()
location_manager = LocationManager()

if __name__ == '__main__':
    window = MyWindow(configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT, caption=configs.WINDOW_TITLE, resizable=False,
                      vsync=True)
    hit_test = HitTest(window, UIRenderer.get_main_batch())
    input_helper = InputHelper(window)
    camera = Camera(window)
    camera.set_zoom(5)

    temp_sprite = UISprite("image.png", Vector2(610, 200), Vector2(120, 120), 3, 0, 8, Vector2(120, 120), 4, 8,
                           scale=1.0)

    # temp = UIBase(Vector2(610, 200), Vector2(120, 120), image_fill_color=ColorHelper.RED)

    pyglet.clock.schedule_interval(window.update, 1.0 / float(configs.DESIRED_FPS))
    pyglet.app.run()
