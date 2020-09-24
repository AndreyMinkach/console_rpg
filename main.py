import configs
from Gameplay.Quests.quest_manager import QuestManager
from Helpers.color_helper import ColorHelper
from Helpers.window_event_helper import EventHelper
from UI.renderer import *
from UI.ui_scrollable_container import ScrollableContainer
from UI.ui_sprite import UIBase, UISprite
from UI.ui_text import UIText

clock = pygame.time.Clock()
renderer = Renderer()
event_helper = EventHelper()
storyboard = Storyboard()

quest_manager = QuestManager()


def main():
    pygame.init()
    pygame.display.set_caption(configs.WINDOW_TITLE)
    screen = pygame.display.set_mode((configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT))
    display_canvas = pygame.Surface((configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT))  # holds each ui object

    temp_ui_1 = UIBase(Vector2(200, 20), Vector2(50, 50))
    temp_ui_1.fill(ColorHelper.LIGHT_BLUE)
    temp_ui_2 = UIBase(Vector2(400, 20), Vector2(50, 50))
    temp_ui_2.fill(ColorHelper.YELLOW)

    temp_scroll_container = ScrollableContainer(Vector2(20, 50), Vector2(80, 200))
    temp_scroll_container.children_margin = Vector2(10, 10)

    quest_manager.set_quest_variable('temp_quest_start_condition', True)
    quest_manager.update()
    quest_manager.set_quest_variable('some_activator1', True)
    quest_manager.update()

    dialog = [
        "на сервисе у вас будут расширены ограничения проверки, предназначенные для гостей, и вы получите возможность проверять гораздо большее количество текстов с помощью нашего сервиса плагиат онлайн.",
        "hello dude", "LOH"]
    temp_ui_dialog = ScrollableContainer(Vector2(100, 300), Vector2(760, 150))
    temp_ui_dialog.add_child(UIText(Vector2.zero, Vector2(760, 30), dialog[0], ColorHelper.GREEN))
    temp_ui_dialog.add_child(UIText(Vector2.zero, Vector2(760, 30), dialog[1], ColorHelper.WHITE))
    temp_ui_dialog.add_child(UIText(Vector2.zero, Vector2(760, 30), dialog[2], ColorHelper.LIGHT_BLUE))

    temp_child_1 = UIBase(Vector2.zero, Vector2(30, 30))
    temp_child_1.fill(ColorHelper.LIGHT_BLUE)
    temp_child_2 = UIBase(Vector2.zero, Vector2(30, 50))
    temp_child_2.fill(ColorHelper.GREEN)
    temp_child_3 = UIBase(Vector2.zero, Vector2(30, 80))
    temp_child_3.fill(ColorHelper.PINK)
    temp_child_4 = UIBase(Vector2.zero, Vector2(30, 40))
    temp_child_4.fill(ColorHelper.WHITE)
    temp_scroll_container.add_child(temp_child_1)
    temp_scroll_container.add_child(temp_child_2)
    temp_scroll_container.add_child(temp_child_3)
    temp_scroll_container.add_child(temp_child_4)

    temp_sprite = UISprite(Vector2(120, 120),
                           r"UI\image.png",
                           Vector2(120, 120), 0.2, 7, 0, 0)
    renderer.add_ui_object(temp_sprite)

    temp_ui_1.fade_in(7)

    temp_ui_2.on_mouse_enter = lambda o: o.fill(ColorHelper.LIGHT_BLUE)
    temp_ui_2.on_mouse_leave = lambda o: o.fill(ColorHelper.YELLOW)
    temp_ui_2.on_click_down = lambda o, b: o.fill(ColorHelper.GREEN)
    temp_ui_2.on_click_up = lambda o, b: o.fill(ColorHelper.PINK)

    temp_ui_3 = UIBase(Vector2(400, 100), Vector2(350, 150))
    temp_ui_3.fill(ColorHelper.PINK)
    temp_ui_4 = UIBase(Vector2(10, 10), Vector2(200, 50))
    temp_ui_4.fill(ColorHelper.GREEN)
    temp_ui_3.children.append(temp_ui_4)

    renderer.add_ui_object(temp_ui_1)
    renderer.add_ui_object(temp_ui_2)
    renderer.add_ui_object(temp_ui_3)

    renderer.add_ui_object(temp_scroll_container)
    renderer.add_ui_object(temp_ui_dialog)

    while not event_helper.should_quit:
        screen.fill(ColorHelper.BLACK)
        display_canvas.fill(ColorHelper.DARK)

        event_helper.update()
        storyboard.update()

        quest_manager.update()

        renderer.update(display_canvas)
        screen.blit(display_canvas, (0, 0))

        pygame.display.update()
        clock.tick(configs.DESIRED_FPS)


if __name__ == "__main__":
    main()
