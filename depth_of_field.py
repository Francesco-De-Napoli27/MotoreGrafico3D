import numpy as np

class DepthOfField:
    def __init__(self, focal_distance=5.0, blur_factor=0.5):
        self.focal_distance = focal_distance
        self.blur_factor = blur_factor

    def calculate_blur_strength(self, object_distance):
        """Determina la quantità di sfocato basata sulla distanza dall'obiettivo"""
        return max(0.0, np.abs(object_distance - self.focal_distance) * self.blur_factor)
