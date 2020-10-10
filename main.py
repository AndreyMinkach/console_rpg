
from Animation.storyboard import Storyboard
from Gameplay.Dialogues.dialogue_manager import DialogManager
from Gameplay.Quests.quest_manager import QuestManager
from Gameplay.inventory import Inventory
from Helpers.color_helper import ColorHelper
from Helpers.input_helper import InputHelper
from Helpers.location_helper import Vector2
from Items.items_loader import ItemLoader
from UI.renderer import Renderer
from UI.ui_base import UIBase
from UI.ui_button import UIButton
from UI.ui_dialog import UIDialogue
from UI.ui_inventory import UIInventory
from UI.ui_scrollable_container import ScrollableContainer
from UI.ui_sprite import UISprite
from UI.ui_text import UIText
from UI.window import MyWindow
from pyglet.gl import *
import configs

renderer = Renderer()
storyboard = Storyboard()
quest_manager = QuestManager()
dialogue_manager = DialogManager()

if __name__ == '__main__':
    window = MyWindow(configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT, caption=configs.WINDOW_TITLE, resizable=True,
                      vsync=True)

    input_helper = InputHelper(window)

    # dialog = dialogue_manager.get_dialog_by_interlocutor('Name1')
    # dialog.chose_phrase('0')
    # temp_ui_text1 = UIText("Death weeks early had ", Vector2.zero, Vector2(300, 270))

    # temp_ui_button1 = UIButton("Instrument terminated of as astonished literature motionless admiration.",
    #                            Vector2(420, 350), Vector2(200, 60), color=(40, 50, 70, 255),
    #                            hover_color=(200, 50, 70, 255),
    #                            document_style=dict(color=(255, 255, 255, 255), align='center'))
    # temp_ui_button1.size = Vector2(300, 80)

    # temp_container1 = ScrollableContainer(Vector2(600, 100), Vector2(300, 200))
    # temp_container1.color = ColorHelper.GREEN[:3]
    # temp_container1.children_margin = Vector2(10, 10)
    # temp_container1.add_child(UIBase(Vector2.zero, Vector2(50, 60), color=ColorHelper.BLACK))
    # temp_container1.add_child(UIBase(Vector2.zero, Vector2(50, 50), color=ColorHelper.PINK))
    # temp_container1.add_child(UIBase(Vector2.zero, Vector2(50, 60), color=ColorHelper.LIGHT_BLUE))
    # temp_container1.add_child(UIBase(Vector2.zero, Vector2(50, 40), color=ColorHelper.YELLOW))
    # temp_container1.add_child(temp_ui_button1)

    # temp_container1.add_child(temp_ui_text1)
    enemy_invent = Inventory()
    all_items = ItemLoader()
    weapon2 = all_items.get_item_by_id(2)
    weapon1 = all_items.get_item_by_id(1)

    outfit3 = all_items.get_item_by_id(52)
    enemy_invent.add_item(weapon1)
    enemy_invent.add_item(outfit3)
    enemy_invent.add_item(weapon2)
    enemy_invent.add_item(outfit3)

    ui_invent = UIInventory(Vector2(10, 150), Vector2(400, 300), enabled=False)
    # ui_invent.show_inventory(enemy_invent)

    ui_dialogue = UIDialogue(Vector2(10, 10), Vector2(500, 130), 'Name')

    # temp_sprite = UISprite("image.png", Vector2(610, 200), Vector2(120, 120), 3, 0, 8, Vector2(120, 120), 4, 8,
    #                       scale=1.0)
    # temp_container1.add_child(temp_sprite)

    pyglet.clock.schedule_interval(window.update, 1.0 / float(configs.DESIRED_FPS))
    pyglet.app.run()
