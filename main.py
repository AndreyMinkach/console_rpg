from pyglet.gl import *

import configs
from Animation.storyboard import Storyboard
from Gameplay.Location.location_manager import LocationManager
from Gameplay.Quests.quest_manager import QuestManager
from Helpers.hit_test import HitTest
from Helpers.input_helper import InputHelper
from Helpers.location_helper import Vector2
from Helpers.map_loader import MapLoader
from Scene.camera import Camera
from Scene.lighting import Lighting, Light
from Scene.renderer import Renderer
from Scene.scene_object import SceneObject
from Scene.spatial_hash import SpatialHash
from UI.ui_renderer import UIRenderer
from UI.ui_sprite import UISprite, TextureAtlas
from UI.window import MyWindow

ui_renderer = UIRenderer()
scene_renderer = Renderer()
storyboard = Storyboard()
quest_manager = QuestManager()
location_manager = LocationManager()

if __name__ == '__main__':
    window = MyWindow(configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT, caption=configs.WINDOW_TITLE, resizable=False,
                      vsync=False)
    configs.set_window(window)
    hit_test = HitTest(window, UIRenderer.get_main_batch())
    input_helper = InputHelper(window)
    camera = Camera(window, zoom=10)
    # map_loader = MapLoader()
    Lighting(*configs.get_window_size().tuple(), camera_lighting_zoom=15)
    SpatialHash(Vector2(100, 100), Vector2(5, 5))

    # configs.set_window_size(500, 500)
    # Lighting.set_resolution(1024, 1024)
    # Lighting.set_resolution(512, 512)

    import math

    window.object_list = []
    window.angle_list = []

    for angle in range(0, 359, 30):
        angle_radians = math.radians(angle)
        x = math.cos(angle_radians) * 4
        y = math.sin(angle_radians) * 4
        scene_object1 = SceneObject(None, (x, y))
        scene_object1.create_hitbox(shadow_caster=True)
        scene_object1.color = (0.5, 1.0, 1.0) if len(window.object_list) % 2 == 0 else (1.0, 0.5, 0.5)
        window.angle_list.append(angle)
        window.object_list.append(scene_object1)

    for _ in range(1):
        window.light1 = Light(Vector2(6, 3))
        window.light2 = Light(Vector2(-6, 3))
        window.light3 = Light(Vector2(6, -3))
        window.light4 = Light(Vector2(-6, -3))

    from timeit import timeit

    # test1 = Camera.world_to_screen(1, 1)
    # test2 = Camera.world_to_screen1(1, 1)
    # test3 = Camera.screen_to_world(1, 1)
    # test4 = Camera.screen_to_world1(1, 1)
    #
    # temp1 = timeit(lambda: Camera.world_to_screen(1, 1), number=100000)
    # temp2 = timeit(lambda: Camera.world_to_screen1(1, 1), number=100000)
    # temp3 = timeit(lambda: Camera.screen_to_world(1, 1), number=100000)
    # temp4 = timeit(lambda: Camera.screen_to_world1(1, 1), number=100000)

    temp_sprite = UISprite("image.png", Vector2(200, 200), Vector2(120, 120), 3, 0, 8, Vector2(120, 120), 4, 8,
                           scale=1.0)

    pyglet.clock.schedule_interval(window.update, 1.0 / float(configs.DESIRED_FPS))
    pyglet.app.run()
