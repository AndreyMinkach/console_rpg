import pyglet
from pyglet.window import key, mouse
from pyglet.gl import *

import configs


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)
        self.sprite1 = pyglet.sprite.Sprite(pyglet.resource.image('Static/Images/basic_white_image.png'), x=0, y=0)
        self.sprite1.scale = 300 / self.sprite1.width
        self.sprite2 = pyglet.sprite.Sprite(pyglet.resource.image('Static/Images/basic_white_image_2.png'), x=300, y=0)
        self.sprite1.opacity = 255

    def on_activate(self):
        glClearColor(0.2, 0.2, 0.2, 0)
        glEnable(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    def on_key_press(self, symbol, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        print(f"{x, y}: {button}")

    def on_draw(self):
        self.clear()

        # self.sprite2.scale += 0.01

        self.sprite2.draw()

        self.sprite1.draw()

    def update(self, dt):
        pass


if __name__ == '__main__':
    window = MyWindow(configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT, caption=configs.WINDOW_TITLE, resizable=True,
                      vsync=True)
    pyglet.clock.schedule_interval(window.update, 1.0 / float(configs.DESIRED_FPS))
    pyglet.app.run()
