import time

class Metrics:
    def __init__(self):
        self.latencies = []
        self.power_usage = []
        self.throughput = []
        self.start_time = time.time()
    
    def record_latency(self, latency):
        self.latencies.append(latency)
    
    def record_power(self, power):
        self.power_usage.append(power)
    
    def record_throughput(self, count):
        self.throughput.append(count)
    
    def get_average_latency(self):
        return sum(self.latencies) / len(self.latencies) if self.latencies else 0
    
    def get_average_power(self):
        return sum(self.power_usage) / len(self.power_usage) if self.power_usage else 0
    
    def get_throughput_rate(self):
        elapsed = time.time() - self.start_time
        return sum(self.throughput) / elapsed if elapsed > 0 else 0
    
    def reset(self):
        self.latencies = []
        self.power_usage = []
        self.throughput = []
        self.start_time = time.time()