
## 2024-05-15 - Unbounded Stream Processing leading to DoS
**Vulnerability:** The proxy's `collect(stream)` utility function read arbitrary size bodies into memory using `chunks.push(c)`. An attacker could send a massive payload, leading to an Out-Of-Memory (OOM) crash and Denial of Service.
**Learning:** In Node.js, when manually buffering data chunks from a stream (like `req` or `proxyRes`), it's critical to track the total size of accumulated buffers and immediately `stream.destroy()` if it exceeds a reasonable limit for the application's context (e.g., 10MB).
**Prevention:** Always enforce a maximum payload limit (`MAX_PAYLOAD_SIZE`) inside `stream.on('data')` listeners before pushing the chunk to the memory array.

## 2026-06-24 - Overly Permissive CORS Configuration
**Vulnerability:** The local proxy dynamically reflected any `Origin` header while setting `Access-Control-Allow-Credentials` to `true`. This could allow a malicious website visited by the user to make authenticated requests to the proxy on `localhost:8443` or exfiltrate responses.
**Learning:** Even though the proxy runs locally on the user's machine, browsers can still make cross-origin requests to `localhost`. Reflecting any origin circumvents CORS protections entirely.
**Prevention:** Hardcode an explicit whitelist of allowed origins (e.g., Office domains and localhost). Validate incoming `Origin` headers against the whitelist before returning them in `Access-Control-Allow-Origin`. For local desktop clients with a `null` origin, `null` is safe to permit, but fallback to a safe default like `https://localhost:8443` for unauthorized domains.
