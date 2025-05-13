# mesh_loader.py
from OpenGL.GL import *
import numpy as np
from obj_loader import OBJLoader

class Mesh:
    def __init__(self, obj_path):
        obj = OBJLoader(obj_path)

        self.vertex_count = len(obj.indices)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.data = []
        for i in obj.indices:
            self.data.extend(obj.vertices[i])
            self.data.extend(obj.normals[i])

        self.data = np.array(self.data, dtype=np.float32)
        self.indices = np.array(obj.indices, dtype=np.uint32)

        # Creazione VBO
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.data.nbytes, self.data, GL_STATIC_DRAW)

        # Creazione EBO
        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        stride = 6 * 4
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.vertex_count, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
