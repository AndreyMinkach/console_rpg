from ctypes import byref

from pyglet.gl import *
from pyglet.image import Texture

import configs


class FBO:
    __slots__ = ['width', 'height', 'frame_buffer', 'texture']

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.texture: Texture = Texture.create(self.width, self.height, GL_RGBA)
        self.frame_buffer = self.create_fbo()

        # we have to unbind created FBO
        self.unbind_fbo()

    def __del__(self):
        self.unbind_fbo()
        glDeleteFramebuffers(1, self.frame_buffer)
        del self.texture

    def bind_fbo(self):
        """
        Binds FBO for the further usage
        """
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindFramebuffer(GL_FRAMEBUFFER, self.frame_buffer)
        glViewport(0, 0, self.width, self.height)

    @staticmethod
    def unbind_fbo():
        """
        Binds the default FBO, so that everything will be rendered on the screen
        """
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, configs.WINDOW_WIDTH, configs.WINDOW_HEIGHT)

    def create_fbo(self):
        """
        Creates and initializes a new FrameBufferObject
        """
        frame_buffer = GLuint(0)
        glGenFramebuffers(1, byref(frame_buffer))
        glBindFramebuffer(GL_FRAMEBUFFER, frame_buffer)
        glDrawBuffer(GL_COLOR_ATTACHMENT0)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture.id, 0)

        # check for errors
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print('ERROR: Frame buffer is not complete!')

        return frame_buffer
