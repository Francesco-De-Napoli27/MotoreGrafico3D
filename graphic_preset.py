class GraphicsPreset:
    def __init__(self):
        self.presets = {
            "Ultra": {"HDR": True, "Bloom": True, "MotionBlur": True, "DOF": True, "SSR": True},
            "High": {"HDR": True, "Bloom": True, "MotionBlur": False, "DOF": True, "SSR": True},
            "Medium": {"HDR": True, "Bloom": False, "MotionBlur": False, "DOF": False, "SSR": True},
            "Low": {"HDR": False, "Bloom": False, "MotionBlur": False, "DOF": False, "SSR": False},
        }
        self.current_preset = "Ultra"

    def set_preset(self, preset):
        """Modifica il preset attivo"""
        if preset in self.presets:
            self.current_preset = preset

    def get_current_preset(self):
        """Restituisce il preset attuale"""
        return self.current_preset
