## 2023-10-24 - Accessibility improvements to custom tabs
**Learning:** Custom tab implementations using `<div>` elements frequently miss critical ARIA roles (`tablist`, `tab`), attributes (`aria-selected`), and keyboard accessibility features (like `focus-visible` styles and semantic `<button>` elements). This is a common pattern in plain HTML/JS documentation sites.
**Action:** When encountering custom tab systems built with divs, convert them to semantic `<button>` elements, add appropriate ARIA roles and states, and ensure focus indicators are visible for keyboard navigation.
