# Quality Control: Testing & Verification

## 1. Parallel Node Testing
*   Use `pytest-asyncio` to verify that `yolo_node` and `qwen_node` can execute concurrently without resource contention[cite: 1].

## 2. Determinism & Replay
*   **Replay Test**: Verify that providing the same image hash and LLM seed results in identical agent task assignments[cite: 1].
*   **Checkpoint Test**: Verify that the system can resume from a `PostgresSaver` checkpoint if a node fails during execution[cite: 1].

## 3. Safety Benchmarks
*   **Zero Misses**: The system must have a 0% false-negative rate for CRITICAL urgency events (Lying/Bent poses)[cite: 1].