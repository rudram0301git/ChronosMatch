"""
Memory-mapped ring buffer for ChronosMatch.
"""

import mmap
import os

from .constants import (
    BUFFER_CAPACITY,
    HEADER_SIZE,
    ORDER_SIZE,
    BUFFER_FILE,
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