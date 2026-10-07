"""
Simple market order simulator for ChronosMatch.
"""

import random
import time


class MarketSimulator:

    def __init__(self, ring_buffer, orders_per_second=100):
        self.ring_buffer = ring_buffer
        self.orders_per_second = orders_per_second

    def generate_order(self, order_id):
        side = random.choice([b"B", b"S"])

        price = round(
            random.uniform(99.0, 101.0),
            2
        )

        quantity = random.randint(1, 10)

        timestamp = time.time_ns()

        return {
            "order_id": order_id,
            "side": side,
            "price": price,
            "quantity": quantity,
            "timestamp": timestamp,
        }

    def send_order(self, order_id):

        order = self.generate_order(order_id)

        return self.ring_buffer.write_order(
            order["side"],
            order["price"],
            order["quantity"],
            order["timestamp"],
        )

    def run(self, count=10):

        successful_orders = 0

        for order_id in range(count):

            if self.send_order(order_id):
                successful_orders += 1

            if self.orders_per_second > 0:
                time.sleep(
                    1 / self.orders_per_second
                )

        return successful_orders