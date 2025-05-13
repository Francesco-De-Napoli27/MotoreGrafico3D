import numpy as np

def translation_matrix(t):
    mat = np.identity(4, dtype=np.float32)
    mat[:3, 3] = t
    return mat

def rotation_matrix_x(angle):
    rad = np.radians(angle)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[1, 0, 0, 0],
                     [0, c, -s, 0],
                     [0, s, c, 0],
                     [0, 0, 0, 1]], dtype=np.float32)

def rotation_matrix_y(angle):
    rad = np.radians(angle)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c, 0, s, 0],
                     [0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [0, 0, 0, 1]], dtype=np.float32)

def rotation_matrix_z(angle):
    rad = np.radians(angle)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c, -s, 0, 0],
                     [s, c, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]], dtype=np.float32)

def scale_matrix(s):
    return np.diag(np.append(s, 1.0)).astype(np.float32)
