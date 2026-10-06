from ipc.ring_buffer import RingBuffer


def test_empty_buffer():
    buffer = RingBuffer("data/test_empty.mmap", 10)

    assert buffer.is_empty()
    assert not buffer.is_full()

    buffer.close()


def test_write_and_read():
    buffer = RingBuffer("data/test_read_write.mmap", 10)

    result = buffer.write_order(
        b"B",
        100.50,
        10,
        123456789,
    )

    assert result is True
    assert not buffer.is_empty()

    order = buffer.read_order()

    assert order is not None
    assert order["side"] == b"B"
    assert order["price"] == 100.50
    assert order["quantity"] == 10

    assert buffer.is_empty()

    buffer.close()


def test_multiple_orders():
    buffer = RingBuffer("data/test_multiple.mmap", 10)

    for i in range(5):
        buffer.write_order(
            b"B",
            100.0 + i,
            i + 1,
            1000 + i,
        )

    for i in range(5):
        order = buffer.read_order()

        assert order is not None
        assert order["quantity"] == i + 1

    assert buffer.is_empty()

    buffer.close()


if __name__ == "__main__":
    test_empty_buffer()
    test_write_and_read()
    test_multiple_orders()

    print("All IPC tests passed.")