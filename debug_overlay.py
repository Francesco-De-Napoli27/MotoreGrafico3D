import glfw
import time
import numpy as np
from OpenGL.GL import *
import aimgui
from aimgui.integrations.glfw import GlfwRenderer

class DebugOverlay:
    def __init__(self):
        """Inizializza l'overlay di debug con ImGui"""
        imgui.create_context()
        self.impl = None
        self.last_time = time.time()
        self.frame_count = 0
        self.fps = 0.0

    def set_window(self, window):
        """Collega l'overlay alla finestra di rendering"""
        self.impl = GlfwRenderer(window)

    def update_fps(self):
        """Calcola gli FPS medi in tempo reale"""
        current_time = time.time()
        self.frame_count += 1
        delta = current_time - self.last_time
        if delta >= 1.0:
            self.fps = self.frame_count / delta
            self.frame_count = 0
            self.last_time = current_time

    def render(self):
        """Renderizza il pannello di debug"""
        imgui.new_frame()

        if imgui.begin("Debug Overlay"):
            imgui.text(f"FPS: {self.fps:.2f}")
            imgui.separator()
            imgui.text(f"GPU Utilization: {self.get_gpu_usage()}%")
            imgui.text(f"Active Effects:")
            imgui.text("- HDR")
            imgui.text("- Bloom")
            imgui.text("- Motion Blur")
            imgui.text("- Depth of Field")
            imgui.text("- SSR")
            imgui.end()

        imgui.render()
        self.impl.render(imgui.get_draw_data())

    def get_gpu_usage(self):
        """Simulazione del monitoraggio dell'utilizzo GPU"""
        return np.random.randint(30, 90)  # Simulazione casuale
