# Admin Credentials

**Created**: 2025-12-19  
**Purpose**: Testing and administration

---

## Admin Account

**Email**: `admin@marketplace.local`  
**Password**: `Admin123!@#`  
**Name**: Admin User  
**User ID**: `24d6eac2-1056-4f43-8adb-2408f341bf04`

---

## Usage

### Login via UI
1. Open http://localhost:5173
2. Click "Login" button
3. Enter credentials above
4. Click "Login"

### Login via API
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@marketplace.local",
    "password": "Admin123!@#"
  }'
```

---

## Features Available When Logged In

- ✅ Save to Database button
- ✅ Load from Database button
- ✅ SQL Export option
- ✅ Auto-sync every 30 seconds
- ✅ Sync status indicator
- ✅ User menu with logout

---

## Security Notes

- ⚠️ This is a **test account** for development/testing only
- ⚠️ Do NOT use in production
- ⚠️ Change password if deploying to public server
- ⚠️ Account is stored in PostgreSQL database (persists across restarts)

---

## Database Access

**PostgreSQL**:
```bash
docker exec -it marketplace-postgres psql -U marketplace_user -d marketplace_db

# View user
SELECT * FROM users WHERE email = 'admin@marketplace.local';
```

**Redis** (session data):
```bash
docker exec -it marketplace-redis redis-cli
KEYS *admin*
```

