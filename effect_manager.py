from shadow_map import ShadowMap
from post_processing import PostProcessingEngine
from bloom import Bloom

WIDTH = 800  # Larghezza finestra
HEIGHT = 600  # Altezza finestra

class EffectManager:
    def __init__(self):
        """Inizializza gli effetti grafici"""
        self.shadow_mapping = ShadowMap(1024, 1024)  # Assicurati di avere questa classe
        self.post_processing = PostProcessingEngine(WIDTH, HEIGHT)
        self.bloom = Bloom()
        self.effects = {
            "HDR": {"enabled": True, "intensity": 1.2},
            "Bloom": {"enabled": True, "blur_strength": 1.2},
            "MotionBlur": {"enabled": True, "blur_strength": 0.8},
            "DOF": {"enabled": True, "focal_distance": 5.0, "blur_factor": 0.5},
            "SSR": {"enabled": True, "max_distance": 50.0, "reflectivity": 0.8},
        }

    def adjust_quality(self, frame_time):
        """Regola la qualità degli effetti in base alla performance"""
        if frame_time > 16.6:  # Se l'FPS scende sotto 60
            for effect in self.effects:
                if self.effects[effect]["enabled"]:
                    self.effects[effect]["intensity"] *= 0.9  # Riduce l'intensità per ottimizzare
        elif frame_time < 8.3:  # Se l'FPS è sopra 120
            for effect in self.effects:
                if self.effects[effect]["enabled"]:
                    self.effects[effect]["intensity"] *= 1.1  # Aumenta l'intensità per migliore qualità

    def toggle_effect(self, effect_name, state):
        """Attiva o disattiva un effetto"""
        if effect_name in self.effects:
            self.effects[effect_name]["enabled"] = state

    def apply_effects(self, shader):
        """Applica gli effetti attivi al motore grafico"""
        for effect_name, settings in self.effects.items():
            if settings["enabled"]:
                for param, value in settings.items():
                    if param != "enabled":
                        shader.set_uniform_float(param, value)

    def enable_all(self):
        """Abilita tutti gli effetti grafici"""
        self.shadow_mapping.enable()
        self.post_processing.enable()
        self.bloom.enable()
