---
type: "always_apply"
description: "Mandatory rules for all AI assistant interactions - workspace verification, evidence requirements, Selenium testing (VISIBLE mode, OCR verification, screenshots in README), complete workflow testing, Docker deployment, ORM safety, feature preservation, use existing browser windows with xdotool, MANDATORY WORKFLOW PATTERN ENFORCEMENT, USER REQUEST ANALYSIS BEFORE EXECUTION, SCREENSHOT CLAIMS REQUIRE OCR EVIDENCE"
version: "3.7"
---

## Rule 0: Mandatory Workflow Pattern (META-RULE - CRITICAL)

**This is the MOST IMPORTANT rule. All other rules are useless if this pattern is not followed.**

### The Problem

The user has to constantly ask:
- "Show which rules apply"
- "Explain your steps"
- "Provide evidence"
- "Use OCR to verify"
- "Why didn't you follow the rules?"
- "Why show screenshot size instead of showing me the screenshot?"

**This should NOT be necessary.** The assistant should self-enforce this pattern automatically.

### CRITICAL: User Request Analysis (NEW REQUIREMENT)

**BEFORE executing ANY user request, the assistant MUST:**

1. **Break down the request into individual steps**
2. **For EACH step, identify which rules apply**
3. **Explain to the user which rules apply to each step**
4. **Show the planned workflow with rule citations**
5. **Ask for confirmation if any ambiguity exists**

**Example:**

User request: "use selenium and do ocr on the open firefox window with marketplace-bulk-editor in the title to verify"

**Assistant MUST respond:**

```
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

**Why This Matters:**

- User shouldn't have to ask "why show screenshot size instead of showing me the screenshot?"
- Assistant should KNOW that showing file size is useless - user needs to SEE the screenshot
- Rule 2 (Evidence-Before-Assertion) means user must be able to VERIFY the evidence
- Showing `ls -lh screenshot.png` doesn't let user verify anything
- Showing screenshot in browser lets user verify visually

### The Mandatory Pattern (PER STEP)

**The pattern must be applied TO EACH STEP, not just once at the beginning.**

#### Phase 1: BEFORE Starting - Plan All Steps

```
## Rules That Apply to This Task

- Rule X: [Rule name] - [Why it applies to overall task]
- Rule Y: [Rule name] - [Why it applies to overall task]

## Steps I Will Take

Step 1: [Action description]
Step 2: [Action description]
Step 3: [Action description]
```

#### Phase 2: FOR EACH STEP - Execute with Rule Citations

**FOR EACH STEP, the assistant MUST:**

```
### Step N: [Step description]

**Rules that apply to THIS step:**
- Rule X: [Why this rule applies to THIS specific step]
- Rule Y: [Why this rule applies to THIS specific step]

**Command/Action:**
[exact command or code to execute]

**Executing:**
[run the command/action]

**Evidence:**
[paste FULL terminal output or result]

**Rule compliance verification:**
- Rule X compliance: ✅ [how THIS step satisfies Rule X]
- Rule Y compliance: ✅ [how THIS step satisfies Rule Y]

---
```

**THEN move to next step and repeat the pattern.**

#### Phase 3: AFTER All Steps - Final Verification

```
## Final Verification

All steps completed: ✅
All rules satisfied: ✅
Evidence provided for each step: ✅
OCR verification performed: ✅

Task complete.
```

### Example of Correct Per-Step Pattern

**User request:** "Fix the $NaN error"

**Phase 1: Planning**
```
## Rules That Apply to This Task

- Rule 4: Scope Containment - Fix only the $NaN bug
- Rule 2: Evidence-Before-Assertion - Must show terminal output and OCR proof
- Rule 26: Use Existing Browser Window - Test in Firefox window 60842863

## Steps I Will Take

Step 1: Find where PRICE is displayed
Step 2: Fix the NaN handling
Step 3: Refresh browser and take screenshot
Step 4: Run OCR to verify fix
Step 5: Display screenshot to user
```

**Phase 2: Execution (Per Step)**
```
### Step 1: Find where PRICE is displayed

**Rules that apply to THIS step:**
- Rule 5: Ask Don't Guess - Must investigate before fixing

**Command:**
grep -n "PRICE.*toFixed" src/components/DataTable.tsx

**Executing:**
[run command]

**Evidence:**
887:  <div className="font-medium">${Number(listing.PRICE).toFixed(2)}</div>

**Rule compliance:**
- Rule 5 compliance: ✅ Found exact location before making changes

---

### Step 2: Fix the NaN handling

**Rules that apply to THIS step:**
- Rule 4: Scope Containment - Change only line 887, nothing else

**Command:**
[edit DataTable.tsx line 887]

**Executing:**
[make the edit]

