## 2026-06-21 - [Event Loop Blocking by fs.readFileSync]
**Learning:** The proxy-cors.js loads its config synchronously using fs.readFileSync on every request, which blocks the Node.js event loop and severely degrades concurrency.
**Action:** Add a lightweight in-memory cache with a TTL (e.g., 2 seconds) to avoid reading the file system synchronously on every request while preserving hot-reload.
