import numpy as np

class Light:
    def __init__(self, position, color=[1.0, 1.0, 1.0], intensity=1.0):
        self.position = np.array(position, dtype=np.float32)
        self.color = np.array(color, dtype=np.float32)
        self.intensity = intensity

    def update_position(self, new_position):
        """Aggiorna la posizione della luce"""
        self.position = np.array(new_position, dtype=np.float32)
