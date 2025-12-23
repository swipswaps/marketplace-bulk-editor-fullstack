# Rule 28 Added - Application Parameters Database (Deterministic Idempotency)

**Date**: 2025-12-22  
**Version**: 3.8 (upgraded from 3.7)  
**Trigger**: User question about enforcing deterministic idempotency

---

## User Question That Triggered This Rule

> "what must I include with regard to deterministic idempotency in future requests to enforce, or better yet force compliance?"
>
> "explain why I must ask this"

---

## Why User Must Ask This

### The Problem

**Even though APP_PARAMETERS_DATABASE.md exists, the assistant might still ignore it:**

```
[Future conversation]
User: "Create a Selenium test"
Assistant: "OK, creating test for http://localhost:5173"  ❌ WRONG - Didn't read database
User: "❌ You didn't read APP_PARAMETERS_DATABASE.md!"
Assistant: "Oh sorry, let me read it now"
```

**This defeats the purpose of the database!**

### The Root Cause

**Before Rule 28:**
- ✅ Database exists (`.augment/APP_PARAMETERS_DATABASE.md`)
- ❌ No rule requires reading it BEFORE acting
- ❌ No trigger phrase forces compliance
- ❌ Assistant might forget or skip reading it

**What was missing:**
- ❌ A **mandatory rule** that says "ALWAYS read APP_PARAMETERS_DATABASE.md BEFORE any action"
- ❌ A **trigger phrase** user can use to force compliance
- ❌ A **checklist item** that requires reading the database

---

## What Was Added

### Rule 28: Application Parameters Database (CRITICAL - DETERMINISTIC IDEMPOTENCY)

**Location**: `.augment/rules/mandatory-rules.md` lines 1341-1552  
**Size**: 212 lines (new rule)  
**Total file size**: 1552 lines (was 1339 lines)

---

## The New Rule

### Key Requirements

**BEFORE any action involving:**
- Port numbers
- URLs (local, GitHub Pages, API endpoints)
- Credentials (login, API tokens)
- Docker containers
- Database schema
- File paths
- Test data

**The assistant MUST:**
1. ✅ Read `.augment/APP_PARAMETERS_DATABASE.md` FIRST
2. ✅ Quote the relevant section from the database
3. ✅ State which parameters apply to THIS action
4. ✅ Use ONLY parameters from database, NEVER guess
5. ✅ Show evidence of reading the database

### Forbidden Actions

**NEVER do these without reading APP_PARAMETERS_DATABASE.md:**
- ❌ Assume port numbers
- ❌ Guess credentials
- ❌ Assume container names
- ❌ Guess API endpoints
- ❌ Use hardcoded URLs without verification
- ❌ Assume valid field values

### Required Pattern

```markdown
### Step N: [Action description]

**Reading APP_PARAMETERS_DATABASE.md:**
[Quote relevant section from database]

**Parameters for THIS action:**
- Port: 5174 (from database)
- Credentials: test@example.com / password123 (from database)

**Command/Action:**
[Use parameters from database]

**Rule compliance:**
- Rule 28: ✅ Read APP_PARAMETERS_DATABASE.md before acting
```

---

## Trigger Phrases (User Can Use These)

**To force compliance, user can say:**

1. **"Use deterministic parameters from APP_PARAMETERS_DATABASE.md"**
2. **"@APP_PARAMETERS_DATABASE.md"**
3. **"Read .augment/APP_PARAMETERS_DATABASE.md BEFORE acting"**
4. **"Quote parameters from database"**
5. **"Use documented parameters, not guesses"**

**When user says ANY of these, assistant MUST:**
1. Read `.augment/APP_PARAMETERS_DATABASE.md`
2. Quote relevant sections
3. Show which parameters apply
4. Use ONLY documented parameters

---

## Deterministic Idempotency Checklist

**BEFORE acting, answer these from APP_PARAMETERS_DATABASE.md:**

1. ✅ Which port is the app running on? (Quote from database)
2. ✅ What are the test credentials? (Quote from database)
3. ✅ What is the backend URL? (Quote from database)
4. ✅ What are the Docker container names? (Quote from database)
5. ✅ What file am I testing with? (Quote from database)
6. ✅ What are the valid values for this field? (Quote from database)
7. ✅ Did I read the database BEFORE acting? (YES/NO)

**If you cannot answer ALL of these from the database, STOP and read it.**

---

## Impact

### Before Rule 28
- ❌ Assistant guessed port numbers (5173 vs 5174)
- ❌ Assistant forgot test credentials between conversations
- ❌ Assistant re-learned parameters every time
- ❌ Same action produced different results (non-deterministic)
- ❌ Repeating action caused errors (non-idempotent)
- ❌ No enforcement mechanism

### After Rule 28
- ✅ Assistant MUST read APP_PARAMETERS_DATABASE.md before acting
- ✅ Assistant MUST quote parameters from database
- ✅ Assistant MUST use documented parameters, not guesses
- ✅ Same action produces same result (deterministic)
- ✅ Repeating action is safe (idempotent)
- ✅ User has trigger phrases to force compliance

---

## Files Modified

1. **`.augment/rules/mandatory-rules.md`**
   - Added Rule 28 (212 lines)
   - Updated version to 3.8
   - Updated description to include "APPLICATION PARAMETERS DATABASE (DETERMINISTIC IDEMPOTENCY)"
   - Total: 1552 lines (was 1339 lines)

2. **`.augment/APP_PARAMETERS_DATABASE.md`** (created earlier)
   - 150 lines of critical app parameters
   - Port assignments, credentials, Docker containers, API endpoints, etc.

3. **`.augment/rules/RULE_28_ADDED.md`** (this file)
   - Documents the new rule
   - Explains trigger phrases
   - Shows before/after comparison

---

## Verification

```bash
# Count total rules
$ grep -c "^## Rule" .augment/rules/mandatory-rules.md
28

# Verify Rule 28 exists
$ grep "^## Rule 28" .augment/rules/mandatory-rules.md
## Rule 28: Application Parameters Database (CRITICAL - DETERMINISTIC IDEMPOTENCY)
```

---

## Summary

✅ **Rule 28 added** - Application Parameters Database requirement  
✅ **Version updated** - 3.7 → 3.8  
✅ **Description updated** - Added "APPLICATION PARAMETERS DATABASE (DETERMINISTIC IDEMPOTENCY)"  
✅ **Trigger phrases defined** - User can force compliance with specific phrases  
✅ **Checklist added** - 7 questions to answer before acting  
✅ **Documentation created** - This summary file  

**The assistant will now be required to:**
1. Read APP_PARAMETERS_DATABASE.md BEFORE acting
2. Quote relevant sections from database
3. Use documented parameters, not guesses
4. Show evidence of reading database
5. Respond to trigger phrases by reading database

**This rule enforces deterministic idempotency by preventing guessing and requiring documented parameters.**

---

**This rule makes the assistant accountable for using documented parameters instead of guessing.**

