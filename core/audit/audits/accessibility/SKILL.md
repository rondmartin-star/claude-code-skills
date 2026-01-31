---
name: accessibility
description: >
  Accessibility audit checking WCAG compliance, semantic HTML, ARIA attributes, keyboard
  navigation, and screen reader support. Validates inclusive user experience. Use when:
  accessibility review, WCAG validation, or part of user methodology audits.
---

# Accessibility Audit

**Purpose:** Comprehensive accessibility validation (WCAG 2.1 AA)
**Type:** Audit Type (Part of User Methodology)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Audit accessibility"
- "Check WCAG compliance"
- "Validate screen reader support"
- "Check keyboard navigation"

**Context Indicators:**
- Accessibility compliance required
- Part of convergence (user methodology)
- Pre-release validation
- Legal/regulatory requirements

---

## Accessibility Checks

### 1. Semantic HTML

**Check for:**
- Proper heading hierarchy (h1 → h2 → h3)
- Semantic elements vs divs
- Form labels
- Button vs div with onclick

**Detection:**
```javascript
function checkSemanticHTML(ast) {
  const issues = [];
  const headings = [];

  traverse(ast, {
    JSXElement: (path) => {
      const tagName = path.node.openingElement.name.name;

      // Check heading hierarchy
      if (/^h[1-6]$/.test(tagName)) {
        const level = parseInt(tagName[1]);
        headings.push({ level, loc: path.node.loc });

        if (headings.length > 1) {
          const prevLevel = headings[headings.length - 2].level;
          if (level > prevLevel + 1) {
            issues.push({
              type: 'heading_skip',
              location: path.node.loc,
              from: prevLevel,
              to: level,
              severity: 'medium',
              suggestion: `Don't skip heading levels (h${prevLevel} to h${level})`
            });
          }
        }
      }

      // Check divs with onClick
      if (tagName === 'div') {
        const hasOnClick = path.node.openingElement.attributes.some(
          attr => attr.name?.name === 'onClick'
        );

        if (hasOnClick) {
          issues.push({
            type: 'div_with_click',
            location: path.node.loc,
            severity: 'high',
            suggestion: 'Use <button> instead of <div onClick>'
          });
        }
      }

      // Check form inputs without labels
      if (['input', 'select', 'textarea'].includes(tagName)) {
        if (!hasAssociatedLabel(path)) {
          issues.push({
            type: 'missing_label',
            element: tagName,
            location: path.node.loc,
            severity: 'high',
            suggestion: 'Add <label> or aria-label'
          });
        }
      }
    }
  });

  return issues;
}
```

### 2. ARIA Attributes

**Required ARIA:**
- `aria-label` or `aria-labelledby` for interactive elements
- `role` for custom components
- `aria-hidden` for decorative elements
- `aria-live` for dynamic content

**Detection:**
```javascript
function checkARIA(ast) {
  const issues = [];

  traverse(ast, {
    JSXElement: (path) => {
      const tag = path.node.openingElement.name.name;
      const attrs = path.node.openingElement.attributes;

      // Custom interactive elements need role
      if (isCustomComponent(tag) && hasInteraction(attrs)) {
        const hasRole = attrs.some(a => a.name?.name === 'role');

        if (!hasRole) {
          issues.push({
            type: 'missing_role',
            component: tag,
            location: path.node.loc,
            severity: 'high',
            suggestion: 'Add role attribute (button, link, etc.)'
          });
        }
      }

      // Icons need aria-hidden or aria-label
      if (isIcon(tag)) {
        const hasAriaHidden = attrs.some(a =>
          a.name?.name === 'aria-hidden' && a.value?.value === 'true'
        );
        const hasAriaLabel = attrs.some(a =>
          a.name?.name === 'aria-label'
        );

        if (!hasAriaHidden && !hasAriaLabel) {
          issues.push({
            type: 'icon_without_aria',
            location: path.node.loc,
            severity: 'medium',
            suggestion: 'Add aria-hidden="true" or aria-label'
          });
        }
      }

      // Check invalid ARIA combinations
      const role = getAttrValue(attrs, 'role');
      if (role && !isValidARIARole(role)) {
        issues.push({
          type: 'invalid_aria_role',
          role,
          location: path.node.loc,
          severity: 'high',
          suggestion: 'Use valid ARIA role'
        });
      }
    }
  });

  return issues;
}
```

### 3. Color Contrast

**WCAG Requirements:**
- Normal text: 4.5:1 contrast ratio (AA)
- Large text: 3:1 contrast ratio (AA)
- Enhanced: 7:1 for normal, 4.5:1 for large (AAA)

**Detection:**
```javascript
async function checkColorContrast(styles) {
  const issues = [];

  for (const rule of styles) {
    const fg = rule.color;
    const bg = rule.backgroundColor;

    if (fg && bg) {
      const ratio = calculateContrastRatio(fg, bg);
      const fontSize = parseFloat(rule.fontSize);
      const isLarge = fontSize >= 18 || (fontSize >= 14 && rule.fontWeight >= 700);

      const threshold = isLarge ? 3.0 : 4.5;

      if (ratio < threshold) {
        issues.push({
          type: 'low_contrast',
          selector: rule.selector,
          ratio: ratio.toFixed(2),
          required: threshold,
          foreground: fg,
          background: bg,
          severity: 'high',
          suggestion: `Increase contrast (current: ${ratio.toFixed(2)}, required: ${threshold})`
        });
      }
    }
  }

  return issues;
}

