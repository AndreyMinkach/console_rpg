from pyglet.gl import *

import configs
from Animation.storyboard import Storyboard
from Creatures.player import Player
from Creatures.zombie import Weapon
from Gameplay.Location.location_manager import LocationManager
from Gameplay.Quests.quest_manager import QuestManager
from Helpers.atlas_helper import TextureAtlas
from Helpers.color_helper import ColorHelper
from Helpers.hit_test import HitTest
from Helpers.input_helper import InputHelper
from Helpers.location_helper import Vector2
from Helpers.map_loader import MapLoader
from Helpers.shader_manager import ShaderManager
from Scene.camera import Camera
from Scene.renderer import Renderer
from Scene.scene_object import SceneObject
from UI.ui_renderer import UIRenderer
from UI.ui_base import UIBase
from UI.ui_button import UIButton
from UI.ui_scrollable_container import ScrollableContainer
from UI.ui_sprite import UISprite
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
    camera.set_zoom(15)
    map = MapLoader()
    temp_sprite = UISprite("cat_movement.png", Vector2(610, 200), Vector2(120, 120), 3, 0, 8, Vector2(120, 120), 4, 8,
                           scale=1.0)
    weapon = Player("cat_movement.png")
    pyglet.clock.schedule_interval(window.update, 1.0 / float(configs.DESIRED_FPS))
    pyglet.app.run()
