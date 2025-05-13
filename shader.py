from OpenGL.GL import *
import os
import numpy as np
from OpenGL.GL import glGetError, GL_NO_ERROR
from OpenGL.error import GLError


def check_gl_error():
    err = glGetError()
    if err != GL_NO_ERROR:
        raise GLError(f"OpenGL Error: {err}")

class Shader:
    def __init__(self, vertex_path, fragment_path):
        self.program_id = glCreateProgram()

        # Carica e compila gli shaders dai file
        self.vertex_shader = self.load_shader_from_file(vertex_path, GL_VERTEX_SHADER)
        self.fragment_shader = self.load_shader_from_file(fragment_path, GL_FRAGMENT_SHADER)

        # Attacca gli shaders al programma
        glAttachShader(self.program_id, self.vertex_shader)
        glAttachShader(self.program_id, self.fragment_shader)
        glLinkProgram(self.program_id)

        # Controllo del linking del programma
        if glGetProgramiv(self.program_id, GL_LINK_STATUS) != GL_TRUE:
            error = glGetProgramInfoLog(self.program_id).decode()
            raise RuntimeError(f"Linking error: {error}")
        else:
            print("Programma shader correttamente linkato.")


    def load_shader_from_file(self, path, shader_type):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Il file shader {path} non esiste!")

        with open(path, 'r') as file:
            shader_code = file.read()

        shader_id = glCreateShader(shader_type)
        glShaderSource(shader_id, shader_code)
        glCompileShader(shader_id)

        if glGetShaderiv(shader_id, GL_COMPILE_STATUS) != GL_TRUE:
            error = glGetShaderInfoLog(shader_id).decode()
            raise RuntimeError(f"Shader compile error in {path}:\n{error}")

        return shader_id

    def use(self):
        glUseProgram(self.program_id)
        # Verifica che il programma sia stato effettivamente usato
        if glGetProgramiv(self.program_id, GL_ACTIVE_UNIFORMS) == 0:
            print("Nessuna uniforme attiva nel programma shader.")

    def stop(self):
        glUseProgram(0)

    def set_uniform_vec3(self, name, vec3):
        loc = glGetUniformLocation(self.program_id, name)
        glUniform3f(loc, *vec3)

    def set_uniform_float(self, name, value):
        loc = glGetUniformLocation(self.program_id, name)
        glUniform1f(loc, value)

    def set_uniform_mat4(self, name, matrix):
        loc = glGetUniformLocation(self.program_id, name)
        if loc == -1:
            raise ValueError(f"Uniforme {name} non trovata nello shader.")

        # Controlla se la matrice è già 1D (array di 16 elementi)
        if matrix.shape != (16,):
            # Se non è 1D, appiattisci la matrice 4x4
            matrix = np.array(matrix, dtype=np.float32).flatten()

        print(f"Matrix for uniform {name}: {matrix}, Shape: {matrix.shape}")
        glUniformMatrix4fv(loc, 1, GL_TRUE, matrix)

        # Verifica errori dopo l'operazione OpenGL
        check_gl_error()

    def delete(self):
        if hasattr(self, 'vertex_shader'):
            glDeleteShader(self.vertex_shader)
        if hasattr(self, 'fragment_shader'):
            glDeleteShader(self.fragment_shader)
        if hasattr(self, 'program_id'):
            glDeleteProgram(self.program_id)

    def __del__(self):
        self.delete()
