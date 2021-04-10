from pyglet.image import Animation, AnimationFrame


def get_animation(images: list, durations: list) -> Animation:
    return Animation([AnimationFrame(images[i], durations[i]) for i in range(len(images))])
