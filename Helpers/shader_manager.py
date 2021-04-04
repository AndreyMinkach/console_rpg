import pyshaders
from pyglet.gl import glDeleteProgram
from pyshaders import ShaderProgram

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


class ShaderManager:
    _instance: 'ShaderManager' = None

    def __init__(self):
        self.__class__._instance = self
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
