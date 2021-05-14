#version 330 core

varying vec2 vertex_pos;
varying vec2 vertex_uv;
varying vec4 vertex_color;

uniform sampler2D tex;
uniform float blur_value = 0;

const vec2 offsets_one[4] = vec2[4](vec2(-1.0, -1.0), vec2(1.0, -1.0), vec2(1.0, 1.0), vec2(-1.0, 1.0));
const vec2 offsets_two[4] = vec2[4](vec2(0.0, -1.0), vec2(.0, 1.0), vec2(-1.0, 0.0), vec2(1.0, 0.0));

vec4 blur(sampler2D tex_sampler, vec2 coord)
{
    vec4 total = vec4(0.0);
    vec4 grabPixel = vec4(0.0);
    vec2 tex_size = textureSize(tex_sampler, 0);

    total += texture2D(tex_sampler, coord + offsets_one[0] * blur_value / tex_size);
    grabPixel = texture2D(tex_sampler, coord + offsets_two[0] * blur_value / tex_size);
    total += grabPixel * 2.0;
    total += texture2D(tex_sampler, coord + offsets_one[1] * blur_value / tex_size);
    grabPixel = texture2D(tex_sampler, coord + offsets_two[1] * blur_value / tex_size);
    total += grabPixel * 2.0;
    total += texture2D(tex_sampler, coord + offsets_one[2] * blur_value / tex_size);
    grabPixel = texture2D(tex_sampler, coord + offsets_two[2] * blur_value / tex_size);
    total += grabPixel * 2.0;
    total += texture2D(tex_sampler, coord + offsets_one[3] * blur_value / tex_size);
    grabPixel = texture2D(tex_sampler, coord + offsets_two[3] * blur_value / tex_size);
    total += grabPixel * 2.0;

    grabPixel = texture2D(tex_sampler, coord);
    total += grabPixel * 4.0;

    return total * 1.0 / 16.0;
}

void main(void)
{
    gl_FragColor = blur(tex, vertex_uv) * vertex_color;
}