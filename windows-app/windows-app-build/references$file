# Plugin Integration for Windows App Build

This reference documents how to integrate installed plugins with the windows-app-build skill workflow.

---

## Complementary Plugins

| Plugin | Purpose | When to Use |
|--------|---------|-------------|
| `code-simplifier` | Simplify and refine code | After implementation |
| `code-review` | Automated PR review | Before commit |
| `pr-review-toolkit` | 6 specialized review agents | Thorough review |
| `security-guidance` | Security warnings | Always active (auto) |
| `feature-dev` | 7-phase development | Complex features |

---

## Integration Points

### After ADD Mode (New Feature)

1. **Implement** using windows-app-build patterns
2. **Simplify** with code-simplifier:
   ```
   Task(subagent_type="code-simplifier:code-simplifier",
        prompt="Simplify the [feature] implementation")
   ```
3. **Review** with code-review:
   ```
   /code-review
   ```

### After FIX Mode (Bug Fix)

1. **Fix** the specific issue
2. **Verify** error handling:
   ```
   "Check for silent failures in [module]"
   → Triggers: silent-failure-hunter
   ```
3. **Review** the fix:
   ```
   "Review my recent changes"
   → Triggers: code-reviewer
   ```

### Before SHIP Mode (Delivery)

Run comprehensive review:

```
"I'm preparing to deliver this package. Please:
1. Review test coverage
2. Check for silent failures
3. Verify code quality
4. Simplify any complex code"
```

This triggers:
- `pr-test-analyzer` - Test coverage
- `silent-failure-hunter` - Error handling
- `code-reviewer` - Code quality
- `code-simplifier` - Code clarity

---

## Plugin Usage Patterns

### code-simplifier

**Purpose:** Simplify code for clarity and maintainability

**When:** After any significant implementation

**How:**
```python
Task(
    subagent_type="code-simplifier:code-simplifier",
    prompt="Simplify the recently modified code in app/routes/"
)
```

**What it does:**
- Removes duplicate code
- Consolidates related logic
- Improves naming
- Reduces nesting
- Follows project standards from CLAUDE.md

### code-review

**Purpose:** Quick automated code review

**When:** Before committing changes

**How:**
```
/code-review
```

**What it does:**
- Checks CLAUDE.md compliance
- Finds style violations
- Detects potential bugs
- Rates issues by confidence (0-100)

### pr-review-toolkit Agents

**Purpose:** Specialized deep reviews

| Agent | Focus | Trigger |
|-------|-------|---------|
| `comment-analyzer` | Comment accuracy | "Check if comments are accurate" |
| `pr-test-analyzer` | Test coverage | "Check if tests are thorough" |
| `silent-failure-hunter` | Error handling | "Check for silent failures" |
| `type-design-analyzer` | Type design | "Review the type design" |
| `code-reviewer` | General quality | "Review my changes" |

### security-guidance

**Purpose:** Automatic security warnings

**When:** Always active when editing files

**What it warns about:**
- Command injection risks
- XSS vulnerabilities
- SQL injection patterns
- Unsafe code patterns

---

## Recommended Workflow

```
┌─────────────────┐
│ 1. Implement    │  ← windows-app-build skill
│    (ADD/FIX)    │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. Simplify     │  ← code-simplifier plugin
│                 │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. Review       │  ← code-review / pr-review-toolkit
│                 │
└────────┬────────┘
         ▼
┌─────────────────┐
│ 4. Commit       │  ← commit-commands plugin
│                 │     /commit or /commit-push-pr
└────────┬────────┘
         ▼
┌─────────────────┐
│ 5. Ship         │  ← windows-app-build SHIP mode
│    (Checklist)  │
└─────────────────┘
```

---

## Cross-Reference

- **Full plugin documentation:** `plugin-ecosystem` skill
- **Workflow patterns:** `plugin-ecosystem/references/workflow-patterns.md`
- **Plugin registry:** `plugin-ecosystem` SKILL.md

---

*End of Plugin Integration Reference*
