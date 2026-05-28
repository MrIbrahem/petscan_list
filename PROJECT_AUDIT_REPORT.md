# PetScan List — Project Audit Report

> **Date:** 2026-05-27
> **Scope:** Full codebase audit — Python application, deployment scripts, frontend assets, templates, internationalization
> **Repository:** [MrIbrahem/petscan_list](https://github.com/MrIbrahem/petscan_list)

---

## Executive Summary

PetScan List is a Flask-based web application and Wikipedia bot deployed on [Wikimedia Toolforge](https://wikitech.wikimedia.org/wiki/Help:Toolforge). It automates the processing of `{{petscan list}}` templates on Wikipedia pages — querying the PetScan API, formatting results as bulleted lists or wikitables, and writing them back to wiki pages via bot credentials.

### Technology Stack

| Layer | Technology |
|---|---|
| Runtime | Python 3.11 |
| Web Framework | Flask |
| Wiki API | mwclient, pywikibot |
| Wikitext Parsing | wikitextparser |
| HTTP Client | requests |
| Frontend | Vanilla JS, CSS custom properties |
| Hosting | Wikimedia Toolforge |
| CI/CD | GitHub Actions (SSH deploy on push to `main`) |
| Scheduler | Toolforge job scheduler (`jobs.yaml`) |

### Architecture Overview

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Browser /   │────▶│  Flask App   │────▶│  PetScanList/   │
│  Bot Runner  │     │  app.py      │     │  (core package) │
└─────────────┘     │  bot.py      │     └────────┬────────┘
                    └──────────────┘              │
                         │                        ▼
                    ┌────┴─────┐          ┌───────────────┐
                    │ Jinja2   │          │ PetScan API   │
                    │ Templates│          │ MediaWiki API │
                    └──────────┘          └───────────────┘
```

The system has two entry points — a Flask web server (`app.py`) and a batch bot (`bot.py`) — both delegating to the `PetScanList` core package. Deployment is automated via GitHub Actions pushing to Toolforge over SSH, with shell scripts handling venv management, dependency installation, and service restarts.

---

## Project Health Assessment

### Overall Code Quality: **6 / 10**

The codebase is functional and reasonably organized. Each module in the `PetScanList/` package has a clear single responsibility. Type hints are present on key functions. However, inconsistent logging (mix of `print()` and `logging`), code duplication across modules, and commented-out dead code bring the score down.

### Maintainability: **6 / 10**

Modules are short (most under 130 lines) and well-separated. The flat package structure is easy to navigate. The absence of any tests is the single largest maintainability risk — refactoring without a test safety net is dangerous.

### Scalability: **5 / 10**

All processing is synchronous and sequential. Batch bot mode processes up to 3000 pages per wiki one at a time with no concurrency. PetScan API calls and MediaWiki edits are blocking. The system works for the current load (Arabic Wikipedia/Wikisource only) but would not scale to dozens of wikis or frequent runs.

### Security Posture: **5 / 10**

- No CSRF protection on POST endpoints
- No security headers (`X-Frame-Options`, `CSP`, `X-Content-Type-Options`)
- Credential loading defaults to empty strings instead of failing fast
- Potential XSS in the `tt.js` tooltip library (unverified)
- No input sanitization beyond `output_limit` on PetScan parameters

### Production Readiness: **Moderate**

The application is currently running in production on Toolforge and serving users. However, the lack of tests, security hardening, and deployment health checks means changes carry significant risk. The CI/CD pipeline deploys on every push to `main` with no test gate.

---

## Cross-Project Analysis

### Shared Architectural Patterns

1. **Two-tier architecture** — Thin entry points (`app.py`, `bot.py`) delegate to a core package. This is a sound pattern that keeps concerns separated.
2. **Facade via `__init__.py`** — The core package exports a clean public API through `__all__`, hiding internal complexity.
3. **Configuration as code** — `sites.py` and `params.py` define constants at module level rather than using external config files. Simple and effective for the current scope.
4. **Toolforge-native deployment** — Scripts use platform idioms (`webservice`, `toolforge-jobs`, `become`) correctly.

### Repeated Weaknesses

| Weakness | Occurrences | Files Affected |
|---|---|---|
| `print()` instead of `logging` | 4+ | `text_bot.py`, `pages.py`, `make_template.py` |
| `{{!}}` / `{{\|}}` replacement duplication | 3 | `text_bot.py:28`, `text_bot.py:43`, `make_template.py:58` |
| `requests.session()` created per call | 2 | `petscan_bot.py:59`, `I18n.py:14` |
| Hardcoded Arabic strings outside I18n | 1 file | `wikitable.py:5-14` |
| Commented-out dead code blocks | 3+ | `one_page_bot.py`, `text_bot.py` |
| Unquoted shell variables | 3 | `install.sh`, `runall.sh` |

### Common Technical Debt

1. **Zero test coverage** — No unit, integration, or end-to-end tests across the entire project.
2. **No Python packaging** — No `pyproject.toml` or `setup.py`. The package cannot be installed via pip.
3. **Inconsistent error handling** — Some functions return dicts with `result_text`/`result_class`, others return empty dicts, others raise exceptions. No unified error model.
4. **Dead files** — `templates/main copy.html` is a duplicate that should not be in version control.
5. **Stale documentation** — The root README references a `confs/` directory that doesn't exist.

### Dependency Issues

| Dependency | Version Pinned | Concern |
|---|---|---|
| flask | No | Could break on major version bump |
| mwclient | No | Critical for wiki editing — should be pinned |
| pywikibot | No | Heavy dependency used only for `showDiff` |
| wikitextparser | No | Core dependency — should be pinned |
| requests | No | Transitive risk |
| python-dotenv | No | Low risk but should still be pinned |

No dependency versions are pinned in `requirements.txt`. The `install.sh` script pins `pip==24.0` and `wheel==0.42.0` but these are for the pip tool itself, not the application dependencies.

### Integration Concerns

1. **PetScan API dependency** — The entire application depends on `petscan.wmflabs.org`. No caching, retry logic, or fallback exists.
2. **MediaWiki API rate limits** — No rate limiting on wiki edits. Aggressive batch runs could hit API limits.
3. **Toolforge coupling** — Shell scripts are tightly coupled to Toolforge's `webservice` and `toolforge-jobs` commands. Moving to another platform requires rewriting deployment.

---

## Critical Findings

### High-Risk Issues

#### 1. No Test Suite
**Risk:** High | **Impact:** Every code change carries regression risk

Zero tests exist. The CI/CD pipeline deploys directly to production on push to `main` with no validation gate. A single bad commit takes the service offline.

#### 2. CSRF Vulnerability on `/template` Endpoint
**Risk:** Medium-High | **Impact:** An attacker can submit forms on behalf of authenticated users

```python
# app.py line 53-67 — POST form with no CSRF token
@app.route("/template", methods=["POST", "GET"])
def template():
    url = request.form.get("url")
```

The `template_form.html` submits via POST without a CSRF token. Flask-WTF or manual token validation is missing.

#### 3. Unsafe String Splitting Can Corrupt Wiki Pages
**Risk:** Medium | **Impact:** Page content corruption

```python
# text_bot.py line 134
pet_section = text.split(template_string)[1].split(template_end_string)[0]
```

If `template_string` appears multiple times in the page text, `[1]` selects the wrong occurrence, potentially replacing the wrong section of the page.

### Security Vulnerabilities

| # | Vulnerability | Severity | Location |
|---|---|---|---|
| 1 | No CSRF on POST forms | Medium-High | `app.py:53`, `templates/template_form.html` |
| 2 | No security headers | Medium | `app.py` (no `after_request` handler) |
| 3 | Credential fail-silent (empty defaults) | Medium | `account.py:9-10` |
| 4 | No input sanitization on PetScan params | Medium | `petscan_bot.py:28-40` |
| 5 | Potential XSS in tooltip rendering | Low-Medium | `static/tt.js` (needs audit) |
| 6 | Logging `sys.argv` could leak secrets | Low | `one_page_bot.py:51` |

### Performance Bottlenecks

1. **Sequential page processing** — `one_page_bot.py:133-138` processes pages one at a time in a loop. For 3000 pages, this takes hours.
2. **No HTTP session reuse** — `requests.session()` is created per API call in `petscan_bot.py` and `I18n.py` instead of being shared.
3. **No PetScan result caching** — The same PetScan query could be made multiple times within a single bot run.
4. **Synchronous Flask** — The web app uses Flask's built-in development server in production (via `app.run()`), which is single-threaded.

### Stability Concerns

1. **`logging.basicConfig()` at import time** (`one_page_bot.py:11`) — Overrides the caller's logging configuration, including Flask's.
2. **No graceful shutdown** — The bot has no signal handling; interrupting it mid-run leaves pages partially processed.
3. **No retry logic** — PetScan API or MediaWiki API failures are logged and silently skipped with no retry.

### Missing Infrastructure

| Item | Status | Impact |
|---|---|---|
| Test suite | Missing | Cannot validate changes |
| `pyproject.toml` | Missing | Cannot install as a package |
| Dependency pinning | Missing | Builds are not reproducible |
| Health check endpoint | Missing | No way to verify service status |
| Structured logging | Missing | Difficult to monitor in production |
| Error tracking (Sentry, etc.) | Missing | Silent failures go unnoticed |
| Rate limiting | Missing | Could hit API limits during batch runs |

---

## Strengths

### 1. Clean Module Separation
The `PetScanList/` package is well-organized. Each module has a single responsibility: `petscan_bot.py` handles the API, `text_bot.py` handles wikitext, `one_page_bot.py` handles wiki editing, `wikitable.py` handles table generation. This makes the codebase navigable and each module independently understandable.

### 2. Explicit Public API
`PetScanList/__init__.py` uses `__all__` to define a clean export surface. Consumers import from the package level without needing to know internal module names. This is a textbook Python packaging pattern.

### 3. Defensive Error Handling
`petscan_bot.py` catches specific `requests` exception types (`HTTPError`, `ConnectionError`, `Timeout`, `RequestException`) rather than using bare `except`. `one_page_bot.py` handles `mwclient.errors.LoginError` and `PageError` distinctly.

### 4. User-Agent Compliance
All HTTP requests include a proper `User-Agent` header with tool name, URL, and contact email. This is required by Wikimedia's API etiquette policy and shows attention to platform requirements.

### 5. Backup-on-Deploy with Rollback
`update.sh` creates timestamped backups before every deployment and automatically restores the backup if `git clone` fails. This is a robust deployment pattern that prevents broken deploys from taking the service offline.

### 6. Dual Output Modes
The template system supports both bulleted lists and wikitables via the `_result_=table` parameter, with customizable line formats. This flexibility serves different wiki community preferences.

### 7. Lua Companion Module
`petscan.lua` provides server-side PetScan URL generation within MediaWiki's Scribunto framework. This reduces client-side dependencies and allows the template to generate URLs without the Python backend.

### 8. CI/CD Pipeline
GitHub Actions automatically deploys to Toolforge on push to `main`. The pipeline handles SSH authentication, source updates, dependency installation, and service restarts in a single workflow.

---

## Improvement Roadmap

### Immediate Fixes (1-3 days)

| # | Action | Effort | Risk Reduced |
|---|---|---|---|
| 1 | Add fail-fast in `account.py` — raise `ValueError` if credentials are empty | 30 min | Credential confusion |
| 2 | Remove `logging.basicConfig()` from `one_page_bot.py` | 15 min | Logging conflicts |
| 3 | Replace all `print()` with `logging` | 1-2 hrs | Observability |
| 4 | Delete `templates/main copy.html` | 1 min | Repository hygiene |
| 5 | Clean up commented-out dead code | 30 min | Readability |
| 6 | Fix README — remove reference to nonexistent `confs/` | 15 min | Documentation accuracy |
| 7 | Quote all shell variable expansions in `shs/` | 30 min | Deployment reliability |

### Short-Term Improvements (1-2 weeks)

| # | Action | Effort | Benefit |
|---|---|---|---|
| 8 | Add unit tests for `petscan_bot.py`, `text_bot.py`, `make_template.py`, `wikitable.py` | 3-5 days | Regression safety |
| 9 | Add CSRF protection via Flask-WTF | 2-3 hrs | Security |
| 10 | Add security headers (`X-Frame-Options`, `CSP`, `X-Content-Type-Options`) | 1 hr | Security |
| 11 | Pin dependency versions in `requirements.txt` | 30 min | Build reproducibility |
| 12 | Extract shared `fix_value()` and session utilities | 2-3 hrs | Code deduplication |
| 13 | Create `I18n/en.json` for English fallback | 30 min | I18n completeness |
| 14 | Move hardcoded Arabic labels in `wikitable.py` to I18n | 1 hr | Internationalization |
| 15 | Add `pyproject.toml` for proper packaging | 1 hr | Installability |

### Long-Term Strategic Refactoring (1-3 months)

| # | Action | Effort | Benefit |
|---|---|---|---|
| 16 | Add async/concurrent batch processing (`asyncio` + `aiohttp`) | 1-2 weeks | Performance (10-50x faster batch runs) |
| 17 | Split `WikiBot` into `WikiAuthenticator` + `PageEditor` | 3-5 days | Maintainability |
| 18 | Add integration tests with mocked APIs | 1 week | Confidence in changes |
| 19 | Build a proper CLI with `click` or `argparse` | 2-3 days | Developer experience |
| 20 | Add PetScan result caching (TTL-based) | 2-3 days | Performance, API courtesy |
| 21 | Implement structured logging (JSON format) | 1-2 days | Production monitoring |
| 22 | Add retry logic with exponential backoff for API calls | 1-2 days | Reliability |
| 23 | Add a `/health` endpoint | 30 min | Deployment validation |

### Security Hardening Priorities

| Priority | Action |
|---|---|
| **P0** | Add CSRF tokens to all POST forms |
| **P0** | Fail-fast on missing credentials |
| **P1** | Add security response headers |
| **P1** | Audit `tt.js` for XSS vulnerabilities |
| **P1** | Sanitize PetScan query parameters |
| **P2** | Add Content Security Policy |
| **P2** | Review `sys.argv` logging for secret leakage |

### DevOps and Testing Recommendations

1. **Add a test gate to CI** — Run `pytest` before deploying. A failing test should block the deploy.
2. **Pin Python version** — Add `.python-version` or `runtime.txt` for Toolforge.
3. **Add a health check** — The `update.sh` script should curl the service after restart to verify it's responding.
4. **Add dependency vulnerability scanning** — Use `pip-audit` or Dependabot.
5. **Add a staging environment** — Test changes on a non-production Toolforge instance before deploying to the live service.

---

## Final Evaluation

| Metric | Score | Notes |
|---|---|---|
| **Overall Project Score** | **6.0 / 10** | Functional and deployed, but significant gaps in testing, security, and tooling |
| **Risk Level** | **Medium** | No tests + auto-deploy = high regression risk; CSRF and string-splitting bugs present |
| **Technical Debt Level** | **Medium** | Code duplication, dead code, inconsistent patterns, no packaging |
| **Production Readiness** | **65%** | Currently serving users on Toolforge, but fragile — no test gate, no health checks, no monitoring |
| **Code Quality** | **6.5 / 10** | Good module separation and type hints, undermined by mixed logging and duplication |
| **Security Posture** | **5.0 / 10** | Missing CSRF, security headers, input validation; credential handling needs hardening |
| **Testability** | **3.0 / 10** | Modules are structured for testability but have zero actual tests |

### Summary Verdict

The PetScan List project is a **working, deployed tool** that serves its purpose well for the Arabic Wikipedia community. The architecture is sound — clean module separation, a proper facade API, and sensible use of platform-native deployment patterns. The deployment pipeline with backup-and-rollback is a particular strength.

However, the project carries significant risk due to the **complete absence of tests** combined with **automatic deployment on every push**. A single bad commit takes the service offline with no automated detection. Security gaps (CSRF, headers, input validation) need addressing before the project can be considered hardened.

The codebase is well-positioned for improvement. The modular structure makes it straightforward to add tests, extract shared utilities, and introduce concurrency. The recommended immediate fixes (7 items, ~1 day of work) would meaningfully reduce risk. The short-term improvements (8 items, 1-2 weeks) would bring the project to a solid production-ready state.

### Recommended Next Steps

1. **Today:** Implement the 7 immediate fixes listed above.
2. **This week:** Add a test suite for the 4 core modules and add CSRF protection.
3. **This month:** Pin dependencies, add security headers, create `pyproject.toml`, and set up a test gate in CI.
4. **This quarter:** Add async batch processing, split the `WikiBot` class, and implement structured logging with monitoring.
