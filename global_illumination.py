import numpy as np

class GlobalIllumination:
    def __init__(self, intensity=1.0, bounce_factor=0.5):
        self.intensity = intensity
        self.bounce_factor = bounce_factor

    def calculate_bounce(self, normal, light_direction):
        """Calcola la direzione della luce riflessa"""
        reflected_light = light_direction - 2 * np.dot(light_direction, normal) * normal
        return reflected_light * self.bounce_factor
