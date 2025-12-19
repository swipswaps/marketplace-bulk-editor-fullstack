#!/bin/bash

# Backend Linting and Code Quality Check

echo "========================================="
echo "BACKEND CODE QUALITY CHECK"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠${NC} Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Install linting tools if not present
echo "Installing linting tools..."
pip install -q flake8 black mypy 2>/dev/null

echo ""
echo "=== 1. Code Formatting (Black) ==="
black --check . 2>&1 | head -20
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Code formatting is correct"
else
    echo -e "${YELLOW}⚠${NC} Code formatting issues found. Run: black ."
fi

echo ""
echo "=== 2. Linting (Flake8) ==="
# Critical errors only
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=venv,migrations
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} No critical errors found"
else
    echo -e "${RED}✗${NC} Critical errors found"
    exit 1
fi

# Style warnings (non-blocking)
echo ""
echo "Style warnings (non-blocking):"
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude=venv,migrations | head -10

echo ""
echo "=== 3. Type Checking (MyPy) ==="
mypy . --ignore-missing-imports --exclude venv --exclude migrations 2>&1 | head -20
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Type checking passed"
else
    echo -e "${YELLOW}⚠${NC} Type checking warnings (non-blocking)"
fi

echo ""
echo "=== 4. Import Sorting (isort check) ==="
pip install -q isort 2>/dev/null
isort --check-only . --skip venv --skip migrations 2>&1 | head -10
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Imports are sorted correctly"
else
    echo -e "${YELLOW}⚠${NC} Import sorting issues. Run: isort ."
fi

echo ""
echo "=== 5. Security Check (Bandit) ==="
pip install -q bandit 2>/dev/null
bandit -r . -ll -x venv,migrations 2>&1 | tail -20
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} No security issues found"
else
    echo -e "${YELLOW}⚠${NC} Security warnings found (review recommended)"
fi

echo ""
echo "========================================="
echo "LINT CHECK COMPLETE"
echo "========================================="
echo ""
echo "To auto-fix formatting issues:"
echo "  black ."
echo "  isort ."
echo ""
echo "To see detailed linting report:"
echo "  flake8 . --exclude=venv,migrations"
echo ""

