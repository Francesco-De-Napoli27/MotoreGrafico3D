from OpenGL.GL import *

class ShadowMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Creazione del framebuffer
        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

        # Creazione della texture depth map
        self.shadow_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.shadow_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, width, height, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        border_color = [1.0, 1.0, 1.0, 1.0]
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, border_color)

        # Attacca la texture depth al framebuffer
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.shadow_texture, 0)
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError("Errore nella creazione del framebuffer delle ombre!")

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def enable(self):
        """Abilita il shadow mapping: alias per bind()"""
        self.bind()

    def bind(self):
        """Attiva il framebuffer delle ombre per la render pass"""
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glViewport(0, 0, self.width, self.height)
        glClear(GL_DEPTH_BUFFER_BIT)

    def unbind(self):
        """Ripristina il framebuffer principale"""
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
