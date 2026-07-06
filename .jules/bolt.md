## 2024-05-24 - Avoid O(N^2) String Slicing in Parsers
**Learning:** Even when avoiding `.split('\n')` for zero-allocation parsing, reassigning `buffer = buffer.slice(newlineIdx + 1)` inside a loop over a single chunk creates an O(N^2) string copying bottleneck and high GC churn.
**Action:** Always maintain a `startIdx` offset when scanning strings in a loop (`indexOf('\n', startIdx)`), and only slice the unparsed remainder of the buffer once at the very end of the data event handler.
