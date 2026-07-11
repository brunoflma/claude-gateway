## 2026-07-11 - Semantic tags and ARIA for Documentation
**Learning:** Using `role="alert"` or `role="status"` on static content is an anti-pattern as they are designed for dynamically injected content (live regions). Screen readers handle static semantic elements (like generic `<div class="warn">` styled with CSS or proper headers) better during normal document flow reading.
**Action:** Only use ARIA live regions for content that changes dynamically after the page load. Use native semantic elements instead of ARIA roles for static structures.
