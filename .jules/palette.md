## 2026-06-19 - Improved Tab Accessibility
**Learning:** Found that custom `<div>` based tab systems lack native keyboard focus and ARIA semantics (`role="tablist"`, `role="tab"`). This makes them invisible to screen readers and difficult to navigate via keyboard.
**Action:** Always use `<button>` for interactive tab elements. Make sure to add `role="tablist"` to the container, `role="tab"` and `aria-selected` to the tab buttons, and ensure proper focus styling via `:focus-visible`.
