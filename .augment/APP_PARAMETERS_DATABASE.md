# Application Parameters Database
# CRITICAL: Read this BEFORE every action to ensure deterministic idempotency

**Last Updated**: 2025-12-22  
**Purpose**: Prevent re-learning app parameters and making the same mistakes repeatedly

---

## Port Assignments (CRITICAL - DO NOT GUESS)

### marketplace-bulk-editor
- **Frontend Port**: 5173 (when running in Docker) OR 5174 (when running with npm run dev)
- **Backend Port**: 5000
- **Local URL**: http://localhost:5173 OR http://localhost:5174
- **GitHub Pages URL**: https://swipswaps.github.io/marketplace-bulk-editor/
- **Repository**: /home/owner/Documents/694533e8-ac54-8329-bbf9-22069a0d424e/marketplace-bulk-editor

### receipts-ocr (for reference)
- **Frontend Port**: 5174 (changed from 5173 to avoid conflict)
- **Backend Port**: 5001
- **Local URL**: http://localhost:5174
- **GitHub Pages URL**: https://swipswaps.github.io/receipts-ocr/

### Port Conflict Resolution History
**Date**: 2025-12-21  
**Issue**: Both apps wanted port 5173  
**Solution**: Changed receipts-ocr to port 5174  
**Files Modified**: receipts-ocr/vite.config.ts, receipts-ocr/scripts/start.sh  

---

## Docker Containers

### marketplace-bulk-editor Containers
```bash
# Container names
marketplace-backend
marketplace-postgres
marketplace-redis

# Check status
docker ps --filter "name=marketplace-"

# Start containers
./docker-start.sh

# Stop containers
./docker-stop.sh
```

### receipts-ocr Containers (for reference)
```bash
# Container names
receipts-ocr-backend
receipts-ocr-postgres

# Port mappings
receipts-ocr-backend: 5001:5000
receipts-ocr-postgres: 5433:5432
```

---

## Authentication & Test Credentials

### Test User Credentials
**Email**: test@example.com  
**Password**: password123 OR SecurePass123!  
**Full Name**: Test User  

### JWT Token Expiry
- **Access Token**: 15 minutes
- **Refresh Token**: 7 days

### Registration Endpoint
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123!","full_name":"Test User"}'
```

### Login Endpoint
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

---

## CORS Configuration (CRITICAL)

### Backend ALLOWED_ORIGINS
**File**: backend/config.py  
**Must include**:
- http://localhost:5173
- http://localhost:5174
- https://swipswaps.github.io

**Why**: GitHub Pages (HTTPS) needs to connect to localhost backend (HTTP)

### CORS Issue History
**Date**: 2025-12-21  
**Issue**: GitHub Pages couldn't connect to backend  
**Root Cause**: Missing https://swipswaps.github.io in ALLOWED_ORIGINS  
**Solution**: Added to backend/config.py  

---

## Database Schema

### Listings Table
```sql
CREATE TABLE listings (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    title VARCHAR(150) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    condition VARCHAR(50) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    offer_shipping BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Valid CONDITION Values (Facebook Marketplace)
- "New"
- "Used - Like New"
- "Used - Good"
- "Used - Fair"

**NEVER**: "Refurbished" (invalid - must auto-fill to "Used - Like New")

---

## File Upload & Validation

### Test Files
- **test_solar_equipment_import.xlsx**: 22 listings, row 20 has "Refurbished" CONDITION
- **Location**: /home/owner/Documents/694533e8-ac54-8329-bbf9-22069a0d424e/marketplace-bulk-editor/

### Validation Modal Behavior
- **Valid rows**: All required fields filled with valid values
- **Auto-filled rows**: Empty or invalid fields auto-filled with defaults
- **Rejected rows**: Missing TITLE (required field)

### Auto-Fill Defaults
- **Empty PRICE**: $0
- **Empty CONDITION**: "New"
- **Invalid CONDITION** (e.g., "Refurbished"): "Used - Like New"

---

## API Endpoints

### Backend Base URL
- **Local**: http://localhost:5000
- **From GitHub Pages**: http://localhost:5000 (requires CORS)

### Key Endpoints
```
GET  /health                    - Health check
POST /api/auth/register         - User registration
POST /api/auth/login            - User login
POST /api/auth/refresh          - Refresh JWT token
GET  /api/auth/me               - Get current user
POST /api/listings              - Create listing
GET  /api/listings              - Get all listings
POST /api/listings/bulk         - Bulk create listings
POST /api/export/csv            - Export as CSV
POST /api/export/json           - Export as JSON
POST /api/export/xlsx           - Export as Excel
POST /api/export/sql            - Export as SQL
POST /api/export/text           - Export as tab-delimited text
POST /api/ocr/process           - Process image with PaddleOCR
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Guessing Port Numbers
**WRONG**: Assume app is on port 5173  
**CORRECT**: Check `ps aux | grep vite` or `curl http://localhost:5173` vs `curl http://localhost:5174`

### ❌ Mistake 2: Not Checking Backend Status
**WRONG**: Create Selenium test without verifying backend is running  
**CORRECT**: Check `docker ps --filter "name=marketplace-"` first

### ❌ Mistake 3: Forgetting CORS Configuration
**WRONG**: Assume GitHub Pages can connect to localhost without CORS  
**CORRECT**: Verify backend/config.py has https://swipswaps.github.io in ALLOWED_ORIGINS

### ❌ Mistake 4: Using Wrong Test Credentials
**WRONG**: Guess credentials or use random values  
**CORRECT**: Use test@example.com / password123

### ❌ Mistake 5: Not Restarting Vite After Changes
**WRONG**: Make changes and assume Vite hot-reloads everything  
**CORRECT**: Kill and restart `npm run dev` after dependency changes

---

## Selenium Testing Parameters

### Browser Configuration
```python
from selenium.webdriver.chrome.options import Options

options = Options()
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
# DO NOT use --headless unless explicitly requested

driver = webdriver.Chrome(options=options)
```

### Test URLs
- **Local**: http://localhost:5174 (check which port is actually running!)
- **GitHub Pages**: https://swipswaps.github.io/marketplace-bulk-editor/

### Screenshot Locations
- **/tmp/selenium_*.png** - Selenium screenshots
- **/tmp/screenshot_*.png** - Manual screenshots

---

## Deterministic Idempotency Checklist

**Before EVERY action, verify:**
1. ✅ Which port is the app actually running on? (5173 or 5174?)
2. ✅ Are Docker containers running? (`docker ps --filter "name=marketplace-"`)
3. ✅ Is backend accessible? (`curl http://localhost:5000/health`)
4. ✅ What are the test credentials? (test@example.com / password123)
5. ✅ What file am I testing with? (test_solar_equipment_import.xlsx)
6. ✅ What are the valid CONDITION values? (New, Used - Like New, Used - Good, Used - Fair)
7. ✅ Did I read this file BEFORE acting? (YES/NO)

**If you can't answer ALL of these, STOP and read this file again.**

---

**This database prevents:**
- ❌ Targeting wrong port
- ❌ Using wrong credentials
- ❌ Forgetting CORS configuration
- ❌ Re-learning app parameters
- ❌ Making the same mistakes repeatedly
- ❌ Wasting time on trial-and-error

**This database enables:**
- ✅ Deterministic actions (same input → same output)
- ✅ Idempotent operations (repeating action → same result)
- ✅ Faster development (no re-learning)
- ✅ Fewer mistakes (parameters documented)
- ✅ Better testing (known good values)

