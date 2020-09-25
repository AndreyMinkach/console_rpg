import time

from UI.ui_base import *


class UISprite(UIBase):
    def __init__(self, position: Vector2, filename: str, sprite_size: Vector2,
                 sprite_frame_time: float, sprite_count: int, row: int, column: int):
        try:
            self.sprite_size = sprite_size
            self.sheet = pygame.image.load(filename)
            self.sprite_count = sprite_count
            self.sprite_frame_time = sprite_frame_time
            self.time_to_change_sprite = float(time.time()) + self.sprite_frame_time
            self.current_sprite_index = 0
            self.row = row
            self.column = column
        except AttributeError:
            print(f"Unable to load sprite sheet image: {filename}")
        super().__init__(position, Vector2(self.sheet.get_size()[0], self.sheet.get_size()[1]))

    def cut_image(self, rectangle, color_key: (int, int, int) = ColorHelper.BLACK):
        """Load a specific image from a specific rectangle."""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey(color_key)
        return image

    def cut_images_from_list(self, list_of_rect, color_key: (int, int, int)):
        """Load a whole bunch of images and return them as a list."""
        return [self.cut_image(rect, color_key) for rect in list_of_rect]

    def get_list_of_sprites(self, sprite_rect, image_count, color_key: (int, int, int)):
        """Load a whole strip of images, and return them as a list."""
        list_of_rect = [(sprite_rect[0] + sprite_rect[2] * x, sprite_rect[1], sprite_rect[2], sprite_rect[3])
                        for x in range(image_count)]
        return self.cut_images_from_list(list_of_rect, color_key)

    def update(self, display_canvas: Surface):
        if self.current_sprite_index == self.sprite_count + 1:
            self.current_sprite_index = 0
        if time.time() - self.time_to_change_sprite >= self.sprite_frame_time:
            self.time_to_change_sprite += self.sprite_frame_time
            current_rect = pygame.Rect(self.sprite_size.x * self.current_sprite_index + self.column * self.sprite_size.x,
                                       self.row * self.sprite_size.y,
                                       self.sprite_size.x,
                                       self.sprite_size.y)
            self.current_sprite_index += 1
        else:
            current_rect = pygame.Rect(
                self.sprite_size.x * self.current_sprite_index + self.column * self.sprite_size.x,
                self.row * self.sprite_size.y,
                self.sprite_size.x,
                self.sprite_size.y)
        display_canvas.blit(self.cut_image(current_rect), (self.position.x, self.position.y))
