#version 330 core

varying vec2 vertex_pos;
varying vec2 vertex_uv;

uniform sampler2D tex;
uniform int pixels_to_skip = 1; // the more number the better performance

void main(void)
{
    vec2 uv = vertex_uv;
    vec2 tex_size = textureSize(tex, 0);
    float pixel_size = float(pixels_to_skip) / tex_size.x;

    vec3 tex_color = vec3(1.0);
    for (float xx = uv.x - pixel_size; xx >= 0.0; xx -= pixel_size){
        tex_color *= texture(tex, vec2(uv.x - xx, uv.y)).xyz;
    }
    gl_FragColor = vec4(tex_color, 1.0);
}