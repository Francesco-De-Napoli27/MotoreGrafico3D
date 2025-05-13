import numpy as np


class AmbientOcclusion:
    def __init__(self, intensity=0.5, radius=0.3, samples=16):
        self.intensity = intensity
        self.radius = radius
        self.samples = samples

    def get_occlusion_factor(self, normal, position, sample_positions):
        """Calcola il fattore di occlusione sommando i contributi delle posizioni di campionamento"""
        occlusion = 0.0
        for sample in sample_positions:
            direction = normalize(sample - position)
            contribution = max(0.0, np.dot(normal, direction))
            occlusion += contribution

        occlusion /= self.samples
        return 1.0 - (occlusion * self.intensity)
