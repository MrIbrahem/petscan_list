[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/MrIbrahem/petscan_list)

# PetScan List Application

A Flask web application and Wikipedia bot that manages and processes [PetScan](https://petscan.wmcloud.org/) lists for Wikipedia articles. It reads `{{petscan list}}` templates from wiki pages, queries the PetScan API for results, and writes formatted lists or wikitables back to the page.

## Project Overview

### What It Does

1. **Web Interface** — Users submit a Wikipedia page title; the app reads the page, finds `{{petscan list}}` templates, queries PetScan, and writes the formatted results back.
2. **Bot Mode** — Automatically scans all pages containing `{{petscan list}}` across configured wikis and processes them in batch.
3. **Template Generator** — Converts a PetScan URL into a `{{petscan list}}` wikitext template that can be pasted into any wiki page.

### Main Components

| Component | File(s) | Purpose |
|---|---|---|
| Flask Web App | `app.py` | HTTP routes for web interface |
| Bot Entry Point | `bot.py` | Batch processing for all configured wikis |
| Core Package | `PetScanList/` | API client, wikitext parser, wiki editor, i18n |
| Frontend | `static/`, `templates/` | CSS, JS, and Jinja2 HTML templates |
| Deployment | `shs/` | Shell scripts for Toolforge deployment |
| Translations | `I18n/` | Localized strings (Arabic) |
| CI/CD | `.github/workflows/update.yml` | Auto-deploy on push to `main` |

### Technologies & Dependencies

- **Python 3.11** — Runtime
- **Flask** — Web framework
- **mwclient** — MediaWiki API client
- **pywikibot** — Diff display utility
- **wikitextparser** — Wikitext parsing and manipulation
- **requests** — HTTP client for PetScan API
- **python-dotenv** — Environment variable loading
- **Wikimedia Toolforge** — Production hosting platform

---

## Prerequisites

- Python 3.x
- pip (Python package installer)
- Wikipedia account with bot password

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/MrIbrahem/petscan_list.git
   cd petscan_list
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   .\venv\Scripts\activate  # On Windows
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a bot password for your Wikipedia account:
   - Go to Special:BotPasswords on Wikipedia (https://ar.wikipedia.org/wiki/Special:BotPasswords)
   - Create a new bot password with necessary permissions

2. Set up your credentials:
   - Create a `.env` file in the project root with the following content:
     ```env
     WIKIPEDIA_BOT_USERNAME=YOUR_USERNAME
     WIKIPEDIA_BOT_PASSWORD=YOUR_BOT_PASSWORD
     ```
   Replace `YOUR_USERNAME` with your Wikipedia username and `YOUR_BOT_PASSWORD` with your bot password.

   Alternatively, you can set environment variables directly:
   ```bash
   set WIKIPEDIA_BOT_USERNAME=YOUR_USERNAME
   set WIKIPEDIA_BOT_PASSWORD=YOUR_BOT_PASSWORD
   ```

## Running the Application

### 1. Web Interface (Flask Application)

Start the Flask development server:
```bash
python app.py
```

Then open your web browser and navigate to:
```
http://localhost:5000
```

The web interface allows you to:
- Process individual Wikipedia articles
- View results directly in your browser
- Interactive usage with immediate feedback

### 2. Bot Mode (Automated Processing)

Run the bot script to automatically process multiple pages:
```bash
python bot.py
```

The bot mode:
- Automatically searches for pages with "petscan list" template
- Processes all found pages in batch
- Works specifically with Arabic Wikipedia
- Runs continuously without manual intervention

## Project Structure

```
petscan_list/
├── app.py                  # Flask web application
├── bot.py                  # Batch bot entry point
├── requirements.txt        # Python dependencies
├── jobs.yaml               # Toolforge job scheduler config
├── run.bat                 # Windows dev launcher
├── PetScanList/            # Core Python package
│   ├── __init__.py         # Public API exports
│   ├── petscan_bot.py      # PetScan HTTP client
│   ├── text_bot.py         # Wikitext template processor
│   ├── one_page_bot.py     # WikiBot class (auth + page editing)
│   ├── make_template.py    # URL → wikitext template converter
│   ├── wikitable.py        # Wikitable generator
│   ├── I18n.py             # Translation loader
│   ├── sites.py            # Supported wiki whitelist
│   ├── pages.py            # Page listing helper
│   ├── params.py           # Parameter constants
│   ├── account.py          # Credential loading
│   └── petscan.lua         # Lua Scribunto module for MediaWiki
├── shs/                    # Deployment shell scripts
│   ├── install.sh          # Initial Toolforge setup
│   ├── pip.sh              # Dependency refresh
│   ├── runall.sh           # Daily batch job
│   └── update.sh           # Live deployment update
├── I18n/                   # Translation files
│   └── ar.json             # Arabic translations
├── static/                 # Frontend assets (CSS, JS)
│   ├── style.css           # Main styles
│   ├── theme.css / theme.js # Light/dark theme
│   ├── autocomplete.js     # Wiki selector autocomplete
│   ├── tt.js               # Tooltip functionality
│   └── images/             # Image assets
├── templates/              # Jinja2 HTML templates
│   ├── index.html          # Homepage
│   ├── main.html           # Base layout
│   ├── result.html         # Operation result page
│   ├── pages.html          # Page listing
│   ├── template_form.html  # Template generator form
│   ├── tutorials.html      # Usage tutorials
│   └── error.html          # Error page
└── .github/workflows/
    └── update.yml          # CI/CD: auto-deploy on push to main
```

## Scripts

- `shs/install.sh` — Initial Toolforge setup (create venv, clone repo, start webservice)
- `shs/update.sh` — Live deployment update with backup and rollback
- `shs/pip.sh` — Dependency refresh
- `shs/runall.sh` — Daily batch bot execution

## Usage

### Web Interface
1. Navigate to the homepage at `http://localhost:5000`
2. Enter the Wikipedia article title
3. The application will process the PetScan list and display the results

### Bot Mode
1. Make sure your credentials are properly configured
2. Run `python bot.py`
3. The bot will automatically:
   - Find pages with "petscan list" template
   - Process each page
   - Show progress in the terminal

### Template Generator
1. Navigate to `/template`
2. Paste a PetScan URL with query parameters
3. Optionally set `_line_format_`, `at_start`, `at_end`
4. The tool generates `{{petscan list}}` wikitext ready to paste

## Template Format Params

These parameters are optional:

- **`|_result_=table`**: Display the result as a wikitable instead of a bulleted list.
- **`|_line_format_=`**: Customize the line format. `$1` is replaced with the page title. Example:
   ```wiki
   |_line_format_ = # {{user:Mr. Ibrahem/link|$1}}
   ```
- **`|_at_start_=`**: Custom content before the list (default: `{{Div col|colwidth=20em}}`)
- **`|_at_end_=`**: Custom content after the list (default: `{{Div col end}}`)

## Default Values
- **`|output_limit = 3000`**: Maximum number of results to display.

---

## Architecture & Code Quality Review

### Code Organization

The project follows a clean two-tier architecture:
- **Entry points** (`app.py`, `bot.py`) at the root — thin wrappers that delegate to the core package.
- **Core package** (`PetScanList/`) — contains all business logic, API clients, and utilities.
- **Presentation** (`templates/`, `static/`) — separated from logic.

### Design Patterns

- **Facade**: `PetScanList/__init__.py` exports a simplified API.
- **Separation of Concerns**: API client, wikitext processing, and wiki editing are distinct modules.
- **Configuration as Code**: `sites.py` and `params.py` define constants at module level.
- **CI/CD**: GitHub Actions auto-deploys on push to `main` via SSH to Toolforge.

### Maintainability

- Modules are short and focused (most under 130 lines).
- Type hints are present on key functions.
- Each module has a clear single responsibility.

### Readability

- Variable naming is generally descriptive.
- Some Arabic strings are hardcoded outside the I18n system.
- Commented-out dead code exists in several files.

### Scalability

- Synchronous processing — no concurrency for batch operations.
- PetScan API results are capped at 3000 via `OUTPUT_LIMIT`.
- Site objects are cached per wiki in `WikiBot.sites`.

---

## Strengths

1. **Clean module separation** — Each file in `PetScanList/` has a single, well-defined responsibility.
2. **Explicit public API** — `__all__` in `__init__.py` makes the import surface clear and intentional.
3. **Defensive error handling** — Specific exception handling for HTTP errors, login failures, and page-not-found.
4. **User-Agent compliance** — All HTTP requests include a proper `User-Agent` with contact info.
5. **Backup-on-deploy** — `update.sh` creates timestamped backups before every deployment with automatic rollback on failure.
6. **Dual output modes** — Supports both bulleted lists and wikitables via the `_result_` parameter.
7. **Lua companion module** — `petscan.lua` provides server-side PetScan URL generation within MediaWiki.
8. **Automated CI/CD** — GitHub Actions deploys to Toolforge on every push to `main`.
9. **Toolforge-native** — Uses `toolforge-jobs` for scheduled batch runs and `webservice` for the web app.

---

## Weaknesses

### 1. No Tests
Zero unit tests, integration tests, or end-to-end tests. Any refactoring is risky without a test safety net.

### 2. Inconsistent Logging
Some modules use `logging`, others use `print()`. `one_page_bot.py` calls `logging.basicConfig()` at import time, overriding the caller's configuration.

### 3. Code Duplication
- `fix_value()` logic appears in both `text_bot.py` and `make_template.py`.
- `{{!}}` / `{{|}}` replacement is done in at least 3 places.
- Session creation (`requests.session()`) is duplicated in `petscan_bot.py` and `I18n.py`.

### 4. Hardcoded Arabic Content
Column headers in `wikitable.py` are hardcoded Arabic strings instead of using the I18n system.

### 5. No Python Packaging
No `setup.py`, `pyproject.toml`, or `__main__.py`. The package can't be installed via pip or run with `python -m PetScanList`.

### 6. Dead Files and Code
- `templates/main copy.html` — duplicate template file.
- Commented-out blocks in `one_page_bot.py` and `text_bot.py`.
- `confs/` directory referenced in README doesn't exist.

### 7. Synchronous Batch Processing
`bot.py` processes all pages sequentially. For large result sets (up to 3000 pages per wiki), this is very slow.

---

## Critical Issues

### 1. Missing CSRF Protection (Medium-High)
The `/template` POST endpoint has no CSRF token. An attacker could craft a form on another site that submits to this endpoint.

### 2. Credential Fail-Silent (Medium)
`account.py` defaults to empty strings if env vars are missing. The bot will attempt API calls with empty credentials, producing confusing errors instead of failing fast.

### 3. Unsafe String Splitting (Medium)
`text_bot.py` line 134:
```python
pet_section = text.split(template_string)[1].split(template_end_string)[0]
```
If `template_string` appears multiple times, `[1]` picks the wrong occurrence, potentially corrupting the page.

### 4. No Security Headers (Medium)
No `X-Frame-Options`, `X-Content-Type-Options`, or `Content-Security-Policy` headers. The app is vulnerable to clickjacking and MIME-type sniffing.

### 5. Logging Side Effect at Import (Low)
`one_page_bot.py` line 11:
```python
logging.basicConfig(level=LOGGING_LEVEL)
```
This runs at import time and overrides any logging configuration set by Flask or the calling application.

### 6. Potential XSS in Static JS (Low-Medium)
`tt.js` (tooltip library) needs manual audit to verify it properly escapes user-supplied content.

---

## Areas That Need Attention

| Category | Issue | Priority |
|---|---|---|
| **Testing** | Zero tests exist | High |
| **Security** | No CSRF on POST forms | High |
| **Security** | No security headers | Medium |
| **Code Quality** | Mixed logging (print vs logging) | Medium |
| **Code Quality** | Code duplication across modules | Medium |
| **Documentation** | `confs/` referenced in README but doesn't exist | Medium |
| **Dead Code** | `templates/main copy.html` should be deleted | Low |
| **Dead Code** | Commented-out blocks in multiple files | Low |
| **I18n** | No `en.json` for English fallback | Low |
| **I18n** | Hardcoded Arabic in `wikitable.py` | Low |
| **Packaging** | No `pyproject.toml` or `setup.py` | Low |
| **Deployment** | No health check after webservice restart | Low |
| **Performance** | No concurrency for batch page processing | Low |

---

## Improvement Plan

### Quick Wins (1-2 days)
1. Add fail-fast validation in `account.py` — raise `ValueError` if credentials are empty.
2. Remove `logging.basicConfig()` from `one_page_bot.py` — let entry points configure logging.
3. Replace all `print()` calls with `logging` across the codebase.
4. Delete `templates/main copy.html`.
5. Clean up commented-out dead code.
6. Fix the README — remove reference to nonexistent `confs/` directory.
7. Extract shared `fix_value()` and session-creation utilities.

### Medium-Term Improvements (1-2 weeks)
8. Add unit tests for `petscan_bot.py`, `text_bot.py`, `make_template.py`, and `wikitable.py`.
9. Add CSRF protection via Flask-WTF.
10. Add security headers via Flask `after_request` hook.
11. Move hardcoded Arabic labels in `wikitable.py` to the I18n system.
12. Create `en.json` for English translation fallback.
13. Add `pyproject.toml` for proper Python packaging.
14. Add input validation/sanitization for PetScan parameters.

### Long-Term Refactoring (1-2 months)
15. Add async/concurrent processing for batch page operations (`asyncio` + `aiohttp`).
16. Split `WikiBot` into smaller classes: `WikiAuthenticator`, `PageEditor`.
17. Add integration tests with mocked PetScan/MediaWiki APIs.
18. Create a proper CLI using `argparse` or `click`.
19. Add a build pipeline for frontend assets (minification, cache-busting).
20. Add Content Security Policy headers.
21. Expand wiki support beyond Arabic Wikipedia/Wikisource.

---

## Comprehensive Review

| Metric | Rating | Notes |
|---|---|---|
| **Overall Project Rating** | **6 / 10** | Functional and deployed, but lacks testing and security hardening |
| **Production Readiness** | Moderate | Running on Toolforge, but no tests validate changes before deploy |
| **Technical Debt** | Medium | Code duplication, mixed logging, dead code, no tests |
| **Risk Assessment** | Low-Medium | CSRF vulnerability, credential handling edge cases, unsafe string splitting |
| **Maintainability** | **6 / 10** | Good separation of concerns, but no tests make refactoring risky |
| **Code Quality** | **6.5 / 10** | Clean modules with type hints, but inconsistent logging and duplication |
| **Security** | **5 / 10** | No CSRF, no security headers, potential XSS in JS |
| **Testability** | **3 / 10** | Zero tests; modules are structured for testability but untested |

### Sub-Project READMEs

Each subfolder has its own detailed README:

- [`PetScanList/README.md`](PetScanList/README.md) — Core package deep-dive
- [`shs/README.md`](shs/README.md) — Deployment scripts analysis
- [`I18n/README.md`](I18n/README.md) — Internationalization review
- [`static/README.md`](static/README.md) — Frontend assets review
- [`templates/README.md`](templates/README.md) — HTML templates review
