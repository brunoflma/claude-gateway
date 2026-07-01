## 2024-05-30 - Synchronous fs I/O bottleneck
**Learning:** In a local proxy server receiving frequent, potentially concurrent requests (even just `/ping` checks from the frontend), reading a JSON configuration file via synchronous `fs.readFileSync` on every single request acts as a massive bottleneck, severely degrading latency and concurrency handling in Node.js' single-threaded event loop.
**Action:** Always employ caching for file reads on the hot path (like configuration checks). Use a TTL (e.g., 2000ms) to preserve hot-reloading features without destroying performance.

## 2026-06-25 - Explicit connection pooling for upstream proxy requests
**Learning:** Node.js `https.request` without an explicit `agent` does not reuse connections (no keep-alive pooling) by default. In a proxy server forwarding many API requests to the same upstream host, this forces a new TCP connection and full TLS handshake on *every single request*, adding 100-200ms of latency per call.
**Action:** Always instantiate and provide a global `new https.Agent({ keepAlive: true })` when making frequent outgoing requests to the same host in Node.js proxies.

## 2024-05-31 - Unbounded Map memory leak
**Learning:** In long-running Node.js proxy servers, caching values using a `Map` without an eviction strategy acts as a memory leak that can degrade performance over time. `reasoningCache` grew indefinitely for every tool call.
**Action:** Always implement an eviction strategy for in-memory caches. A simple FIFO mechanism (`if (cache.size > N) cache.delete(cache.keys().next().value)`) efficiently caps memory usage.

## 2026-07-01 - Cache CORS origins and preflight requests
**Learning:** Browser clients issue a preflight OPTIONS request prior to every new cross-origin request. In this codebase's reverse proxy architecture serving frequent chat model streaming API requests, these repetitive OPTIONS requests can cause significant network overhead and proxy CPU time.
**Action:** Always ensure that `access-control-max-age` is configured to cache preflight OPTIONS requests, effectively halving the number of network roundtrips, and cache URL origin parsing locally to save redundant repetitive logic in hot paths.
