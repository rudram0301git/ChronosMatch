"""
Simple ChronosMatch latency monitor.
"""

import time


class LatencyMonitor:

    def __init__(self):
        self.latencies = []
        self.orders = 0

    def record(self, latency_microseconds):
        self.latencies.append(latency_microseconds)
        self.orders += 1

    def average_latency(self):
        if not self.latencies:
            return 0

        return sum(self.latencies) / len(self.latencies)

    def minimum_latency(self):
        if not self.latencies:
            return 0

        return min(self.latencies)

    def maximum_latency(self):
        if not self.latencies:
            return 0

        return max(self.latencies)

    def display(self):
        print("\n" + "=" * 40)
        print("       CHRONOSMATCH DASHBOARD")
        print("=" * 40)

        print(f"Orders processed : {self.orders}")
        print(
            f"Average latency  : "
            f"{self.average_latency():.2f} us"
        )
        print(
            f"Minimum latency  : "
            f"{self.minimum_latency():.2f} us"
        )
        print(
            f"Maximum latency  : "
            f"{self.maximum_latency():.2f} us"
        )

        print("=" * 40)


if __name__ == "__main__":

    monitor = LatencyMonitor()

    for i in range(10):
        start = time.perf_counter_ns()

        time.sleep(0.00001)

        end = time.perf_counter_ns()

        latency = (end - start) / 1000

        monitor.record(latency)

    monitor.display()