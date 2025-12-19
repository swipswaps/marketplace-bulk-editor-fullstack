#!/bin/bash

# Pre-flight check before running the backend

echo "========================================="
echo "BACKEND PRE-FLIGHT CHECK"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# 1. Check Python version
echo "=== 1. Python Version ==="
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"
if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 11) else 1)'; then
    echo -e "${GREEN}✓${NC} Python 3.11+ detected"
else
    echo -e "${RED}✗${NC} Python 3.11+ required"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo "=== 2. Required Files ==="
REQUIRED_FILES=(
    "app.py"
    "config.py"
    "requirements.txt"
    ".env.example"
    "models/__init__.py"
    "routes/__init__.py"
    "schemas/__init__.py"
    "utils/__init__.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file (MISSING)"
        ERRORS=$((ERRORS + 1))
    fi
done

echo ""
echo "=== 3. Environment Configuration ==="
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} .env file exists"
else
    echo -e "${YELLOW}⚠${NC} .env file not found (will copy from .env.example)"
    cp .env.example .env
fi

echo ""
echo "=== 4. Virtual Environment ==="
if [ -d "venv" ]; then
    echo -e "${GREEN}✓${NC} Virtual environment exists"
else
    echo -e "${YELLOW}⚠${NC} Virtual environment not found (will be created)"
fi

echo ""
echo "=== 5. Code Quality Check ==="
echo "Running linter..."
if [ -f "lint.sh" ]; then
    chmod +x lint.sh
    ./lint.sh
else
    echo -e "${YELLOW}⚠${NC} lint.sh not found, skipping code quality check"
fi

echo ""
echo "========================================="
echo "PRE-FLIGHT CHECK RESULTS"
echo "========================================="

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ ALL CHECKS PASSED${NC}"
    echo ""
    echo "Ready to start backend!"
    echo "Run: ./run.sh"
    exit 0
else
    echo -e "${RED}✗ $ERRORS ERROR(S) FOUND${NC}"
    echo ""
    echo "Please fix errors before running backend."
    exit 1
fi

