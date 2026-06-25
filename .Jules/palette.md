## 2024-06-18 - Accessibility Improvement: OS Tabs
**Learning:** Found custom tab components built using `<div>` tags which were inaccessible to keyboard and screen reader users. Replaced them with native `<button>` elements, added ARIA roles (`tablist`, `tab`, `tabpanel`), `aria-controls`, and `aria-selected` attributes. Added `:focus-visible` styling for clear keyboard focus indication.
**Action:** Always prefer native interactive elements like `<button>` over `<div>` for interactive components to inherit built-in keyboard support. Remember to pair visual state changes (like an `active` class) with programmatic state changes (like `aria-selected`).

## 2026-06-25 - Copy Button Interactive State Feedback
**Learning:** When implementing 'Copy to clipboard' buttons with a temporary success state (e.g., 'Copiado!' text change), dynamically storing the original text via `btn.textContent` on click can cause the success state to get stuck if the user double-clicks the button before the timeout resets it. The second click captures the success text ('Copiado!') as the original text.
**Action:** Hardcode the reset text (e.g., 'Copiar') in the timeout callback instead of storing it dynamically from the button's current state, or implement debouncing/disable the button during the success state to prevent race conditions on double-clicks.
