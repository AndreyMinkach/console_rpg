from pyglet.graphics import Batch, OrderedGroup
from UI.ui_base import *


class UISprite(UIBase):
    def __init__(self, image_path: str, position: Vector2, size: Vector2, row: int, col: int, frame_number: int,
                 sprite_size: Vector2, sheet_row: int, sheet_col: int, scale: float, frame_time: float = 0.1):
        super().__init__(position, size, tint_color=ColorHelper.TRANSPARENT)
        image = pyglet.image.load('Static/Images/' + image_path)
        sprite_grid = pyglet.image.ImageGrid(image, sheet_row, sheet_col, item_width=sprite_size.x,
                                             item_height=sprite_size.y)
        row_image_sprite_number = image.width // sprite_size.x
        col_image_sprite_number = image.height // sprite_size.y
        sprite_texture = pyglet.image.TextureGrid(sprite_grid)
        start_sprite = (row * row_image_sprite_number) + col
        sprite_animation = pyglet.image.Animation.from_image_sequence(
            sprite_texture[start_sprite: start_sprite + frame_number], frame_time, loop=True)
        self.sprite = pyglet.sprite.Sprite(sprite_animation, x=position.x, y=position.y, batch=self.batch,
                                           group=OrderedGroup(self.group.order + 1))
        self.sprite.update(scale=scale)

    @UIBase.batch.setter
    def batch(self, value: Batch):
        UIBase.batch.fset(self, value)
        self.sprite.batch = value

    @UIBase.group.setter
    def group(self, value: OrderedGroup):
        UIBase.group.fset(self, value)
        self.sprite.group = value

    @UIBase.position.setter
    def position(self, value: Vector2):
        UIBase.position.fset(self, value)
        self.sprite.x = value.x
        self.sprite.y = value.y

    def set_enabled(self, enable: bool):
        super().set_enabled(enable)
        self.sprite.batch = self.batch
