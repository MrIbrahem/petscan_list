# PetScanList — Core Python Package

## Project Overview

`PetScanList` is the core Python package powering the PetScan List application. It provides a complete pipeline for querying the [PetScan](https://petscan.wmcloud.org/) API, parsing MediaWiki `{{petscan list}}` templates, generating formatted output (bulleted lists or wikitables), and editing Wikipedia pages via bot credentials.

### Main Modules

| Module | Purpose |
|---|---|
| `__init__.py` | Public API surface — re-exports all key functions |
| `petscan_bot.py` | PetScan HTTP client — builds URLs, fetches JSON, processes results |
| `text_bot.py` | Wikitext parser — finds `{{petscan list}}` templates, generates formatted output, replaces content |
| `one_page_bot.py` | `WikiBot` class — authenticates with mwclient, reads/writes wiki pages |
| `make_template.py` | Converts a PetScan URL query string into a `{{petscan list}}` wikitext template |
| `wikitable.py` | Generates MediaWiki `{| class="wikitable" |}` markup from structured data |
| `I18n.py` | Loads translation strings from local JSON files or the Tooltranslate service |
| `sites.py` | Defines the whitelist of supported wikis and projects |
| `pages.py` | Convenience wrapper to retrieve all pages containing `{{petscan list}}` for a given wiki |
| `params.py` | Constants for PetScan parameter filtering (ignored params, no-newline params) |
| `account.py` | Loads bot credentials from environment variables / `.env` file |
| `petscan.lua` | Lua Scribunto module for MediaWiki — generates PetScan URLs server-side |

### Dependencies

- **mwclient** — MediaWiki API client for page read/write
- **pywikibot** — Used solely for `showDiff` functionality
- **wikitextparser** — Parses and manipulates MediaWiki wikitext
- **requests** — HTTP client for PetScan API calls
- **python-dotenv** — Loads `.env` credentials
- **flask** — (Used by the parent `app.py`, not directly imported here)

---

## Architecture & Code Quality Review

### Code Organization

The package follows a flat module structure with a clean `__init__.py` that exports a well-defined public API (`__all__`). Each module has a single responsibility:

```
PetScanList/
├── __init__.py          # Public API
├── account.py           # Credential loading
├── I18n.py              # Translations
├── make_template.py     # URL → wikitext template
├── one_page_bot.py      # WikiBot class (auth + page editing)
├── pages.py             # Page listing helper
├── params.py            # Parameter constants
├── petscan_bot.py       # PetScan API client
├── sites.py             # Wiki whitelist
├── text_bot.py          # Wikitext processing engine
├── wikitable.py         # Wikitable generator
└── petscan.lua          # Lua module for MediaWiki
```

### Design Patterns

- **Facade Pattern**: `__init__.py` exposes a simplified API hiding internal complexity.
- **Separation of Concerns**: API client (`petscan_bot`), wikitext processing (`text_bot`), and wiki interaction (`one_page_bot`) are cleanly separated.
- **Configuration as Code**: `sites.py` and `params.py` use module-level constants.

### Maintainability

- Modules are short (most under 120 lines) and focused.
- Function signatures use type hints (`Dict`, `List`, `Union`, `str`, `int`).
- Docstrings are present on most public functions.

### Readability

- Variable naming is generally clear (`formatted_list`, `template_string`, `other_params`).
- Some Arabic comments and hardcoded Arabic strings exist (e.g., `"العنوان"`, `"النطاق"` in `wikitable.py`), which may hinder non-Arabic-speaking contributors.

### Scalability Considerations

- PetScan API requests are synchronous and sequential — no concurrency for batch operations.
- The `WikiBot` class caches `mwclient.Site` objects in a dict, avoiding repeated logins per wiki.

---

## Strengths

1. **Clean module separation** — Each file has a single, well-defined responsibility.
2. **Explicit public API** — `__all__` in `__init__.py` makes the import surface clear.
3. **Defensive error handling** — `petscan_bot.py` catches specific `requests` exceptions; `one_page_bot.py` handles `mwclient.errors.LoginError` and `PageError`.
4. **User-Agent compliance** — HTTP requests include a proper `User-Agent` string with contact info.
5. **Configurable output** — Supports both bulleted lists and wikitables via `_result_=table` parameter.
6. **Lua companion module** — `petscan.lua` provides server-side URL generation, reducing client dependency.
7. **Type hints** — Present on most function signatures in `petscan_bot.py`, `pages.py`, and `I18n.py`.

---

## Weaknesses

### 1. Inconsistent Error Handling
- `text_bot.py` uses `print()` for warnings instead of `logging` (lines 59, 120-121).
- `pages.py` uses `print()` for error reporting (line 28).
- `one_page_bot.py` configures `logging.basicConfig()` at module import time (line 11), which is a side effect that affects the entire application.

### 2. Code Duplication
- The `fix_value()` function exists in both `text_bot.py` (line 18) and `make_template.py` (line 9) with similar but not identical logic.
- `{{!}}` / `{{|}}` replacement is done in at least 3 places: `text_bot.py:28`, `text_bot.py:43`, and `make_template.py:58`.

### 3. Hardcoded Arabic Labels
- `wikitable.py` lines 5-14 hardcode Arabic column headers (`"العنوان"`, `"آخر تعديل"`, etc.). These should come from the I18n system.

### 4. Mixed Concerns in `one_page_bot.py`
- The `WikiBot` class handles authentication, page reading, text processing delegation, saving, and diff display — it's a god class that could be split.

### 5. Unused Import
- `pywikibot` is imported in `one_page_bot.py` (line 4) solely for `showDiff`, but `showDiff` is only used when `"ask"` is in `sys.argv`. This adds a heavy dependency for a rarely-used debug feature.

---

## Critical Issues

### 1. Credential Exposure Risk (Medium)
`account.py` loads credentials from environment variables with empty-string defaults:
```python
username = os.getenv("WIKIPEDIA_BOT_USERNAME", "")
password = os.getenv("WIKIPEDIA_BOT_PASSWORD", "")
```
If the `.env` file is missing or incomplete, the bot will attempt to authenticate with empty credentials, generating login errors rather than failing fast.

### 2. No Input Validation on PetScan Parameters (Medium)
`petscan_bot.py` `validate_and_sanitize_params()` only validates `output_limit`. Other parameters are passed directly to the PetScan URL without sanitization, which could lead to unexpected API behavior or injection of arbitrary query parameters.

### 3. Unsafe String Splitting in `add_result_to_text()` (Low-Medium)
`text_bot.py` line 134:
```python
pet_section = text.split(template_string)[1].split(template_end_string)[0]
```
If `template_string` appears multiple times in the text, `[1]` picks the second occurrence, potentially corrupting the page. No guard exists for this case.

### 4. Logging Configuration Side Effect (Low)
`one_page_bot.py` line 11:
```python
logging.basicConfig(level=LOGGING_LEVEL)
```
This runs at import time and overrides any logging configuration set by the calling application (e.g., Flask).

### 5. Synchronous Blocking in Bot Mode (Low)
`one_page_bot.py` `many_pages()` processes pages sequentially in a loop. For large result sets (up to 3000 pages), this could take hours with no parallelism.

---

## Areas That Need Attention

- **No tests** — Zero unit tests or integration tests exist for any module.
- **No `setup.py` / `pyproject.toml`** — The package cannot be installed via pip.
- **No logging consistency** — Some modules use `logging`, others use `print()`.
- **No rate limiting** — PetScan API and MediaWiki API calls have no throttling.
- **Missing type hints** — `text_bot.py`, `wikitable.py`, and `make_template.py` have incomplete type annotations.
- **No docstrings** — `account.py`, `sites.py`, `params.py`, and `wikitable.py` lack module-level docstrings.
- **Dead code** — Commented-out blocks in `one_page_bot.py` (lines 87-91) and `text_bot.py` (lines 181, 190-191).
- **`petscan.lua`** — Not tested or documented alongside the Python code; unclear if it's kept in sync.

---

## Improvement Plan

### Quick Wins
1. Replace all `print()` calls with `logging` for consistent observability.
2. Remove `logging.basicConfig()` from `one_page_bot.py` — let the entry point configure logging.
3. Add fail-fast validation in `account.py` — raise an error if credentials are empty.
4. Extract `fix_value()` and `{{!}}` replacement into a shared utility to eliminate duplication.
5. Clean up commented-out dead code.

### Medium-Term Improvements
6. Add unit tests for `petscan_bot.py`, `text_bot.py`, `make_template.py`, and `wikitable.py`.
7. Add `pyproject.toml` for proper Python packaging.
8. Move hardcoded Arabic labels in `wikitable.py` to the I18n system.
9. Add rate limiting (e.g., `time.sleep()` between API calls) for batch operations.
10. Add input validation/sanitization for PetScan parameters.

### Long-Term Refactoring
11. Split `WikiBot` into smaller classes: `WikiAuthenticator`, `PageEditor`, `DiffViewer`.
12. Add async/concurrent processing for batch page operations (e.g., `asyncio` + `aiohttp`).
13. Add integration tests with mocked PetScan/MediaWiki APIs.
14. Create a proper CLI interface using `argparse` or `click` instead of raw `sys.argv` checks.

---

## Comprehensive Review

| Metric | Score | Notes |
|---|---|---|
| **Overall Rating** | **6.5 / 10** | Functional but lacks testing and has some architectural debt |
| **Production Readiness** | Moderate | Works in production via Toolforge, but no tests or CI validation |
| **Technical Debt** | Medium | Code duplication, mixed logging, commented-out code |
| **Risk Assessment** | Low-Medium | Credential handling and string splitting edge cases are the main risks |
| **Maintainability** | 6 / 10 | Good separation of concerns, but no tests make refactoring risky |
