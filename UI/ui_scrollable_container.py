from pygame import Surface

from Helpers.color_helper import ColorHelper
from Helpers.input_helper import InputHelper
from Helpers.location_helper import Vector2
from UI.ui_base import UIBase
from UI.ui_text import UIText


class ScrollableContainer(UIBase):
    def __init__(self, position: Vector2, size: Vector2):
        super().__init__(position, size)
        self.children_margin = Vector2.zero
        self._viewer_extent = Vector2.zero  # the total area occupied by all child elements
        self._vertical_offset = 0
        self._offset_value = 30
        self._children = []
        # super().set_colorkey(ColorHelper.BLACK)  # makes the container transparent

    def add_child(self, child: UIBase):
        child.parent = self
        self._children.append(child)
        self.calculate_viewer_extent()

    def add_from_string_list(self, position: Vector2, size: Vector2, string_list: list,
                             foreground: (int, int, int), font_size: int = 25, font_name: str = None):
        for sting in string_list:
            self.add_child(UIText(position, size, sting, foreground, font_size, font_name))

    def clear_children(self):
        self._children.clear()

    def remove_child(self, child: UIBase):
        child.parent = None
        self._children.remove(child)
        self.calculate_viewer_extent()

    def calculate_viewer_extent(self):
        extent_x, extent_y = (0, 0)
        child_number = len(self._children)
        for child in self._children:
            extent_x = max(child.size.x, extent_x)
            extent_y += child.size.y
        self._viewer_extent = Vector2(extent_x, extent_y + self.children_margin.y * child_number)

    def update(self, display_canvas: Surface):
        super().update(display_canvas)
        self.fill(ColorHelper.BLACK)
        self._update_scroll()

        viewer_height = 0  # stores a total height of viewer as if the children were placed one behind the other
        for i in range(len(self._children)):
            child = self._children[i]
            if isinstance(child, UIBase):
                viewer_height += self.children_margin.y
                child.position = Vector2(self.children_margin.x, viewer_height + self._vertical_offset)
                child.update(self)
                viewer_height += child.size.y

    def _update_scroll(self):
        mouse_pos = InputHelper.instance.mouse_position
        is_cursor_inside = self.is_point_inside(mouse_pos)
        if is_cursor_inside:
            self._vertical_offset += InputHelper.instance.mouse_wheel_delta * self._offset_value
            self._vertical_offset = max(min(0, self.size.y - self._viewer_extent.y - self.children_margin.y),
                                        min(self._vertical_offset, 0))
