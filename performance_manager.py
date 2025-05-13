import glfw
import time


class PerformanceManager:
    def __init__(self):
        self.last_time = time.time()
        self.frame_count = 0
        self.current_fps = 60
        self.quality_level = "Ultra"

    def update_fps(self):
        """Calcola gli FPS e adatta la qualità grafica dinamicamente"""
        current_time = time.time()
        self.frame_count += 1

        if current_time - self.last_time >= 1.0:
            self.current_fps = self.frame_count
            self.frame_count = 0
            self.last_time = current_time

            self.adjust_quality()

    def adjust_quality(self):
        """Regola la qualità grafica in base agli FPS"""
        if self.current_fps >= 60:
            self.quality_level = "Ultra"
        elif self.current_fps >= 45:
            self.quality_level = "Alta"
        elif self.current_fps >= 30:
            self.quality_level = "Media"
        else:
            self.quality_level = "Bassa"

    def get_quality(self):
        return self.quality_level
