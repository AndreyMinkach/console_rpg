from pyglet.image import Animation, AnimationFrame, TextureRegion, pyglet


def get_animation(images: list, durations: list) -> Animation:
    return Animation([AnimationFrame(images[i], durations[i]) for i in range(len(images))])


def get_animation_from_sprite_grid(sprite_image: TextureRegion, sprite_row: int, frame_width: int, frame_height: int,
                                   frames_count: int, frame_time: float = 0.1, loop=True):
    sprite_grid = pyglet.image.ImageGrid(
        image=sprite_image, rows=sprite_image.height // frame_height, columns=sprite_image.width // frame_width,
        item_width=frame_width, item_height=frame_height
    )
    sprite_texture = pyglet.image.TextureGrid(sprite_grid)
    start_sprite = (sprite_row * sprite_image.width // frame_width)
    q = sprite_texture[start_sprite: start_sprite + frames_count]
    sprite_animation = pyglet.image.Animation.from_image_sequence(
        sprite_texture[start_sprite: start_sprite + frames_count], frame_time, loop=loop)
    return sprite_animation
