---
name: navigation-auditor
description: >
  Verify that all features have complete navigation paths. Checks that new features
  are reachable from expected entry points, validates CLAUDE.md navigation documentation,
  and generates navigation tests. Use when: auditing navigation, checking feature
  reachability, or after adding new features.
---

# Navigation Auditor Skill

**Purpose:** Verify features are reachable from expected UI entry points
**Size:** ~8 KB
**Philosophy:** Features without navigation paths are hidden features

---

## LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "audit navigation"
- "check feature reachability"
- "verify navigation paths"
- "is this feature accessible?"
- "add navigation tests"
- "check if users can reach..."

**Context Indicators:**
- After adding new features (routes + templates)
- Before SHIP mode
- When features seem "hidden" or unreachable
- Updating CLAUDE.md navigation documentation

## DO NOT LOAD WHEN

- General codebase auditing (use codebase-audit plugin)
- Writing navigation code (just write it)
- Simple link fixes

---

## Core Concept: Navigation Chains

A **complete navigation chain** connects a feature to its entry point:

```
Entry Point → Intermediate Links → Feature Page
     ↓              ↓                    ↓
  Sidebar    Settings Tab/Button    Target Template
```

### Example: Asset Attributes Feature

| Step | Element | File Location |
|------|---------|---------------|
| 1 | Sidebar "Settings" link | admin/base.html |
| 2 | "Assets" tab in settings | admin/settings.html |
| 3 | "Manage Asset Attributes" button | admin/settings.html:1208 |
| 4 | Attributes management page | admin/settings/attributes.html |

**All 4 steps must exist** for the feature to be reachable.

---

## Audit Process

### Step 1: Inventory Features

Identify all features that need navigation:

```
1. Scan routes for feature endpoints
   - Routes with templates (not API-only)
   - Admin routes that render pages

2. Scan templates for standalone pages
   - Pages that aren't just partials
   - Pages with unique functionality
```

### Step 2: Trace Navigation Paths

For each feature, verify the chain:

```
Feature: [Name]
Route: [route_name] at [path]
Template: [template_path]

Navigation Chain:
[ ] Entry point exists (sidebar/header link)
[ ] Intermediate links exist (tabs/buttons)
[ ] url_for() points to valid route
[ ] Route handler renders correct template
```

### Step 3: Cross-Reference Documentation

Check CLAUDE.md for navigation references:

```
Pattern: "Settings > X" or "Settings → X"
Pattern: "Admin -> X"
Pattern: "Navigate to X"

For each reference:
- Verify the path exists in actual UI
- Flag discrepancies
```

### Step 4: Validate Help Content

Check help articles for navigation guidance:

```
Pattern: "Go to X"
Pattern: "Click the Y button"
Pattern: "In the Z page"

Verify referenced elements exist
```

---

## Quick Reference Tables

### Common Entry Points

| Entry Point | Location | Typical Features |
|-------------|----------|------------------|
| Sidebar | admin/base.html | Main modules (PMS, AMS, EVMS) |
| Settings tabs | admin/settings.html | Configuration sub-features |
| Page action buttons | detail.html pages | Related actions (duplicate, proposals) |
| Floating buttons | base templates | Help, quick actions |

### Navigation Test Patterns

| What to Test | How to Test |
|--------------|-------------|
| Sidebar link exists | Check base.html for url_for('route') |
| Settings tab exists | Check settings.html for data-bs-target |
| Sub-feature link exists | Check parent page for url_for() |
| Template reachable | Verify file exists at path |

---

## Output Format

### Navigation Audit Results

```markdown
## Navigation Audit: [Project Name]

### Summary
- Features audited: N
- Complete chains: N
- Missing navigation: N
- Documentation mismatches: N

### CRITICAL: Hidden Features
Features with routes/templates but NO navigation path:

| Feature | Route | Template | Missing Element |
|---------|-------|----------|-----------------|
| Asset Attributes | admin.attribute_definitions | settings/attributes.html | Link in Settings > Assets tab |

### HIGH: Documentation Mismatches
CLAUDE.md says X but UI shows Y:

| Documentation Says | Actual UI | Suggested Fix |
|--------------------|-----------|---------------|
| "Settings > Assets > Attributes" | No link in Assets tab | Add link to settings.html |

### Navigation Chains Verified
- [x] Dashboard (Sidebar → dashboard.html)
- [x] Work Requests (Sidebar → requests/list.html)
- [ ] Asset Attributes (Settings → ??? → attributes.html) INCOMPLETE

### Recommended Actions
1. Add link in settings.html Assets tab to attribute_definitions route
2. Update CLAUDE.md to match actual navigation path
3. Add navigation test to prevent regression
```

---

## Generating Navigation Tests

After auditing, generate regression tests:

```python
class TestFeatureNavigation:
    """Verify [Feature] is reachable from [Entry Point]."""

    def test_feature_reachable(self, templates_dir: Path):
        """
        Feature: [Name]
        Expected path: [Entry] > [Intermediate] > [Feature]
        """
        # Step 1: Entry point
        base = templates_dir / "admin" / "base.html"
        assert "[route_name]" in base.read_text(), \
            "[Entry] missing link to [Feature]"

        # Step 2: Intermediate (if applicable)
        settings = templates_dir / "admin" / "settings.html"
        assert "[intermediate_element]" in settings.read_text(), \
            "Settings missing [intermediate] for [Feature]"

        # Step 3: Feature template exists
        feature = templates_dir / "[feature_path]"
        assert feature.exists(), \
            "[Feature] template missing"
```

---

## Integration with Codebase Audit

This skill complements the codebase-audit plugin:

| Auditor | Checks | Navigation Auditor Adds |
|---------|--------|------------------------|
| routes-auditor | Routes exist, url_for valid | Routes are **reachable** from UI |
| ui-auditor | Templates render, filters work | Templates have **navigation paths** |
| docs-auditor | CLAUDE.md matches code | Navigation docs match **actual UI** |

Run navigation audit as 6th agent in parallel with existing 5.

---

## Anti-Pattern: The Hidden Feature

**Symptoms:**
- Route exists and works when URL is typed directly
- Template renders correctly
- No way for users to discover or reach it

**Root Cause:**
- Feature added (route + template) without navigation link
- Link accidentally removed during refactoring
- Settings restructured without updating links

**Prevention:**
- Add navigation test when adding feature
- Include navigation in feature checklist
- Run navigation audit before SHIP

---

## Checklist for New Features

When adding a new feature, verify:

```
[ ] Route created with appropriate name
[ ] Template created and renders
[ ] Navigation link added to appropriate location:
    [ ] Sidebar (for main modules)
    [ ] Settings tab (for configuration)
    [ ] Parent page (for sub-features)
[ ] url_for() uses correct route name
[ ] CLAUDE.md updated with navigation path
[ ] Navigation test added to test_navigation.py
```
