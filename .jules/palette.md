# Palette's UX Journal

## 2024-05-24 - Static HTML Code Block Copy Buttons
**Learning:** When injecting interactive elements like "Copy" buttons into static HTML documentation (`<pre><code>` blocks), using `position: relative` on the `pre` container and `position: absolute` on the button ensures it doesn't disrupt the document flow. For accessibility, it's critical to provide an `aria-label` (e.g., "Copiar código") and visual feedback (e.g., changing text to "Copiado ✓" and background color) to confirm the action. Furthermore, `opacity` transitions combined with `:focus-visible` ensure the button is discoverable by keyboard users even if it's hidden by default for mouse users, maintaining a clean aesthetic without sacrificing accessibility.
**Action:** Re-use this CSS/JS injection pattern (absolute positioning + focus-visible + temporary success state) for any future static HTML guides that contain command-line instructions or paths to improve user experience.
