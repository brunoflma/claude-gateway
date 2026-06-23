## 2026-06-23 - [Proxy Config Read Sync Blocking]
**Learning:** The Node.js proxy server in this codebase used `fs.readFileSync` synchronously on every single request inside `loadConfig()`. While it achieves "hot-reload", it completely blocks the event loop under heavy load or concurrency.
**Action:** When implementing "hot-reload" configurations in Node.js, always use a short TTL cache (like 2 seconds) to avoid synchronous I/O bottlenecks.
