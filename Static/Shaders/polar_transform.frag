#version 330 core

#define PI 3.14159265359
#define PI_2 6.28318530718

varying vec2 vertex_pos;
varying vec2 vertex_uv;
varying vec4 vertex_color;

uniform sampler2D tex;

void main(void)
{
    float r = vertex_uv.x;
    float theta = vertex_uv.y * PI_2;
    vec2 uv = vec2(r * sin(theta), r * cos(theta)) + vec2(0.5);

    vec3 tex_color = vec3(texture(tex, uv).xyz == vec3(1.0, 1.0, 1.0));
    gl_FragColor = vec4(tex_color, 1.0);
}