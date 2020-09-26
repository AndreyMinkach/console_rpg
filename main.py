import pyglet
from pyglet.window import key, mouse
from pyglet.gl import *


class Triangle:
    def __init__(self):
        self.vertices = pyglet.graphics.vertex_list(3, ('v3f', [-0.5, -0.5, 0.0, 0.5, -0.5, 0.0, 0.0, 0.5, 0.0]),
                                                    ('c3b', [100, 200, 220, 200, 110, 100, 100, 250, 100]))


triangle = Triangle()


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(400, 300)

    def on_activate(self):
        self.set_caption("Not a console RPG")
        self.set_vsync(True)

    def on_close(self):
        print('close')

    def on_key_press(self, symbol, modifiers):
        if symbol == key.A:
            print('A')

    def on_mouse_press(self, x, y, button, modifiers):
        print(f"({x, y}): {button}")

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)

    def on_draw(self):
        window.clear()
        triangle.vertices.draw(GL_TRIANGLES)
        # window.flip()


if __name__ == '__main__':
    window = MyWindow(1280, 620, caption="Not a console game", resizable=True)
    pyglet.app.run()
