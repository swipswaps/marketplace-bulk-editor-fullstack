---
type: "always_apply"
---

# Augment Rules for Marketplace Bulk Editor

This directory contains rules that guide AI assistant behavior in this workspace.

---

## Files

### 1. **mandatory-rules.md** (796 lines)
**Source**: Imported from `/home/owner/Documents/johnkimball/Marketplace-Bulk-Master-2/.augment/rules/` and enhanced with lessons from chat logs

**Contains 20 mandatory rules**:

1. **Authoritative Workspace Declaration** - Verify repository before any actions
2. **Evidence-Before-Assertion** - No claims without proof (terminal output, screenshots, etc.)
3. **Conflict Escalation** - Stop and ask when tools disagree
4. **Scope Containment** - Fix only what's requested, don't expand scope
5. **Ask Don't Guess** - Stop and ask when uncertain
6. **Documentation Derivation** - Document from actual running code, not assumptions
7. **Selenium Testing & Evidence Collection** - ENHANCED with:
   - Browser selection (Firefox → Chromium → Chrome)
   - Mandatory screenshots at all key points
   - Console log capture (errors, warnings, info)
   - Network activity monitoring
   - Page source saving on errors
   - OCR for visual verification
   - Comprehensive error reporting
   - No headless mode for debugging
8. **Test Before Deploy** - Always test locally and on live URL
9. **Tool Capability Truthfulness** - Don't claim tool limitations without documentation
10. **Execution Authority** - Don't imply you executed actions you can't perform
11. **Correction Reset** - Acknowledge and internalize user corrections
12. **Environment Provenance** - Tag observations by layer (filesystem, build, runtime, deployment)
13. **Stop-the-Line Conditions** - Stop on conflicts, ambiguity, or unverified claims
14. **User Constraint Precedence** - User constraints override all defaults
15. **Tone Control After Failure** - Use neutral, technical language after errors
16. **Workflow Context Preservation** - NEW: Understand and preserve complete user workflows (OCR → Scripts → Web UI → Export)
17. **Data Format Compatibility** - NEW: Maintain compatibility with external formats (Facebook Marketplace, APIs)
18. **Feature Removal Prohibition** - NEW: Never remove features without explicit permission
19. **OCR Data Handling** - NEW: Handle OCR artifacts and noise without auto-deleting data
20. **UI State Preservation** - NEW: Persist user preferences (dark mode, column settings) across sessions

---

### 2. **workspace-guidelines.md** (198 lines)
**Source**: Imported from `/home/owner/Documents/johnkimball/Marketplace-Bulk-Master-2/.augment/rules/` and adapted for this workspace

**Contains workspace-specific guidelines**:

- **Workspace Structure**: Repository location and GitHub Pages URL
- **Pre-Flight Checklist**: Verify repository, directory, file structure before edits
- **Testing Requirements**: Selenium testing protocols (local + live URL)
- **Selenium Best Practices**: Chrome with CDP for console logging
- **Deployment Workflow**: Test → Commit → Push → Wait → Test live URL
- **Common Pitfalls**: False success claims, hidden console errors, scope creep
- **Development Server**: Commands for dev, build, preview
- **File Structure**: Current project structure
- **Evidence-Based Development**: All claims must have evidence

---

### 3. **new_rules.md**
**Source**: Pre-existing in this workspace

Contains additional workspace-specific rules.

---

## Key Principles

### 🔍 Evidence-Based
- No claims without proof
- Show full terminal output
- Capture console logs
- Test both local and live URLs

### 🛑 Stop-the-Line
- Stop on tool conflicts
- Stop on workspace ambiguity
- Stop on unverified claims
- Ask for clarification

### 📋 Scope Control
- Fix only what's requested
- Don't add unrequested features
- Don't refactor unrelated code
- Ask before expanding scope

### 🧪 Testing Protocol
1. Test locally with Selenium
2. Deploy to production
3. Test live URL with Selenium
4. Show all test output

### 🎯 User Constraints
- User constraints override defaults
- Constraints remain active until revoked
- Examples: "do not guess", "use full paths", "Selenium required"

---

## Usage

These rules are automatically applied to all AI assistant interactions in this workspace through the Augment system.

**Type**: `always_apply` - Rules are always active

---

## Maintenance

**Last Updated**: 2025-12-19  
**Imported From**: Marketplace-Bulk-Master-2 workspace  
**Adapted For**: marketplace-bulk-editor workspace  

### Customization

The `workspace-guidelines.md` file has been customized for this workspace:
- Repository path: `/home/owner/Documents/694533e8-ac54-8329-bbf9-22069a0d424e/marketplace-bulk-editor`
- GitHub Pages: https://swipswaps.github.io/marketplace-bulk-editor/
- File structure reflects current project layout

The `mandatory-rules.md` file is universal and applies to all workspaces.

---

## Related Documentation

- **IMPROVEMENT_PLAN.md** - Comprehensive plan for app improvements
- **IMPLEMENTATION_SUMMARY.md** - Quick reference for improvements
- **QUICK_START_GUIDE.md** - Setup instructions
- **README_IMPROVEMENTS.md** - Overview of improvement documentation

---

## Rule Enforcement

These rules help ensure:
- ✅ Correct workspace identification
- ✅ Evidence-based claims
- ✅ Proper testing protocols
- ✅ Scope containment
- ✅ User constraint compliance
- ✅ Professional communication
- ✅ Security best practices

**Violations of these rules should be corrected immediately.**

