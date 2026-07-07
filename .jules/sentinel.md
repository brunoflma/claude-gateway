## 2024-05-24 - Prototype Pollution in SSE Tool Call Parsing
**Vulnerability:** Prototype pollution possible when processing streaming tool calls if an attacker controls `tc.index` (e.g. setting it to `__proto__`), allowing them to modify `Object.prototype` since the `toolCalls` dictionary was initialized with `{}`.
**Learning:** Initializing dictionaries or associative arrays with `{}` when processing untrusted JSON data keys is dangerous.
**Prevention:** Always initialize dictionaries using `Object.create(null)` instead of `{}` when parsing untrusted external JSON data to ensure the object has no prototype chain.
