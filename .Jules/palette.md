## 2024-06-18 - Accessibility Improvement: OS Tabs
**Learning:** Found custom tab components built using `<div>` tags which were inaccessible to keyboard and screen reader users. Replaced them with native `<button>` elements, added ARIA roles (`tablist`, `tab`, `tabpanel`), `aria-controls`, and `aria-selected` attributes. Added `:focus-visible` styling for clear keyboard focus indication.
**Action:** Always prefer native interactive elements like `<button>` over `<div>` for interactive components to inherit built-in keyboard support. Remember to pair visual state changes (like an `active` class) with programmatic state changes (like `aria-selected`).

## 2024-07-25 - Copy Code Blocks Accessibility & Layout
**Learning:** Adding dynamically injected absolutely positioned copy buttons inside horizontally scrolling code blocks (`overflow-x: auto`) can cause the button to scroll out of view or obscure text. Wrapping the `pre` block in a `relative` container and applying padding to the `pre` element ensures the button stays fixed in the top right corner relative to the block without overlapping code content.
**Action:** When adding fixed controls to scrollable content (like code snippets), always wrap the scrollable element in a relative parent container and use padding on the inner element to preserve a safe area for the absolute control.

## 2024-06-28 - Global State Synchronization for Multi-step Guides
**Learning:** In multi-step tutorials with OS-specific instructions, requiring users to repeatedly select their OS on each step causes unnecessary friction. Users expect their initial preference to persist across the entire document.
**Action:** Always implement global state synchronization (e.g., updating all tabs simultaneously) for multi-step guides rather than scoped/local state changes, keeping the user's interaction fluid and reducing cognitive load.

## 2026-07-02 - Dynamic SVG Icons in Copy Buttons
**Learning:** Swapping plain text for HTML containing inline SVGs prevents unexpected layout shifts when button state changes, keeping interactive elements visually stable.
**Action:** Always favor structured icons with `aria-hidden="true"` over plain text approximations when modifying button states to ensure consistent layout and reduce redundant screen-reader announcements.
