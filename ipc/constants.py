"""
Constants used by the ChronosMatch IPC ring buffer.
"""

BUFFER_CAPACITY = 10000

HEADER_SIZE = 16

ORDER_FORMAT = "<QcdIQ"

ORDER_SIZE = 29

BUFFER_FILE = "data/chronosmatch.mmap"