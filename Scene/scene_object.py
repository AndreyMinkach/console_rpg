from math import radians
import numpy as np
from PIL import Image
from pyglet.image import TextureRegion
from pyrr import Matrix44

from typing import Any
from OpenGL.GL import *

from Scene.camera import Camera
from Scene.renderer import Renderer
from UI.ui_renderer import UIRenderer

VS = '''
#version 330 core

layout(location = 0)in vec2 vertices;
layout(location = 1)in vec4 colors;
layout(location = 2)in vec2 uvs;

varying vec4 vertex_pos;
varying vec4 vertex_color;
varying vec2 vertex_uv;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec4 color;

void main ()
{
    vertex_pos = projectionMatrix * viewMatrix * modelMatrix * vec4(vertices, 0.0, 1.0);
    vertex_color = colors;
    vertex_uv = uvs;
    gl_Position = vertex_pos;
}
'''

FS = '''
#version 330 core

varying vec4 vertex_pos;
varying vec4 vertex_color;
varying vec2 vertex_uv;

out vec4 FragColor;

uniform sampler2D texture1;

void main()
{
    FragColor = texture(texture1, vertex_uv) * vertex_color;
}
'''


class Shader:
    def __init__(self, vs_source: str, fs_source: str) -> None:
        self.program = glCreateProgram()
        self.compile(vs_source, fs_source)

    def __del__(self) -> None:
        glUseProgram(0)
        glDeleteProgram(self.program)

    @staticmethod
    def load_shader(src: str, shader_type: int) -> int:
        shader = glCreateShader(shader_type)
        glShaderSource(shader, src)
        glCompileShader(shader)
        compile_status = glGetShaderiv(shader, GL_COMPILE_STATUS)
        if compile_status != GL_TRUE:
            info = glGetShaderInfoLog(shader)
            glDeleteShader(shader)
            raise Exception(info)
        return shader

    def compile(self, vs_src: str, fs_src: str) -> None:
        vs = self.load_shader(vs_src, GL_VERTEX_SHADER)
        fs = self.load_shader(fs_src, GL_FRAGMENT_SHADER)
        if not vs or not fs:
            return
        glAttachShader(self.program, vs)
        glAttachShader(self.program, fs)
        glLinkProgram(self.program)
        link_status = glGetProgramiv(self.program, GL_LINK_STATUS)
        glDeleteShader(vs)
        glDeleteShader(fs)
        if link_status != GL_TRUE:
            info = glGetShaderInfoLog(self.program)
            raise Exception(info)

    def set_matrix4x4(self, uniform_name: str, value):
        location = glGetUniformLocation(self.program, uniform_name)
        glUniformMatrix4fv(location, 1, GL_FALSE, value)

    def use(self):
        glUseProgram(self.program)

    @staticmethod
    def unuse():
        glUseProgram(0)


class VertexAttrib:
    def __init__(self, slot: int, stride: int, data: Any):
        self.buffer_id = glGenBuffers(1)
        self.slot = slot
        self.stride = stride
        self.data = data

    def set_vertex_attribute(self, attrib_type=GL_FLOAT):
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_id)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(self.data), self.data, GL_STATIC_DRAW)
        glEnableVertexAttribArray(self.slot)
        glVertexAttribPointer(self.slot, self.stride, attrib_type, GL_FALSE, 0, None)

    def __del__(self) -> None:
        glDeleteBuffers(1, [self.buffer_id])


