## 2026-07-08 - Zero-allocation string parsing
**Learning:** In high-throughput Node.js proxy servers handling SSE data streams, using `buffer.split("\n")` and reassigning `buffer = buffer.slice(...)` inside parsing loops creates an O(N^2) string copying bottleneck and high GC churn.
**Action:** Use zero-allocation parsing by maintaining a `startIdx` offset (`buffer.indexOf("\n", startIdx)`), extracting lines with `buffer.substring()`, and slicing the unparsed remainder only once at the end of the event handler.
