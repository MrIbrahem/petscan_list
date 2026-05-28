# templates — HTML Templates (Jinja2)

## Project Overview

The `templates/` directory contains Jinja2 HTML templates for the Flask web application. These render the user-facing pages: the homepage, result pages, page listings, tutorials, template generation form, and error pages.

### Files

| Template | Route | Purpose |
|---|---|---|
| `index.html` | `/` | Homepage — wiki selector and main navigation |
| `main.html` | (base layout) | Base template with common structure |
| `main copy.html` | — | Duplicate/backup of `main.html` |
| `result.html` | `/update` | Displays bot operation results (success/error) |
| `pages.html` | `/pages` | Lists pages containing `{{petscan list}}` templates |
| `template_form.html` | `/template` | Form to generate `{{petscan list}}` wikitext from a PetScan URL |
| `tutorials.html` | `/tutorials` | Usage tutorials and documentation |
| `error.html` | 404/500 | Error page display |

### Technologies

- **Jinja2** templating (Flask default)
- **HTML5**
- References external CSS from `static/` and JS from `static/`

---

## Architecture & Code Quality Review

### Code Organization

Templates follow a flat structure. `main.html` appears to serve as a base layout, with other templates extending or including it.

### Design Patterns

- **Template inheritance** — `main.html` provides the base layout.
- **Translation integration** — Templates use `tt` variables for i18n strings passed from the Flask app.

### Maintainability

- Templates are short and focused (5–180 lines each).
- No template-level comments explaining sections.

### Readability

- HTML is generally well-structured.
- Some templates mix Arabic and English content.

---

## Strengths

1. **Clean separation** — Each page has its own template file.
2. **Translation support** — Templates receive `tt` variables for localized strings.
3. **Error handling** — Dedicated `error.html` for 404/500 errors.
4. **Reasonable size** — No template exceeds 200 lines.

---

## Weaknesses

### 1. `main copy.html` — Dead File
This is a duplicate of `main.html` that should not be in version control. It's either a backup artifact or leftover from development.

### 2. No CSRF Protection
The `template_form.html` uses a POST form but there's no CSRF token. The Flask app doesn't appear to use Flask-WTF or any CSRF protection.

### 3. Inline Styles/Scripts
Some templates may contain inline styles or JavaScript instead of referencing the external `static/` files.

### 4. No Template Linting
No HTML/Jinja2 linting configuration (e.g., djlint, htmlhint).

---

## Critical Issues

### 1. Missing CSRF Token on POST Form (Medium)
`template_form.html` submits a form via POST to `/template` without a CSRF token. This makes the endpoint vulnerable to cross-site request forgery attacks.

### 2. Potential XSS in Template Rendering (Medium)
If template variables (`tt`, `title`, `url`, `result_text`) are not auto-escaped by Jinja2, they could allow XSS. Jinja2 auto-escapes by default, but this should be verified — especially for any `| safe` filters used.

### 3. No `X-Frame-Options` Header (Low)
The application doesn't set `X-Frame-Options`, making it susceptible to clickjacking.

---

## Areas That Need Attention

- **Delete `main copy.html`** — It's a dead file that adds confusion.
- **Add CSRF protection** — Integrate Flask-WTF or add manual CSRF token validation.
- **Audit for `| safe` filter usage** — Ensure no user input bypasses Jinja2 auto-escaping.
- **Add `X-Content-Type-Options: nosniff`** and `X-Frame-Options: DENY` headers.
- **Add template comments** — Document the purpose of major template blocks.

---

## Improvement Plan

### Quick Wins
1. Delete `main copy.html`.
2. Add `<!-- Template: filename.html -->` comments at the top of each file.
3. Verify no `| safe` filter is used on user-supplied variables.

### Medium-Term Improvements
4. Add Flask-WTF for CSRF protection on all POST forms.
5. Add security headers via Flask's `after_request` hook.
6. Add template linting to CI (e.g., `djlint`).

### Long-Term Recommendations
7. Add a Content Security Policy header.
8. Consider adding HTML minification for production.
9. Add accessibility attributes (ARIA labels, semantic HTML) to forms.

---

## Comprehensive Review

| Metric | Score | Notes |
|---|---|---|
| **Overall Rating** | **5.5 / 10** | Functional templates with some security gaps |
| **Production Readiness** | Moderate | Works, but lacks CSRF and security headers |
| **Technical Debt** | Low-Medium | One dead file, no linting |
| **Risk Assessment** | Medium | CSRF vulnerability on POST endpoint |
| **Maintainability** | 6 / 10 | Clean structure, but no documentation or linting |
