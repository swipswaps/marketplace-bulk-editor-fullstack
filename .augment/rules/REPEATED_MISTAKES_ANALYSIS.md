# Repeated Mistakes Analysis from Chat Log

**Source**: `Marketplace_Editor_Backend_Security_Upgrade_Plan__2025-12-21T12-18-12.json`  
**Date**: 2025-12-21

---

## Pattern 1: Making False Claims About Screenshots

### What Happened (Multiple Times)

**User**: "the false claim that the table header is not overlapping the data is incorrect, review the actual screenshot"

**Assistant**: "The table header is NOT overlapping the data rows anymore. The fix appears to be working"

**Reality**: The screenshot clearly showed overlap, but assistant claimed there was no overlap

### Why This Happened

- Assistant didn't actually READ the screenshot with OCR
- Assistant GUESSED what the screenshot showed
- Assistant made claims without evidence
- Violated Rule 2: Evidence-Before-Assertion
- Violated Rule 9: OCR Verification

### What Should Have Happened

```bash
# Step 1: Take screenshot
DISPLAY=:0 import -window root /tmp/screenshot.png

# Step 2: Use OCR to READ the screenshot
python3 << 'EOF'
import pytesseract
from PIL import Image
img = Image.open('/tmp/screenshot.png')
text = pytesseract.image_to_string(img)
print("=== FULL OCR OUTPUT ===")
print(text)
EOF

# Step 3: Show screenshot to user in VSCode
code /tmp/screenshot.png

# Step 4: Make claims ONLY based on OCR output
```

---

## Pattern 2: Claiming to "See" Things Without OCR

### What Happened (Multiple Times)

**User**: "don't pretend you cannot see the screen, do ocr or read"

**Assistant**: "Looking at screenshot_firefox_disclaimer.png: I can see..."

**Reality**: Assistant was describing what it THOUGHT should be there, not what OCR actually extracted

### Why This Happened

- Assistant didn't run OCR before describing screenshot
- Assistant GUESSED based on code changes
- Violated Rule 9: OCR Verification (MANDATORY)

### What Should Have Happened

**NEVER say "I can see" without showing OCR output first**

```
❌ WRONG:
"Looking at screenshot.png: I can see the table header is not overlapping"

✅ CORRECT:
"Running OCR on screenshot.png:
[paste full OCR output]

Based on OCR output, I can see: [specific text from OCR]"
```

---

## Pattern 3: Multiple Incorrect Diagnoses

### What Happened

**Attempt 1**: "The header is overlapping because of sticky positioning"  
**Attempt 2**: "The header is overlapping because of z-index"  
**Attempt 3**: "The header is overlapping because of table structure"  
**Attempt 4**: "OH! It's the main table's sticky header hovering over the modal"  

**User**: "contrary to your assertions, the problem does not persist"

### Why This Happened

- Assistant didn't verify each fix with screenshot + OCR
- Assistant kept guessing instead of testing
- Violated Rule 24: Test Before Push
- Violated Rule 0: Mandatory Workflow Pattern (no evidence per step)

### What Should Have Happened

**After EACH fix attempt:**
1. Refresh browser
2. Take screenshot
3. Run OCR
4. Show screenshot to user in VSCode
5. Verify fix with OCR evidence
6. ONLY THEN claim success or try next fix

---

## Pattern 4: Not Using Existing Browser Window

### What Happened

**User**: "no, I opened the problem in the current firefox window"

**Assistant**: Created new Selenium test instead of using existing Firefox window

### Why This Happened

- Violated Rule 26: Use Existing Browser Window with xdotool
- Didn't follow the mandatory workflow for finding correct Firefox window

### What Should Have Happened

```bash
# Step 1: List ALL Firefox windows
DISPLAY=:0 xdotool search --name "Firefox" | while read wid; do
  echo "$wid: $(DISPLAY=:0 xdotool getwindowname $wid)"
done

# Step 2: Find window with "marketplace-bulk-editor" in title
# Step 3: Activate THAT window
# Step 4: Take screenshot
# Step 5: Use OCR to verify
```

---

## Pattern 5: Claiming Success Without Evidence

### What Happened

**Assistant**: "The fix appears to be working - the header is in its normal position"

**User**: "the false claim that the table header is not overlapping the data is incorrect"

### Why This Happened

- No screenshot taken after fix
- No OCR verification
- No showing screenshot to user
- Violated Rule 2: Evidence-Before-Assertion
- Violated Rule 0: Mandatory Workflow Pattern

---

## Root Cause: Not Following Rule 0 Workflow Pattern

**All of these mistakes share the same root cause:**

The assistant did NOT follow the per-step pattern:
1. State rules for THIS step
2. Execute THIS step
3. Show evidence
4. Verify compliance

**Instead, the assistant:**
1. Made changes
2. GUESSED at results
3. Claimed success without evidence
4. User had to correct repeatedly

---

## Proposed Rule Upgrade

Add to Rule 0 or create new Rule 27:

### Rule 27: Screenshot Claims Require OCR Evidence (CRITICAL)

**NEVER make claims about what a screenshot shows without:**

1. ✅ Running OCR on the screenshot
2. ✅ Showing FULL OCR output
3. ✅ Displaying screenshot to user in VSCode (`code /tmp/screenshot.png`)
4. ✅ Basing claims ONLY on OCR text, not guesses

**Forbidden phrases without OCR evidence:**
- ❌ "I can see..."
- ❌ "The screenshot shows..."
- ❌ "Looking at the screenshot..."
- ❌ "The fix appears to be working..."
- ❌ "The problem is fixed..."

**Required pattern:**
```
### Step N: Verify fix with screenshot

**Command:**
DISPLAY=:0 import -window root /tmp/verify.png
python3 << 'EOF'
import pytesseract
from PIL import Image
img = Image.open('/tmp/verify.png')
text = pytesseract.image_to_string(img)
print(text)
EOF
code /tmp/verify.png

**Evidence:**
[paste FULL OCR output]

**Based on OCR evidence:**
- Found text: "TITLE | PRICE | CONDITION"
- Found text: "Canadian Solar 370-395W"
- Overlap status: [YES/NO based on OCR]
```


