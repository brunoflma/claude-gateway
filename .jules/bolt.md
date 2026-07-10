## 2024-05-24 - [Zero-Allocation SSE Parsing]
**Learning:** Inside high-throughput Node.js proxy servers handling SSE data streams, reassigning `buffer.slice(...)` within the loop causes an O(N^2) string copying bottleneck and high GC churn.
**Action:** Use a `startIdx` offset for zero-allocation parsing with `indexOf` and slice the buffer only once at the end.
