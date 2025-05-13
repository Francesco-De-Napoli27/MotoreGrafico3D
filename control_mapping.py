import glfw
import json

class ControlMapping:
    def __init__(self, config_file="controls.json"):
        self.config_file = config_file
        self.controls = {
            "move_forward": glfw.KEY_W,
            "move_backward": glfw.KEY_S,
            "move_left": glfw.KEY_A,
            "move_right": glfw.KEY_D,
            "jump": glfw.KEY_SPACE,
            "crouch": glfw.KEY_LEFT_CONTROL,
            "action": glfw.MOUSE_BUTTON_LEFT,
            "cancel": glfw.KEY_ESCAPE
        }
        self.load_config()

    def load_config(self):
        """Carica la configurazione dei controlli dal file JSON"""
        try:
            with open(self.config_file, "r") as file:
                data = json.load(file)
                self.controls.update(data)
        except FileNotFoundError:
            print("⚠️ Nessuna configurazione trovata. Uso valori di default.")

    def save_config(self):
        """Salva la configurazione dei controlli nel file JSON"""
        with open(self.config_file, "w") as file:
            json.dump(self.controls, file, indent=4)
        print("✅ Controlli salvati!")

    def remap_control(self, action, new_key):
        """Modifica il tasto assegnato a un’azione"""
        if action in self.controls:
            self.controls[action] = new_key
            self.save_config()

    def get_control(self, action):
        """Restituisce il tasto assegnato a un'azione"""
        return self.controls.get(action, None)
