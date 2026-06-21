## 2024-05-18 - Semantic OS Tabs
**Learning:** Using `<div>` for interactive tabs prevents screen readers from understanding the control. Adding `role="tab"`, `aria-selected` dynamically managed via JavaScript, and converting the element to a `<button>` drastically improves accessibility.
**Action:** Always use semantic `<button>` tags with correct ARIA roles for custom tabbed interfaces. Ensure `focus-visible` styles are maintained when resetting button defaults.
