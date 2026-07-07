## 2026-07-07 - Zero-allocation LLM Stream Parsing
**Learning:** Reassigning `buffer = buffer.slice(...)` repeatedly inside a Node.js streaming `on('data')` loop creates an O(N^2) string copying bottleneck and excessive Garbage Collection (GC) churn, severely degrading throughput for large LLM payloads.
**Action:** Use zero-allocation parsing by maintaining a `startIdx` offset (e.g., `buffer.indexOf('\n', startIdx)`), extracting chunks with `buffer.substring()`, and only slicing the unparsed remainder of the buffer once at the end of the event handler block.
