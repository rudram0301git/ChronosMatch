import os
import time

from ipc.ring_buffer import RingBuffer
from simulator.market_simulator import MarketSimulator
from engine.order_book import OrderBook
from dashboard.latency_monitor import LatencyMonitor


def run_integration_test():

    file_path = "data/full_integration.mmap"

    if os.path.exists(file_path):
        os.remove(file_path)

    buffer = RingBuffer(
        file_path,
        100
    )

    simulator = MarketSimulator(
        buffer,
        orders_per_second=0
    )

    engine = OrderBook()

    monitor = LatencyMonitor()

    orders = 50

    written = simulator.run(orders)

    print("Orders generated:", written)

    processed = 0

    while not buffer.is_empty():

        start = time.perf_counter_ns()

        order = buffer.read_order()

        if order is None:
            break

        engine.add_order(
            order["side"],
            order["price"],
            order["quantity"]
        )

        end = time.perf_counter_ns()

        latency = (
            end - start
        ) / 1000

        monitor.record(latency)

        processed += 1

    buffer.close()

    print("Orders processed:", processed)
    print("Trades:", engine.get_trade_count())

    monitor.display()

    assert written == orders
    assert processed == orders

    print("\nFull integration test passed.")


if __name__ == "__main__":
    run_integration_test()