import psutil
import time

class ResourceMonitor:
    def __init__(self, device_id):
        self.device_id = device_id
        self.start_time = time.time()
    
    def get_metrics(self):
        return {
            "uptime": round(time.time() - self.start_time),
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "energy": self.estimate_energy()
        }
    
    def estimate_energy(self):
        """Estimate energy consumption based on CPU usage"""
        base_power = 0.5  # Base power in watts
        cpu_factor = 0.02  # Additional watts per CPU percentage
        cpu_usage = psutil.cpu_percent()
        return base_power + (cpu_usage * cpu_factor)