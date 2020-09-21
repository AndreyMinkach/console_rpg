from pydoc import locate

import configs
from Helpers.color_helper import ColorHelper
from Helpers.window_event_helper import EventHelper
from UI.renderer import *
from UI.ui_scrollable_container import ScrollableContainer

clock = pygame.time.Clock()
renderer = Renderer()
event_helper = EventHelper()
storyboard = Storyboard()


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

    temp_ui_1.fade_in(7)

    renderer.add_ui_object(temp_ui_1)
    renderer.add_ui_object(temp_ui_2)
    renderer.add_ui_object(temp_scroll_container)

    while not event_helper.should_quit:
        screen.fill(ColorHelper.BLACK)
        display_canvas.fill(ColorHelper.DARK)

        event_helper.update()
        storyboard.update()

        renderer.update(display_canvas)
        screen.blit(display_canvas, (0, 0))

        pygame.display.update()
        clock.tick(configs.DESIRED_FPS)


if __name__ == "__main__":
    main()
