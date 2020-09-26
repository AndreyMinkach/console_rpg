import pyglet
from pyglet.window import key, mouse

window = pyglet.window.Window(1280, 620)


@window.event
def on_activate():
    window.set_caption("Not a console RPG")
    window.set_vsync(True)


@window.event
def on_close():
    print('close')


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.A:
        print('A')


@window.event
def on_mouse_press(x, y, button, modifiers):
    print(f"({x, y}): {button}")


@window.event
def on_draw():
    window.clear()
    pyglet.graphics.draw(2, pyglet.gl.GL_POINTS,
                         ('v2i', (10, 15, 30, 35))
                         )
    window.flip()


if __name__ == '__main__':
    pyglet.app.run()
