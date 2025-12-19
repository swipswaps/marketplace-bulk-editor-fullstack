#!/bin/bash

# Marketplace Bulk Editor - Implementation Verification Script

echo "========================================="
echo "MARKETPLACE BULK EDITOR"
echo "Implementation Verification"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TOTAL=0
PASSED=0
FAILED=0

check_file() {
    TOTAL=$((TOTAL + 1))
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗${NC} $1 (MISSING)"
        FAILED=$((FAILED + 1))
    fi
}

check_dir() {
    TOTAL=$((TOTAL + 1))
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗${NC} $1/ (MISSING)"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== Backend Structure ==="
check_dir "backend"
check_dir "backend/models"
check_dir "backend/routes"
check_dir "backend/schemas"
check_dir "backend/utils"
check_dir "backend/tests"

echo ""
echo "=== Core Files ==="
check_file "backend/app.py"
check_file "backend/config.py"
check_file "backend/requirements.txt"
check_file "backend/Dockerfile"
check_file "backend/.env.example"
check_file "backend/init_db.py"
check_file "backend/test_api.py"
check_file "backend/run.sh"

echo ""
echo "=== Database Models ==="
check_file "backend/models/__init__.py"
check_file "backend/models/user.py"
check_file "backend/models/listing.py"
check_file "backend/models/template.py"
check_file "backend/models/ocr_scan.py"
check_file "backend/models/audit_log.py"

echo ""
echo "=== API Routes ==="
check_file "backend/routes/__init__.py"
check_file "backend/routes/auth.py"
check_file "backend/routes/listings.py"
check_file "backend/routes/templates.py"
check_file "backend/routes/ocr.py"
check_file "backend/routes/export.py"

echo ""
echo "=== Validation Schemas ==="
check_file "backend/schemas/__init__.py"
check_file "backend/schemas/user_schema.py"
check_file "backend/schemas/listing_schema.py"
check_file "backend/schemas/template_schema.py"
check_file "backend/schemas/ocr_schema.py"

echo ""
echo "=== Utilities ==="
check_file "backend/utils/__init__.py"
check_file "backend/utils/auth.py"
check_file "backend/utils/file_upload.py"
check_file "backend/utils/audit.py"

echo ""
echo "=== Tests ==="
check_file "backend/tests/__init__.py"
check_file "backend/tests/conftest.py"
check_file "backend/tests/test_auth.py"
check_file "backend/tests/test_listings.py"
check_file "backend/tests/test_export.py"
check_file "backend/pytest.ini"

echo ""
echo "=== Docker Configuration ==="
check_file "docker-compose.yml"
check_file "Dockerfile.frontend"

echo ""
echo "=== Documentation ==="
check_file "backend/README.md"
check_file "backend/tests/README.md"
check_file "IMPROVEMENT_PLAN.md"
check_file "PHASE_1_PROGRESS.md"
check_file "BACKEND_IMPLEMENTATION_COMPLETE.md"
check_file "DEVELOPER_QUICKSTART.md"

echo ""
echo "=== CI/CD ==="
check_file ".github/workflows/backend-tests.yml"

echo ""
echo "========================================="
echo "VERIFICATION RESULTS"
echo "========================================="
echo -e "Total Checks: ${TOTAL}"
echo -e "${GREEN}Passed: ${PASSED}${NC}"
echo -e "${RED}Failed: ${FAILED}${NC}"

if [ $FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ ALL CHECKS PASSED!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. cd backend && ./run.sh"
    echo "2. python backend/test_api.py"
    echo "3. docker-compose up -d"
    exit 0
else
    echo ""
    echo -e "${RED}✗ SOME CHECKS FAILED${NC}"
    echo "Please review missing files above."
    exit 1
fi

