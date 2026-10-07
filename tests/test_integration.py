import os
import time

from ipc.ring_buffer import RingBuffer
from dashboard.latency_monitor import LatencyMonitor


def run_integration_test():

    file_path = "data/integration_test.mmap"

    if os.path.exists(file_path):
        os.remove(file_path)

    buffer = RingBuffer(
        file_path,
        100
    )

    monitor = LatencyMonitor()

    total_orders = 90

    for i in range(total_orders):

        timestamp = time.time_ns()

        written = buffer.write_order(
            b"B",
            100.0 + (i * 0.01),
            i + 1,
            timestamp,
        )

        assert written is True

    for _ in range(total_orders):

        start = time.perf_counter_ns()

        order = buffer.read_order()

        end = time.perf_counter_ns()

        assert order is not None

        latency = (
            end - start
        ) / 1000

        monitor.record(latency)

    buffer.close()

    monitor.display()

    print("\nIntegration test passed.")
    print(f"Orders processed: {monitor.orders}")


if __name__ == "__main__":
    run_integration_test()