## 2026-06-22 - Config Hot-Reload Blocking Event Loop
**Learning:** In `.office-addin-dev-certs/.app/proxy-cors.js`, hot-reloading configurations used a synchronous `fs.readFileSync` on every single request. In a Node.js environment, this blocks the main event loop, significantly degrading request throughput and latency.
**Action:** Replaced synchronous reads on the critical path with an in-memory cached variable that is updated asynchronously via `fs.watchFile`. Always avoid synchronous I/O operations inside request handlers in Node.js.