function calculateContrastRatio(fg, bg) {
  const fgLum = getRelativeLuminance(fg);
  const bgLum = getRelativeLuminance(bg);
  const lighter = Math.max(fgLum, bgLum);
  const darker = Math.min(fgLum, bgLum);
  return (lighter + 0.05) / (darker + 0.05);
}
```

### 4. Keyboard Navigation

**Requirements:**
- All interactive elements focusable
- Logical tab order
- Focus visible
- No keyboard traps

**Detection:**
```javascript
function checkKeyboardNav(ast) {
  const issues = [];

  traverse(ast, {
    JSXElement: (path) => {
      const attrs = path.node.openingElement.attributes;
      const hasOnClick = attrs.some(a => a.name?.name === 'onClick');
      const tabIndex = getAttrValue(attrs, 'tabIndex');

      // Interactive elements need to be focusable
      if (hasOnClick && tabIndex === '-1') {
        issues.push({
          type: 'unfocusable_interactive',
          location: path.node.loc,
          severity: 'critical',
          suggestion: 'Remove tabIndex="-1" or use button element'
        });
      }

      // Negative tabIndex on non-interactive
      if (tabIndex && parseInt(tabIndex) < -1) {
        issues.push({
          type: 'invalid_tabindex',
          tabIndex,
          location: path.node.loc,
          severity: 'medium',
          suggestion: 'Use 0 or -1 for tabIndex'
        });
      }

      // Positive tabIndex (discouraged)
      if (tabIndex && parseInt(tabIndex) > 0) {
        issues.push({
          type: 'positive_tabindex',
          tabIndex,
          location: path.node.loc,
          severity: 'low',
          suggestion: 'Avoid positive tabIndex, use DOM order'
        });
      }
    }
  });

  return issues;
}
```

### 5. Images and Media

**Requirements:**
- Images have alt text
- Decorative images have empty alt
- Media has captions/transcripts
- No autoplay without controls

**Detection:**
```javascript
function checkImages(ast) {
  const issues = [];

  traverse(ast, {
    JSXElement: (path) => {
      const tag = path.node.openingElement.name.name;
      const attrs = path.node.openingElement.attributes;

      // Images need alt
      if (tag === 'img') {
        const alt = getAttrValue(attrs, 'alt');

        if (alt === undefined) {
          issues.push({
            type: 'missing_alt',
            location: path.node.loc,
            severity: 'critical',
            suggestion: 'Add alt attribute (empty for decorative images)'
          });
        }
      }

      // Video/audio need captions
      if (['video', 'audio'].includes(tag)) {
        const hasTrack = path.node.children.some(
          child => child.openingElement?.name.name === 'track'
        );

        if (!hasTrack) {
          issues.push({
            type: 'missing_captions',
            element: tag,
            location: path.node.loc,
            severity: 'high',
            suggestion: 'Add <track> element for captions'
          });
        }

        // Check autoplay
        const autoplay = getAttrValue(attrs, 'autoplay');
        if (autoplay) {
          issues.push({
            type: 'autoplay_media',
            element: tag,
            location: path.node.loc,
            severity: 'medium',
            suggestion: 'Remove autoplay or provide controls'
          });
        }
      }
    }
  });

  return issues;
}
```

### 6. Forms

**Requirements:**
- Labels for all inputs
- Error messages
- Required field indication
- Fieldset/legend for groups

**Detection:**
```javascript
function checkForms(ast) {
  const issues = [];

  traverse(ast, {
    JSXElement: (path) => {
      const tag = path.node.openingElement.name.name;
      const attrs = path.node.openingElement.attributes;

      if (tag === 'input') {
        // Required fields need indication
        const required = getAttrValue(attrs, 'required');
        const ariaRequired = getAttrValue(attrs, 'aria-required');

        if (required === 'true' && !ariaRequired) {
          issues.push({
            type: 'missing_aria_required',
            location: path.node.loc,
            severity: 'low',
            suggestion: 'Add aria-required="true"'
          });
        }

        // Error states
        const hasError = hasErrorState(path);
        const ariaInvalid = getAttrValue(attrs, 'aria-invalid');

        if (hasError && !ariaInvalid) {
          issues.push({
            type: 'missing_aria_invalid',
            location: path.node.loc,
            severity: 'high',
            suggestion: 'Add aria-invalid="true" for error state'
          });
        }
      }

      // Radio/checkbox groups need fieldset
      if (tag === 'form' && hasRadioOrCheckboxGroup(path)) {
        const hasFieldset = path.node.children.some(
          child => child.openingElement?.name.name === 'fieldset'
        );

        if (!hasFieldset) {
          issues.push({
            type: 'missing_fieldset',
            location: path.node.loc,
            severity: 'medium',
            suggestion: 'Wrap radio/checkbox groups in <fieldset>'
          });
        }
      }
    }
  });

  return issues;
}
```

### 7. Focus Management

**Requirements:**
- Focus visible (outline)
- Focus order logical
- Modal focus trap
- Focus restoration

**Detection:**
```javascript
function checkFocus(styles) {
  const issues = [];

  styles.forEach(rule => {
    // Check for outline: none without alternative
    if (rule.outline === 'none' || rule.outline === '0') {
      const hasFocusStyle =
        rule.boxShadow ||
        rule.border ||
        rule.backgroundColor !== rule.backgroundColorBase;

      if (!hasFocusStyle) {
        issues.push({
          type: 'no_focus_indicator',
          selector: rule.selector,
          severity: 'critical',
          suggestion: 'Provide visible focus indicator'
        });
      }
    }
  });

  return issues;
}
```

---

## Configuration

### corpus-config.json

```json
{
  "audit": {
    "convergence": {
      "methodologies": [
        {
          "name": "user",
          "audits": [
            {
              "id": "accessibility",
              "config": {
                "wcag_level": "AA",
                "check_color_contrast": true,
                "min_contrast_ratio": 4.5,
                "check_keyboard_nav": true,
                "check_screen_reader": true,
                "check_aria": true,
                "check_semantic_html": true,
                "excluded_paths": [
                  "test/**",
                  "**/*.test.jsx"
                ]
              }
            }
          ]
        }
      ]
    }
  }
}
```

---

## Auto-Fix Capabilities

### ✓ Fully Automatic

**Missing alt attributes:**
```
Issue: <img> without alt
Fix: Add alt="" for decorative, suggest descriptive text
Strategy: Safe default (empty alt)
```

**ARIA attributes:**
```
Issue: Icon without aria-hidden
Fix: Add aria-hidden="true"
Strategy: Decorative icons can be hidden
```

### ⚠ User Approval Required

**Semantic HTML:**
```
Issue: <div onClick>
Fix: Replace with <button>
Strategy: Generate replacement, user approves
```

**Color Contrast:**
```
Issue: Insufficient contrast (3.2:1)
Fix: Suggest darker/lighter colors
Strategy: Provide color options, user chooses
```

### ✗ Manual Only

**Heading Hierarchy:**
```
Issue: Skip from h1 to h3
Fix: Requires content restructuring
Strategy: Flag for manual review
```

**Focus Management:**
```
Issue: Modal without focus trap
Fix: Requires custom focus logic
Strategy: Provide implementation guidance
```

---

## Output Format

```json
{
  "audit_type": "accessibility",
  "timestamp": "2026-01-31T10:00:00Z",
  "project_path": "/path/to/project",
  "summary": {
    "files_scanned": 85,
    "wcag_level": "AA",
    "semantic_issues": 12,
    "aria_issues": 8,
    "contrast_issues": 5,
    "keyboard_issues": 3,
    "image_issues": 15
  },
  "issues": [
    {
      "severity": "critical",
      "category": "missing_alt",
      "location": "src/components/Hero.jsx:15",
      "suggestion": "Add alt attribute",
      "auto_fixable": true
    },
    {
      "severity": "high",
      "category": "low_contrast",
      "selector": ".button-secondary",
      "ratio": "3.2",
      "required": "4.5",
      "foreground": "#999",
      "background": "#fff",
      "suggestion": "Use #767676 for 4.5:1 contrast",
      "auto_fixable": false
    }
  ]
}
```

---

## Integration with User Methodology

Accessibility audit is part of the **user methodology** in 3-3-1 convergence:

```json
{
  "methodologies": [
    {
      "name": "user",
      "description": "How it's experienced",
      "audits": [
        "accessibility",     // ← This audit
        "content",
        "ux-performance"
      ]
    }
  ]
}
```

**User Perspective:**
- Can all users navigate the interface?
- Is content accessible to screen readers?
- Are color choices inclusive?
- Can keyboard-only users interact?

---

*End of Accessibility Audit*
*Part of v4.0.0 Universal Skills Ecosystem*
*Methodology: User (How it's experienced)*
*WCAG 2.1 AA compliance validation*
