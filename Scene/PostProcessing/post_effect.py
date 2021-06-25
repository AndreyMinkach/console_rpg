import pyglet
from pyglet.gl import GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from pyglet.graphics import Batch, glClearColor, glClear, GL_COLOR_BUFFER_BIT

from Helpers.shader_manager import ShaderManager, UniformSetter, ShadedGroup
from Scene.PostProcessing.fbo import FBO, FBOAttachment


class PostEffect:
    __slots__ = ['fbo', 'width', 'height', 'x', 'y', '_shader', 'uniforms', '_texture', '_batch', '_group',
                 'vertex_list', '_clear_color', '_clear_mask']

    def __init__(self,
                 width: int,
                 height: int,
                 shader_name: str,
                 fbo_resolution: (int, int) = (256, 256),
                 clear_color: (float, float, float, float) = (1.0, 1.0, 1.0, 1.0),
                 clear_mask: int = GL_COLOR_BUFFER_BIT,
                 blend_src: int = GL_SRC_ALPHA,
                 blend_dest: int = GL_ONE_MINUS_SRC_ALPHA,
                 fbo_attachment: FBOAttachment = FBOAttachment.Color
                 ):
        """
        Initializes a new PostEffect object

        :param width: Effect width in screen space
        :param height: Effect height in screen space
        :param shader_name: The name of the shader that will be used by the effect
        :param fbo_resolution: The resolution of the effect's FBO
        :param clear_color: Clear color of the effect's FBO
        """
        self.fbo = FBO(*fbo_resolution, fbo_attachment=fbo_attachment)
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self._clear_color = clear_color
        self._clear_mask = clear_mask
        self._texture = self.fbo.texture
        self._shader = ShaderManager.get_shader_by_name(shader_name)
        self.uniforms = UniformSetter(self._shader)
        self._batch = Batch()
        self._group = ShadedGroup(self._texture, self._shader, self.uniforms, None, blend_src, blend_dest)
        self._create_vertex_list()

    @property
    def group(self) -> ShadedGroup:
        return self._group

    def bind(self):
        """
        Binds FBO for the further usage. Everything that will be rendered after the call of this method will be rendered
        into the FBO's texture
        """
        self.fbo.bind_fbo()
        glClearColor(*self._clear_color)
        glClear(self._clear_mask)

    def unbind(self):
        """
        Binds the default FBO which will render to the screen
        """
        self.fbo.unbind_fbo()

    def render(self):
        """
        Applies the current shader to a texture stored in the FBO and draws it in a quad on top of the rest
        """
        self._batch.draw()

    def set_resolution(self, width: int, height: int):
        """
        Sets a new resolution for the FBO

        :param width: New FBO texture width
        :param height: New FBO texture height
        """
        del self.fbo
        self.fbo = FBO(width, height)
        self._group.texture = self._texture = None
        self._group.texture = self._texture = self.fbo.texture
        self.vertex_list.delete()
        self._create_vertex_list()

    def set_size(self, width: int, height: int):
        """
        Sets a new size for effect rectangle

        :param width: New effect rectangle width
        :param height: New effect rectangle height
        """
        self.width = width
        self.height = height
        self._update_vertices()

    def set_boundaries(self, x: int, y: int, width: int, height: int):
        """
        Sets a new boundaries for effect rectangle

        :param x: X position of the effect rectangle
        :param y: Y position of the effect rectangle
        :param width: New post effect rectangle width
        :param height: New post effect rectangle height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._update_vertices()

    def _create_vertex_list(self):
        """
        Creates the vertex list for the further
        """
        self.vertex_list = self._batch.add(
            4, pyglet.gl.GL_QUADS, self._group, 'v2f', ('t3f', self._texture.tex_coords))
        self._update_vertices()

    def _update_vertices(self):
        """
        Creates a vertices list
        """
        x1, y1 = self.x, self.y
        x2 = x1 + self.width
        y2 = y1 + self.height
        vertices = (x1, y1, x2, y1, x2, y2, x1, y2)
        self.vertex_list.vertices[:] = vertices
