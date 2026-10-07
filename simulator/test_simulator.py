from ipc.ring_buffer import RingBuffer
from simulator.market_simulator import MarketSimulator


def test_simulator():

    buffer = RingBuffer(
        "data/simulator_test.mmap",
        20
    )

    simulator = MarketSimulator(
        buffer,
        orders_per_second=0
    )

    result = simulator.run(5)

    assert result == 5

    for _ in range(5):
        order = buffer.read_order()
        assert order is not None

    assert buffer.is_empty()

    buffer.close()

    print("Simulator test passed.")


if __name__ == "__main__":
    test_simulator()