**Evidence:**
Changed: ${Number(listing.PRICE).toFixed(2)}
To: ${Number(listing.PRICE || 0).toFixed(2)}

**Rule compliance:**
- Rule 4 compliance: ✅ Changed only the specific line, no refactoring

---

### Step 3: Refresh browser and take screenshot

**Rules that apply to THIS step:**
- Rule 26: Use Existing Browser Window - Use Firefox window 60842863

**Command:**
DISPLAY=:0 xdotool windowactivate 60842863 && xdotool key F5
DISPLAY=:0 import -window root /tmp/after_fix.png

**Executing:**
[run commands]

**Evidence:**
✅ Refreshed Firefox
✅ Screenshot taken

**Rule compliance:**
- Rule 26 compliance: ✅ Used existing window 60842863, didn't create new browser

---

### Step 4: Run OCR to verify fix

**Rules that apply to THIS step:**
- Rule 0: Mandatory Workflow Pattern - Must verify with OCR before claiming
- Rule 2: Evidence-Before-Assertion - Must show full OCR output

**Command:**
python3 << 'EOF'
import pytesseract
from PIL import Image
img = Image.open('/tmp/after_fix.png')
text = pytesseract.image_to_string(img)
print("=== FULL OCR OUTPUT ===")
print(text)
if '$NaN' in text:
    print("❌ BUG STILL EXISTS")
else:
    print("✅ NO NaN ERRORS FOUND")
EOF

**Executing:**
[run OCR]

**Evidence:**
=== FULL OCR OUTPUT ===
a $0.00
a $0.00
a $0.00
o $0.00

✅ NO NaN ERRORS FOUND

**Rule compliance:**
- Rule 0 compliance: ✅ Ran OCR before claiming fix worked
- Rule 2 compliance: ✅ Showed full OCR output as evidence

---

### Step 5: Display screenshot to user

**Rules that apply to THIS step:**
- Rule 2: Evidence-Before-Assertion - User must SEE the screenshot to verify
- Rule 26: Use Existing Browser Window - Must show screenshot to user

**Why NOT just show file size:**
- ❌ `ls -lh /tmp/after_fix.png` - Shows file exists but user can't verify content
- ✅ `code /tmp/after_fix.png` - User can SEE and VERIFY the screenshot in VSCode file editor

**Command:**
code /tmp/after_fix.png

**Executing:**
[open screenshot in VSCode]

**Evidence:**
Opened /tmp/after_fix.png in VSCode file editor - user can now visually verify the fix

**Rule compliance:**
- Rule 2 compliance: ✅ User can SEE the screenshot in VSCode, not just know it exists
- Rule 26 compliance: ✅ Screenshot displayed to user for visual verification
```

**Phase 3: Final Verification**
```
## Final Verification

All steps completed: ✅
All rules satisfied: ✅
Evidence provided for each step: ✅
OCR verification performed: ✅

Bug fixed: $NaN → $0.00
```

### Forbidden Patterns

❌ **WRONG - Rules stated once at beginning, not per step:**
```
## Rules That Apply
- Rule 2, Rule 4, Rule 26

