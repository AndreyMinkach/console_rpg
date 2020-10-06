from pyglet import gl
from pyglet.graphics import Batch, OrderedGroup

from Helpers.input_helper import InputHelper
from Helpers.location_helper import Vector2
from UI.renderer import Renderer
from UI.ui_base import UIBase


class ScrollableContainer(UIBase):
    def __init__(self, position: Vector2, size: Vector2, offset_value=30):
        super().__init__(position, size)
        Renderer.instance.remove_ui_object(self)
        Renderer.instance.add_ui_object_scissor(self)

        self.children_margin = Vector2.zero
        self._child_batch = Batch()
        self._child_group = OrderedGroup(self.group.order + 1)
        self._viewer_extent = Vector2.zero  # the total area occupied by all child elements
        self._vertical_offset = 0
        self._offset_value = offset_value
        self._children = []
        self._was_scissor_enabled = False

    def _enable_scissor_test(self):
        gl.glPushAttrib(gl.GL_ENABLE_BIT | gl.GL_TRANSFORM_BIT | gl.GL_CURRENT_BIT)
        self._was_scissor_enabled = gl.glIsEnabled(gl.GL_SCISSOR_TEST)
        gl.glEnable(gl.GL_SCISSOR_TEST)
        gl.glScissor(int(self.x), int(self.y), int(self.width), int(self.height))

    def _disable_scissor_test(self):
        if not self._was_scissor_enabled:
            gl.glDisable(gl.GL_SCISSOR_TEST)
        gl.glPopAttrib()

    def add_child(self, child: UIBase):
        child.parent = self
        child.batch = self._child_batch
        child.group = self._child_group
        self._children.append(child)
        self._calculate_viewer_extent()

    def remove_child(self, child: UIBase):
        self._remove_child(child)

    def _remove_child(self, child: UIBase, only_detach: bool = False):
        child.parent = None
        child.batch = Renderer.instance.get_batch()
        child.group = Renderer.instance.get_main_group()
        if not only_detach:
            self._children.remove(child)
        self._calculate_viewer_extent()

    def clear_children(self):
        for child in self._children:
            self._remove_child(child, True)
        self._children.clear()

    def delete_children(self):
        for child in self._children:
            child.batch = None
            child.group = None
        self._children.clear()
        del self._children[:]

    def _calculate_viewer_extent(self):
        extent_x, extent_y = (0, 0)
        child_number = len(self._children)
        for child in self._children:
            extent_x = max(child.size.x, extent_x)
            extent_y += child.size.y
        self._viewer_extent = Vector2(extent_x, extent_y + self.children_margin.y * child_number)
        self._vertical_offset = self.size.y - self._viewer_extent.y - self.children_margin.y

    def update_logic(self, **kwargs):
        self._enable_scissor_test()
        super().update_logic()
        self._update_scroll()

        viewer_height = 0  # stores a total height of viewer as if the children were placed one behind the other
        for i in range(len(self._children) - 1, -1, -1):
            child = self._children[i]
            if isinstance(child, UIBase):
                viewer_height += self.children_margin.y
                child.position = self.position + Vector2(self.children_margin.x, viewer_height + self._vertical_offset)
                child.update_logic()
                viewer_height += child.size.y

        self._child_batch.draw()

        self._disable_scissor_test()

    def _update_scroll(self):
        mouse_pos = InputHelper.instance.get_mouse_pos()
        is_cursor_inside = self.is_point_inside(mouse_pos)
        if is_cursor_inside:
            self._vertical_offset += -InputHelper.instance.get_mouse_scroll() * self._offset_value
            self._vertical_offset = max(self.size.y - self._viewer_extent.y - self.children_margin.y,
                                        min(self._vertical_offset, 0))
