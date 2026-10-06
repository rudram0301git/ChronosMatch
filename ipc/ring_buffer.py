"""
Memory-mapped ring buffer for ChronosMatch.
"""

import mmap
import os
import struct

from .constants import (
    BUFFER_CAPACITY,
    HEADER_SIZE,
    ORDER_SIZE,
    BUFFER_FILE,
    ORDER_FORMAT,
)


class RingBuffer:

    def __init__(
        self,
        file_path=BUFFER_FILE,
        capacity=BUFFER_CAPACITY,
    ):
        self.file_path = file_path
        self.capacity = capacity

        self.total_size = HEADER_SIZE + (
            capacity * ORDER_SIZE
        )

        directory = os.path.dirname(file_path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        self.file = open(file_path, "a+b")

        self.file.seek(0, os.SEEK_END)

        if self.file.tell() < self.total_size:
            self.file.truncate(self.total_size)

        self.file.flush()

        self.memory = mmap.mmap(
            self.file.fileno(),
            self.total_size,
        )

    def _get_write_position(self):
        return struct.unpack_from(
            "<Q",
            self.memory,
            0,
        )[0]

    def _get_read_position(self):
        return struct.unpack_from(
            "<Q",
            self.memory,
            8,
        )[0]

    def _set_write_position(self, position):
        struct.pack_into(
            "<Q",
            self.memory,
            0,
            position,
        )

    def _set_read_position(self, position):
        struct.pack_into(
            "<Q",
            self.memory,
            8,
            position,
        )

    def is_empty(self):
        return (
            self._get_write_position()
            == self._get_read_position()
        )

    def is_full(self):
        write_position = self._get_write_position()

        next_position = (
            write_position + 1
        ) % self.capacity

        return (
            next_position
            == self._get_read_position()
        )

    def write_order(
        self,
        side,
        price,
        quantity,
        timestamp,
    ):
        if self.is_full():
            return False

        write_position = self._get_write_position()

        offset = HEADER_SIZE + (
            write_position * ORDER_SIZE
        )

        struct.pack_into(
            ORDER_FORMAT,
            self.memory,
            offset,
            write_position,
            side,
            price,
            quantity,
            timestamp,
        )

        next_position = (
            write_position + 1
        ) % self.capacity

        self._set_write_position(next_position)

        return True

    def read_order(self):
        if self.is_empty():
            return None

        read_position = self._get_read_position()

        offset = HEADER_SIZE + (
            read_position * ORDER_SIZE
        )

        order_id, side, price, quantity, timestamp = (
            struct.unpack_from(
                ORDER_FORMAT,
                self.memory,
                offset,
            )
        )

        next_position = (
            read_position + 1
        ) % self.capacity

        self._set_read_position(next_position)

        return {
            "order_id": order_id,
            "side": side,
            "price": price,
            "quantity": quantity,
            "timestamp": timestamp,
        }

    def close(self):
        self.memory.flush()
        self.memory.close()
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()