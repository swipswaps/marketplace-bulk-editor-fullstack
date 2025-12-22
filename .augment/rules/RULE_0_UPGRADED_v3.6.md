# Rule 0 Upgraded - User Request Analysis Required

**Date**: 2025-12-21  
**Version**: 3.6 (upgraded from 3.5)  
**Trigger**: User question: "why 'show screenshot size' in step 4 and not 'show screenshot in file editor'?"

---

## User Complaint That Triggered This Upgrade

> "why 'show screenshot size' in step 4 and not 'show screenshot in file editor'?"

---

## What Was Wrong

### The Problem

The assistant was showing **file size** instead of **showing the screenshot to the user**:

```bash
# WRONG - What assistant was doing
ls -lh /tmp/screenshot.png
# Output: -rw-r--r--. 1 owner owner 175K Dec 21 06:20 /tmp/screenshot.png
```

**Why this is useless:**
- User can't SEE the screenshot
- User can't VERIFY the content
- User can't confirm the test actually worked
- File size tells user nothing about what's in the screenshot

**What assistant SHOULD do:**
```bash
# CORRECT - Show screenshot to user in VSCode file editor
code /tmp/screenshot.png
```

**Why this is correct:**
- User can SEE the screenshot in VSCode
- User can VERIFY the content visually
- User can confirm the test worked
- Follows Rule 2: Evidence-Before-Assertion (user must be able to verify evidence)

---

## Root Cause

**The assistant didn't analyze the user's request step-by-step with rule citations.**

When user says: "use selenium and do ocr on the open firefox window with marketplace-bulk-editor in the title to verify"

**Assistant should have analyzed:**

1. **Step 1**: Find Firefox window → Rule 26 applies
2. **Step 2**: Take screenshot → Rule 26 applies
3. **Step 3**: Use OCR → Rule 9 applies
4. **Step 4**: Display screenshot → **Rule 2 applies** (user must SEE evidence, not just know it exists)
5. **Step 5**: Verify content → Rule 0 applies

**But assistant didn't do this analysis**, so it missed that Step 4 requires showing the screenshot to the user.

---

## What Was Added to Rule 0

### New Section: "CRITICAL: User Request Analysis"

**BEFORE executing ANY user request, the assistant MUST:**

1. **Break down the request into individual steps**
2. **For EACH step, identify which rules apply**
3. **Explain to the user which rules apply to each step**
4. **Show the planned workflow with rule citations**
5. **Ask for confirmation if any ambiguity exists**

### Example Added to Rule 0

```
User request: "use selenium and do ocr on the open firefox window with marketplace-bulk-editor in the title to verify"

Assistant MUST respond:

## Analyzing Your Request

Your request breaks down into these steps:

### Step 1: Find the open Firefox window with "marketplace-bulk-editor" in title
**Rules that apply:**
- Rule 26: Use Existing Browser Window with xdotool - Must find correct Firefox window by title
- Rule 5: Ask Don't Guess - Must list all windows and find the correct one, not guess

### Step 2: Take screenshot of that window
**Rules that apply:**
- Rule 26: Use Existing Browser Window - Must activate window and verify it's in focus
- Rule 2: Evidence-Before-Assertion - Must show screenshot to user, not just file size

### Step 3: Use OCR to read the screenshot
**Rules that apply:**
- Rule 9: OCR Verification - Must show full OCR output, not just summary
- Rule 2: Evidence-Before-Assertion - Must show actual extracted text

### Step 4: Display screenshot to user
**Rules that apply:**
- Rule 2: Evidence-Before-Assertion - User must SEE the screenshot, not just know it exists
- **CRITICAL**: Must use `code /tmp/screenshot.png` to show screenshot in VSCode file editor

### Step 5: Verify expected content
**Rules that apply:**
- Rule 0: Mandatory Workflow Pattern - Must verify compliance with OCR evidence
- Rule 2: Evidence-Before-Assertion - Must show what was found vs what was expected

Proceeding with execution...
```

---

## Updated Example in Rule 0

### Step 5: Display screenshot to user

**Rules that apply to THIS step:**
- Rule 2: Evidence-Before-Assertion - User must SEE the screenshot to verify
- Rule 26: Use Existing Browser Window - Must show screenshot to user

**Why NOT just show file size:**
- ❌ `ls -lh /tmp/after_fix.png` - Shows file exists but user can't verify content
- ✅ `code /tmp/after_fix.png` - User can SEE and VERIFY the screenshot in VSCode file editor

**Command:**
```bash
code /tmp/after_fix.png
```

**Evidence:**
Opened /tmp/after_fix.png in VSCode file editor - user can now visually verify the fix

**Rule compliance:**
- Rule 2 compliance: ✅ User can SEE the screenshot in VSCode, not just know it exists
- Rule 26 compliance: ✅ Screenshot displayed to user for visual verification

---

## Impact

### Before Upgrade (v3.5)
- ❌ Assistant didn't analyze user requests step-by-step
- ❌ Assistant didn't identify which rules apply to each step
- ❌ Assistant showed file size instead of screenshot
- ❌ User had to ask "why show screenshot size instead of showing me the screenshot?"

### After Upgrade (v3.6)
- ✅ Assistant MUST analyze user requests before executing
- ✅ Assistant MUST identify rules for each step
- ✅ Assistant MUST explain which rules apply
- ✅ Assistant will show screenshots to user (not just file size)
- ✅ User shouldn't have to ask why assistant did the wrong thing

---

## Files Modified

1. **`.augment/rules/mandatory-rules.md`**
   - Added "CRITICAL: User Request Analysis" section to Rule 0
   - Updated Step 5 example to show correct screenshot display
   - Updated version to 3.6
   - Updated description to include "USER REQUEST ANALYSIS BEFORE EXECUTION"

2. **`.augment/rules/RULE_0_UPGRADED_v3.6.md`** (this file)
   - Documents the upgrade
   - Explains user complaint
   - Shows before/after comparison

---

**This upgrade makes Rule 0 self-enforcing by requiring request analysis BEFORE execution.**

