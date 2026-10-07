# ChronosMatch

## Zero-Copy High-Frequency Trading Engine

ChronosMatch is a simple low-latency trading engine designed to
process market orders efficiently using memory-mapped communication.

The project demonstrates how a market simulator can send orders through
a memory-mapped ring buffer to a Cython-based matching engine while
tracking processing latency.

---

## Objective

The main objective of ChronosMatch is to demonstrate:

- Low-latency order processing
- Memory-mapped IPC
- Ring buffer communication
- Cython-based matching
- Market order simulation
- Basic latency monitoring

---

## Architecture

```text
Market Simulator
       |
       v
Memory-Mapped Ring Buffer
       |
       v
Cython Matching Engine
       |
       v
Latency Dashboard