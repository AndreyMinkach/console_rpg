from ctypes import byref
from enum import Enum

from pyglet.gl import *
from pyglet.image import Texture

import configs
from Helpers import helper


class FBOAttachment(Enum):
    Color = dict(internal_format=GL_RGBA, data_type=GL_UNSIGNED_BYTE, attachment=GL_COLOR_ATTACHMENT0)
    Depth = dict(internal_format=GL_DEPTH_COMPONENT, data_type=GL_FLOAT, attachment=GL_DEPTH_ATTACHMENT)


class FBO:
    __slots__ = ['width', 'height', 'frame_buffer', 'texture']

    def __init__(self,
                 width: int,
                 height: int,
                 fbo_attachment: FBOAttachment = FBOAttachment.Color
                 ):
        """
        Initializes a new FBO with specified parameters

        :param width: FBO texture width
        :param height: FBO texture height
        """

        self.width = width
        self.height = height
        fbo_parameters = fbo_attachment.value
        self.texture: Texture = helper.create_texture(width, height, internal_format=fbo_parameters['internal_format'],
                                                      data_type=fbo_parameters['data_type'], allocate_memory=False)
        self.frame_buffer = self.create_fbo(fbo_parameters['attachment'])

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

    def create_fbo(self, attachment: int):
        """
        Creates and initializes a new FrameBufferObject
        """
        frame_buffer = GLuint(0)
        glGenFramebuffers(1, byref(frame_buffer))
        glBindFramebuffer(GL_FRAMEBUFFER, frame_buffer)
        glFramebufferTexture2D(GL_FRAMEBUFFER, attachment, GL_TEXTURE_2D, self.texture.id, 0)

        # check for errors
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print('ERROR: Frame buffer is not complete!')

        # we have to unbind created FBO
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        return frame_buffer
