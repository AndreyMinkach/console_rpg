import pygame
import pygame.gfxdraw
import configs
from Helpers.color_helper import *
from UI.renderer import *

clock = pygame.time.Clock()
renderer = Renderer()


def main():
    pygame.init()
    pygame.display.set_caption(configs.WINDOW_TITLE)
    screen = pygame.display.set_mode((configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT))
    display_canvas = pygame.Surface((configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT))  # holds each ui object

    temp_ui_1 = UIBase(200, 20, 50, 50)
    temp_ui_1.fill(ColorHelper.LIGHT_BLUE)
    temp_ui_2 = UIBase(400, 20, 50, 50)
    temp_ui_2.fill(ColorHelper.YELLOW)
    renderer.add_ui_object(temp_ui_1)
    renderer.add_ui_object(temp_ui_2)

    while True:
        screen.fill(ColorHelper.WHITE)
        display_canvas.fill(ColorHelper.DARK)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

        renderer.update(display_canvas)

        screen.blit(display_canvas, (0, 0))
        pygame.display.update()
        clock.tick(configs.DESIRED_FPS)


if __name__ == "__main__":
    main()
