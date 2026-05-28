# I18n — Internationalization

## Project Overview

The `I18n/` directory contains translation files for the PetScan List application. These provide localized strings used by the bot when editing Wikipedia pages (edit summaries, section titles) and by the web interface.

### Files

| File | Purpose |
|---|---|
| `ar.json` | Arabic translations — the primary (and currently only) language |

### How It Works

Translations are loaded by `PetScanList/I18n.py` using this lookup order:
1. Local file: `I18n/{lang}.json`
2. Remote fallback: Tooltranslate service (`tools-static.wmflabs.org`)
3. English fallback: `I18n/en.json` (if it exists)

The key `"summary"` provides the edit summary used by the bot. The key `"section_title"` provides the section header for generated lists.

---

## Architecture & Code Quality Review

### Code Organization

A single JSON file per language. The structure is flat — just key-value pairs. This is appropriate for the small number of strings needed.

### Design Pattern

- **Fallback chain**: Local file → remote service → English default.
- **Key-based lookup**: Simple string interpolation via `translations.get(key, key)`.

### Maintainability

- Adding a new language requires only creating a new JSON file.
- No schema validation — malformed JSON would silently fail.

### Readability

- The Arabic translations are clear and well-formed.

---

## Strengths

1. **Simple structure** — Easy to add new languages.
2. **Fallback mechanism** — Gracefully degrades if a translation file is missing.
3. **Remote fallback** — Can pull translations from Tooltranslate if local files are incomplete.

---

## Weaknesses

### 1. No English Translation File
The code falls back to English in `I18n.py` line 42 (`get_translations("en")`), but no `en.json` exists. The fallback would return the raw key string (e.g., `"summary"` instead of a human-readable English message).

### 2. No Schema Validation
No JSON schema or validation. A typo in a key name would silently return the key itself.

### 3. Incomplete Coverage
Only 2 keys are defined (`summary`, `section_title`). Other UI-facing strings (error messages, status labels) are hardcoded elsewhere in the codebase.

### 4. No Documentation of Keys
There's no manifest listing all expected translation keys and their usage context.

---

## Critical Issues

None — this is a simple data directory with minimal risk.

---

## Areas That Need Attention

- **Create `en.json`** — The English fallback is referenced but doesn't exist.
- **Add more translation keys** — Error messages in `one_page_bot.py` (e.g., `"page_not_found"`, `"empty_page"`, `"ns0_not_supported"`) are returned as raw keys, not localized strings.
- **Document expected keys** — Add a comment or schema file listing all translation keys.

---

## Improvement Plan

### Quick Wins
1. Create `en.json` with English translations for all keys.
2. Document the expected key format in a comment at the top of each JSON file.

### Medium-Term Improvements
3. Add a JSON schema file for validation.
4. Expand translations to cover all error/status messages used in `one_page_bot.py`.
5. Add support for more languages (e.g., `fr.json`, `de.json`) if the tool is used beyond Arabic Wikipedia.

### Long-Term Recommendations
6. Integrate with the Tooltranslate platform for community-contributed translations.
7. Add automated validation in CI to check for missing keys across language files.

---

## Comprehensive Review

| Metric | Score | Notes |
|---|---|---|
| **Overall Rating** | **5 / 10** | Minimal but functional; needs expansion |
| **Production Readiness** | Adequate | Works for the current Arabic-only use case |
| **Technical Debt** | Low | Simple structure, easy to extend |
| **Risk Assessment** | Low | Missing translations degrade gracefully |
| **Maintainability** | 8 / 10 | Just add a JSON file for new languages |
