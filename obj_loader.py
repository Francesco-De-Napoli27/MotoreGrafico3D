import os
import numpy as np


class OBJLoader:
    def __init__(self, path):
        self.vertices = []
        self.normals = []
        self.indices = []

        if not os.path.isfile(path):
            raise FileNotFoundError(f"Il file {path} non esiste!")

        self.load_obj(path)

    def load_obj(self, path):
        positions = []
        normals = []
        temp_indices = []

        with open(path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if not parts:
                    continue

                if parts[0] == "v":  # Vertici
                    positions.append([float(parts[1]), float(parts[2]), float(parts[3])])
                elif parts[0] == "vn":  # Normali
                    normals.append([float(parts[1]), float(parts[2]), float(parts[3])])
                elif parts[0] == "f":  # Facce
                    for vertex in parts[1:]:
                        v, _, vn = vertex.split("/")  # Estrai indici vertice/normale
                        temp_indices.append(int(v) - 1)
                        self.normals.append(normals[int(vn) - 1])

        self.vertices = positions
        self.indices = temp_indices
