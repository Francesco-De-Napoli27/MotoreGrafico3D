import numpy as np

class HDR:
    def __init__(self, exposure=1.0, gamma=2.2):
        self.exposure = exposure
        self.gamma = gamma

    def apply_tone_mapping(self, color):
        """Applica il tone mapping e la correzione gamma"""
        mapped_color = np.array(color) / (np.array(color) + 1.0)
        corrected_color = np.power(mapped_color, 1.0 / self.gamma)
        return corrected_color * self.exposure
