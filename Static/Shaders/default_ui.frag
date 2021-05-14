#version 330 core

uniform sampler2D tex;

varying vec2 vertex_pos;
varying vec2 vertex_uv;
varying vec4 vertex_color;

void main(void)
{
    gl_FragColor = texture2D(tex, vertex_uv) * vertex_color;
}
