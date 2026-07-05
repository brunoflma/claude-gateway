
## 2024-05-15 - Unbounded Stream Processing leading to DoS
**Vulnerability:** The proxy's `collect(stream)` utility function read arbitrary size bodies into memory using `chunks.push(c)`. An attacker could send a massive payload, leading to an Out-Of-Memory (OOM) crash and Denial of Service.
**Learning:** In Node.js, when manually buffering data chunks from a stream (like `req` or `proxyRes`), it's critical to track the total size of accumulated buffers and immediately `stream.destroy()` if it exceeds a reasonable limit for the application's context (e.g., 10MB).
**Prevention:** Always enforce a maximum payload limit (`MAX_PAYLOAD_SIZE`) inside `stream.on('data')` listeners before pushing the chunk to the memory array.

## 2026-06-24 - Overly Permissive CORS Configuration
**Vulnerability:** The local proxy dynamically reflected any `Origin` header while setting `Access-Control-Allow-Credentials` to `true`. This could allow a malicious website visited by the user to make authenticated requests to the proxy on `localhost:8443` or exfiltrate responses.
**Learning:** Even though the proxy runs locally on the user's machine, browsers can still make cross-origin requests to `localhost`. Reflecting any origin circumvents CORS protections entirely.
**Prevention:** Hardcode an explicit whitelist of allowed origins (e.g., Office domains and localhost). Validate incoming `Origin` headers against the whitelist before returning them in `Access-Control-Allow-Origin`. For local desktop clients with a `null` origin, `null` is safe to permit, but fallback to a safe default like `https://localhost:8443` for unauthorized domains.

## 2026-07-01 - Sandboxed Iframe Cross-Origin Vulnerability and DoS via Unhandled Promise Rejections
**Vulnerability:** First, `Access-Control-Allow-Credentials: true` was sent for `Origin: null` and `Origin: *`, allowing potential cross-origin vulnerabilities via sandboxed iframes. Second, the async `handleRequest` function in Node.js v22+ could throw unhandled promise rejections on network stream failures, crashing the server.
**Learning:** Sandboxed iframes (often used to isolate untrusted content) have an origin of `null`. Allowing credentials for `null` origins is a security risk. In modern Node.js, unhandled promise rejections cause the process to exit, creating an easy DoS vector if robust error boundaries aren't in place around stream or network request handlers.
**Prevention:** Dynamically omit `Access-Control-Allow-Credentials: true` if the origin is `null` or `*`. Ensure all async entry points in network listeners are wrapped in `.catch()` blocks with a graceful failure strategy.

## 2026-07-03 - Prevent Cache Bypass DoS in Origin Validation
**Vulnerability:** The CORS origin cache failed to cache invalid origins that threw exceptions during parsing (`new URL(origin)`). This allowed an attacker to bypass the cache by sending a flood of requests with malformed `Origin` headers, leading to repeated exceptions and high CPU usage (Denial of Service).
**Learning:** Performance optimizations like caching must handle negative outcomes (errors/invalid inputs) just as robustly as positive outcomes. If invalid inputs aren't cached, the cache can become a DoS vector.
**Prevention:** Ensure "negative caching" is implemented. When catching exceptions for malformed inputs in performance-critical paths, always cache the resulting fallback or failure state to prevent repeated expensive operations.

## 2026-07-04 - Unbounded Decompression leading to DoS (Zip Bomb)
**Vulnerability:** The proxy decompresses upstream HTTP responses (`gzip` and `brotli`) without any constraints on the output size. A highly compressed payload (e.g., a "zip bomb") could result in gigabytes of decompressed data, causing an Out-Of-Memory (OOM) crash and Denial of Service.
**Learning:** Node.js `zlib` asynchronous decompression functions (`zlib.gunzip`, `zlib.brotliDecompress`) do not enforce size limits by default. If decompression bounds are not specified, processing payloads from untrusted or compromised upstreams can exhaust memory.
**Prevention:** Always use the `maxOutputLength` option when calling `zlib` decompression methods, ensuring that decompressed payloads do not exceed a safe maximum size (e.g., 10MB) for the given application context.
