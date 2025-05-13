import numpy as np

class MotionBlur:
    def __init__(self, blur_strength=0.8):
        self.blur_strength = blur_strength
        self.previous_positions = {}

    def calculate_blur_vector(self, current_position, object_id):
        """Calcola la direzione dello sfocato basata sul movimento"""
        previous_position = self.previous_positions.get(object_id, current_position)
        blur_vector = np.array(current_position) - np.array(previous_position)
        self.previous_positions[object_id] = current_position
        return blur_vector * self.blur_strength
