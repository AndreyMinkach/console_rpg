#version 330 core

#define PI 3.14159265359
#define PI_2 6.28318530718

layout(location = 0)in vec3 vertices;
layout(location = 1)in vec4 colors;
layout(location = 2)in vec3 tex_coords;

varying vec3 vertex_pos;
varying vec2 vertex_uv;
varying vec4 vertex_color;

uniform mat4 zoomMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    vertex_pos = vertices;

    float r = vertex_pos.x;
    float theta = vertex_pos.y * PI_2;
    vec2 new_vertex = vec2(r * sin(theta), r * cos(theta)) + vec2(0.5);

    gl_Position = projectionMatrix * zoomMatrix *  viewMatrix * vec4(vertices, 1.0);
    vertex_uv = tex_coords.xy;
    vertex_color = colors;
}