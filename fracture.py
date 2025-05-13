from particles import Particle
import numpy as np
import os
from OpenGL import *
import math

def fracture_object(body, impact_force_threshold=50.0, num_fragments=5):
    """Divide un oggetto in frammenti e genera particelle visive se l'impatto è abbastanza forte."""
    impact_force = np.linalg.norm(body.velocity) * body.mass

    if impact_force < impact_force_threshold:
        return [body], []  # Nessuna rottura, quindi nessuna particella

    fragments = []
    particles = []
    for _ in range(num_fragments):
        fragment_size = np.array(body.size) * (0.4 + 0.2 * np.random.rand())
        fragment_position = np.array(body.position) + np.random.uniform(-fragment_size, fragment_size)
        fragment_velocity = np.array(body.velocity) * np.random.uniform(0.5, 1.5)

        fragment = RigidBody(position=fragment_position, size=fragment_size, velocity=fragment_velocity,
                             mass=body.mass / num_fragments, bounciness=body.bounciness, friction=body.friction)
        fragments.append(fragment)

        # Genera particelle di detriti
        for _ in range(10):
            particle_velocity = fragment_velocity * np.random.uniform(0.3, 0.7)
            particle = Particle(position=fragment_position, velocity=particle_velocity, lifespan=np.random.uniform(0.5, 2.0))
            particles.append(particle)

    return fragments, particles
