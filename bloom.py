import numpy as np
from OpenGL.GL import *

class Bloom:
    def __init__(self, blur_strength=1.2):
        self.blur_strength = blur_strength

    def apply_blur(self, texture):
        """Simula l'effetto Bloom sfocando le zone luminose"""
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def enable(self):
        """
        Metodo di abilitazione per l'effetto Bloom.
        Qui puoi inserire la logica necessaria per attivare l'effetto,
        ad esempio legando un framebuffer, impostando shader dedicati o applicando una blur
        su una texture specifica.
        Al momento, come placeholder, stampiamo un messaggio.
        """
        print("Bloom effect enabled!")
        # Se disponi di una texture di riferimento per il bloom, puoi chiamare:
        # self.apply_blur(texture)
