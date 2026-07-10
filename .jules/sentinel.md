
## 2024-05-28 - Prevent Prototype Pollution in Node.js Proxy Server
**Vulnerability:** The SSE data stream handler in `proxy-cors.js` initialized the `toolCalls` associative array with `const toolCalls = {};`. Because keys came directly from external JSON, a malicious `tc.index` value like `__proto__` could lead to prototype pollution on the global `Object.prototype`.
**Learning:** Initializing objects with `{}` exposes them to prototype chain manipulation if untrusted data is used as keys. This is especially risky in proxy servers that parse external streams without tight schema validation.
**Prevention:** Always initialize dictionaries or associative arrays that parse external/untrusted data in Node.js using `Object.create(null)`. This creates an object with no prototype chain, making it immune to `__proto__` manipulation.
