import math
from collision import *

GRAVITY = [0, -9.81, 0]

rigid_bodies = []  # Lista globale

class RigidBody:
    def __init__(self, position, mass=1.0, velocity=[0, 0, 0], angular_velocity=[0, 0, 0], size=[1, 1, 1],
                 bounciness=0.3, friction=0.8, static=False):
        self.position = list(position)
        self.velocity = list(velocity)
        self.angular_velocity = list(angular_velocity)
        self.mass = mass
        self.size = size
        self.bounciness = bounciness
        self.friction = friction
        self.forces = [0, 0, 0]
        self.torques = [0, 0, 0]
        self.static = static

        # Definisce un cubo con 8 vertici e 12 spigoli
        self.edges = [
            [[-0.5, -0.5, -0.5], [0.5, -0.5, -0.5]],
            [[0.5, -0.5, -0.5], [0.5, 0.5, -0.5]],
            [[0.5, 0.5, -0.5], [-0.5, 0.5, -0.5]],
            [[-0.5, 0.5, -0.5], [-0.5, -0.5, -0.5]],
            [[-0.5, -0.5, 0.5], [0.5, -0.5, 0.5]],
            [[0.5, -0.5, 0.5], [0.5, 0.5, 0.5]],
            [[0.5, 0.5, 0.5], [-0.5, 0.5, 0.5]],
            [[-0.5, 0.5, 0.5], [-0.5, -0.5, 0.5]],
            [[-0.5, -0.5, -0.5], [-0.5, -0.5, 0.5]],
            [[0.5, -0.5, -0.5], [0.5, -0.5, 0.5]],
            [[0.5, 0.5, -0.5], [0.5, 0.5, 0.5]],
            [[-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5]]
        ]

    def apply_torque(self, torque):
        for i in range(3):
            self.torques[i] += torque[i]

    def update_angular_velocity(self, torque, dt):
        """Aggiorna la velocità angolare del corpo rigido in base al torque applicato."""
        I = (1 / 12) * self.mass * (self.size[0] ** 2 + self.size[1] ** 2)
        angular_acceleration = scale(torque, 1 / I)
        self.angular_velocity = add(self.angular_velocity, scale(angular_acceleration, dt))

    def apply_force(self, force):
        for i in range(3):
            self.forces[i] += force[i]

    def apply_gravity(self):
        """Applica la forza di gravità al corpo rigido."""
        gravity_force = scale(GRAVITY, self.mass)
        self.apply_force(gravity_force)

    def update(self, dt):
        if self.static:
            return

        # Applica la forza di gravità
        self.apply_gravity()

        # Calcolo dell'attrito dinamico
        friction_force = multiply(self.velocity, -self.friction)
        self.apply_force(friction_force)

        # Simulazione della resistenza dell'aria
        air_resistance = multiply(self.velocity, -0.02)  # Fattore di resistenza
        self.apply_force(air_resistance)

        # Aggiornamento della posizione
        for i in range(3):
            self.velocity[i] += self.forces[i] * dt / self.mass
            self.position[i] += self.velocity[i] * dt

        # Aggiornamento della velocità angolare con torques
        self.update_angular_velocity(dt)

        # Reset delle forze dopo l'aggiornamento
        self.forces = [0, 0, 0]
        self.torques = [0, 0, 0]

        # Controllo collisioni
        self.check_collision_with_ground()

    def check_collision_with_ground(self, ground_y=0.0):
        min_y = self.position[1] - self.size[1] / 2
        if min_y < ground_y:
            self.position[1] = ground_y + self.size[1] / 2
            self.velocity[1] *= -self.bounciness
            self.velocity[0] *= self.friction
            self.velocity[2] *= self.friction

    def draw(self):
        from OpenGL.GL import glBegin, glEnd, glVertex3f, glPushMatrix, glPopMatrix, glTranslatef, GL_LINES

        glPushMatrix()
        glTranslatef(*self.position)
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3f(*vertex)
        glEnd()
        glPopMatrix()

# Funzione di aggiornamento globale
def update_physics():
    dt = 0.016  # Update rate 60 FPS
    for body in rigid_bodies:
        body.update(dt)
    check_all_collisions()

def check_all_collisions():
    from collision import sphere_sphere_collision, aabb_aabb_collision
    for i in range(len(rigid_bodies)):
        for j in range(i + 1, len(rigid_bodies)):
            a, b = rigid_bodies[i], rigid_bodies[j]
            if a.static and b.static:
                continue
            if a.size == b.size:
                aabb_aabb_collision(a, b)
            else:
                sphere_sphere_collision(a, b)



class Constraint:
    def __init__(self, bodyA, bodyB, rest_length, stiffness=0.5):
        self.bodyA = bodyA
        self.bodyB = bodyB
        self.rest_length = rest_length
        self.stiffness = stiffness

    def apply(self):
        dist_vector = subtract(self.bodyA.position, self.bodyB.position)
        current_length = length(dist_vector)

        # Calcola la forza elastica della molla
        correction = multiply(normalize(dist_vector), (current_length - self.rest_length) * self.stiffness)
        self.bodyA.apply_force(subtract([0, 0, 0], correction))
        self.bodyB.apply_force(correction)
