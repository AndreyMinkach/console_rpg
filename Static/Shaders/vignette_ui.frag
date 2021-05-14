#version 330 core

varying vec2 vertex_pos;
varying vec2 vertex_uv;
varying vec4 vertex_color;

uniform sampler2D tex;
uniform vec2 texture_size = vec2(0);
uniform float vignette_intensity = 0.0;
uniform float vignette_radius = 0.0;
uniform float vignette_softness = 0.1;

const vec2 uv_center = vec2(0.5, 0.5);

vec4 vignette(vec4 tex_color, vec2 coord)
{
    vec2 uv_boundaries = texture_size / textureSize(tex, 0);
    float norm_factor = length(uv_boundaries) * 0.5;
    float distance = length(coord - uv_center * uv_boundaries);

    float vignette_value = clamp(1.0 - vignette_intensity + smoothstep(vignette_radius * norm_factor,
                                vignette_radius * norm_factor - vignette_softness * norm_factor, distance), 0, 1);

    return vec4(tex_color.rgb * vec3(vignette_value), 1.0);
}

void main(void)
{
    vec4 tex_color = texture2D(tex, vertex_uv) * vertex_color;
    gl_FragColor = vignette(tex_color, vertex_uv);
}