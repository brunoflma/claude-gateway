## 2026-07-08 - Semantic HTML & ARIA Live Regions for Visual Callouts
**Learning:** Applying visual styles (like `.warn` or `.info`) without corresponding ARIA attributes creates screen reader blind spots. In static HTML, `<table>` elements must use structural tags (`<thead>`, `<tbody>`, `<th scope="col">`) to communicate column headers to screen readers properly.
**Action:** Always include semantic `<thead>`/`<tbody>` for tables and map visual status boxes to `role="alert"` (for warnings) and `role="status"` (for info/success) to ensure the intent is announced.
