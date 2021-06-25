#version 330 core

#define DIAGONAL 0.70710678118
#define DIAGONAL_SQR 1.41421356237
#define PI 3.14159265359
#define PI_2 6.28318530718

varying vec2 vertex_pos;
varying vec2 vertex_uv;
varying vec2 resolution;

uniform sampler2D tex;
uniform int pixels_to_skip = 2;// the more number the better performance
uniform int shadow_bias = 2;// helps to fix the issue when the shadow is rendered behind the object

const float acos_zero = acos(0);

float get_shadow_limit(vec2 uv)
{
    float aspect_ratio = resolution.x / resolution.y;
    float amplitude = 0.5 - (acos_zero / (PI * aspect_ratio));// controls the amplitude of shadow limiting function
    float a = abs(sin(PI_2 * uv.y));
    float b = 1.0 - abs(cos(PI_2 * uv.y));
    return 0.5 - min(a, PI * b) * amplitude;
}

void main(void)
{
    vec2 uv = vertex_uv;
    vec3 tex_color = vec3(1.0);
    vec2 tex_size = textureSize(tex, 0);

    //    int steps_number = 30;
    //    float skip = int(uv.x * steps_number * DIAGONAL_SQR) + 1.0;
    //    float pixel_size = (pixels_to_skip + skip) / tex_size.x;
    //    float pixel_size = 1.0 / tex_size.x;

    float pixel_size = pixels_to_skip / tex_size.x;
    float shadow_offset = shadow_bias / tex_size.x;
    float tex_value = 1.0;

    float shadow_limit = get_shadow_limit(uv);

    for (float xx = uv.x - pixel_size; xx >= 0.0 && xx <= shadow_limit; xx -= pixel_size){
        //pixel_size = (xx * steps_number + 1.0) / tex_size.x;
        float local_x = max(uv.x - xx - shadow_offset, shadow_offset);
        tex_value *= texture(tex, vec2(local_x, uv.y)).r;
    }

    gl_FragColor = vec4(tex_color * tex_value, 1.0);
}