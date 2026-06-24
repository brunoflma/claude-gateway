## 2024-05-30 - Synchronous fs I/O bottleneck
**Learning:** In a local proxy server receiving frequent, potentially concurrent requests (even just `/ping` checks from the frontend), reading a JSON configuration file via synchronous `fs.readFileSync` on every single request acts as a massive bottleneck, severely degrading latency and concurrency handling in Node.js' single-threaded event loop.
**Action:** Always employ caching for file reads on the hot path (like configuration checks). Use a TTL (e.g., 2000ms) to preserve hot-reloading features without destroying performance.

## 2024-05-31 - Unbounded Map memory leak
**Learning:** In long-running Node.js proxy servers, caching values using a `Map` without an eviction strategy acts as a memory leak that can degrade performance over time. `reasoningCache` grew indefinitely for every tool call.
**Action:** Always implement an eviction strategy for in-memory caches. A simple FIFO mechanism (`if (cache.size > N) cache.delete(cache.keys().next().value)`) efficiently caps memory usage.
