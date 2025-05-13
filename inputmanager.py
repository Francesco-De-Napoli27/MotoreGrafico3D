import glfw
from OpenGL.GL import *
import math
from control_mapping import ControlMapping


class InputManager:
    def __init__(self, window):
        self.window = window
        self.keys = {}
        self.mouse_position = (0.0, 0.0)
        self.mouse_buttons = {}
        self.prev_mouse_position = (0.0, 0.0)  # Inizializza la posizione precedente del mouse
        self.control_mapping = ControlMapping()
        self.gamepad_buttons = {}
        self.gamepad_axes = {}

        # Imposta i callback per la tastiera e il mouse
        glfw.set_key_callback(window, self.key_callback)
        glfw.set_cursor_pos_callback(window, self.cursor_position_callback)
        glfw.set_mouse_button_callback(window, self.mouse_button_callback)

        # Controlla se il gamepad è connesso
        self.check_gamepad_connection()

    def check_gamepad_connection(self):
        """Verifica la connessione di un gamepad"""
        for i in range(glfw.JOYSTICK_LAST):
            if glfw.joystick_present(i):
                self.gamepad_id = i
                print(f"Gamepad connesso: {glfw.get_gamepad_name(i)}")
                return

        self.gamepad_id = None
        print("Nessun gamepad rilevato.")

    def update_gamepad_state(self):
        """Aggiorna lo stato dei pulsanti e degli assi del gamepad"""
        if self.gamepad_id is not None and glfw.joystick_present(self.gamepad_id):
            buttons, axes = glfw.get_gamepad_buttons(self.gamepad_id), glfw.get_gamepad_axes(self.gamepad_id)
            self.gamepad_buttons = {i: buttons[i] == glfw.PRESS for i in range(len(buttons))}
            self.gamepad_axes = {i: axes[i] for i in range(len(axes))}

    def is_gamepad_button_pressed(self, button):
        return self.gamepad_buttons.get(button, False)

    def get_gamepad_axis(self, axis):
        return self.gamepad_axes.get(axis, 0.0)

    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS or action == glfw.REPEAT:
            self.keys[key] = True
        elif action == glfw.RELEASE:
            self.keys[key] = False

    def is_action_triggered(self, action):
        """Verifica se l'azione è stata attivata dal tasto mappato"""
        assigned_key = self.control_mapping.get_control(action)
        return self.keys.get(assigned_key, False)

    def remap_action(self, action, new_key):
        """Permette di cambiare la mappatura di un’azione"""
        self.control_mapping.remap_control(action, new_key)

    def cursor_position_callback(self, window, xpos, ypos):
        self.mouse_position = (xpos, ypos)

    def mouse_button_callback(self, window, button, action, mods):
        if action == glfw.PRESS:
            self.mouse_buttons[button] = True
        elif action == glfw.RELEASE:
            self.mouse_buttons[button] = False

    def is_key_pressed(self, key):
        return self.keys.get(key, False)

    def is_mouse_button_pressed(self, button):
        return self.mouse_buttons.get(button, False)

    def get_mouse_position(self):
        return self.mouse_position

    def get_relative_mouse_position(self):
        width, height = glfw.get_window_size(self.window)
        x, y = self.mouse_position
        return x / width * 2.0 - 1.0, -(y / height * 2.0 - 1.0)  # Coordinate normalizzate

    def get_mouse_delta(self):
        # Restituisce il movimento del mouse in pixel dall'ultimo aggiornamento
        current_position = self.mouse_position
        delta = (current_position[0] - self.prev_mouse_position[0], current_position[1] - self.prev_mouse_position[1])
        self.prev_mouse_position = current_position  # Aggiorna la posizione precedente
        return delta

    def update(self):
        """Aggiorna tutti gli input (tastiera, mouse e gamepad)"""
        self.update_gamepad_state()

    def reset_input(self):
        """Pulisce lo stato dell'input per il prossimo frame"""
        self.keys.clear()
        self.mouse_buttons.clear()
        self.gamepad_buttons.clear()
