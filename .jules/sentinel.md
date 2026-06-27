
## 2024-05-15 - Unbounded Stream Processing leading to DoS
**Vulnerability:** The proxy's `collect(stream)` utility function read arbitrary size bodies into memory using `chunks.push(c)`. An attacker could send a massive payload, leading to an Out-Of-Memory (OOM) crash and Denial of Service.
**Learning:** In Node.js, when manually buffering data chunks from a stream (like `req` or `proxyRes`), it's critical to track the total size of accumulated buffers and immediately `stream.destroy()` if it exceeds a reasonable limit for the application's context (e.g., 10MB).
**Prevention:** Always enforce a maximum payload limit (`MAX_PAYLOAD_SIZE`) inside `stream.on('data')` listeners before pushing the chunk to the memory array.

## 2024-06-27 - Unhandled Promise Rejection leading to DoS
**Vulnerability:** The proxy's `collect(stream)` utility function rejects large streams when they exceed 10MB to prevent DoS. However, `await collect(req)` was called without a `try...catch` block. This caused an unhandled promise rejection when an oversized payload was sent, crashing the server entirely.
**Learning:** In Node.js, failing to catch promise rejections can crash the process (especially in newer Node.js versions). Always wrap asynchronous calls that can reject in `try...catch` or `.catch()`, especially when processing untrusted user input like HTTP request bodies.
**Prevention:** Always implement robust error handling around `await` calls that process network streams or user input. Return secure, sanitized HTTP error codes (like 413 Payload Too Large) without leaking stack traces.
