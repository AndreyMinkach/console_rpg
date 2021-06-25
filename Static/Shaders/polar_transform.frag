#version 330 core

varying vec3 vertex_pos;
varying vec2 vertex_uv;
varying vec4 vertex_color;

uniform sampler2D tex;

void main(void)
{
    vec4 color = texture2D(tex, vertex_uv) * vertex_color;
    gl_FragColor = color;
}