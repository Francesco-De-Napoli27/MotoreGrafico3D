import numpy as np

class Frustum:
    def __init__(self, camera):
        self.camera = camera
        self.planes = []

    def update_frustum_planes(self):
        view_proj = np.dot(self.camera.get_projection_matrix(800.0 / 600.0), self.camera.get_view_matrix())
        self.planes = [view_proj[i, :] + view_proj[3, :] for i in range(3)]

    def is_visible(self, obj_position, obj_radius):
        for plane in self.planes:
            if np.dot(plane[:3], obj_position) + plane[3] + obj_radius < 0:
                return False
        return True

class Camera:
    def __init__(self, input_manager):
        self.position = np.array([0.0, 0.0, 3.0], dtype=np.float32)
        self.target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)

    def get_view_matrix(self):
        return look_at(self.position, self.target, self.up)

    def get_projection_matrix(self, aspect_ratio, fov=60.0, near=0.1, far=100.0):
        f = 1.0 / np.tan(np.radians(fov) / 2.0)
        proj = np.zeros((4, 4), dtype=np.float32)
        proj[0, 0] = f / aspect_ratio
        proj[1, 1] = f
        proj[2, 2] = (far + near) / (near - far)
        proj[2, 3] = (2 * far * near) / (near - far)
        proj[3, 2] = -1.0
        return proj


# Utility
def normalize(v):
    return v / np.linalg.norm(v)

def look_at(eye, center, up):
    f = normalize(center - eye)
    s = normalize(np.cross(f, up))
    u = np.cross(s, f)

    result = np.identity(4, dtype=np.float32)
    result[0, :3] = s
    result[1, :3] = u
    result[2, :3] = -f
    result[:3, 3] = -np.dot(result[:3, :3], eye)
    return result

def perspective(fov, aspect, near, far):
    tan_half_fov = np.tan(fov / 2)
    result = np.zeros((4, 4), dtype=np.float32)
    result[0, 0] = 1 / (aspect * tan_half_fov)
    result[1, 1] = 1 / (tan_half_fov)
    result[2, 2] = -(far + near) / (far - near)
    result[2, 3] = -1
    result[3, 2] = -(2 * far * near) / (far - near)
    return result
