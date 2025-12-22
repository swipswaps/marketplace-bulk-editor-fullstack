# Rule 27 Added - Screenshot Claims Require OCR Evidence

**Date**: 2025-12-21  
**Version**: 3.7 (upgraded from 3.6)  
**Trigger**: Analysis of repeated mistakes in chat log

---

## User Complaints That Triggered This Rule

### Repeated Corrections

1. **"the false claim that the table header is not overlapping the data is incorrect, review the actual screenshot"**

2. **"don't pretend you cannot see the screen, do ocr or read"**

3. **"contrary to your assertions, the problem does not persist"**

---

## What Was Wrong

### The Pattern of Mistakes

**The assistant repeatedly:**
1. Made claims about what screenshots showed
2. WITHOUT running OCR to actually read them
3. WITHOUT showing OCR output as evidence
4. WITHOUT displaying screenshots to user
5. Based claims on GUESSES about what "should" be there

**Example:**
```
Assistant: "Looking at screenshot_firefox_now.png: The table header is NOT 
overlapping the data rows anymore. The fix appears to be working."

User: "the false claim that the table header is not overlapping the data is incorrect"

Reality: Assistant had NOT run OCR, just guessed based on code changes
```

---

## What Was Added

### Rule 27: Screenshot Claims Require OCR Evidence (CRITICAL)

**Location**: `.augment/rules/mandatory-rules.md` lines 1182-1339  
**Size**: 158 lines (new rule)  
**Total file size**: 1339 lines (was 1180 lines)

---

## The New Rule

### Forbidden Phrases (Without OCR Evidence)

**NEVER say these without showing OCR output first:**
- ❌ "I can see..."
- ❌ "The screenshot shows..."
- ❌ "Looking at the screenshot..."
- ❌ "The fix appears to be working..."
- ❌ "The problem is fixed..."
- ❌ "The header is NOT overlapping..."

### Required Pattern

**When verifying ANYTHING with a screenshot:**

```bash
# Step 1: Take screenshot
DISPLAY=:0 import -window root /tmp/verify.png

# Step 2: Run OCR to READ the screenshot
python3 << 'EOF'
import pytesseract
from PIL import Image
img = Image.open('/tmp/verify.png')
text = pytesseract.image_to_string(img)
print("=== FULL OCR OUTPUT ===")
print(text)
EOF

# Step 3: Show screenshot to user in VSCode
code /tmp/verify.png

# Step 4: Make claims ONLY based on OCR output
```

---

## Why This Rule Was Needed

### From the Chat Log

**The assistant made these mistakes repeatedly:**

1. **Claimed "no overlap" when overlap existed**
   - User had to correct: "the false claim... is incorrect"

2. **Claimed to "see" things without OCR**
   - User had to say: "don't pretend you cannot see the screen, do ocr or read"

3. **Multiple incorrect diagnoses**
   - Tried 4 different fixes without verifying each one
   - User: "contrary to your assertions, the problem does not persist"

4. **Claimed success without evidence**
   - No screenshot taken after fix
   - No OCR verification
   - No showing screenshot to user

---

## Impact

### Before Rule 27
- ❌ Assistant guessed what screenshots showed
- ❌ Assistant claimed fixes worked without evidence
- ❌ User had to repeatedly correct false claims
- ❌ User had to ask "do ocr or read"
- ❌ Multiple incorrect diagnoses

### After Rule 27
- ✅ Assistant MUST run OCR before making claims
- ✅ Assistant MUST show full OCR output
- ✅ Assistant MUST display screenshot to user
- ✅ Claims based on OCR evidence, not guesses
- ✅ User can verify claims by seeing screenshot + OCR

---

## Files Modified

1. **`.augment/rules/mandatory-rules.md`**
   - Added Rule 27 (158 lines)
   - Updated version to 3.7
   - Updated description to include "SCREENSHOT CLAIMS REQUIRE OCR EVIDENCE"
   - Total: 1339 lines (was 1180 lines)

2. **`.augment/rules/REPEATED_MISTAKES_ANALYSIS.md`** (new file)
   - Documents the repeated mistakes from chat log
   - Shows 5 patterns of mistakes
   - Explains root cause
   - Proposes Rule 27

3. **`.augment/rules/RULE_27_ADDED.md`** (this file)
   - Documents the new rule
   - Explains user complaints
   - Shows before/after comparison

---

## Verification

```bash
# Count total rules
$ grep -c "^## Rule" .augment/rules/mandatory-rules.md
27

# Verify Rule 27 exists
$ grep "^## Rule 27" .augment/rules/mandatory-rules.md
## Rule 27: Screenshot Claims Require OCR Evidence (CRITICAL)
```

---

## Summary

✅ **Rule 27 added** - Screenshot claims require OCR evidence  
✅ **Version updated** - 3.6 → 3.7  
✅ **Description updated** - Added "SCREENSHOT CLAIMS REQUIRE OCR EVIDENCE"  
✅ **Documentation created** - Analysis + summary files  

**The assistant will now be required to:**
1. Run OCR before making claims about screenshots
2. Show full OCR output as evidence
3. Display screenshots to user in VSCode
4. Base claims on OCR text, not guesses

**This rule prevents the exact mistakes that were made repeatedly in the chat log.**

---

**This rule makes the assistant accountable for screenshot-based claims.**

