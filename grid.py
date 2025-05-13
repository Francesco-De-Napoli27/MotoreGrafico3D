from OpenGL.GL import *
import numpy as np

class Grid:
    def __init__(self, size=10, step=1):
        lines = []

        for i in range(-size, size + 1, step):
            # Linee parallele all'asse Z
            lines.append([i, 0, -size])
            lines.append([i, 0, size])
            # Linee parallele all'asse X
            lines.append([-size, 0, i])
            lines.append([size, 0, i])

        self.vertex_count = len(lines)
        self.vertices = np.array(lines, dtype=np.float32).flatten()

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_LINES, 0, self.vertex_count)
        glBindVertexArray(0)
