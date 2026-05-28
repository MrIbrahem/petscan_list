# shs — Shell Scripts (Operations & Deployment)

## Project Overview

The `shs/` directory contains shell scripts for deploying, updating, and operating the PetScan List application on [Wikimedia Toolforge](https://wikitech.wikimedia.org/wiki/Help:Toolforge). These scripts handle the full lifecycle: initial installation, dependency management, daily batch runs, and live updates.

### Files

| Script | Purpose |
|---|---|
| `install.sh` | One-time initial setup — creates venv, clones repo, installs deps, starts webservice |
| `pip.sh` | Dependency refresh — upgrades pip and reinstalls requirements |
| `runall.sh` | Daily job — activates venv and runs `bot.py` for batch processing |
| `update.sh` | Live update — backs up current source, pulls latest code, reinstalls deps, restarts webservice |

### Technologies

- **Bash** (strict mode: `set -euo pipefail`)
- **Toolforge CLI** (`webservice`, `toolforge-jobs`)
- **Python 3.11** virtual environment
- **Git** for source deployment

---

## Architecture & Code Quality Review

### Code Organization

Scripts follow a logical separation: `install.sh` for bootstrap, `update.sh` for deployments, `pip.sh` for dependency management, and `runall.sh` for scheduled execution. Each script is self-contained and can be run independently.

### Design Patterns

- **Backup-before-update**: `update.sh` creates timestamped backups before overwriting source.
- **Fail-safe rollback**: If `git clone` fails in `update.sh`, the backup is restored.
- **Strict mode**: All scripts use `set -euo pipefail` (except `runall.sh` which uses `set -e` only).

### Maintainability

- Scripts are short (6–35 lines each) and easy to understand.
- Environment paths are consistent (`$HOME/www/python/`).

### Readability

- Clear variable naming (`backup_dir`, `REPO_URL`, `REPO_BRANCH`).
- Minimal comments — the scripts are simple enough to be self-documenting.

---

## Strengths

1. **Backup strategy** — `update.sh` creates timestamped backups before every deployment.
2. **Rollback on failure** — If clone fails, the previous version is restored automatically.
3. **Configurable repository** — `REPO_URL` and `REPO_BRANCH` are configurable via environment variables with sensible defaults.
4. **Strict error handling** — `set -euo pipefail` prevents silent failures.
5. **Toolforge-native** — Uses the platform's job scheduler and webservice management correctly.

---

## Weaknesses

### 1. Inconsistent Strict Mode
`runall.sh` uses only `set -e` while the others use `set -euo pipefail`. This means unset variable references won't fail in `runall.sh`.

### 2. Hardcoded Python Version
All scripts reference `python3.11` directly. Upgrading the Python version requires editing every script.

### 3. No Logging
Scripts produce no log output beyond what the commands themselves print. No timestamps, no script names, no status messages.

### 4. Unquoted Variables
Several variables are used without quotes:
- `install.sh:12`: `pip install -r $HOME/www/python/src/requirements.txt`
- `runall.sh:6`: `python3 $HOME/www/python/src/bot.py`
- `pip.sh:10`: `pip install -r "$HOME/www/python/src/requirements.txt"` (this one is quoted — inconsistent)

Paths with spaces would break these scripts.

---

## Critical Issues

### 1. Destructive `rm -rf` in `install.sh` (High)
```bash
rm -rf www/python
```
This deletes the entire `www/python` directory unconditionally during installation. If run accidentally on a production system, it destroys the live deployment with no confirmation prompt.

### 2. No Validation Before Restart (Medium)
`update.sh` runs `webservice python3.11 restart` without verifying that the new code is valid or that dependencies installed successfully. A broken deployment goes live immediately.

### 3. Missing `set -u` in `runall.sh` (Low)
Without `set -u`, unset variables silently expand to empty strings, which could cause `bot.py` to run with unexpected behavior.

---

## Areas That Need Attention

- **No deployment health check** — After restart, there's no verification that the service is responding.
- **No log rotation** — Bot output goes to stdout with no log management.
- **No version pinning** — `pip.sh` upgrades pip but doesn't pin dependency versions.
- **Missing `set -u` and `set -o pipefail`** in `runall.sh`.
- **No dry-run mode** — `update.sh` has no way to preview changes before applying them.

---

## Improvement Plan

### Quick Wins
1. Add `set -euo pipefail` to `runall.sh` for consistency.
2. Quote all variable expansions: `"$HOME/www/python/src/requirements.txt"`.
3. Add `echo` status messages with timestamps to each script.
4. Extract `PYTHON_VERSION=python3.11` as a variable at the top of each script.

### Medium-Term Improvements
5. Add a health check after `webservice restart` (e.g., curl the endpoint).
6. Add a confirmation prompt or `--force` flag to `install.sh`'s `rm -rf`.
7. Add `--dry-run` support to `update.sh`.

### Long-Term Recommendations
8. Migrate to a CI/CD pipeline that runs tests before deployment (partially done via GitHub Actions).
9. Add rollback capability that can be triggered manually.
10. Add structured logging to capture deployment status.

---

## Comprehensive Review

| Metric | Score | Notes |
|---|---|---|
| **Overall Rating** | **6 / 10** | Functional deployment scripts with good backup strategy, but lacking safety checks |
| **Production Readiness** | Moderate | Currently running in production on Toolforge |
| **Technical Debt** | Low | Scripts are small and straightforward |
| **Risk Assessment** | Medium | `rm -rf` and lack of post-deploy validation are the main risks |
| **Maintainability** | 7 / 10 | Simple scripts, easy to modify |
