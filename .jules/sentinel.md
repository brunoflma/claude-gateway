
## 2024-05-15 - Unbounded Stream Processing leading to DoS
**Vulnerability:** The proxy's `collect(stream)` utility function read arbitrary size bodies into memory using `chunks.push(c)`. An attacker could send a massive payload, leading to an Out-Of-Memory (OOM) crash and Denial of Service.
**Learning:** In Node.js, when manually buffering data chunks from a stream (like `req` or `proxyRes`), it's critical to track the total size of accumulated buffers and immediately `stream.destroy()` if it exceeds a reasonable limit for the application's context (e.g., 10MB).
**Prevention:** Always enforce a maximum payload limit (`MAX_PAYLOAD_SIZE`) inside `stream.on('data')` listeners before pushing the chunk to the memory array.

## 2024-05-15 - Information Leakage via Error Responses
**Vulnerability:** The proxy server forwarded raw error payloads and internal exception messages (`errBody.substring`, `respStr.substring`, and `err.message`) directly to the client in HTTP responses. This violates the principle of failing securely, potentially exposing internal paths, stack traces, upstream server details, or unhandled states to an attacker.
**Learning:** Directly proxying or returning backend/internal errors to the end-user is a common anti-pattern that leads to Information Leakage. Errors must be sanitized at the boundary.
**Prevention:** Always catch and log raw errors locally, but return a generic, non-descriptive error message to the client (e.g., "Internal Server Error - Check logs").
