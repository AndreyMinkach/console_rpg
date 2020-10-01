from UI.ui_base import *


class UISprite(UIBase):
    def __init__(self, image_path: str, position: Vector2, size: Vector2, row: int, col: int, frame_number: int,
                 sprite_size: Vector2):
        super().__init__(position, size, transparent=True)
        image = pyglet.image.load('Static/Images/' + image_path)
        sprite_grid = pyglet.image.ImageGrid(image, 4, 8, item_width=sprite_size.x, item_height=sprite_size.y)
        row_image_sprite_number = image.width // sprite_size.x
        col_image_sprite_number = image.height // sprite_size.y
        sprite_texture = pyglet.image.TextureGrid(sprite_grid)
        start_sprite = (row * row_image_sprite_number) + col
        sprite_animation = pyglet.image.Animation.from_image_sequence(
            sprite_texture[start_sprite: start_sprite + frame_number], 0.1, loop=True)
        self.sprite = pyglet.sprite.Sprite(sprite_animation, x=position.x, y=position.y)

    @UIBase.position.setter
    def position(self, value: Vector2):
        UIBase.position.fset(self, value)
        self.sprite.x = value.x
        self.sprite.y = value.y

    def update_logic(self):
        super().update_logic()
        self.sprite.draw()
