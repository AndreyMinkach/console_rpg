from pyglet.gl import *
import configs
from Animation.storyboard import Storyboard
from Gameplay.Dialogues.dialogue_manager import DialogManager
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
from UI.ui_dialog import UIDialog
from UI.ui_inventory import UIInventory
from UI.ui_scrollable_container import ScrollableContainer
from UI.ui_sprite import UISprite
from UI.ui_text import UIText
from UI.window import MyWindow

renderer = Renderer()
storyboard = Storyboard()
quest_manager = QuestManager()
location_manager = LocationManager()
dialog_manager = DialogManager()

if __name__ == '__main__':
    window = MyWindow(configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT, caption=configs.WINDOW_TITLE, resizable=False,
                      vsync=True)
    hit_test = HitTest(window)
    input_helper = InputHelper(window)
    quest_manager.start_quest('my_temp_quest')
    quest_manager.set_quest_variable('temp_quest_start_condition', True)
    UIDialog(Vector2.zero, Vector2(500, 200), 'Name')

    # q = UIText('asd', Vector2.zero, Vector2(100, 200))

    temp_sprite = UISprite("image.png", Vector2(610, 200), Vector2(120, 120), 3, 0, 8, Vector2(120, 120), 4, 8,
                          scale=1.0)

    pyglet.clock.schedule(window.update)
    pyglet.app.run()
