import glfw
from OpenGL.GL import *
import numpy as np
import time

class UIEngine:
    def __init__(self, window):
        """Usa la finestra esistente per la UI e gestisce gli input"""
        self.window = window
        glfw.make_context_current(self.window)  # Assicura che OpenGL sia attivo
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_cursor_pos_callback(self.window, self.cursor_callback)

        self.mouse_position = (0, 0)
        self.keys_pressed = {}
        self.quality_text = "Qualità: Ultra"

        # Monitoraggio FPS
        self.last_time = time.time()
        self.frame_count = 0
        self.current_fps = 60

        self.texture_id = None  # Creiamo la texture più tardi



    def load_font_texture(self, path):
        """Carica la texture solo quando il contesto OpenGL è attivo"""
        if self.texture_id is None:  # Controlla se la texture è già stata generata
            self.texture_id = glGenTextures(1)

    def update_fps(self):
        """Calcola gli FPS e aggiorna il livello di qualità grafica"""
        current_time = time.time()
        self.frame_count += 1

        if current_time - self.last_time >= 1.0:
            self.current_fps = self.frame_count
            self.frame_count = 0
            self.last_time = current_time

            self.adjust_quality()

    def adjust_quality(self):
        """Regola la qualità grafica in base agli FPS"""
        if self.current_fps >= 60:
            self.quality_text = "Qualità: Ultra"
        elif self.current_fps >= 45:
            self.quality_text = "Qualità: Alta"
        elif self.current_fps >= 30:
            self.quality_text = "Qualità: Media"
        else:
            self.quality_text = "Qualità: Bassa"

    def key_callback(self, window, key, scancode, action, mods):
        """Gestisce gli input da tastiera"""
        if action == glfw.PRESS or action == glfw.REPEAT:
            self.keys_pressed[key] = True
        elif action == glfw.RELEASE:
            self.keys_pressed[key] = False

    def cursor_callback(self, window, xpos, ypos):
        """Registra la posizione del mouse"""
        self.mouse_position = (xpos, ypos)

    def draw_textured_quad(self, x, y, width, height):
        """Disegna un quad con una parte della texture dei caratteri"""
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex2f(x, y)
        glTexCoord2f(1.0, 0.0); glVertex2f(x + width, y)
        glTexCoord2f(1.0, 1.0); glVertex2f(x + width, y + height)
        glTexCoord2f(0.0, 1.0); glVertex2f(x, y + height)
        glEnd()

        glDisable(GL_TEXTURE_2D)

    def render(self):
        """Renderizza la UI e inizializza la texture solo quando OpenGL è attivo"""
        if self.texture_id is None:
            self.texture_id = glGenTextures(1)  # Creiamo la texture nel primo frame


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.update_fps()
        self.draw_textured_quad(-0.9, 0.85, 0.3, 0.1)
        glfw.swap_buffers(self.window)
        glfw.poll_events()
