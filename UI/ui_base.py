import warnings
from typing import List

import pyglet
from pyglet.gl import *
from pyglet.graphics import Batch, OrderedGroup
from pyglet.image import AbstractImage
from pyglet.sprite import Sprite, SpriteGroup
from pyshaders import ShaderProgram

from Animation.number_field_animation import NumberFieldAnimation
from Animation.storyboard import Storyboard
from Helpers.color_helper import ColorHelper
from Helpers.hit_test import HitTest
from Helpers.location_helper import Vector2
from Helpers.shader_manager import ShaderManager
from UI.ui_renderer import UIRenderer


class ScissorGroup(OrderedGroup):
    def __init__(self, x, y, width, height, order, parent=None):
        super().__init__(order=order, parent=parent)
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.order = order

    @property
    def area(self):
        return self.x, self.y, self.width, self.height

    @area.setter
    def area(self, area):
        self.x, self.y, self.width, self.height = area

    def set_state(self):
        super().set_state()
        glEnable(GL_SCISSOR_TEST)
        glScissor(int(self.x), int(self.y), int(self.width), int(self.height))

    def unset_state(self):
        super().unset_state()
        glDisable(GL_SCISSOR_TEST)


class UniformSetter:
    def __init__(self, shader: ShaderProgram):
        self.shader = shader
        self._uniforms = {}
        self._need_to_update = True
        for i in self.shader.uniforms:
            uniform_name = i[0]
            uniform_value = self.shader.uniforms.__getattr__(uniform_name)
            if uniform_value is not None and uniform_name != 'screen_size':
                self._uniforms[uniform_name] = [uniform_value, type(uniform_value)]

    def set_uniform(self, name: str, value):
        if name in self._uniforms.keys():
            uniform_list = self._uniforms[name]
            if type(value) is uniform_list[1]:
                uniform_list[0] = value
                self._need_to_update = True
            else:
                warnings.warn(
                    f"Wrong value type of '{name}' uniform: '{uniform_list[1]}' expected, '{type(value)}' got")
        else:
            warnings.warn(f"There is no uniform named '{name}' in the shader!!")

    def set_uniforms(self, uniform_dict: dict):
        for key, value in uniform_dict.items():
            self.set_uniform(key, value)

    def apply(self):
        if self._need_to_update:
            for key, value in self._uniforms.items():
                self.shader.uniforms.__setattr__(key, value[0])
            self._need_to_update = False


class ShadedGroup(SpriteGroup):
    def __init__(self, texture, shader: ShaderProgram, uniform_setter: UniformSetter, parent=None,
                 blend_src: int = GL_SRC_ALPHA,
                 blend_dest: int = GL_ONE_MINUS_SRC_ALPHA):
        super().__init__(texture, blend_src, blend_dest, parent)
        self.shader: ShaderProgram = shader
        self.uniform_setter = uniform_setter

    def set_state(self):
        super().set_state()
        self.shader.use()
        self.shader.uniforms.screen_size = UIRenderer.get_window_size()
        self.uniform_setter.apply()

    def unset_state(self):
        super().unset_state()
        self.shader.clear()


