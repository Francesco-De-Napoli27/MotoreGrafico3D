import numpy as np

class ScreenSpaceReflections:
    def __init__(self, max_distance=50.0, reflectivity=0.8):
        self.max_distance = max_distance
        self.reflectivity = reflectivity

    def calculate_reflection_vector(self, normal, view_direction):
        """Calcola il vettore di riflessione rispetto alla normale della superficie"""
        return view_direction - 2 * np.dot(view_direction, normal) * normal
