#version 330 core

varying vec2 vertex_pos;
varying vec2 vertex_uv;
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
        for (int i = 0; i < 8; i++)
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

out vec4 output_color;

void main(void)
{
    output_color = outline(tex, vertex_uv.xy);
}