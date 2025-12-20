# Rule 0 Added - Mandatory Workflow Pattern (META-RULE)

**Date**: 2025-12-20  
**Version**: 3.5 (upgraded from 3.4)  
**Trigger**: User complaint about having to constantly ask for rule compliance

---

## User Complaints That Triggered This Rule

### Initial Complaint
> "explain why I have to ask this"
>
> "What should happen automatically:
> - I should state applicable rules BEFORE acting
> - I should show planned steps BEFORE executing
> - I should provide evidence AFTER each step
> - I should verify with OCR BEFORE claiming results
>
> This is a meta-rule violation - the rules exist but I'm not following the pattern"

### Follow-Up Clarification
> User: "explain what rules apply as you go through the steps"
>
> Assistant: "Should I update Rule 0 to enforce the per-step pattern?"
>
> User: "What is the correct answer?"
>
> Assistant: "The correct answer is YES. Rule 0 must enforce the pattern PER STEP, not just once at the beginning."

---

## What Was Wrong

### The Problem
- Rules 1-26 existed but assistant didn't follow the **workflow pattern**
- Assistant would:
  - State rules once at the beginning
  - Execute all steps in bulk
  - Provide evidence at the end
  - Not connect each action to its rule justification
- User had to constantly ask:
  - "Which rules apply?"
  - "Show your steps"
  - "Provide evidence"
  - "Use OCR to verify"
  - "Explain what rules apply as you go through the steps"

### The Root Cause
**Meta-rule violation**: The rules existed but there was no enforcement of the **workflow pattern itself**.

The assistant was doing:
```
State all rules → Execute all steps → Show all evidence
```

Instead of:
```
FOR EACH STEP:
  State rules for THIS step → Execute THIS step → Show evidence → Verify compliance
```

---

## What Was Added

### Rule 0: Mandatory Workflow Pattern (META-RULE - CRITICAL)

**Location**: `.augment/rules/mandatory-rules.md` lines 7-341  
**Size**: 335 lines (was 0 lines - new rule)  
**Total file size**: 1115 lines (was 778 lines)

---

## The Mandatory Pattern (PER STEP)

### Phase 1: BEFORE Starting - Plan All Steps
```
## Rules That Apply to This Task
- Rule X: [Why it applies to overall task]

## Steps I Will Take
Step 1: [Action description]
Step 2: [Action description]
```

### Phase 2: FOR EACH STEP - Execute with Rule Citations
```
### Step N: [Step description]

**Rules that apply to THIS step:**
- Rule X: [Why this rule applies to THIS specific step]

**Command/Action:**
[exact command or code to execute]

**Executing:**
[run the command/action]

**Evidence:**
[paste FULL terminal output or result]

**Rule compliance verification:**
- Rule X compliance: ✅ [how THIS step satisfies Rule X]

---
```

### Phase 3: AFTER All Steps - Final Verification
```
## Final Verification
All steps completed: ✅
All rules satisfied: ✅
Evidence provided for each step: ✅
OCR verification performed: ✅
```

---

## Example Included in Rule 0

The rule includes a complete example showing:
- User request: "Fix the $NaN error"
- Phase 1: Planning (3 rules, 5 steps)
- Phase 2: Execution with per-step pattern (5 steps, each with rules/command/evidence/compliance)
- Phase 3: Final verification

---

## Forbidden Patterns

❌ Rules stated once at beginning, not per step  
❌ No evidence after each step  
❌ No rule compliance verification per step  
❌ Claims without OCR proof  
❌ Bulk execution without per-step pattern  

---

## Success Criteria

✅ User never has to ask "which rules apply"  
✅ User never has to ask "show your steps"  
✅ User never has to ask "provide evidence"  
✅ User never has to ask "use OCR to verify"  
✅ User never has to ask "explain what rules apply as you go through the steps"  
✅ User can trace each action to its rule justification  
✅ User can verify compliance step-by-step, not just at the end  
✅ User can trust assistant is following rules automatically  

---

## Key Principle

**The pattern is PER STEP, not per task.**

- ❌ WRONG: State all rules → Execute all steps → Show all evidence
- ✅ CORRECT: For each step: State rules → Execute → Evidence → Verify compliance

---

## Files Modified

1. **`.augment/rules/mandatory-rules.md`**
   - Added Rule 0 (335 lines)
   - Updated version to 3.5
   - Updated description to include "MANDATORY WORKFLOW PATTERN ENFORCEMENT"
   - Total: 1115 lines (was 778 lines)

2. **`.augment/rules/RULE_0_ADDED.md`** (this file)
   - Documents the new meta-rule
   - Explains user complaints
   - Shows the mandatory pattern
   - Lists success criteria

---

## Impact

### Before Rule 0
- ❌ User had to constantly police compliance
- ❌ Rules existed but weren't followed systematically
- ❌ Evidence disconnected from actions
- ❌ No way to trace actions to rule justifications

### After Rule 0
- ✅ Self-enforcing workflow pattern
- ✅ Per-step rule citations
- ✅ Evidence immediately following each action
- ✅ Compliance verification per step
- ✅ User can trust the pattern is followed automatically

---

**This rule makes all other rules actually work.**

