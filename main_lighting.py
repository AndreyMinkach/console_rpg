from random import random, seed

import OpenGL.GL
import numpy as np
from pyglet.gl import *
from pyglet.graphics import Batch

fs = """
uniform vec3 lightLocation;
uniform vec3 lightColor;

const float gamma = 2.2;

void main() {
    float distance = length(lightLocation.xy - gl_FragCoord.xy);
    float radius = lightLocation.z;
    float a = 2.0 / radius;
    float b = 1.0 / (radius * radius);
    //float attenuation = 1.0 / (1.0 + a * distance + b * distance * distance);
    //float attenuation = clamp(1.0 / (pow(distance, 2.4)), 0, 1);
    //float attenuation = clamp(1.0 - pow(distance/radius, 2), 0.0, 1.0);
    float attenuation = clamp(pow((radius - distance) / pow(radius, 1.2), 1.3), 0.0, 1.0);
    vec4 color = vec4(attenuation, attenuation, attenuation, pow(attenuation, 3)) * vec4(lightColor, 1);
    //vec4 color = vec4(lightColor, 1) * attenuation;
    
    gl_FragColor = vec4(pow(color.rgb, vec3(1.0 / gamma)), pow(attenuation, 0.5));
    //gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
"""


class Block:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._vertices = [
            np.array([self.x, self.y]),
            np.array([self.x, self.y + self.height]),
            np.array([self.x + self.width, self.y + self.height]),
            np.array([self.x + self.width, self.y])
        ]
        self._normals = []
        self._edges = []
        for i in range(len(self._vertices)):
            current_vertex = self._vertices[i]
            next_vertex = self._vertices[(i + 1) % len(self._vertices)]
            self._edges.append([current_vertex, next_vertex])
            edge = next_vertex - current_vertex
            self._normals.append(np.array([edge[1], -edge[0]]))
        self._edges = np.array(self._edges)
        self._normals = np.array(self._normals).T

    def get_vertices(self):
        return self._vertices

    def get_normals(self):
        return self._normals

    def get_edges(self):
        return self._edges


class Light:
    def __init__(self, location, radius, red, green, blue):
        self.location = location
        self.radius = radius
        self.red = red
        self.green = green
        self.blue = blue


