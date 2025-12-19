# Backend Linting and Code Quality Guide

## Quick Start

### Option 1: Run with Pre-flight Checks (Recommended)

```bash
cd backend
./run.sh
```

This will automatically:
1. ✅ Check Python version
2. ✅ Verify required files exist
3. ✅ Run code quality checks (linting)
4. ✅ Start the backend server

### Option 2: Skip Pre-flight Checks

```bash
cd backend
./run.sh --skip-checks
```

Use this if you want to start quickly without linting.

### Option 3: Run Linting Only

```bash
cd backend
chmod +x lint.sh
./lint.sh
```

---

## Linting Tools

### 1. Black (Code Formatting)

**Check formatting:**
```bash
black --check .
```

**Auto-fix formatting:**
```bash
black .
```

### 2. Flake8 (Linting)

**Check for errors:**
```bash
flake8 . --exclude=venv,migrations
```

**Critical errors only:**
```bash
flake8 . --select=E9,F63,F7,F82 --exclude=venv,migrations
```

### 3. MyPy (Type Checking)

**Check types:**
```bash
mypy . --ignore-missing-imports --exclude venv
```

### 4. isort (Import Sorting)

**Check import order:**
```bash
isort --check-only . --skip venv
```

**Auto-fix imports:**
```bash
isort . --skip venv
```

### 5. Bandit (Security Scanning)

**Check for security issues:**
```bash
bandit -r . -ll -x venv,migrations
```

---

## Common Issues and Fixes

### Issue: "Code formatting issues found"

**Fix:**
```bash
black .
```

### Issue: "Import sorting issues"

**Fix:**
```bash
isort .
```

### Issue: "Flake8 errors"

**Common fixes:**
- Remove unused imports
- Fix line length (max 127 characters)
- Add blank lines between functions
- Remove trailing whitespace

### Issue: "Type checking warnings"

**Fix:**
Add type hints to functions:
```python
def my_function(name: str) -> dict:
    return {"name": name}
```

---

## Pre-commit Hook (Optional)

To automatically run linting before each commit:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
EOF

# Install hooks
pre-commit install
```

---

## CI/CD Integration

Linting runs automatically on GitHub Actions:

- **On**: Push to main/develop, Pull Requests
- **Checks**: Black, Flake8, MyPy, Bandit
- **See**: `.github/workflows/backend-tests.yml`

---

## Recommended Workflow

### Before Starting Development

```bash
cd backend
./run.sh  # Runs pre-flight checks + starts server
```

### During Development

```bash
# Auto-fix formatting
black .
isort .

# Check for errors
flake8 . --exclude=venv
```

### Before Committing

```bash
# Run full lint check
./lint.sh

# If all passes, commit
git add .
git commit -m "Your message"
```

---

## Configuration Files

### pyproject.toml (Black configuration)

```toml
[tool.black]
line-length = 127
target-version = ['py311']
exclude = '''
/(
    \.git
  | \.venv
  | venv
  | migrations
)/
'''
```

### .flake8 (Flake8 configuration)

```ini
[flake8]
max-line-length = 127
exclude = venv,migrations,.git,__pycache__
ignore = E203,W503
```

### setup.cfg (isort configuration)

```ini
[isort]
profile = black
line_length = 127
skip = venv,migrations
```

---

## Summary

**Before running backend:**
```bash
./run.sh  # Includes pre-flight checks
```

**To skip checks:**
```bash
./run.sh --skip-checks
```

**To run linting only:**
```bash
./lint.sh
```

**To auto-fix most issues:**
```bash
black .
isort .
```

