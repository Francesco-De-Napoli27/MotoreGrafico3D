import numpy as np

class Particle:
    def __init__(self, position, velocity, lifespan=1.5, color=[1.0, 1.0, 1.0]):
        self.position = np.array(position, dtype=np.float32)
        self.velocity = np.array(velocity, dtype=np.float32)
        self.lifespan = lifespan
        self.color = np.array(color, dtype=np.float32)

    def update(self, dt):
        """Aggiorna la posizione e riduce la durata della particella"""
        self.position += self.velocity * dt
        self.lifespan -= dt

    def is_alive(self):
        """Verifica se la particella è ancora attiva"""
        return self.lifespan > 0
