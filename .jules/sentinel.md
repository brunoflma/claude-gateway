
## 2024-05-15 - Unbounded Stream Processing leading to DoS
**Vulnerability:** The proxy's `collect(stream)` utility function read arbitrary size bodies into memory using `chunks.push(c)`. An attacker could send a massive payload, leading to an Out-Of-Memory (OOM) crash and Denial of Service.
**Learning:** In Node.js, when manually buffering data chunks from a stream (like `req` or `proxyRes`), it's critical to track the total size of accumulated buffers and immediately `stream.destroy()` if it exceeds a reasonable limit for the application's context (e.g., 10MB).
**Prevention:** Always enforce a maximum payload limit (`MAX_PAYLOAD_SIZE`) inside `stream.on('data')` listeners before pushing the chunk to the memory array.

## 2024-05-15 - Unhandled Promise Rejection leading to DoS
**Vulnerability:** The proxy's `collect(stream)` function rejected the returned Promise when payload limit exceeded, but the async caller `handleRequest()` did not use a `try...catch` block. This resulted in an unhandled promise rejection crashing the Node.js process and causing a Denial of Service (DoS) for all users relying on the proxy.
**Learning:** In Node.js, `async` function calls inside an HTTP request handler must have their errors caught, either via `try...catch` blocks or `.catch()` attachments. Otherwise, the unhandled rejection can crash the entire server application.
**Prevention:** Always wrap `await` calls that can reject (like `await collect(...)`) within a `try...catch` in your request handlers, and gracefully return an appropriate HTTP error response (like `413 Payload Too Large`).
