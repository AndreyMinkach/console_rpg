import glob
import warnings
from os import path

import pyshaders
from pyglet.gl import glDeleteProgram, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from pyglet.sprite import SpriteGroup
from pyshaders import ShaderProgram

from UI.ui_renderer import UIRenderer

pyshaders.transpose_matrices(False)


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
            uniform_list[0] = value
            self._need_to_update = True
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
        if 'screen_size' in self.shader.uniforms:
            self.shader.uniforms.screen_size = UIRenderer.get_window_size()
        self.uniform_setter.apply()

    def unset_state(self):
        super().unset_state()
        self.shader.clear()


class ShaderManager:
    _instance: 'ShaderManager' = None

    def __init__(self):
        self.__class__._instance = self
        self._vertex_shaders: dict = {}
        self._fragment_shaders: dict = {}
        self._shader_programs: dict = {}

        self._load_shaders()

    @staticmethod
    def _from_string(verts, frags):
        """
            High level loading function.

            Load a shader using sources passed in sequences of string.
            Each source is compiled in a shader unique shader object.
            Return a linked shaderprogram. The shaderprogram owns the gl resource.

            verts: Sequence of vertex shader sources
            frags: Sequence of fragment shader sources
        """
        if isinstance(verts, str):
            verts = (verts,)
        elif verts is None:
            verts = ()
        if isinstance(frags, str):
            frags = (frags,)

        logs, objs = "", []

        for src in verts:
            vert = pyshaders.ShaderObject.vertex()
            vert.source = src
            objs.append(vert)

        for src in frags:
            frag = pyshaders.ShaderObject.fragment()
            frag.source = src
            objs.append(frag)

        for obj in objs:
            if obj.compile() is False:
                logs += obj.logs

        if len(logs) == 0:
            prog = ShaderProgram.new_program()
            prog.attach(*objs)
            if not prog.link():
                raise pyshaders.ShaderCompilationError(prog.logs)

            return prog

        raise pyshaders.ShaderCompilationError(logs)

    def _load_shaders(self, shaders_folder: str = 'Static/Shaders/'):
        """
        Loads all shaders from a specified folder

        :param shaders_folder: Folder to load shaders from
        """
        # initialize vertex shaders
        for filename in glob.glob(shaders_folder + "*.vert"):
            shader_name = path.splitext(path.basename(filename))[0]
            with open(filename, 'r') as f:
                self._vertex_shaders[shader_name] = f.read()

        # initialize fragment shaders
        for filename in glob.glob(path.join(shaders_folder, "*.frag")):
            shader_name = path.splitext(path.basename(filename))[0]
            with open(filename, 'r') as f:
                self._fragment_shaders[shader_name] = f.read()

        # initialize shader programs
        for fs_name, fs_code in self._fragment_shaders.items():
            try:
                if fs_name in self._vertex_shaders:  # is there a vertex shader with the same name?
                    vs_name = fs_name
                else:  # use default vertex shader
                    if '_pps' in fs_name:  # is this shader a post-processing shader?
                        vs_name = 'default_pps'
                    elif '_ui' in fs_name:  # is this shader a ui shader?
                        vs_name = 'default_ui'
                    else:
                        vs_name = 'default'
                vs_code = self._vertex_shaders[vs_name]
                self._shader_programs[fs_name] = self._from_string(vs_code, fs_code)
            except Exception as e:
                print("Compilation of \'{0}\' shader failed!"
                      " Because of the following errors:\n{1}".format(fs_name, *e.args))

    @classmethod
    def get_shader_by_name(cls, name: str) -> ShaderProgram:
        self = cls._instance
        if name not in self._shader_programs:
            default_name = 'default_ui' if 'ui' in name else 'default'
            print(f"ERROR: There is no shader named '{name}', the '{default_name}' shader will be used!")
            return self._shader_programs[default_name]
        return self._shader_programs[name]

    @classmethod
    def _delete_shader(cls, shader: ShaderProgram):
        if shader.owned and shader.valid():
            shader.detach(*shader.shaders())
            glDeleteProgram(shader.pid)

    @classmethod
    def close(cls):
        self = cls._instance
        for shader in self._shader_programs.values():
            cls._delete_shader(shader)


shader_manager = ShaderManager()
