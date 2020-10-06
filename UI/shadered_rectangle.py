import pyshaders
from PIL import Image
from pyshaders import ShaderProgram
from pyglet.gl import *

import configs
from Helpers.location_helper import Vector2

my_fragment_shader = """
#version 330 core

varying vec2 vertex_pos;
in vec2 texture_coords;

uniform sampler2D texture1;

const vec4 tint = vec4(vec3(1), 1.0);
const float smoothing = 1.0/512.0;
const vec2 shadowOffset = vec2(1.0/32);
const vec4 glowColor = vec4(1, 0.5, 0.5, 1.0);
const float glowMin = 0.2;
const float glowMax = 0.8;

uniform vec2 iResolution = vec2(2.0, 2.0);

float normpdf(in float x, in float sigma)
{
    return 0.39894*exp(-0.5*x*x/(sigma*sigma))/sigma;
}

vec4 blur(sampler2D tex, vec2 texCoord)
{
    vec4 sum = vec4(0.0);
    
    //our original texcoord for this fragment
    vec2 tc = texCoord.xy/iResolution.xy;
    
    //the amount to blur, i.e. how far off center to sample from 
    //1.0 -> blur by one pixel
    //2.0 -> blur by two pixels, etc.
    float blur = 4.0 / (iResolution.x / iResolution.y); 
    
    //the direction of our blur
    //(1.0, 0.0) -> x-axis blur
    //(0.0, 1.0) -> y-axis blur
    float hstep = 1.0;
    float vstep = 0.0;
    
    //apply blurring, using a 9-tap filter with predefined gaussian weights
    
    sum += texture(tex, vec2(tc.x - 4.0*blur*hstep/iResolution.x, tc.y - 4.0*blur*vstep/iResolution.y)) * 0.0162162162;
    sum += texture(tex, vec2(tc.x - 3.0*blur*hstep/iResolution.x, tc.y - 3.0*blur*vstep/iResolution.y)) * 0.0540540541;
    sum += texture(tex, vec2(tc.x - 2.0*blur*hstep/iResolution.x, tc.y - 2.0*blur*vstep/iResolution.y)) * 0.1216216216;
    sum += texture(tex, vec2(tc.x - 1.0*blur*hstep/iResolution.x, tc.y - 1.0*blur*vstep/iResolution.y)) * 0.1945945946;
    
    sum += texture(tex, vec2(tc.x, tc.y)) * 0.2270270270;
    
    sum += texture(tex, vec2(tc.x + 1.0*blur*hstep/iResolution.x, tc.y + 1.0*blur*vstep/iResolution.y)) * 0.1945945946;
    sum += texture(tex, vec2(tc.x + 2.0*blur*hstep/iResolution.x, tc.y + 2.0*blur*vstep/iResolution.y)) * 0.1216216216;
    sum += texture(tex, vec2(tc.x + 3.0*blur*hstep/iResolution.x, tc.y + 3.0*blur*vstep/iResolution.y)) * 0.0540540541;
    sum += texture(tex, vec2(tc.x + 4.0*blur*hstep/iResolution.x, tc.y + 4.0*blur*vstep/iResolution.y)) * 0.0162162162;
    
    //discard alpha for our simple demo, multiply by vertex color and return
    return vec4(sum.rgb, 1.0);
}

void main()
{
    vec4 texColor = texture(texture1, texture_coords);
    float dst = texColor.a;
    float alpha = smoothstep(0.5 - smoothing, 0.5 + smoothing, dst);

    float glowDst = blur(texture1, texture_coords + shadowOffset).a;
    //float glowDst = texture(texture1, texture_coords + shadowOffset).a;
    vec4 glow = glowColor * smoothstep(glowMin, glowMax, glowDst);

    float mask = 1.0-alpha;

    vec4 base = texColor * vec4(vec3(1.0), alpha) * tint;
    //gl_FragColor = mix(base, glow, mask);
    gl_FragColor = blur(texture1, texture_coords);
}
"""
# my_fragment_shader = """
# #version 330 core
#
# in vec2 texture_coords;
#
# uniform sampler2D texture1;
#
# out vec4 out_color;
# void main()
# {
#     out_color = texture2D(texture1, texture_coords);
# }
# """

my_vertex_shader = """
#version 330 core
layout(location = 0)in vec2 vertex;
layout(location = 1)in vec2 vertex_uv;

varying vec2 vertex_pos;

out vec2 texture_coords;
void main()
{
    gl_Position = vec4(vertex, 0.0, 1.0);
    texture_coords = vertex_uv;
    vertex_pos = vertex;
}
"""


def _ss_to_cs(x: int, y: int) -> Vector2:
    """
    Converts point from screen space in pixels to clip space
    :param x:
    :param y:
    :return:
    """
    return Vector2()


class UIRectangle:
    def __init__(self, image_path: str, position: Vector2 = Vector2.zero, size: Vector2 = Vector2.one):
        self.position = position
        self.size = size
        self._shader: ShaderProgram = pyshaders.from_string(my_vertex_shader, my_fragment_shader)
        self._vertices = self._get_vertices()
        self._vbo = GLuint(0)
        self._bind_buffers()
        self.texture_id = self._read_texture(configs.IMAGE_FOLDER + image_path)

    def _read_texture(self, image_path: str):
        opened_image = Image.open(image_path)
        try:
            width, height, image_data = opened_image.size[0], opened_image.size[1], opened_image.tobytes("raw", "RGBA",
                                                                                                         0, -1)
        except SystemError:
            width, height, image_data = opened_image.size[0], opened_image.size[1], opened_image.tobytes("raw", "RGBX",
                                                                                                         0, -1)

        glEnable(GL_TEXTURE_2D)
        texture_id = GLuint(0)
        glGenTextures(1, texture_id)

        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        opened_image.close()

        return texture_id

    def _get_vertices(self):
        #       vertices    uvs
        return [-0.5, -0.5, 0.0, 0.0,
                -0.5, 0.5, 0.0, 1.0,
                0.5, 0.5, 1.0, 1.0,
                0.5, -0.5, 1.0, 0.0]

    def _bind_buffers(self):
        self._clean()
        glGenBuffers(1, self._vbo)
        glBindBuffer(GL_ARRAY_BUFFER, self._vbo)
        glBufferData(GL_ARRAY_BUFFER, len(self._vertices) * 4, (GLfloat * len(self._vertices))(*self._vertices),
                     GL_STATIC_DRAW)

    def _clean(self):
        glDeleteBuffers(1, self._vbo)

    def draw(self):
        self._shader.use()
        self._shader.attributes['vertex'].point_to(0, GL_FLOAT, 2, GL_FALSE, 16)
        self._shader.attributes['vertex_uv'].point_to(8, GL_FLOAT, 2, GL_FALSE, 16)
        self._shader.enable_all_attributes()
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glDrawArrays(GL_QUADS, 0, 4)
        glBindTexture(GL_TEXTURE_2D, 0)
        self._shader.disable_all_attributes()
        self._shader.clear()