width = 1280
height = 680
window = pyglet.window.Window(width, height, vsync=False)
window.set_location((window.screen.width - window.width) // 2, (window.screen.height - window.height) // 2)
glClearColor(0.0, 0.0, 0.0, 1)

lights = []
blocks = []

shader_program: int
fragment_shader: int


def init_shader():
    global shader_program, fragment_shader

    shader_program = OpenGL.GL.glCreateProgram()
    fragment_shader = OpenGL.GL.glCreateShader(GL_FRAGMENT_SHADER)

    OpenGL.GL.glShaderSource(fragment_shader, fs)
    OpenGL.GL.glCompileShader(fragment_shader)
    if OpenGL.GL.glGetShaderiv(fragment_shader, GL_COMPILE_STATUS) == gl.GL_FALSE:
        print("Fragment shader not compiled!")

    OpenGL.GL.glAttachShader(shader_program, fragment_shader)
    OpenGL.GL.glLinkProgram(shader_program)
    OpenGL.GL.glValidateProgram(shader_program)


init_shader()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
OpenGL.GL.glOrtho(0, width, height, 0, 1, -1)
glMatrixMode(GL_MODELVIEW)

glEnable(GL_STENCIL_TEST)


def set_up_objects():
    light_count = 5 + int(random() * 1)
    block_count = 20 + int(random() * 1)

    for i in range(light_count):
        location = np.array([random() * width, random() * height])
        radius = (random() * 500)
        lights.append(Light(location, radius, random() * 10.0, random() * 10, random() * 10.0))

    for i in range(block_count):
        block_width, block_height = 50, 50
        x = int(random() * (width - block_width))
        y = int(random() * (height - block_height))
        blocks.append(Block(x, y, block_width, block_height))


seed(1)
set_up_objects()

edges_array = np.array([[[272, 275], [272, 325]],
                        [[272, 325], [322, 325]],
                        [[322, 325], [322, 275]],
                        [[322, 275], [272, 275]]])
normal_array = np.array([[50, 0], [0, - 50], [-50, 0], [0, 50]])
light_pos_array = np.array([977.63151229, 173.4469375])

vertex_array = edges_array[:, 0]

from time import time

iterations = 1000

time_sum = 0
for _ in range(iterations):
    start = time()
    light_dir_array = vertex_array - light_pos_array
    result = light_dir_array.dot(normal_array.T)
    time_sum += time() - start
# temp = np.einsum('ij,ij->i', light_dir_array.dot(normal_array.T), light_dir_array)

print(time_sum)

light_dir_array = edges_array[:, 0] - light_pos_array
time_sum = 0
for _ in range(iterations):
    start = time()
    result1 = np.dot(normal_array[0], light_dir_array[0])
    result2 = np.dot(normal_array[1], light_dir_array[1])
    result3 = np.dot(normal_array[2], light_dir_array[2])
    result4 = np.dot(normal_array[3], light_dir_array[3])
    time_sum += time() - start

print(time_sum)
print()


def calculate_dots(lights, blocks) -> (list, list):
    dot_list = []
    light_direction_list = []
    for light in lights:

        for block in blocks:
            vertices = block.get_vertices()
            normals = block.get_normals()

            light_directions = vertices - light.location
            dot_list.append(light_directions.dot(normals))
            light_direction_list.append(light_directions)
    return dot_list, light_direction_list


@window.event
def on_draw():
    window.set_caption(f"FPS: {pyglet.clock.get_fps()}")
    window.clear()

    current_index = 0
    dots_result, light_dirs_result = calculate_dots(lights, blocks)

    for light in lights:
        glColorMask(False, False, False, False)
        glStencilFunc(GL_ALWAYS, 1, 1)
        glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)

        batch = Batch()
        # verts =

        for block in blocks:
            edges = block.get_edges()

            light_directions = light_dirs_result[current_index]
            dots = dots_result[current_index]
            for i in range(len(edges)):
                if dots[i][i] > 0:
                    current_vertex, next_vertex = edges[i]
                    light_direction = light_directions[i]
                    point1 = current_vertex + light_direction * width
                    point2 = next_vertex + (next_vertex - light.location) * width

                    batch.add(4, GL_QUADS, None, ('v2f', (current_vertex[0], current_vertex[1],
                                                          point1[0], point1[1], point2[0], point2[1],
                                                          next_vertex[0], next_vertex[1])))
                    # print((current_vertex[0], current_vertex[1]))
                    # print((point1[0], point1[1]))
                    # print((point2[0], point2[1]))
                    # print((next_vertex[0], next_vertex[1]))

                    # glBegin(GL_QUADS)
                    # glVertex2f(current_vertex[0], current_vertex[1])
                    # glVertex2f(point1[0], point1[1])
                    # glVertex2f(point2[0], point2[1])
                    # glVertex2f(next_vertex[0], next_vertex[1])
                    # glEnd()

            current_index += 1

        batch.draw()

        glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)
        glStencilFunc(GL_EQUAL, 0, 1)
        glColorMask(True, True, True, True)

        glUseProgram(shader_program)
        OpenGL.GL.glUniform3f(OpenGL.GL.glGetUniformLocation(shader_program, "lightLocation"), light.location[0],
                              light.location[1], light.radius)
        OpenGL.GL.glUniform3f(OpenGL.GL.glGetUniformLocation(shader_program, "lightColor"), light.red, light.green,
                              light.blue)
        glEnable(GL_BLEND)
        # glBlendEquation(GL_FUNC_REVERSE_SUBTRACT)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(0, height)
        glVertex2f(width, height)
        glVertex2f(width, 0)
        glEnd()

        glDisable(GL_BLEND)
        glUseProgram(0)
        glClear(GL_STENCIL_BUFFER_BIT)

    glColor3f(0.3, 0.1, 0)
    for block in blocks:
        glBegin(GL_QUADS)
        for vertex in block.get_vertices():
            glVertex2f(vertex[0], vertex[1])
        glEnd()


def update(dt):
    pass


@window.event
def on_close():
    glDeleteShader(fragment_shader)
    glDeleteProgram(shader_program)


pyglet.clock.schedule_interval(update, 1.0 / 1000.0)
pyglet.app.run()
