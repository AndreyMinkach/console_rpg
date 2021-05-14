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