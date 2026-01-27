# Skill Maintenance Reference

Load this file when maintaining skills, integrating error learnings, or refactoring oversized skills.

---

## Error-Driven Improvement Process

### Step 1: Collect Error Data

Sources of improvement data:
- `ERROR-AND-FIXES-LOG.md` from projects
- User feedback ("the skill missed X")
- Validation failures
- Repeated questions in conversations

### Step 2: Categorize Each Error

For each error, determine:

| Question | Answer Options |
|----------|----------------|
| Which skill should own this? | [skill name] or "new skill needed" |
| Is this a quick fix or deep pattern? | quick → error table, deep → reference |
| Is this new or enhancing existing? | new section vs. update existing |
| How often does this occur? | rare (document) vs. frequent (prominent) |

### Step 3: Integrate into Skills

**For Quick Fixes (add to SKILL.md):**

```markdown
## Common Errors Quick Fix

| Error | Cause | Fix |
|-------|-------|-----|
| [new error] | [cause] | [fix] |
```

**For Deep Patterns (add to references/):**

```markdown
### Error N: [Title]

**Error**: [Full error message]

**Symptoms**:
- [Observable symptom 1]
- [Observable symptom 2]

**Root Cause**: [Detailed explanation of why this happens]

**Fix**: 
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Prevention**: [What to add to checklists/audits]

**Integrated**: [Date] from [source project]
```

### Step 4: Update Validation

Add prevention to relevant checklist:

```markdown
## [Phase] Checklist

- [ ] [existing items...]
- [ ] [NEW] Verify [thing that prevents this error]
```

### Step 5: Cross-Reference

If error affects multiple skills:
1. Add quick fix to most relevant skill
2. Add "See also: [other-skill]" reference
3. Consider if orchestrator needs awareness

---

## Refactoring Oversized Skills

### When to Refactor

| Skill Size | Action |
|------------|--------|
| < 15 KB | No action needed |
| 15-20 KB | Plan refactor, identify extractable content |
| 20-25 KB | Refactor soon |
| > 25 KB | Refactor immediately |

### Refactoring Process

**Step 1: Identify Extractable Content**

Look for:
- Long code templates (> 20 lines)
- Detailed step-by-step procedures
- Extended examples
- Full checklists with many items
- CSS/script templates

**Step 2: Create Reference File**

```bash
mkdir -p [skill-name]/references/
```

Move detailed content to appropriately named reference file.

**Step 3: Leave Pointer in SKILL.md**

Replace extracted content with:

```markdown
**For detailed [templates/examples/procedures]:**
\`\`\`
/mnt/skills/user/[skill-name]/references/[file].md
\`\`\`
```

**Step 4: Keep Summary in SKILL.md**

Leave a condensed version:

| Before (in SKILL.md) | After (in SKILL.md) |
|----------------------|---------------------|
| 50-line code template | 5-line summary + pointer |
| 20-item checklist | 5 critical items + pointer |
| 3 detailed examples | 1 example + pointer |

### Refactoring Example

**Before (25 KB SKILL.md):**
```markdown
## Error Patterns

### Pattern 1: Variable Shadowing
[20 lines of explanation]
[15 lines of code example]
[10 lines of fix]

### Pattern 2: ...
[similar length]
```

**After (15 KB SKILL.md):**
```markdown
## Error Patterns Quick Fix

| Pattern | Wrong | Right |
|---------|-------|-------|
| Variable shadowing | `templates = count` | `template_count = count` |
| [pattern 2] | [wrong] | [right] |

**For detailed patterns with examples:**
\`\`\`
/mnt/skills/user/[skill]/references/error-patterns.md
\`\`\`
```

---

## Skill Consolidation

### When to Consolidate

Signs that skills should be merged:
- Significant content overlap (> 30%)
- Users frequently need both together
- One skill is very small (< 5 KB)
- Natural workflow combines them

### Consolidation Process

1. **Identify overlap** - List shared content
2. **Choose primary skill** - Which has broader scope?
3. **Merge content** - Combine, removing duplicates
4. **Update triggers** - Combine trigger phrases
5. **Update orchestrator** - Point to consolidated skill
6. **Deprecate old skill** - Mark as superseded

---

## Skill Splitting

### When to Split

Signs that a skill should be split:
- Size exceeds 25 KB even after moving to references
- Covers multiple distinct phases
- Different users need different parts
- Natural boundaries exist

### Splitting Process

1. **Identify boundaries** - Where does content divide?
2. **Create new skills** - One per logical unit
3. **Distribute content** - Move sections to new homes
4. **Create orchestrator** - If skills work together
5. **Update triggers** - Each skill gets specific triggers
6. **Cross-reference** - Skills point to related skills

---

## Periodic Maintenance Checklist

Run monthly or after major projects:

### Size Audit
```bash
# Check all SKILL.md sizes
for skill in /mnt/skills/user/*/SKILL.md; do
  size=$(wc -c < "$skill")
  if [ $size -gt 15000 ]; then
    echo "WARNING: $skill is $(($size/1024))KB - needs refactor"
  fi
done
```

### Content Review
- [ ] Any new error patterns to add?
- [ ] Any outdated patterns to remove?
- [ ] Any user feedback to address?
- [ ] Any triggers that don't work?
- [ ] Any missing cross-references?

### Ecosystem Health
- [ ] Orchestrator accurately detects all phases?
- [ ] Exit gates are still valid?
- [ ] State file template is current?
- [ ] All skills have README.md?
- [ ] Installation instructions accurate?

---

## Version Management

### When to Version

- Major content additions → increment minor (1.0 → 1.1)
- Structural changes → increment minor (1.1 → 1.2)
- Breaking changes → increment major (1.x → 2.0)
- Error fixes only → note in changelog, no version change

### Changelog Format

```markdown
## Changelog

### v1.2 - YYYY-MM-DD
- Added: [new feature/content]
- Fixed: [error pattern integrated]
- Changed: [refactored section]

### v1.1 - YYYY-MM-DD
- Added: [content]
```

---

## Skill Deprecation

When a skill is superseded:

1. **Add deprecation notice** at top of SKILL.md:
```markdown
> ⚠️ **DEPRECATED**: This skill has been superseded by [new-skill].
> Use [new-skill] instead. This skill will be removed on [date].
```

2. **Update orchestrator** to point to new skill
3. **Keep old skill** for transition period (30-90 days)
4. **Remove old skill** after transition period

---

## Quality Metrics

Track skill ecosystem health:

| Metric | Target | Measure |
|--------|--------|---------|
| Avg SKILL.md size | < 15 KB | `wc -c */SKILL.md` |
| Trigger accuracy | > 90% | User feedback |
| Error coverage | Increasing | Errors in log vs. skill |
| Load time | < 2 skills/prompt | Orchestrator efficiency |
| User satisfaction | Positive | Feedback/complaints ratio |

---

*End of Skill Maintenance Reference*
