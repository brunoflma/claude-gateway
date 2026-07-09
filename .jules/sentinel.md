## 2025-05-14 - Prototype Pollution in Stream Parsing
**Vulnerability:** Untrusted index from SSE stream payload used as key in `{}` object.
**Learning:** Object initialization with `{}` inherits `Object.prototype`, leaving it vulnerable to `__proto__` injection.
**Prevention:** Initialize associative arrays with `Object.create(null)` when keys come from external sources.
