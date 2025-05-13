from OpenGL.GL import *
from hdr import HDR
from bloom import Bloom
from motion_blur import MotionBlur
from depth_of_field import DepthOfField
from ssr import ScreenSpaceReflections

class PostProcessingEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.hdr = HDR(exposure=1.2, gamma=2.2)
        self.bloom = Bloom(blur_strength=1.2)
        self.motion_blur = MotionBlur(blur_strength=0.8)
        self.depth_of_field = DepthOfField(focal_distance=5.0, blur_factor=0.5)
        self.screen_reflections = ScreenSpaceReflections(max_distance=50.0, reflectivity=0.8)

        # Creazione del framebuffer
        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

        # Creazione della texture per il colore
        self.color_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.color_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Creazione della texture depth
        self.depth_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.depth_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, width, height, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        # Attacca le texture al framebuffer
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.color_texture, 0)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.depth_texture, 0)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError("Errore nella creazione del framebuffer di post-processing!")

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def bind(self):
        """Attiva il framebuffer di post-processing"""
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glViewport(0, 0, self.width, self.height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def unbind(self):
        """Ripristina il framebuffer principale"""
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def enable(self):
        """Metodo aggiunto per abilitare il framebuffer, equivalente a bind()"""
        self.bind()

    def apply_effects(self, shader):
        """Applica tutti gli effetti in sequenza"""
        shader.use()
        shader.set_uniform_float("exposure", self.hdr.exposure)
        shader.set_uniform_float("gamma", self.hdr.gamma)
        shader.set_uniform_float("blurStrength", self.bloom.blur_strength)
        shader.set_uniform_float("motionBlurStrength", self.motion_blur.blur_strength)
        shader.set_uniform_float("focalDistance", self.depth_of_field.focal_distance)
        shader.set_uniform_float("blurFactor", self.depth_of_field.blur_factor)
        shader.set_uniform_float("maxDistance", self.screen_reflections.max_distance)
        shader.set_uniform_float("reflectivity", self.screen_reflections.reflectivity)
