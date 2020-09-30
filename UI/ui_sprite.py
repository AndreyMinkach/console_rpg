import time

from UI.ui_base import *


class UISprite(UIBase):
    def __init__(self, image_path: str, position: Vector2, size: Vector2, row: int, col: int, frame_number: int,
                 sprite_height: int, sprite_width: int):
        super().__init__(position, size, transparent=False)
        image = pyglet.image.load('Static/Images/' + image_path)
        sprite_grid = pyglet.image.ImageGrid(image, 4, 8, item_width=sprite_width, item_height=sprite_height)
        row_image_sprite_number = image.width // sprite_width
        col_image_sprite_number = image.height // sprite_height
        sprite_texture = pyglet.image.TextureGrid(sprite_grid)
        start_sprite = (row * row_image_sprite_number) + col
        sprite_animation = pyglet.image.Animation.from_image_sequence(
            sprite_texture[start_sprite: start_sprite + frame_number], 0.1, loop=True)
        self.sprite = pyglet.sprite.Sprite(sprite_animation, x=position.x, y=position.y)

    def update_and_draw(self):
        self.sprite.draw()