class SceneObject:
    def __init__(self, sprite_path: str) -> None:
        self._anchor: tuple = (0.0, 0.0)
        self._position: list = [0] * 3
        self._rotation: float = 0.0
        self._scale: list = [1.0] * 3

        self.texture: TextureRegion = UIRenderer.load_image(sprite_path)
        self.texture_coords: list = self._get_texture_uv(self.texture)

        self.shader = Shader(VS, FS)
        self.vertices = VertexAttrib(0, 2, np.array([-0.5, -0.5, -0.5, 0.5, 0.5, 0.5, 0.5, -0.5], dtype=np.float32))
        self.colors = VertexAttrib(1, 4, np.array([1.0, 1.0, 1.0, 1.0] * 4, dtype=np.float32))
        self.uvs = VertexAttrib(2, 2, np.array(self.texture_coords, dtype=np.float32))

        self.ebo_id = glGenBuffers(1)
        self.indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.int32)

        self._translation_matrix: Matrix44 = Matrix44.from_translation(self._position)
        self._rotation_matrix: Matrix44 = Matrix44.from_z_rotation(self._rotation)
        self._scale_matrix: Matrix44 = Matrix44.from_scale(self._scale)
        self._model_matrix = np.array(self._translation_matrix * self._rotation_matrix * self._scale_matrix,
                                      dtype=np.float32)

        self.test_angle = 0

        Renderer.add_scene_object_to_render_loop(self)

    @staticmethod
    def _get_texture_uv(texture_region: TextureRegion) -> list:
        """
        Finds a texture uv coordinates inside the 'owner' texture(atlas). If the texture_region parameter has no owner
        returns a default uv list
        :param texture_region: InputTexture
        :return: UV coordinate list
        """
        if texture_region.owner is not None:
            uvs = list(texture_region.tex_coords)
            del uvs[3 - 1::3]  # remove every third(z-component) element
            uvs[2], uvs[6] = uvs[6], uvs[2]
            uvs[3], uvs[7] = uvs[7], uvs[3]

            return uvs
        else:
            return [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0]

    def _update_vertices(self):
        x = self._anchor[0]
        y = self._anchor[1]
        self.vertices = VertexAttrib(0, 2, np.array(
            [-0.5 - x, -0.5 - y, -0.5 - x, 0.5 - y, 0.5 - x, 0.5 - y, 0.5 - x, -0.5 - y], dtype=np.float32))

    def set_anchor(self, x: float, y: float):
        """
        Sets anchor point of the scene object. All the rotations of the scene object will be made around
         the anchor point

        Example:
            (x=-0.5, y=-0.5) means that the object's center will be placed at bottom left corner
            (x=0.5, y=0.5) means that the object's center will be placed at upper right corner

        :param x: Horizontal position
        :param y: Vertical position
        """
        self._anchor = (x, y)
        self._update_vertices()

    def set_position(self, x: float, y: float):
        """
        Sets the position of the scene object in world space
        :param x: Horizontal position
        :param y: Vertical position
        """
        self._position = [x, y, 0]
        self._translation_matrix = Matrix44.from_translation(self._position)
        self._model_matrix = np.array(self._translation_matrix * self._rotation_matrix * self._scale_matrix,
                                      dtype=np.float32)

    def add_position(self, x: float, y: float):
        """
        Adds the input (x, y) vector to the existing scene object position
        """
        self.set_position(self._position[0] + x, self._position[1] + y)

    def set_rotation(self, angle: float):
        """
        Sets the rotation of the scene object
        :param angle: Angle value in degrees
        """
        self._rotation = radians(angle)
        self._rotation_matrix: Matrix44 = Matrix44.from_z_rotation(self._rotation)
        self._model_matrix = np.array(self._translation_matrix * self._rotation_matrix * self._scale_matrix,
                                      dtype=np.float32)

    def set_scale(self, x: float, y: float):
        """
        Sets the scale of the scene object at x and y axes
        :param x: Horizontal scale
        :param y: Vertical scale
        """
        self._scale = [x, y, 1]
        self._scale_matrix: Matrix44 = Matrix44.from_scale(self._scale)
        self._model_matrix = np.array(self._translation_matrix * self._rotation_matrix * self._scale_matrix,
                                      dtype=np.float32)

    def __del__(self) -> None:
        glDeleteBuffers(1, [self.ebo_id])
        Renderer.remove_scene_object_to_render_loop(self)

    def draw(self) -> None:
        self.shader.use()

        self.shader.set_matrix4x4('modelMatrix', self._model_matrix)
        self.shader.set_matrix4x4('viewMatrix', Camera.get_view_matrix())
        self.shader.set_matrix4x4('projectionMatrix', Camera.get_camera_matrix())

        # set attributes
        self.vertices.set_vertex_attribute()
        self.colors.set_vertex_attribute()
        self.uvs.set_vertex_attribute()

        # bind texture
        glBindTexture(GL_TEXTURE_2D, self.texture.id)
        # glUniform1i(glGetUniformLocation(self.shader.program, "texture1"), 0)

        # bind element array buffer and data
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo_id)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * self.indices.size, self.indices, GL_STATIC_DRAW)
        # draw indexed array data
        glDrawElements(GL_TRIANGLES, self.indices.size, GL_UNSIGNED_INT, None)

        # unbind EBO & VBOs(vertex attributes)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindTexture(GL_TEXTURE_2D, 0)

        # unuse shader
        self.shader.unuse()
