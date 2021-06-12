import pyglet
from pyglet.graphics import Batch, glClearColor, glClear, GL_COLOR_BUFFER_BIT

from Helpers.shader_manager import ShaderManager, UniformSetter, ShadedGroup
from Scene.PostProcessing.fbo import FBO


class PostEffect:
    __slots__ = ['fbo', 'width', 'height', '_shader', '_uniforms', '_texture', '_batch', '_group', 'vertex_list',
                 '_clear_color']

    def __init__(self, width: int, height: int, shader_name: str, fbo_resolution: (int, int) = (256, 256),
                 clear_color: (float, float, float, float) = (1.0, 1.0, 1.0, 1.0)):
        self.fbo = FBO(*fbo_resolution)
        self.width = width
        self.height = height
        self._clear_color = clear_color
        self._texture = self.fbo.texture
        self._shader = ShaderManager.get_shader_by_name(shader_name)
        self._uniforms = UniformSetter(self._shader)
        self._batch = Batch()
        self._group = ShadedGroup(self._texture, self._shader, self._uniforms, None)
        self._create_vertex_list()

    def bind(self):
        """
        Binds FBO for the further usage. Everything that will be rendered after the call of this method will be rendered
        into the FBO's texture
        """
        self.fbo.bind_fbo()
        glClearColor(*self._clear_color)
        glClear(GL_COLOR_BUFFER_BIT)

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
        x1, y1 = 0, 0
        x2 = x1 + self.width
        y2 = y1 + self.height
        vertices = (x1, y1, x2, y1, x2, y2, x1, y2)
        self.vertex_list.vertices[:] = vertices
