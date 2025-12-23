# Mandatory Rules (Condensed)

**Version**: 3.8 | **Type**: always_apply

---

## Rule 0: Mandatory Workflow Pattern (META-RULE)

**PER STEP pattern required:**
1. State which rules apply to THIS step
2. Execute THIS step
3. Show evidence (full terminal output)
4. Verify compliance

**Forbidden:** Bulk execution, no evidence, claims without OCR

---

## Rule 2: Evidence-Before-Assertion

**No claims without proof:**
- Full terminal output
- OCR verification
- Screenshots displayed to user (`code /tmp/screenshot.png`)

**Forbidden:** "I can see", "appears to work" without evidence

---

## Rule 5: Ask Don't Guess

**If ambiguous → STOP and ask**

Format:
```
CLARIFICATION NEEDED:
- Situation: [what's unclear]
- Options: [possible choices]
- Question: [what you need to know]
```

---

## Rule 26: Use Existing Browser Window

**When user says "page is open in firefox":**

1. List ALL Firefox windows: `xdotool search --name "Firefox"`
2. Find correct window by title (contains "marketplace")
3. Activate THAT window by ID
4. Verify with OCR

**Forbidden:** Creating new Selenium instances, activating wrong window

---

## Rule 27: Screenshot Claims Require OCR

**NEVER say "I can see" without:**
1. Running OCR
2. Showing FULL OCR output
3. Displaying screenshot to user
4. Basing claims ONLY on OCR text

**Forbidden phrases without OCR:**
- "I can see..."
- "The screenshot shows..."
- "The fix appears to be working..."

---

## Rule 28: Application Parameters Database

**BEFORE any action involving ports/URLs/credentials:**

1. Read `.augment/APP_PARAMETERS_DATABASE.md`
2. Quote relevant section
3. Use ONLY documented parameters

**Trigger phrases:**
- `@APP_PARAMETERS_DATABASE.md`
- "Use deterministic parameters"

**Forbidden:** Guessing port numbers, assuming credentials

---

## Other Critical Rules

**Rule 4: Scope Containment** - Fix only what's requested, don't expand scope

**Rule 18: Feature Removal Prohibition** - Never remove features without permission

**Rule 24: Test Before Push** - Never push broken code

**Rule 25: Display Debug in UI** - Add debug logs to UI, not just console

---

## Enforcement

**If assistant violates any rule:**
1. User MUST stop immediately
2. Cite rule number
3. Require restart with proper pattern

---

**Full rules**: See `mandatory-rules.md` (archived)

