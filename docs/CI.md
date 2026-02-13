# Continuous Integration (CI)

This repository uses GitHub Actions for continuous integration to ensure code quality and correctness.

## Workflow Overview

The CI workflow (`.github/workflows/ci.yml`) runs automatically on:
- Push to `main`, `develop`, or `copilot/**` branches
- Pull requests to `main` or `develop` branches
- Manual trigger via `workflow_dispatch`

## CI Jobs

### 1. Lint and Format Check
- **Python Version:** 3.11
- **Tools:**
  - `flake8` - Python linting to catch syntax errors and code quality issues
  - `black` - Code formatting verification
- **Purpose:** Ensures code follows Python best practices and consistent formatting

### 2. Test (Matrix)
- **Python Versions:** 3.8, 3.9, 3.10, 3.11, 3.12
- **Tools:**
  - `pytest` - Runs the test suite
  - `pytest-cov` - Generates code coverage reports
- **Purpose:** Validates functionality across all supported Python versions
- **Coverage:** Reports are uploaded to Codecov (Python 3.11 only)

### 3. Type Check
- **Python Version:** 3.11
- **Tools:**
  - `mypy` - Static type checking
- **Purpose:** Catches type-related issues early
- **Note:** Currently set to continue on error for gradual adoption

## Local Testing

You can run the same checks locally:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run linting
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --statistics

# Check formatting
black --check .

# Format code
black .

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=simulations --cov=analysis --cov-report=term

# Run type checking
mypy simulations --ignore-missing-imports --no-strict-optional
mypy analysis --ignore-missing-imports --no-strict-optional
```

## Configuration Files

- **`.github/workflows/ci.yml`** - GitHub Actions workflow definition
- **`setup.cfg`** - Flake8 configuration
- **`pyproject.toml`** - Black, pytest, and mypy configuration

## First-Time Workflow Approval

When a new workflow is added to a repository, GitHub requires manual approval for security reasons. Repository administrators will see an "Approve and run" button on the workflow run page. Once approved, subsequent runs will execute automatically.

## Status Badge

The CI status badge in the README shows the current state of the workflow:
- ✅ Green (passing) - All checks passed
- ❌ Red (failing) - One or more checks failed
- 🟡 Yellow (action required) - Workflow requires approval or action
