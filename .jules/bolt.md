## 2026-07-09 - Zero-allocation parsing for SSE Streams
**Learning:** In high-throughput Node.js proxy servers handling SSE data streams (e.g., LLM outputs), using `buffer.split('
')` or reassigning `buffer = buffer.slice(...)` inside parsing loops creates an O(N^2) string copying bottleneck and high GC churn.
**Action:** Use zero-allocation parsing by maintaining a `startIdx` offset (`buffer.indexOf('
', startIdx)`), extracting lines with `buffer.substring()`, and slicing the unparsed remainder only once at the end of the event handler.
