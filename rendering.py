import glfw
from OpenGL.GL import *
import numpy as np

# Importazione dei moduli
from shader import Shader
from camera import Camera
from lighting import Light
from shadow_map import ShadowMap
from obj_loader import OBJLoader
from mesh_loader import Mesh
from particles import Particle
from effect_manager import EffectManager
from post_processing import PostProcessingEngine
from collision import SpatialGrid
from transformations import translation_matrix, rotation_matrix_y, scale_matrix
from fracture import fracture_object
from ui_manager import UIEngine  # Gestione UI completamente con OpenGL puro
from performance_manager import PerformanceManager

# Configurazione iniziale
WIDTH, HEIGHT = 800, 600

# Inizializza GLFW
if not glfw.init():
    raise RuntimeError("Errore nell'inizializzazione di GLFW!")

# Creazione finestra (una sola!)
window = glfw.create_window(WIDTH, HEIGHT, "Motore Grafico", None, None)
ui_engine = UIEngine(window)  # Passa la finestra già creata


glfw.make_context_current(window)

# Imposta viewport e OpenGL
glViewport(0, 0, WIDTH, HEIGHT)
glEnable(GL_DEPTH_TEST)

# Inizializza moduli
camera = Camera(None)
light = Light([3.0, 5.0, -2.0])
shadow_map = ShadowMap(1024, 1024)
effect_manager = EffectManager()
post_processing = PostProcessingEngine(WIDTH, HEIGHT)
spatial_grid = SpatialGrid()
ui_engine = UIEngine(window)  # UI completamente gestita con OpenGL

# Caricamento modelli
mesh = Mesh("C:/Users/franc/PycharmProjects/PythonProject/modelli/cube.obj")


# Shader principale
shader = Shader("C:/Users/franc/PycharmProjects/PythonProject/shaders/vertex_shader.glsl", "C:/Users/franc/PycharmProjects/PythonProject/shaders/fragment_shader.glsl")

performance_manager = PerformanceManager() # Inizializza il gestore delle prestazioni
ui_engine = UIEngine(window)

# Loop di rendering
while not glfw.window_should_close(window):
    # 1. Aggiornamento dello stato (FPS, input, logica, ecc.)
    performance_manager.update_fps()
    quality_level = performance_manager.get_quality()

    # Aggiorna il testo della UI (una sola volta, se non cambia tra rendering)
    ui_engine.quality_text = f"Qualità: {quality_level}"

    # 2. Clear del framebuffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # 3. Aggiorna e imposta shader, luci, camera, etc.
    shader.use()
    shader.set_uniform_vec3("lightPos", light.position)
    shader.set_uniform_float("lightIntensity", light.intensity)
    view_matrix = camera.get_view_matrix()
    projection_matrix = camera.get_projection_matrix(WIDTH / HEIGHT)
    shader.set_uniform_mat4("view", view_matrix)
    shader.set_uniform_mat4("projection", projection_matrix)

    # 4. Disegna la scena (es. il mesh)
    mesh.draw()  # Assicurati che Mesh abbia un metodo draw() o simile

    # 5. Adatta gli effetti grafici in base al livello di qualità
    if quality_level == "Ultra":
        effect_manager.enable_all()
    elif quality_level == "Alta":
        effect_manager.reduce_effects()
    elif quality_level == "Media":
        effect_manager.minimize_post_processing()
    else:
        effect_manager.disable_heavy_effects()

    # Applica gli effetti (post-processing, bloom, ecc.)
    effect_manager.apply_effects(shader)

    # 6. Rendering della UI sulla scena finale
    ui_engine.render()

    # 7. Swap dei buffers e polling degli eventi
    glfw.swap_buffers(window)
    glfw.poll_events()
