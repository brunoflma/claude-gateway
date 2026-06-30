## 2024-06-18 - Accessibility Improvement: OS Tabs
**Learning:** Found custom tab components built using `<div>` tags which were inaccessible to keyboard and screen reader users. Replaced them with native `<button>` elements, added ARIA roles (`tablist`, `tab`, `tabpanel`), `aria-controls`, and `aria-selected` attributes. Added `:focus-visible` styling for clear keyboard focus indication.
**Action:** Always prefer native interactive elements like `<button>` over `<div>` for interactive components to inherit built-in keyboard support. Remember to pair visual state changes (like an `active` class) with programmatic state changes (like `aria-selected`).

## 2024-07-25 - Copy Code Blocks Accessibility & Layout
**Learning:** Adding dynamically injected absolutely positioned copy buttons inside horizontally scrolling code blocks (`overflow-x: auto`) can cause the button to scroll out of view or obscure text. Wrapping the `pre` block in a `relative` container and applying padding to the `pre` element ensures the button stays fixed in the top right corner relative to the block without overlapping code content.
**Action:** When adding fixed controls to scrollable content (like code snippets), always wrap the scrollable element in a relative parent container and use padding on the inner element to preserve a safe area for the absolute control.

## 2026-06-30 - Global Context Sync for Setup Guides
**Learning:** When users select an environment toggle (like OS tabs in documentation), they expect this preference to be remembered throughout the entire document. Forcing them to select the same option multiple times in different sections creates unnecessary friction and a disconnected UX.
**Action:** Always sync environment choices (OS, programming language, theme) globally across the entire page when possible, so the user only has to decide once.
