#version 330 core

#define PI 3.14159265359
#define PI_div_2 1.57079632679
#define PI_mul_2 6.28318530718

varying vec2 vertex_pos;
varying vec2 vertex_uv;
varying vec4 vertex_color;

uniform sampler2D tex;

void main(void)
{
    vec2 uv = vertex_uv - vec2(0.5);
    float r = length(uv);
    float theta = (atan(uv.y, -uv.x) - PI_div_2) / PI_mul_2;
    uv = vec2(r, theta);

    vec3 tex_color = texture(tex, uv).xyz;
    gl_FragColor = vec4(tex_color, 1.0);
}