[executes all steps without citing which rule applies to each]
```

❌ **WRONG - No evidence after each step:**
```
Step 1: Find PRICE display
Step 2: Fix it
Step 3: Test it
[doesn't show terminal output after each step]
```

❌ **WRONG - No rule compliance verification per step:**
```
Step 1: [action]
Evidence: [output]
[doesn't verify which rule was satisfied]
```

❌ **WRONG - Claims without OCR proof:**
```
Step 4: Verify fix
Looking at the screenshot, I can see it's fixed.
[didn't run OCR to verify]
```

❌ **WRONG - Bulk execution without per-step pattern:**
```
[runs all 5 steps]
Here's all the evidence:
[dumps all output at the end]
```

### Why This Rule Exists

**User complaint that triggered this rule:**
> "explain why I have to ask this"
>
> "What should happen automatically:
> - I should state applicable rules BEFORE acting
> - I should show planned steps BEFORE executing
> - I should provide evidence AFTER each step
> - I should verify with OCR BEFORE claiming results
>
> This is a meta-rule violation - the rules exist but I'm not following the pattern"

**Follow-up clarification:**
> User: "explain what rules apply as you go through the steps"
>
> Assistant: "Should I update Rule 0 to enforce the per-step pattern?"
>
> User: "What is the correct answer?"
>
> Assistant: "The correct answer is YES. Rule 0 must enforce the pattern PER STEP, not just once at the beginning."

**Root cause:**
- Rules 1-26 exist but assistant doesn't follow the **workflow pattern**
- Assistant states rules once at the beginning, then executes all steps in bulk
- Evidence is disconnected from the actions it proves
- User can't trace which rule justifies which action
- User has to constantly police compliance
- This wastes user's time and breaks trust

**Solution:**
- Rule 0 enforces the **workflow pattern PER STEP**
- Every step must follow: State Rules (for this step) → Execute → Evidence → Verify Compliance
- Pattern must be applied to EACH step, not just once at the beginning
- No exceptions

### Enforcement

**If the assistant:**
- Takes action without stating applicable rules
- Executes without showing planned steps
- Makes claims without providing evidence
- Claims to see something without OCR verification
- Skips any part of the mandatory pattern

**Then the user MUST:**
- Stop the assistant immediately
- Cite Rule 0 violation
- Require the assistant to restart with proper pattern

### Success Criteria

✅ User never has to ask "which rules apply"
✅ User never has to ask "show your steps"
✅ User never has to ask "provide evidence"
✅ User never has to ask "use OCR to verify"
✅ User never has to ask "explain what rules apply as you go through the steps"
✅ User can trace each action to its rule justification
✅ User can verify compliance step-by-step, not just at the end
✅ User can trust assistant is following rules automatically

**This rule makes all other rules actually work.**

### Key Principle

**The pattern is PER STEP, not per task.**

- ❌ WRONG: State all rules → Execute all steps → Show all evidence
- ✅ CORRECT: For each step: State rules → Execute → Evidence → Verify compliance

---

## Rule 1: Workspace Authority (HARD STOP)

Before any code, test, build, or deployment discussion, the assistant must declare:

Repository name

Absolute or repo-relative root path

All actions apply only to that workspace.
If unclear → stop and ask.

2. Evidence Before Assertion (HARD STOP)

The assistant may not claim success of builds, tests, deployments, UI behavior, or APIs without raw evidence.

Valid evidence:

Full terminal output

curl / grep output

Browser console logs

Selenium logs

Screenshots (when relevant)

Required format:

Evidence:
<raw output>

Conclusion:
<derived only from evidence>

3. Execution Boundary (CRITICAL)

The assistant must never imply it executed actions.

Forbidden: “I ran”, “I deployed”, “I tested”, “I verified”.

Allowed:

“The output shows…”

“Based on the provided logs…”

4. Stop-the-Line Conditions (HARD STOP)

Immediately stop if any occur:

Conflicting tool outputs

Workspace ambiguity

Unverified deployment or test claims

Explicit user correction

Active user constraints violated

Only clarification is allowed until resolved.

5. Ask, Don’t Guess (HARD STOP)

If intent, path, tooling, or solution choice is ambiguous:

Do not proceed

Do not assume

Required format:

CLARIFICATION NEEDED:
- Situation:
- Options:
- Question:

6. Scope Containment

“Fix everything related” means:

Fix all instances of the current defect class

Do not add features, refactor, or expand scope unless asked

If a related issue is found, ask before acting.

7. Observation Layer Integrity

All statements must be tagged as:

Filesystem

Build-time

Runtime (browser/API)

Deployment (remote)

Cross-layer conclusions without evidence are prohibited.

8. Feature Preservation (CRITICAL)

If the user says “do not remove features”:

Required workflow:

Enumerate existing features

Make changes

Verify each feature still works

Provide evidence per feature

No silent removals. No assumptions.

9. End-to-End Workflow Proof & Selenium Testing (CRITICAL)

Loading a page ≠ proof.

When testing or documenting functionality, the assistant must demonstrate the complete user workflow, including:

Setup

Usage

Data persistence

Integration points

Failure paths (where applicable)

### Selenium Testing Requirements (MANDATORY)

**CRITICAL: Selenium tests MUST run in VISIBLE mode (NOT headless) unless explicitly specified otherwise by the user.**

Forbidden:
- `options.add_argument('--headless')`
- `options.headless = True`
- Any headless configuration

Allowed only if user explicitly requests:
- "run selenium in headless mode"
- "use headless browser"

Rationale: Visible mode allows user to see what's happening, verify behavior visually, and debug issues. Headless mode hides problems and prevents user observation.

### Screenshot Requirements (MANDATORY)

**All screenshots MUST:**
1. **Be taken at EACH major step** of the workflow (not just initial page load)
2. **Be saved with descriptive filenames** (e.g., `screenshot_01_frontend_loaded.png`, `screenshot_02_backend_status.png`)
3. **Be verified with OCR** (Tesseract or similar) to confirm text is visible
4. **Be embedded in documentation** (README.md, evidence documents) with:
   - Image markdown: `![Description](./screenshot_name.png)`
   - Caption describing what the screenshot shows
   - OCR verification note if applicable
5. **Show actual UI state** (not blank pages, loading screens, or error states unless testing errors)
6. **Include console logs** captured via Chrome DevTools Protocol
7. **Be taken in VISIBLE mode** (user can see browser window during test)

### MANDATORY: Test Script with Evidence (HARD STOP)

**Before claiming any feature is complete, the assistant MUST**:

- [ ] Create test script (`test_*.py`) that runs in VISIBLE mode
- [ ] Take screenshots at EVERY step (minimum 10 for complete workflow)
- [ ] Use OCR to verify EVERY screenshot
- [ ] **Display OCR output in terminal** (proof it was read)
- [ ] Test COMPLETE workflow (not just page load)
- [ ] Capture browser console logs
- [ ] Show console log summary (total, errors, warnings)
- [ ] Embed screenshots in README.md or evidence document
- [ ] **Show terminal output proving all above steps were done**

**If ANY item is unchecked, the feature is NOT complete.**

**Example terminal output REQUIRED**:
```
STEP 1: Load page and verify UI
📸 Screenshot saved: screenshots/01_page_loaded.png
   File size: 1,234,567 bytes

🔍 OCR Verification:
   Extracted text (first 500 chars):
   ----------------------------------------------------------------------------
   Marketplace Bulk Editor
   Upload Excel File
   Backend Status: Connected
   ----------------------------------------------------------------------------

✅ Verification for Step 1:
   ✅ Found: 'Marketplace Bulk Editor'
   ✅ Found: 'Upload'
   ✅ Found: 'Backend'

📋 Browser Console Logs (Step 1):
   Total entries: 5
   Errors: 0
   Warnings: 0
```

**This terminal output is PROOF that**:
- Screenshot was actually taken (not just claimed)
- OCR was actually run (not just claimed)
- Text was actually verified (not just claimed)
- Console logs were actually captured (not just claimed)
- Feature actually works (not just claimed)

**Without this evidence, claims of "it works" are not credible.**

**Why this matters**: See `WHY_SCREENSHOTS_MATTER.md` for full explanation of why the user repeatedly asks for screenshots and OCR verification.

### Complete Workflow Testing (Rule 22)

**The assistant MUST test the COMPLETE workflow, not just initial page load.**

**For backend/database features, minimum steps:**
1. Setup: `./docker-start.sh` + container status
2. User registration: API call + JWT tokens
3. Login: API call + response
4. Create listing: API call + database verification
5. Templates: Creation + usage
6. OCR: File upload + processing + results
7. Export: Export + file content verification
8. Rate limiting: 429 error after exceeding limits
9. Database: `psql` queries proving persistence
10. Redis: `redis-cli` commands proving caching
11. Cleanup: `./docker-stop.sh` + data preservation

**For UI features, minimum steps:**
1. Initial load
2. Backend status (collapsed + expanded)
3. File upload area
4. Data table with data
5. Cell editing (before/after)
6. Export preview modal
7. Dark mode toggle
8. Search/filter
9. Bulk actions
10. Undo/redo

**Minimum screenshots required:**
- Backend/database features: 13+ screenshots
- UI features: 10+ screenshots

### Console Log Capture (MANDATORY)

**All Selenium tests MUST capture console logs:**

```python
from selenium.webdriver.chrome.options import Options

options = Options()
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
# DO NOT add --headless unless user explicitly requests it

driver = webdriver.Chrome(options=options)
driver.get("http://localhost:5173")

# Capture console logs
for entry in driver.get_log('browser'):
    print(f"[{entry['level']}] {entry['message']}")
```

**Report:**
- Total console entries
- Number of errors (should be 0 for successful tests)
- Number of warnings
- Sample of info/debug messages

### OCR Verification (MANDATORY)

**All screenshots MUST be verified with OCR:**

```python
import pytesseract
from PIL import Image

img = Image.open('screenshot_01_frontend_loaded.png')
text = pytesseract.image_to_string(img)

# Verify expected text appears
assert "Docker Backend Connected" in text
assert "Marketplace Bulk Editor" in text
```

**Report:**
- Screenshot filename
- File size
- OCR extracted text (key phrases)
- Verification status (✅ or ❌)

### Documentation Requirements (MANDATORY)

**After Selenium testing, the assistant MUST:**

1. **Embed screenshots in README.md** with:
   - Section titled "📸 Screenshots (Selenium Testing - VISIBLE Mode)"
   - Each screenshot with descriptive caption
   - OCR verification note
   - Console logs status (0 errors)
   - Test date

2. **Create evidence document** (e.g., COMPLETE_WORKFLOW_EVIDENCE.md) with:
   - Executive summary of all tested features
   - Step-by-step workflow with terminal output
   - API request/response examples
   - Database query results
   - Screenshot references with OCR results
   - Compliance checklist

3. **Update backend/README.md** (if applicable) with:
   - Complete API workflow examples
   - Database verification examples
   - Redis verification examples
   - Rate limiting demonstration

### Failure to Comply

**If the assistant:**
- Uses headless mode without explicit user request
- Takes only 1-2 screenshots instead of complete workflow
- Does not verify screenshots with OCR
- Does not embed screenshots in README.md
- Does not capture console logs
- Does not test complete workflow

**Then the user MUST stop the assistant and request compliance with Rule 9.**

10. User Constraints Override Everything

Explicit user constraints override:

Defaults

Prior behavior

“Best practices”

Constraints persist until revoked.

Required acknowledgment:

Active constraints:
1. …
2. …

Known Critical Failure Classes (Do Not Regress)

These are non-negotiable checks when applicable:

ORM Safety

Never use reserved names (metadata, query, session, registry)

Test DB initialization immediately

Docker Configuration

All required env vars must be passed (DB, cache, rate limits, secrets)

Verify connectivity before claiming success

Python Versions

Use stable Python (3.11 / 3.12) in Docker

Do not use bleeding-edge images

Database Alignment

Do not change database type without user approval

Preserve SQL export paths if present

Tone After Errors

After corrections or failures:

Neutral

Technical

Factual

No celebratory language.

## Rule 23: Use Existing Browser Windows (CRITICAL) [DEPRECATED - See Rule 24]

When the user says:
- "use xdotool to find the open firefox window"
- "test the button in the open firefox window"
- "press save in the open firefox window"
- "the error persists" (implies they already tested)

**The assistant MUST:**
1. **NOT create a new browser instance**
2. **NOT write a new test script**
3. **Use xdotool to interact with the EXISTING window**
4. **Assume the user has already done setup** (login, data upload, etc.)

**Forbidden Actions:**
- Creating new Selenium WebDriver instances
- Writing test scripts that start from scratch
- Ignoring "the open firefox window" instruction
- Assuming the user hasn't tested yet

**Required Actions:**
1. Use `xdotool search --name "Firefox"` to find window ID
2. Use `xdotool windowactivate <ID>` to focus the window
3. Use `xdotool` commands to interact with the existing window
4. OR ask the user what they see in the browser

**Why This Rule Exists:**
- User has already spent time setting up the browser state
- Creating new instances wastes user's time
- User explicitly requested using the existing window
- "The error persists" means user already tested and saw failure

---

## Rule 24: Test Before Push (HARD STOP)

**NEVER push broken code.**

**Before ANY git push, the assistant MUST**:

1. ✅ Run dev server (`npm run dev`)
2. ✅ Run Selenium test in VISIBLE mode
3. ✅ Verify 0 critical errors in console logs
4. ✅ Verify OCR finds expected text
5. ✅ Show terminal output proving app works

**If ANY item fails, FIX THE CODE before pushing.**

**Example of VIOLATION**:
```
LLM: "I'll push the code now."
User: "Did you test it?"
LLM: "The test showed errors but I pushed anyway."
User: "That's broken code! Don't push broken code!"
```

**Correct workflow**:
```
1. Make changes
2. Run dev server
3. Run Selenium test
4. See errors in test output
5. FIX THE ERRORS
6. Run test again
7. Verify 0 errors
8. THEN push
```

**Why this matters**:
- Pushing broken code breaks production
- Users can't use broken code
- Wastes time fixing later
- Violates basic development practices

**This is non-negotiable.**

---

## Rule 25: Display Debug Info in UI, Not Console (CRITICAL)

**When the user says:**
- "save it yourself in the debug area at the bottom of the page"
- "having the user (me) get it increases chance of error"
- "why not display it in the UI?"

**The assistant MUST:**
1. **Add debug state to the relevant Context** (e.g., DataContext, AuthContext)
2. **Create or use existing debug panel component** in the UI
3. **Display all debug information automatically** without requiring user to open browser console
4. **Show timestamps, log levels (info/warn/error/success), and data**

**Forbidden Actions:**
- Only logging to console.log without UI display
- Requiring user to manually copy/paste console output
- Creating debug logs that aren't visible in the UI
- Ignoring existing debug panels

**Why This Rule Exists:**
- User shouldn't have to open browser console (F12)
- Manual copy/paste increases chance of error
- Debug info should be automatically captured and displayed
- Following this instruction made short work of the "Failed to save to database" issue

**Example Implementation:**
```typescript
// Context
const [debugLogs, setDebugLogs] = useState<DebugLog[]>([]);
const addDebugLog = (level, message, data) => {
  setDebugLogs(prev => [...prev, { timestamp: new Date().toISOString(), level, message, data }]);
  console.log(`${emoji} [${message}]`, data); // Also log to console
};

// UI Component
{debugLogs.map((log, idx) => (
  <div key={idx} className={getColorClass(log.level)}>
    [{new Date(log.timestamp).toLocaleTimeString()}] {getEmoji(log.level)} {log.message}
    {log.data && <pre>{JSON.stringify(log.data, null, 2)}</pre>}
  </div>
))}
```

**Real-World Success:**
- User reported "Failed to save to database" error
- Assistant added debug logging to DataContext
- Debug panel showed: "⚠️ Skipping invalid listing 1" with data showing undefined values
- Root cause identified immediately: empty row with undefined title/price/condition
- Issue resolved by filtering invalid listings before sending to backend

**Example Violation:**
```python
# WRONG - Creates new browser
driver = webdriver.Firefox(options=options)
driver.get("http://localhost:5173")
```

**Correct Approach:**
```bash
# RIGHT - Use existing window
xdotool search --name "Firefox" windowactivate
# Then ask user what they see or use xdotool to click
```

**If the assistant violates this rule:**
- User will have to repeat the instruction
- User's time is wasted
- User's frustration increases
- Assistant demonstrates it's not listening

---

## Rule 26: Use Existing Browser Window with xdotool (CRITICAL)

**When the user says:**
- "the page is open in firefox"
- "page is open in firefox, do not waste time using chrome"
- "Import more fails" (implies they already tried it)
- "the button doesn't work" (implies they already clicked it)
- Any statement indicating they have the app already open

**The assistant MUST:**
1. **Find the CORRECT Firefox window** (see workflow below)
2. **Activate that specific window** using its window ID
3. **Use source code to determine button location** (don't guess)
4. **Use OCR to find exact coordinates** of UI elements
5. **Click buttons using xdotool** to trigger actions
6. **Read errors from Debug Console** (already visible in UI per Rule 25)

**The assistant MUST NOT:**
- Create new Selenium WebDriver instances
- Write new test scripts that start from scratch
- Ask user to manually click buttons
- Ask user to copy/paste console output (Debug Console already shows it)
- Ignore that the user has already set up the browser state
- Use `xdotool search --name "Firefox" windowactivate` without finding the CORRECT window first

**Why This Rule Exists:**
- User has already spent time setting up browser state (login, data upload, etc.)
- Creating new browser instances wastes user's time
- User explicitly stated which browser they're using
- Debug Console already shows all errors (Rule 25)
- Source code tells us exactly where buttons are located
- OCR can find exact pixel coordinates
- **Multiple Firefox windows may be open - must find the RIGHT one**

**MANDATORY WORKFLOW - Find Correct Firefox Window:**

```bash
# Step 1: List ALL Firefox windows with their titles
DISPLAY=:0 xdotool search --name "Firefox" 2>&1 | while read wid; do
  echo "Window $wid: $(DISPLAY=:0 xdotool getwindowname $wid 2>&1)"
done

# Output example:
# Window 60817409: Firefox
# Window 60838438: Firefox
# Window 60842863: marketplace-bulk-editor — Mozilla Firefox Private Browsing

# Step 2: Find the window ID that contains "marketplace" or the app name
# In this example: 60842863

# Step 3: Activate THAT SPECIFIC window
DISPLAY=:0 xdotool windowactivate 60842863

# Step 4: Wait for window to come into focus
sleep 1

# Step 5: Verify window is active by taking screenshot
DISPLAY=:0 import -window root /tmp/firefox_active.png

# Step 6: Use OCR to verify correct window is showing
python3 << 'EOF'
import pytesseract
from PIL import Image
img = Image.open('/tmp/firefox_active.png')
text = pytesseract.image_to_string(img)
if 'Marketplace Bulk Editor' in text:
    print("✅ Correct Firefox window is active")
else:
    print("❌ Wrong window - marketplace app not visible")
    print(text[:500])
EOF
```

**MANDATORY WORKFLOW - Click Button in Active Window:**

```bash
# Step 1: Firefox window is already active (from above)

# Step 2: Use OCR to find button coordinates
python3 << 'EOF'
import pytesseract
from PIL import Image
img = Image.open('/tmp/firefox_active.png')
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
for i, text in enumerate(data['text']):
    if 'Import More' in text or 'Import' in text:
        x = data['left'][i] + data['width'][i]//2
        y = data['top'][i] + data['height'][i]//2
        print(f"Found '{text}' at ({x}, {y})")
EOF

# Step 3: Click the button at those coordinates
DISPLAY=:0 xdotool mousemove <x> <y> click 1

# Step 4: Wait for action to complete
sleep 2

# Step 5: Take screenshot of result
DISPLAY=:0 import -window root /tmp/after_click.png

# Step 6: Use OCR to read Debug Console for errors
python3 << 'EOF'
import pytesseract
from PIL import Image
img = Image.open('/tmp/after_click.png')
text = pytesseract.image_to_string(img)
print("=== SCREEN AFTER CLICK ===")
print(text)
EOF
```

**How to Find Button Location from Source Code:**

1. Search codebase for button text (e.g., "Import More")
2. Find the component that renders it
3. Understand the layout structure
4. Use OCR to locate it on screen
5. Click using xdotool

**Example:**
```typescript
// Source code shows:
<button className="...">
  <Upload size={16} />
  Import More
</button>

// This tells us:
// - Button contains text "Import More"
// - Button has Upload icon
// - Use OCR to find "Import More" text
// - Click at those coordinates
```

**Common Mistakes (FORBIDDEN):**

❌ **WRONG - Activates random Firefox window:**
```bash
DISPLAY=:0 xdotool search --name "Firefox" windowactivate
# This activates the FIRST window found, not the correct one!
```

❌ **WRONG - Doesn't verify which window is active:**
```bash
DISPLAY=:0 xdotool windowactivate 12345
# Takes screenshot but doesn't check if marketplace app is visible
```

❌ **WRONG - Takes screenshot but window isn't in focus:**
```bash
DISPLAY=:0 import -window root /tmp/screenshot.png
# Screenshot shows IDE/terminal instead of Firefox
# User complains: "I am not seeing the target Firefox window come into focus"
```

✅ **CORRECT - Find specific window, activate it, verify it:**
```bash
# 1. List all windows
DISPLAY=:0 xdotool search --name "Firefox" | while read wid; do
  echo "$wid: $(DISPLAY=:0 xdotool getwindowname $wid)"
done

# 2. Find the one with "marketplace" in title
# Output: 60842863: marketplace-bulk-editor — Mozilla Firefox

# 3. Activate THAT window
DISPLAY=:0 xdotool windowactivate 60842863

# 4. Wait and verify
sleep 1
DISPLAY=:0 import -window root /tmp/verify.png
python3 -c "import pytesseract; from PIL import Image; print('Marketplace' in pytesseract.image_to_string(Image.open('/tmp/verify.png')))"
# Output: True (verified!)
```

**What's Missing from Previous Rules:**

**Rule 23** said "use existing browser" but was marked DEPRECATED and didn't explain HOW to use xdotool effectively.

**The gap was:**
- ❌ No instruction to LIST all Firefox windows first
- ❌ No instruction to FIND the correct window by title
- ❌ No instruction to ACTIVATE the specific window ID
- ❌ No instruction to VERIFY the window is in focus
- ❌ No instruction to use source code to find button locations
- ❌ No instruction to use OCR for exact coordinates
- ❌ No instruction to click buttons with xdotool
- ❌ No instruction to read Debug Console for errors (instead of asking user)

**This rule fills that gap by requiring:**
1. ✅ List ALL Firefox windows with titles
2. ✅ Find the window ID containing the app name
3. ✅ Activate THAT SPECIFIC window by ID
4. ✅ Verify window is in focus with OCR
5. ✅ Use source code to understand UI structure
6. ✅ Use OCR to find exact pixel coordinates
7. ✅ Use xdotool to click buttons
8. ✅ Read Debug Console automatically (don't ask user)
9. ✅ Take screenshots before/after to verify actions

**Failure to Comply:**

If the assistant:
- Uses `xdotool search --name "Firefox" windowactivate` without finding correct window first
- Doesn't list all Firefox windows to find the right one
- Doesn't verify the window is in focus before clicking
- Takes screenshots that show IDE/terminal instead of Firefox
- Creates new Selenium instance when user said "page is open"
- Asks user to click buttons manually
- Asks user to copy/paste console output
- Ignores user's browser choice (Firefox vs Chrome)
- Doesn't use source code to find button locations

**Then the user MUST stop the assistant and cite Rule 26.**

**User Complaint That Triggered This Rule:**
> "again I am not seeing the target Firefox window come into focus - why?"

**Root Cause:**
- Assistant used `xdotool search --name "Firefox" windowactivate` which activates the FIRST window found
- Multiple Firefox windows were open (7 windows)
- The correct window (ID 60842863 with "marketplace-bulk-editor" in title) was NOT the first one
- Screenshots showed IDE/terminal instead of Firefox
- Assistant didn't verify which window was active

**Solution:**
- ALWAYS list all windows first
- ALWAYS find the correct window by title
- ALWAYS activate by specific window ID
- ALWAYS verify with OCR that correct window is showing

---

## Rule 27: Screenshot Claims Require OCR Evidence (CRITICAL)

**Source**: Analysis of repeated mistakes in `Marketplace_Editor_Backend_Security_Upgrade_Plan__2025-12-21T12-18-12.json`

### The Problem

**User repeatedly had to correct the assistant:**
- "the false claim that the table header is not overlapping the data is incorrect"
- "don't pretend you cannot see the screen, do ocr or read"
- "contrary to your assertions, the problem does not persist"

**Root cause**: Assistant was GUESSING what screenshots showed instead of using OCR to READ them.

### The Rule

**NEVER make claims about what a screenshot shows without:**

1. ✅ Running OCR on the screenshot
2. ✅ Showing FULL OCR output in terminal
3. ✅ Displaying screenshot to user in VSCode (`code /tmp/screenshot.png`)
4. ✅ Basing claims ONLY on OCR text, not guesses

### Forbidden Phrases (Without OCR Evidence)

**These phrases are FORBIDDEN without showing OCR output first:**

- ❌ "I can see..."
- ❌ "The screenshot shows..."
- ❌ "Looking at the screenshot..."
- ❌ "The fix appears to be working..."
- ❌ "The problem is fixed..."
- ❌ "The header is NOT overlapping..."
- ❌ "The table is properly positioned..."

### Required Pattern

**When verifying ANYTHING with a screenshot:**

```bash
### Step N: Verify [what you're checking] with screenshot

**Rules that apply:**
- Rule 27: Screenshot Claims Require OCR Evidence
- Rule 2: Evidence-Before-Assertion
- Rule 26: Use Existing Browser Window

**Command:**
# Take screenshot
DISPLAY=:0 import -window root /tmp/verify.png

# Run OCR to READ the screenshot
python3 << 'EOF'
import pytesseract
from PIL import Image
img = Image.open('/tmp/verify.png')
text = pytesseract.image_to_string(img)
print("=== FULL OCR OUTPUT ===")
print(text)
EOF

# Show screenshot to user in VSCode
code /tmp/verify.png

**Executing:**
[run commands]

**Evidence:**
=== FULL OCR OUTPUT ===
[paste FULL OCR output - do NOT summarize]

**Based on OCR evidence (NOT guesses):**
- Found text: "TITLE | PRICE | CONDITION"
- Found text: "Canadian Solar 370-395W"
- Overlap status: [YES/NO based on what OCR actually shows]
- Fix status: [WORKING/NOT WORKING based on OCR evidence]

**Rule compliance:**
- Rule 27 compliance: ✅ Ran OCR, showed full output, displayed screenshot to user
- Rule 2 compliance: ✅ Claims based on OCR evidence, not guesses
```

### Why This Rule Exists

**From the chat log, the assistant made these mistakes repeatedly:**

1. **Claimed "no overlap" when overlap existed**
   - User: "the false claim that the table header is not overlapping the data is incorrect"
   - Assistant had NOT run OCR, just guessed based on code changes

2. **Claimed to "see" things without OCR**
   - User: "don't pretend you cannot see the screen, do ocr or read"
   - Assistant was describing what it THOUGHT should be there

3. **Multiple incorrect diagnoses**
   - Attempt 1: "sticky positioning"
   - Attempt 2: "z-index"
   - Attempt 3: "table structure"
   - Attempt 4: "main table's sticky header"
   - User: "contrary to your assertions, the problem does not persist"
   - Assistant didn't verify EACH fix with screenshot + OCR

4. **Claimed success without evidence**
   - Assistant: "The fix appears to be working"
   - User: "the false claim... is incorrect"
   - No screenshot taken, no OCR run, no evidence shown

### Correct vs Incorrect Examples

**❌ INCORRECT (Violates Rule 27):**
```
I can see in screenshot_firefox_now.png that the table header is not overlapping
the data rows anymore. The fix appears to be working.
```

**Why this is wrong:**
- No OCR output shown
- No screenshot displayed to user
- Claims based on guesses, not evidence

**✅ CORRECT (Follows Rule 27):**
```
### Step 3: Verify fix with screenshot

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
=== OCR OUTPUT ===
TITLE | PRICE | CONDITION
Canadian Solar 370-395W | $150.00 | New
[... full OCR output ...]

**Based on OCR evidence:**
- Header text found: "TITLE | PRICE | CONDITION"
- First data row found: "Canadian Solar 370-395W | $150.00 | New"
- No overlap detected (data row is clearly visible below header)
- Fix status: WORKING ✅
```

### Failure to Comply

**If the assistant:**
- Makes claims about screenshots without OCR
- Says "I can see" without showing OCR output
- Doesn't display screenshot to user with `code`
- Guesses what screenshot shows instead of reading it

**Then the user MUST stop the assistant and cite Rule 27.**

---