import pyshaders
from pyshaders import ShaderProgram

default_vs = """
#version 330 core
layout(location = 0)in vec2 vertex;

varying vec2 vertex_pos;
varying vec3 vertex_uv;
varying vec4 vertex_color;

uniform vec2 screen_size;

vec2 to_clip_space(vec2 pos)
{
    return vec2((pos.x / screen_size.x) * 2.0 - 1.0, (pos.y / screen_size.y) * 2.0 - 1.0);
}

void main()
{
    vertex_pos = to_clip_space(vertex);
    gl_Position = vec4(vertex_pos, 0.0, 1.0);
    vertex_uv = gl_MultiTexCoord0;
    vertex_color = gl_Color;
}
"""
default_fs = """
#version 330 core

uniform sampler2D tex;

varying vec2 vertex_pos;
varying vec3 vertex_uv;
varying vec4 vertex_color;

void main(void) 
{
    gl_FragColor = texture2D(tex, vertex_uv.xy) * vertex_color;
}
"""
outline_fs = """
#version 330 core

varying vec2 vertex_pos;
varying vec3 vertex_uv;
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

void main(void) 
{    
    gl_FragColor = outline(tex, vertex_uv);
}
"""
blur_fs = """
#version 330 core

varying vec2 vertex_pos;
varying vec3 vertex_uv;
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
vignette_fs = """
#version 330 core

varying vec2 vertex_pos;
varying vec3 vertex_uv;
varying vec4 vertex_color;

uniform sampler2D tex;
uniform vec2 uv_boundaries = vec2(0.29296875, 0.22412109375);
uniform float vignette_intensity = 0.9;
uniform float vignette_radius = 0.5;
uniform float vignette_softness = 0.1;

const vec2 uv_center = vec2(0.5, 0.5);

vec4 vignette(vec4 tex_color, vec2 coord)
{
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
        self.default_shader: ShaderProgram = pyshaders.from_string(default_vs, default_fs)
        self.outline_shader: ShaderProgram = pyshaders.from_string(default_vs, outline_fs)
        self.blur_shader: ShaderProgram = pyshaders.from_string(default_vs, blur_fs)
        self.vignette_shader: ShaderProgram = pyshaders.from_string(default_vs, vignette_fs)

    @classmethod
    def default_shader(cls):
        return cls._instance.default_shader

    @classmethod
    def outline_shader(cls):
        return cls._instance.outline_shader

    @classmethod
    def blur_shader(cls):
        return cls._instance.blur_shader

    @classmethod
    def vignette_shader(cls):
        return cls._instance.vignette_shader


shader_manager = ShaderManager()
