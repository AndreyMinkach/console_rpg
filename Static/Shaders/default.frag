#version 330 core

varying vec2 vertex_pos;
varying vec2 vertex_uv;
varying vec4 vertex_color;

uniform sampler2D tex;

vec4 ambientLight = vec4(vec3(255, 224, 179) / 255.0, 0.1); // rbg - color, a - light strength
vec3 pointLight = vec3(0.0, 0.0, 5); // xy - light position, z - light radius
vec3 pointLightColor = vec3(255, 153, 204) / 255.0;

void main(void)
{
    vec4 color = texture2D(tex, vertex_uv) * vertex_color;

//    vec2 toLight = (pointLight.xy - vertex_pos);
//    float attenuation = clamp(1.0 - (length(toLight) / pointLight.z), 0.0, 1.0);
//
//    vec4 light1 = vec4(ambientLight.rgb * ambientLight.a, 1.0);
//    vec4 light2 = vec4(pointLightColor * attenuation, pow(attenuation, 3));
//    vec4 totalLight = light1 + light2;
//
//    vec4 pixelColor = color * clamp(totalLight, 0.0, 1.0);
//    gl_FragColor = clamp(pixelColor, 0.0, 1.0);
    gl_FragColor = color;
}