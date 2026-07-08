## 2026-05-18 - Prevent Prototype Pollution in SSE Stream Parsing
**Vulnerability:** The proxy server was parsing untrusted SSE streams and accumulating tool calls using an object initialized with `const toolCalls = {}`. If an attacker sent a malicious stream with a tool call index of `__proto__`, they could manipulate the global Object prototype.
**Learning:** Initializing objects with `{}` exposes them to Prototype Pollution attacks when using untrusted keys (like parsed JSON arrays/indexes) to assign properties, as the object inherits from `Object.prototype`.
**Prevention:** Always initialize dictionaries or associative arrays that hold untrusted data using `Object.create(null)` instead of `{}`. This creates an object with no prototype chain, preventing manipulation via `__proto__`.
