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