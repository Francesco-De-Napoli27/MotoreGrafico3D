import time
import matplotlib.pyplot as plt

class PerformanceReport:
    def __init__(self):
        self.frame_times = []
        self.memory_usage = []
        self.gpu_usage = []
        self.timestamps = []

    def record_frame_time(self, frame_time):
        """Registra il tempo di rendering di ciascun frame"""
        self.frame_times.append(frame_time)
        self.timestamps.append(time.time())

    def record_memory_usage(self, usage):
        """Registra l'uso della memoria"""
        self.memory_usage.append(usage)

    def record_gpu_usage(self, usage):
        """Registra l'utilizzo della GPU"""
        self.gpu_usage.append(usage)

    def generate_report(self):
        """Genera grafici con i dati di performance"""
        plt.figure(figsize=(12, 6))

        # Grafico degli FPS
        plt.subplot(1, 3, 1)
        fps = [1000.0 / t if t > 0 else 0 for t in self.frame_times]
        plt.plot(self.timestamps, fps, label="FPS")
        plt.xlabel("Tempo (s)")
        plt.ylabel("FPS")
        plt.title("Frame Rate nel tempo")
        plt.legend()
        plt.grid()

        # Grafico della memoria
        plt.subplot(1, 3, 2)
        plt.plot(self.timestamps, self.memory_usage, label="Memoria (MB)")
        plt.xlabel("Tempo (s)")
        plt.ylabel("Memoria utilizzata")
        plt.title("Utilizzo della Memoria")
        plt.legend()
        plt.grid()

        # Grafico dell'uso GPU
        plt.subplot(1, 3, 3)
        plt.plot(self.timestamps, self.gpu_usage, label="GPU (%)")
        plt.xlabel("Tempo (s)")
        plt.ylabel("Utilizzo GPU")
        plt.title("Utilizzo GPU nel tempo")
        plt.legend()
        plt.grid()

        plt.tight_layout()
        plt.show()
