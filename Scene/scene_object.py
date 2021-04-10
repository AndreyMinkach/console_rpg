import math

import pyglet
import pyglet.clock as clock
from pyglet.image import TextureRegion, Animation

from Helpers.shader_manager import ShaderManager
from Scene.camera import Camera
from Scene.renderer import Renderer
from UI.ui_base import ShadedGroup, UniformSetter


class SceneObject:

    def __init__(self, image, position=(0, 0), batch=None, group=None, shader=ShaderManager.default_shader()):
        self._anchor: tuple = (0.5, 0.5)
        self._color: tuple = (1.0, 1.0, 1.0)
        self._position: tuple = position
        self._rotation: float = 0.0
        self._scale: tuple = (1.0, 1.0)

        # animation data
        self._animation = None
        self._is_animation_playing: bool = False
        self._frame_index: int = 0

        if isinstance(image, Animation):
            self._animation = image
            self._texture: TextureRegion = image.frames[0].image.get_texture()
        else:
            self._animation = None
            self._texture: TextureRegion = image

        self.shader = shader
        self.uniforms = UniformSetter(self.shader)
        self._batch = batch if batch is not None else Renderer.batch()
        self._group = ShadedGroup(self._texture, self.shader, self.uniforms,
                                  parent=group if group is not None else Renderer.group())

        self._create_vertex_list()

        # TODO: Make automatic update of the camera matrices
        self.uniforms.set_uniforms(dict(viewMatrix=Camera.get_view_matrix(),
                                        projectionMatrix=Camera.get_camera_matrix()))

        Renderer.add_scene_object_to_render_loop(self)

    def __del__(self):
        try:
            if self.vertex_list is not None:
                self.vertex_list.delete()
        except:
            pass

    def delete(self):
        """Force immediate removal of the sprite from video memory.

        This is often necessary when using batches, as the Python garbage
        collector will not necessarily call the finalizer as soon as the
        sprite is garbage.
        """
        Renderer.remove_scene_object_from_render_loop(self)
        if self._animation:
            clock.unschedule(self._animate)
        self.vertex_list.delete()
        self.vertex_list = None
        self._texture = None

        # Easy way to break circular reference, speeds up GC
        self._group = None

    def _create_vertex_list(self):
        self.vertex_list = self._batch.add(
            4, pyglet.gl.GL_QUADS, self._group, 'v2f', 'c4f', ('t3f', self._texture.tex_coords))
        self._update_vertices()
        self._update_color()

    def _set_texture(self, texture):
        if texture.id is not self._texture.id:
            self._group = ShadedGroup(texture, self.shader, self.uniforms, self._group.parent)
            if self._batch is None:
                self.vertex_list.tex_coords[:] = texture.tex_coords
            else:
                self.vertex_list.delete()
                self._texture = texture
                self._create_vertex_list()
        else:
            self.vertex_list.tex_coords[:] = texture.tex_coords
        self._texture = texture

    def _animate(self, dt=0):
        if not self._is_animation_playing or self._animation is None:
            return
        if self._frame_index >= len(self._animation.frames):
            self._frame_index = 0

        frame = self._animation.frames[self._frame_index]
        self._set_texture(frame.image.get_texture())
        clock.schedule_once(self._animate, frame.duration)
        self._frame_index += 1

    def play_animation(self):
        """
        Starts animation playing
        """
        if self._animation is None:
            return
        self._is_animation_playing = True
        self._frame_index = 0

        self._animate()

    def stop_animation(self):
        """
        Stops animation playing
        :return:
        """
        self._is_animation_playing = False

    @staticmethod
    def _get_texture_uv(texture_region: TextureRegion) -> list:
        """
        Finds a texture uv coordinates inside the 'owner' texture(atlas). If the texture_region parameter has no owner
        returns a default uv list
        :param texture_region: InputTexture
        :return: UV coordinate list
        """
        if texture_region is not None:
            if texture_region.owner is not None:
                uvs = list(texture_region.tex_coords)
                del uvs[3 - 1::3]  # remove every third(z-component) element
                uvs[2], uvs[6] = uvs[6], uvs[2]
                uvs[3], uvs[7] = uvs[7], uvs[3]

                return uvs
        return [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0]

    def _update_vertices(self):
        img = self._texture
        scale_x = self._scale[0]
        scale_y = self._scale[1]
        if self._rotation != 0.0:
            x1 = -self._anchor[0] * scale_x
            y1 = -self._anchor[1] * scale_y
            x2 = x1 + 1 * scale_x
            y2 = y1 + 1 * scale_y
            x = self._position[0]
            y = self._position[1]

            r = -math.radians(self._rotation)
            cr = math.cos(r)
            sr = math.sin(r)
            ax = x1 * cr - y1 * sr + x
            ay = x1 * sr + y1 * cr + y
            bx = x2 * cr - y1 * sr + x
            by = x2 * sr + y1 * cr + y
            cx = x2 * cr - y2 * sr + x
            cy = x2 * sr + y2 * cr + y
            dx = x1 * cr - y2 * sr + x
            dy = x1 * sr + y2 * cr + y
            vertices = (ax, ay, bx, by, cx, cy, dx, dy)
        elif scale_x != 1.0 or scale_y != 1.0:
            x1 = self._position[0] - self._anchor[0] * scale_x
            y1 = self._position[1] - self._anchor[1] * scale_y
            x2 = x1 + 1 * scale_x
            y2 = y1 + 1 * scale_y
            vertices = (x1, y1, x2, y1, x2, y2, x1, y2)
        else:
            x1 = self._position[0] - self._anchor[0]
            y1 = self._position[1] - self._anchor[1]
            x2 = x1 + 1
            y2 = y1 + 1
            vertices = (x1, y1, x2, y1, x2, y2, x1, y2)
        self.vertex_list.vertices[:] = vertices

    def _update_color(self):
        r, g, b = self._color
        self.vertex_list.colors[:] = [r, g, b, 1.0] * 4

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value):
        if self._animation is not None:
            self.stop_animation()
            self._animation = None

        if isinstance(value, Animation):
            self._animation = value
            self._set_texture(value.frames[0].image.get_texture())
        else:
            self._set_texture(value.get_texture())

    @property
    def color(self) -> (float, float, float):
        return self._color

    @color.setter
    def color(self, value: (float, float, float)):
        """
        This method sets the color of the scene object
        :param value: Color of all the vertices of the object.
        Each component the color must be inside the [0, 1] range.
        Examples:
            color = (1.0, 1.0, 1.0) - set white color for all the vertices
        """
        self._color = value
        self._update_color()

    @property
    def anchor(self) -> (float, float):
        return self._anchor

    @anchor.setter
    def anchor(self, value: (float, float)):
        """
        Sets anchor point of the scene object. All the rotations of the scene object will be made around
         the anchor point

        Example:
            (x=-0.5, y=-0.5) means that the object's center will be placed at bottom left corner
            (x=0.5, y=0.5) means that the object's center will be placed at upper right corner

        :param value: Tuple of format (x, y) that represents the horizontal and vertical anchor of the object
        """
        self._anchor = value
        self._update_vertices()

    @property
    def position(self) -> (float, float):
        return self._position

    @position.setter
    def position(self, value: (float, float)):
        """
        Sets the position of the scene object in world space
        :param value: Tuple of format (x, y) that represents the horizontal and vertical position of the object
        """
        self._position = value
        self._update_vertices()

    def add_position(self, x: float, y: float):
        """
        Adds the input (x, y) vector to the existing scene object position
        """
        self.position = (self._position[0] + x, self._position[1] + y)

    @property
    def rotation(self) -> float:
        """
        Represents an rotation(in degrees) of the object
        """
        return self._rotation

    @rotation.setter
    def rotation(self, angle: float):
        """
        Sets the rotation of the scene object
        :param angle: Angle value in degrees
        """
        self._rotation = angle
        self._update_vertices()

    @property
    def scale(self) -> (float, float):
        return self._scale

    @scale.setter
    def scale(self, value: (float, float)):
        """
        Sets the scale of the scene object at x and y axes
        :param value: Tuple of format (x, y) that represents the horizontal and vertical scale of the object
        """
        self._scale = value
        self._update_vertices()
