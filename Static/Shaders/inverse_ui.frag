#version 330 core

uniform sampler2D tex;

varying vec2 vertex_pos;
varying vec2 vertex_uv;
varying vec4 vertex_color;

void main(void)
{
    vec3 color = (1.0 - texture2D(tex, vertex_uv)).rgb;
    gl_FragColor = vec4(color, 1.0);
}
