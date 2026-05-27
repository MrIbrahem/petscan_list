# static — Frontend Assets

## Project Overview

The `static/` directory contains client-side JavaScript and CSS files for the PetScan List web interface. These files provide the UI layer for the Flask application, including theming, autocomplete, interactive tooltips, and styling.

### Files

| File | Purpose |
|---|---|
| `style.css` | Main application styles |
| `lokas-styles.css` | Additional layout/component styles |
| `theme.css` | CSS custom properties for light/dark theme |
| `theme.js` | Theme toggle logic (light/dark mode switching) |
| `interface.js` | UI interaction handlers |
| `autocomplete.js` | Autocomplete widget for wiki/project selection |
| `tt.js` | Tooltip/popover functionality (largest file at ~17KB) |
| `images/` | Image assets |

### Technologies

- **Vanilla JavaScript** (no frameworks)
- **CSS** with custom properties for theming
- No build system or bundler

---

## Architecture & Code Quality Review

### Code Organization

Files are flat in the `static/` directory. No subdirectory structure for JS vs CSS. The `images/` subfolder is the only organizational separation.

### Design Patterns

- **CSS Custom Properties**: `theme.css` uses CSS variables for theme switching.
- **No framework**: Pure vanilla JS — keeps the bundle size small but limits reusability.

### Maintainability

- No minification or bundling pipeline.
- No linting configuration (ESLint, Stylelint).
- File naming is descriptive but inconsistent (`lokas-styles.css` vs `style.css`).

### Readability

- CSS files are reasonably organized.
- JS files would benefit from consistent formatting.

---

## Strengths

1. **Lightweight** — No heavy frameworks; vanilla JS keeps page load fast.
2. **Theme support** — CSS custom properties enable clean light/dark mode switching.
3. **No build step required** — Files can be served directly without compilation.
4. **Focused files** — Each file has a clear purpose (theme, autocomplete, tooltips).

---

## Weaknesses

### 1. No Asset Pipeline
No minification, concatenation, or cache-busting. Each file is a separate HTTP request with no fingerprinting for cache invalidation.

### 2. Duplicate CSS Files
`style.css` and `lokas-styles.css` appear to overlap in purpose. The name "lokas-styles" is unclear and may be a legacy artifact.

### 3. Large `tt.js` File
At ~17KB, `tt.js` is significantly larger than the other JS files. It likely contains inline data or could benefit from code splitting.

### 4. No Documentation
No comments explaining the purpose of individual CSS classes or JS functions.

---

## Critical Issues

### 1. Potential XSS in Tooltip Content (Medium)
If `tt.js` renders user-supplied content in tooltips without escaping, it could be vulnerable to XSS. This needs manual review of the tooltip rendering logic.

### 2. No Content Security Policy (Medium)
No CSP headers are configured. Combined with inline scripts, this increases the XSS attack surface.

---

## Areas That Need Attention

- **Add a build pipeline** — Minify CSS/JS, add cache-busting hashes.
- **Merge duplicate CSS** — Consolidate `style.css` and `lokas-styles.css`.
- **Add source comments** — Document the purpose of major CSS sections and JS functions.
- **Audit `tt.js`** — Review for XSS vulnerabilities in tooltip rendering.
- **Add `.gitattributes` entries** — Mark binary files in `images/` with LFS if needed.

---

## Improvement Plan

### Quick Wins
1. Add comments to CSS files documenting major sections.
2. Consolidate `style.css` and `lokas-styles.css` into a single file.
3. Add `loading="lazy"` to image tags where applicable.

### Medium-Term Improvements
4. Add a simple build step (e.g., `esbuild` or `cssnano`) for minification.
5. Add cache-busting via Flask's `url_for(..., v=hash)` pattern.
6. Audit `tt.js` for XSS vulnerabilities.

### Long-Term Recommendations
7. Consider migrating to a lightweight framework (e.g., Alpine.js) for complex interactions.
8. Add CSP headers to the Flask application.
9. Implement a proper asset pipeline with fingerprinting.

---

## Comprehensive Review

| Metric | Score | Notes |
|---|---|---|
| **Overall Rating** | **5.5 / 10** | Functional but no build tooling or security hardening |
| **Production Readiness** | Moderate | Works, but no optimization or security measures |
| **Technical Debt** | Medium | Duplicate CSS, large tooltip file, no build pipeline |
| **Risk Assessment** | Low-Medium | Potential XSS in tooltips; no CSP |
| **Maintainability** | 5 / 10 | No tooling, no documentation, no linting |
