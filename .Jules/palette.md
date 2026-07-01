## 2024-06-18 - Accessibility Improvement: OS Tabs
**Learning:** Found custom tab components built using `<div>` tags which were inaccessible to keyboard and screen reader users. Replaced them with native `<button>` elements, added ARIA roles (`tablist`, `tab`, `tabpanel`), `aria-controls`, and `aria-selected` attributes. Added `:focus-visible` styling for clear keyboard focus indication.
**Action:** Always prefer native interactive elements like `<button>` over `<div>` for interactive components to inherit built-in keyboard support. Remember to pair visual state changes (like an `active` class) with programmatic state changes (like `aria-selected`).

## 2024-07-25 - Copy Code Blocks Accessibility & Layout
**Learning:** Adding dynamically injected absolutely positioned copy buttons inside horizontally scrolling code blocks (`overflow-x: auto`) can cause the button to scroll out of view or obscure text. Wrapping the `pre` block in a `relative` container and applying padding to the `pre` element ensures the button stays fixed in the top right corner relative to the block without overlapping code content.
**Action:** When adding fixed controls to scrollable content (like code snippets), always wrap the scrollable element in a relative parent container and use padding on the inner element to preserve a safe area for the absolute control.

## 2026-07-01 - Global State Sync for Multi-Step Documentation
**Learning:** Users experience high friction when required to repeatedly select the same contextual preference (like their Operating System) across multiple disconnected UI components in a single document.
**Action:** When a UI contains multiple configuration toggles that represent a global user state, implement synchronization so changing one toggle updates all others, and persist the preference via localStorage so the document remembers the user's environment across reloads.
