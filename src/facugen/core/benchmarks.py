import time
from dataclasses import dataclass

@dataclass
class BenchmarkResult:
    total_time: float
    sample_count: int
    
    @property
    def samples_per_second(self) -> float:
        if self.total_time == 0:
            return 0.0
        return self.sample_count / self.total_time

class BenchmarkTimer:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.sample_count = 0

    def start(self, count: int):
        self.sample_count = count
        self.start_time = time.perf_counter()

    def stop(self) -> BenchmarkResult:
        self.end_time = time.perf_counter()
        return BenchmarkResult(
            total_time=self.end_time - self.start_time,
            sample_count=self.sample_count
        )
