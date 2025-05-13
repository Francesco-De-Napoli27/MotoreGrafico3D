import math

# Funzioni di supporto vettoriale
def length(v):
    return math.sqrt(sum(x * x for x in v))

def normalize(v):
    l = length(v)
    if l == 0:
        return [0, 0, 0]
    return [x / l for x in v]

def dot(a, b):
    return sum(a[i] * b[i] for i in range(3))

def subtract(a, b):
    return [a[i] - b[i] for i in range(3)]

def add(a, b):
    return [a[i] + b[i] for i in range(3)]

def multiply(v, scalar):
    return [x * scalar for x in v]

def cross(v1, v2):
    return [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]

# Funzioni per gestione forme 3D
def sphere_sphere_collision(bodyA, bodyB):
    dist = subtract(bodyA.position, bodyB.position)
    distance = length(dist)
    penetration = bodyA.size[0] / 2 + bodyB.size[0] / 2 - distance
    if penetration > 0:
        normal = normalize(dist)
        resolve_collision(bodyA, bodyB, normal, penetration)

def sphere_aabb_collision(bodyA, bodyB):
    closest_point = [
        clamp(bodyA.position[0], bodyB.position[0] - bodyB.size[0] / 2, bodyB.position[0] + bodyB.size[0] / 2),
        clamp(bodyA.position[1], bodyB.position[1] - bodyB.size[1] / 2, bodyB.position[1] + bodyB.size[1] / 2),
        clamp(bodyA.position[2], bodyB.position[2] - bodyB.size[2] / 2, bodyB.position[2] + bodyB.size[2] / 2)
    ]
    dist = subtract(bodyA.position, closest_point)
    distance = length(dist)
    penetration = bodyA.size[0] / 2 - distance
    if penetration > 0:
        normal = normalize(dist)
        resolve_collision(bodyA, bodyB, normal, penetration)

def aabb_aabb_collision(bodyA, bodyB):
    # Separating Axis Theorem per AABB
    overlap = True
    for i in range(3):
        minA = bodyA.position[i] - bodyA.size[i] / 2
        maxA = bodyA.position[i] + bodyA.size[i] / 2
        minB = bodyB.position[i] - bodyB.size[i] / 2
        maxB = bodyB.position[i] + bodyB.size[i] / 2
        if maxA < minB or maxB < minA:
            overlap = False
            break
    if overlap:
        # Calcola la penetrazione per l'asse separatore
        penetration = min(maxA - minB, maxB - minA)
        normal = [0, 0, 0]  # Da calcolare in modo adeguato
        resolve_collision(bodyA, bodyB, normal, penetration)

def polygon_convex_collision(bodyA, bodyB):
    # Rilevamento delle collisioni tra poligoni convessi usando il SAT
    axes = get_axes(bodyA) + get_axes(bodyB)
    for axis in axes:
        projectionA = project_polygon(bodyA, axis)
        projectionB = project_polygon(bodyB, axis)
        if not overlap(projectionA, projectionB):
            return False  # Nessuna collisione se c'è un separatore
    # Risolvi la collisione se non c'è separatore
    resolve_collision(bodyA, bodyB, axis, 0)
    return True

def get_axes(body):
    # Calcola gli assi separatori per il poligono convesso (utilizza i bordi)
    edges = get_edges(body)
    axes = []
    for edge in edges:
        axes.append(normalize(cross(edge[0], edge[1])))
    return axes

def get_edges(body):
    # Restituisce gli spigoli di un poligono convesso (approssimato)
    edges = []
    vertices = body.vertices
    for i in range(len(vertices)):
        edge = subtract(vertices[i], vertices[(i + 1) % len(vertices)])
        edges.append(edge)
    return edges

def project_polygon(body, axis):
    min_proj = dot(body.vertices[0], axis)
    max_proj = min_proj
    for vertex in body.vertices[1:]:
        projection = dot(vertex, axis)
        min_proj = min(min_proj, projection)
        max_proj = max(max_proj, projection)
    return min_proj, max_proj

def overlap(projectionA, projectionB):
    return not (projectionA[1] < projectionB[0] or projectionB[1] < projectionA[0])

# RISOLUZIONE COLLISIONE
def resolve_collision(bodyA, bodyB, normal, penetration):
    relative_velocity = subtract(bodyB.velocity, bodyA.velocity)
    normal_velocity = dot(relative_velocity, normal)

    if normal_velocity > 0:
        return

    restitution = min(bodyA.bounciness, bodyB.bounciness)
    impulse_magnitude = -(1 + restitution) * normal_velocity / (1 / bodyA.mass + 1 / bodyB.mass)
    impulse = multiply(normal, impulse_magnitude)

    bodyA.velocity = subtract(bodyA.velocity, multiply(impulse, 1 / bodyA.mass))
    bodyB.velocity = add(bodyB.velocity, multiply(impulse, 1 / bodyB.mass))

    correction = multiply(normal, penetration / (1 / bodyA.mass + 1 / bodyB.mass) * 0.8)
    bodyA.position = subtract(bodyA.position, multiply(correction, 1 / bodyA.mass))
    bodyB.position = add(bodyB.position, multiply(correction, 1 / bodyB.mass))

    # Controllo della rottura con effetti particellari
    fractured_A, particles_A = fracture_object(bodyA)
    fractured_B, particles_B = fracture_object(bodyB)

    # Aggiorna la simulazione con nuovi frammenti e particelle
    rigid_bodies.remove(bodyA)
    rigid_bodies.remove(bodyB)
    rigid_bodies.extend(fractured_A)
    rigid_bodies.extend(fractured_B)
    particle_system.extend(particles_A)
    particle_system.extend(particles_B)




def get_contact_point(bodyA, bodyB):
    return [
        (bodyA.position[0] + bodyB.position[0]) / 2,
        (bodyA.position[1] + bodyB.position[1]) / 2,
        (bodyA.position[2] + bodyB.position[2]) / 2
    ]

class SpatialGrid:
    def __init__(self, cell_size=2.0):
        self.cell_size = cell_size
        self.cells = {}

    def get_cell_coords(self, position):
        return tuple(int(position[i] // self.cell_size) for i in range(3))

    def add_body(self, body):
        cell = self.get_cell_coords(body.position)
        if cell not in self.cells:
            self.cells[cell] = []
        self.cells[cell].append(body)

    def clear(self):
        self.cells = {}

    def get_potential_collisions(self, body):
        cell = self.get_cell_coords(body.position)
        neighbors = [cell]

        # Espandi la ricerca alle celle vicine
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    neighbors.append((cell[0] + dx, cell[1] + dy, cell[2] + dz))

        possible_collisions = []
        for neighbor in neighbors:
            if neighbor in self.cells:
                possible_collisions.extend(self.cells[neighbor])

        return possible_collisions
