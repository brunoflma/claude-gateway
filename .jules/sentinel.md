## 2025-07-06 - Prevent Prototype Pollution in SSE Tool Calls
**Vulnerability:** Upstream servers could inject an SSE tool call with `index: "__proto__"`, which bypassed `if (!toolCalls[idx])` and assigned object fields to `Object.prototype`, leading to prototype pollution.
**Learning:** Using a plain `{}` object to map streams using arbitrary upstream IDs/indexes exposes the application to prototype pollution because `__proto__` is a valid index but resolves to the object prototype.
**Prevention:** Use `Object.create(null)` when creating associative arrays/dictionaries that store data based on external keys, guaranteeing there is no prototype to pollute.