class UIBase(Sprite):
    def __init__(self, position: Vector2, size: Vector2, texture: AbstractImage = None,
                 image_fill_color=ColorHelper.WHITE, tint_color: (int, int, int, int) = ColorHelper.WHITE,
                 shader: ShaderProgram = ShaderManager.default_ui_shader()):
        if texture is None:
            texture = UIRenderer.add_texture(
                pyglet.image.SolidColorImagePattern(image_fill_color).create_image(size.x, size.y))

        super().__init__(texture, x=position.x, y=position.y, batch=UIRenderer.get_main_batch())

        self._position = position
        self._size = Vector2(texture.width, texture.height)
        self._is_removing = False
        self.shader = shader
        self.uniforms = UniformSetter(self.shader)
        self.color = tint_color if len(tint_color) == 3 else tint_color[:3]
        self._enabled = True
        self._current_batch = self.batch
        self.children: List[UIBase] = []
        self._set_group(UIRenderer.get_main_group())
        self.children_group = ScissorGroup(position.x, position.y, size.x, size.y, self.group.order + 1)
        self.custom_data = None  # can contain some data to simplify data transfer between scripts
        self.parent: UIBase = None
        self.opacity = tint_color[3] if len(tint_color) >= 4 else 255
        self._opacity = 255
        HitTest.add_ui_object(self)
        self._set_size(size)
        UIRenderer.add_ui_object(self)

        # event handlers
        self.on_click_down = lambda *args: None
        self.on_click_up = lambda *args: None
        self.on_mouse_enter = lambda *args: None
        self.on_mouse_leave = lambda *args: None

    def delete(self):
        # do not call this method on ScrollableContainer instance
        self._is_removing = True
        if self.parent is not None:
            self.parent.remove_child(self)
        UIRenderer.remove_ui_object(self)
        HitTest.remove_ui_object(self)
        super().delete()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: Vector2):
        self._position = value
        self.x = value.x
        self.y = value.y
        pos_difference = value - self.position
        for i in self.children:
            i.position = i.position + pos_difference
        self._position = value
        self.children_group.area = self.position.x, self.position.y, self.size.x, self.size.y
        HitTest.update_position(self)

    @property
    def size(self):
        return self._size

    def _set_size(self, value: Vector2):
        self.scale_x = value.x / float(self._size.x)
        self.scale_y = value.y / float(self._size.y)
        self._size = value
        self.children_group.area = self.position.x, self.position.y, self.size.x, self.size.y
        HitTest.update_size(self)

    @size.setter
    def size(self, value: Vector2):
        self._set_size(value)

    def delete_children(self):
        for child in self.children:
            child.batch = None
            child.group = None
        self.children.clear()
        del self.children[:]

    @Sprite.batch.setter
    def batch(self, value: Batch):
        Sprite.batch.fset(self, value)
        self._current_batch = value
        self.set_enabled(self._enabled)
        if not self._is_removing:
            HitTest.update_batch(self)

    def _set_group(self, value: OrderedGroup):
        self._group = ShadedGroup(self._texture, self.shader, self.uniforms, parent=value)
        if self._batch is not None:
            self._batch.migrate(self._vertex_list, GL_QUADS, self._group, self._batch)

    @Sprite.group.setter
    def group(self, value: OrderedGroup):
        self._set_group(value)
        self.children_group = ScissorGroup(self.position.x, self.position.y, self.size.x, self.size.y,
                                           (value.order if value is not None else 0) + 1)
        for i in self.children:
            i.group = self.children_group
        if not self._is_removing:
            HitTest.update_group(self)

    def set_enabled(self, enable: bool):
        self._enabled = enable
        Sprite.batch.fset(self, self._current_batch if enable else None)
        for i in self.children:
            i.batch = self.batch if enable else None

    def get_enabled(self) -> bool:
        return self._enabled

    def add_child(self, child: 'UIBase'):
        child.parent = self
        child.group = self.children_group
        self.children.append(child)

    def remove_child(self, child: 'UIBase'):
        self._remove_child(child)

    def _remove_child(self, child: 'UIBase', only_detach: bool = False):
        child.parent = None
        child.group = UIRenderer.get_main_group()
        if not only_detach:
            self.children.remove(child)

    def clear_children(self):
        for child in self.children:
            self._remove_child(child, True)
        self.children.clear()

    def update_logic(self, **kwargs):
        pass

    def is_point_inside(self, point: Vector2):
        lb_corner = self.position
        ru_corner = lb_corner + self.size
        return lb_corner.x <= point.x <= ru_corner.x and lb_corner.y <= point.y <= ru_corner.y

    def fade_in(self, duration: float):
        Storyboard.begin_animation(NumberFieldAnimation(self, 'opacity', 0, 255, duration))

    def fade_out(self, duration: float):
        Storyboard.begin_animation(NumberFieldAnimation(self, 'opacity', 0, 255, duration))
