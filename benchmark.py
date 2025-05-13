import time
import psutil
import numpy as np
from graphics_preset import GraphicsPreset

class Benchmark:
    def __init__(self, duration=10.0):
        self.duration = duration
        self.frame_times = []
        self.memory_usage = []
        self.gpu_usage = []
        self.start_time = time.time()

    def record_performance(self, frame_time):
        """Registra i dati di performance per il test"""
        self.frame_times.append(frame_time)
        self.memory_usage.append(psutil.virtual_memory().used / (1024 * 1024))  # MB
        self.gpu_usage.append(psutil.cpu_percent())  # Simulazione uso GPU

    def is_complete(self):
        """Verifica se il benchmark ha raggiunto la durata prevista"""
        return (time.time() - self.start_time) >= self.duration

    def generate_report(self):
        """Genera un rapporto finale delle performance"""
        avg_fps = np.mean([1000.0 / t if t > 0 else 0 for t in self.frame_times])
        avg_memory = np.mean(self.memory_usage)
        avg_gpu = np.mean(self.gpu_usage)

        report = f"""
        📈 **Benchmark Completo**
        -------------------------------
        ⏳ Durata: {self.duration} secondi
        ⚡ FPS Medio: {avg_fps:.2f}
        🖥️ Uso Medio della Memoria: {avg_memory:.2f} MB
        🎮 Utilizzo Medio della GPU: {avg_gpu:.2f}%
        -------------------------------
        """
        return report
