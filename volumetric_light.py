import numpy as np

class VolumetricLight:
    def __init__(self, light_position, light_color=[1.0, 1.0, 1.0], density=0.5):
        self.light_position = np.array(light_position, dtype=np.float32)
        self.light_color = np.array(light_color, dtype=np.float32)
        self.density = density  # Controlla la quantità di diffusione

    def get_scattering_factor(self, view_position):
        """Calcola il coefficiente di scattering basato sulla distanza"""
        distance = np.linalg.norm(self.light_position - view_position)
        return np.exp(-self.density * distance)
