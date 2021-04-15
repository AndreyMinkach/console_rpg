import warnings

import pyshaders
from pyglet.gl import glDeleteProgram, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from pyglet.sprite import SpriteGroup
from pyshaders import ShaderProgram

from UI.ui_renderer import UIRenderer

default_vs = """
#version 330 core

layout(location = 0)in vec2 vertices;
layout(location = 1)in vec4 colors;
layout(location = 2)in vec3 tex_coords;

varying vec2 vertex_pos;
varying vec2 vertex_uv;
varying vec4 vertex_color;

uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    vertex_pos = vertices;
    gl_Position = projectionMatrix *  viewMatrix * vec4(vertices, 0.0, 1.0);
    vertex_uv = tex_coords.xy;
    vertex_color = colors;
}
"""
default_fs = """
#version 330 core

varying vec2 vertex_pos;
varying vec2 vertex_uv;
varying vec4 vertex_color;

uniform sampler2D tex;

vec4 ambientLight = vec4(vec3(255, 224, 179) / 255.0, 0.1); // rbg - color, a - light strength
vec3 pointLight = vec3(0.0, 0.0, 5); // xy - light position, z - light radius
vec3 pointLightColor = vec3(255, 153, 204) / 255.0;

void main(void)
{
    vec4 color = texture2D(tex, vertex_uv) * vertex_color;
    
    vec2 toLight = (pointLight.xy - vertex_pos);
    
    float attenuation = clamp(1.0 - (length(toLight) / pointLight.z), 0.0, 1.0);
    
    vec4 light1 = vec4(ambientLight.rgb * ambientLight.a, 1.0);
    vec4 light2 = vec4(pointLightColor * attenuation, pow(attenuation, 3));
    vec4 totalLight = light1 + light2;
    
    vec4 pixelColor = color * clamp(totalLight, 0.0, 1.0);
    gl_FragColor = clamp(pixelColor, 0.0, 1.0);
}
"""
default_ui_vs = """
#version 330 core

layout(location = 0)in vec2 vertices;
layout(location = 1)in vec4 colors;
layout(location = 2)in vec3 tex_coords;

varying vec2 vertex_pos;
varying vec2 vertex_uv;
varying vec4 vertex_color;

uniform vec2 screen_size;

vec2 to_clip_space(vec2 pos)
{
    return vec2((pos.x / screen_size.x) * 2.0 - 1.0, (pos.y / screen_size.y) * 2.0 - 1.0);
}

void main()
{
    vertex_pos = to_clip_space(vertices);
    gl_Position = vec4(vertex_pos, 0.0, 1.0);
    vertex_uv = tex_coords.xy;
    vertex_color = colors / 255.0;
}
"""
default_ui_fs = """
#version 330 core

uniform sampler2D tex;

varying vec2 vertex_pos;
varying vec2 vertex_uv;
varying vec4 vertex_color;

void main(void) 
{
    gl_FragColor = texture2D(tex, vertex_uv) * vertex_color;
}
"""
outline_ui_fs = """
#version 330 core

varying vec2 vertex_pos;
varying vec2 vertex_uv;
varying vec4 vertex_color;

uniform sampler2D tex;

uniform float outline_width = 0;
uniform vec4 outline_color = vec4(1.0, 1.0, 1.0, 1.0);

const vec2 offsets[8] = vec2[8](vec2(0, 1), vec2(0, -1), vec2(1, 0), vec2(-1, 0), vec2(-1, 1), vec2(-1, -1),
    vec2(1, 1), vec2(1, -1));

vec4 outline(sampler2D tex_sampler, vec2 uvs)
{
    vec4 tex_color = texture(tex_sampler, uvs) * vertex_color;
    float offset = 1.0 / textureSize(tex_sampler, 0).x * outline_width;

    if (tex_color.a == 0.0)
    {
        bool temp_bool = false;   
        for (int i = 0; i < 8 ; i++)
        {
            if (texture2D(tex_sampler, uvs + offsets[i] * offset).a != 0.0)
            {
                temp_bool = true;
                break;
            }
        }
        if (temp_bool == true)
            tex_color = outline_color;
    }
    return tex_color;
}

out vec4 output_color;

void main(void) 
{    
    output_color = outline(tex, vertex_uv.xy);
}
"""
blur_ui_fs = """
#version 330 core

varying vec2 vertex_pos;
varying vec2 vertex_uv;
varying vec4 vertex_color;

uniform sampler2D tex;
uniform float blur_value = 0;

const vec2 offsets_one[4] = vec2[4](vec2(-1.0, -1.0), vec2(1.0, -1.0), vec2(1.0, 1.0), vec2(-1.0, 1.0));
const vec2 offsets_two[4] = vec2[4](vec2(0.0, -1.0), vec2(.0, 1.0), vec2(-1.0, 0.0), vec2(1.0, 0.0));

vec4 blur(sampler2D tex_sampler, vec2 coord)
{
    vec4 total = vec4(0.0);
    vec4 grabPixel = vec4(0.0);
    vec2 tex_size = textureSize(tex_sampler, 0);

    for (int i = 0; i < 4; i++) 
    {
        total += texture2D(tex_sampler, coord + offsets_one[i] * blur_value / tex_size);
        grabPixel = texture2D(tex_sampler, coord + offsets_two[i] * blur_value / tex_size);
        total += grabPixel * 2.0;
    }    
    grabPixel = texture2D(tex_sampler, coord);
    total += grabPixel * 4.0;

    return total * 1.0 / 16.0;
}

void main(void) 
{    
    gl_FragColor = blur(tex, vertex_uv) * vertex_color;
}
"""
vignette_ui_fs = """
#version 330 core

varying vec2 vertex_pos;
varying vec2 vertex_uv;
varying vec4 vertex_color;

uniform sampler2D tex;
uniform vec2 texture_size = vec2(0);
uniform float vignette_intensity = 0.0;
uniform float vignette_radius = 0.0;
uniform float vignette_softness = 0.1;

const vec2 uv_center = vec2(0.5, 0.5);

vec4 vignette(vec4 tex_color, vec2 coord)
{
    vec2 uv_boundaries = texture_size / textureSize(tex, 0);
    float norm_factor = length(uv_boundaries) * 0.5;
    float distance = length(coord - uv_center * uv_boundaries);

    float vignette_value = clamp(1.0 - vignette_intensity + smoothstep(vignette_radius * norm_factor,
                                vignette_radius * norm_factor - vignette_softness * norm_factor, distance), 0, 1);

    return vec4(tex_color.rgb * vec3(vignette_value), 1.0);
}

void main(void) 
{
    vec4 tex_color = texture2D(tex, vertex_uv) * vertex_color;
    gl_FragColor = vignette(tex_color, vertex_uv);
}
"""

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
        self.default_shader: ShaderProgram = pyshaders.from_string(default_vs, default_fs)
        self.default_ui_shader: ShaderProgram = pyshaders.from_string(default_ui_vs, default_ui_fs)
        self.outline_ui_shader: ShaderProgram = pyshaders.from_string(default_ui_vs, outline_ui_fs)
        self.blur_ui_shader: ShaderProgram = pyshaders.from_string(default_ui_vs, blur_ui_fs)
        self.vignette_ui_shader: ShaderProgram = pyshaders.from_string(default_ui_vs, vignette_ui_fs)

    @classmethod
    def _delete_shader(cls, shader: ShaderProgram):
        if shader.owned and shader.valid():
            shader.detach(*shader.shaders())
            glDeleteProgram(shader.pid)

    @classmethod
    def close(cls):
        cls._delete_shader(cls._instance.default_ui_shader)
        cls._delete_shader(cls._instance.outline_ui_shader)
        cls._delete_shader(cls._instance.blur_ui_shader)
        cls._delete_shader(cls._instance.vignette_ui_shader)

    @classmethod
    def default_shader(cls):
        return cls._instance.default_shader

    @classmethod
    def default_ui_shader(cls):
        return cls._instance.default_ui_shader

    @classmethod
    def outline_ui_shader(cls):
        return cls._instance.outline_ui_shader

    @classmethod
    def blur_ui_shader(cls):
        return cls._instance.blur_ui_shader

    @classmethod
    def vignette_ui_shader(cls):
        return cls._instance.vignette_ui_shader


shader_manager = ShaderManager()
