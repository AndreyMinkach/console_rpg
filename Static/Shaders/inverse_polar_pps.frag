#version 330 core

#define PI 3.14159265359
#define PI_2 6.28318530718
#define PI_div_2 1.57079632679

varying vec2 vertex_pos;
varying vec2 vertex_uv;
varying vec2 resolution;

uniform sampler2D tex;
uniform float texture_scale = 1.0;
uniform vec2 light_offset = vec2(0.0, 0.0);
uniform vec3 ambient = vec3(0.0, 0.0, 0.0);
uniform vec3 light_color = vec3(1.0, 1.0, 1.0);
uniform float light_intensity = 1.0;

vec2 get_inverse_polar_uv(vec2 in_uv)
{
    vec2 out_uv = in_uv - vec2(0.5);
    float r = length(out_uv);
    float theta = (atan(out_uv.y, -out_uv.x) - PI_div_2) / PI_2;

    return vec2(r, theta);
}

const float k = 20.0;

void main(void)
{
    vec2 uv = get_inverse_polar_uv(vertex_uv);
    vec3 tex_color = texture(tex, uv).xyz;

    vec2 scaled_resolution = resolution * texture_scale;
    vec2 center = gl_FragCoord.xy - scaled_resolution.xy * 0.5 - light_offset;
    float inner_radius = 0.4 * texture_scale;
    float outer_radius = 0.5 * texture_scale;
    float distance_from_center = length(center);

    float inner_distance = distance_from_center / (inner_radius * resolution.y);
    float attenuation = 1.0 / (1.0 + k * inner_distance * inner_distance);
    attenuation *= smoothstep(outer_radius, inner_radius, distance_from_center / resolution.y);

    vec3 diffuse = attenuation * light_color;
    vec3 total_light = ambient + diffuse;

    gl_FragColor = vec4(tex_color * total_light, attenuation);
}