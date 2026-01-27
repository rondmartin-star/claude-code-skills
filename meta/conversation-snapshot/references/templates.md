# Snapshot Reference

Load when creating snapshots. Contains condensed templates. **Keep all outputs lean.**

---

## Distillation Examples

### Verbose (Don't)
```
During our conversation, we discussed several approaches to handling 
authentication. After considering OAuth, JWT tokens, and session-based 
auth, we ultimately decided to go with session-based authentication 
because it's simpler to implement and doesn't require external services.
```

### Distilled (Do)
```
**Auth:** Session-based (simpler, no external deps)
```

### Verbose (Don't)
```
## Errors Encountered

### Error 1
We encountered an error when trying to create a new service. The error 
message was "TypeError: 'service_time' is an invalid keyword argument 
for Service". This happened because the route was using 'service_time' 
as the parameter name but the model column is named 'time'. We fixed 
this by changing the parameter name in the route to match the model.
```

### Distilled (Do)
```
| Error | Cause | Fix |
|-------|-------|-----|
| Invalid kwarg 'service_time' | Route param ≠ model column | Use `time` not `service_time` |
```

---

## Chat Snapshot Templates

### SNAPSHOT.md (~3 KB target)

```markdown
# Snapshot: [identifier]
[YYDDD-HHMM] | [project] | [reason]

## Summary
[2-3 sentences max: goal, outcome, state]

## Decisions
| Decision | Choice | Why |
|----------|--------|-----|

## Outputs
| File | Status |
|------|--------|

## Learnings
- [Learning]: [application]

## Errors
| Error | Fix | Prevent |
|-------|-----|---------|

## Open
- Q: [questions]
- I: [issues]
- T: [tasks]

## Next
1. [priority 1]
2. [priority 2]
```

### CONTINUATION-PROMPT.md (~1 KB target)

```markdown
Continuing from snapshot. Project knowledge uploaded.

**Project:** [name] | **State:** [phase] | **Snapshot:** [YYDDD-HHMM]

**Context:** [1-2 sentences]

**Decisions (final):**
- [decision]: [rationale]

**Attached:** [files]

**Next:** [first action]

Confirm context, then proceed.
```

---

## Project Snapshot Templates

### 1-PROJECT-CONTEXT.md (~2 KB target)

```markdown
# [Project Name]

**Purpose:** [one line]
**Scope:** [in/out]
**Success:** [criteria]

## Decisions
| Area | Decision | Why |
|------|----------|-----|

## Architecture
[2-3 sentences or simple diagram]

## Constraints
- Must: [list]
- Must not: [list]
```

### 1-CONSOLIDATED-LEARNINGS.md (~2 KB target)

```markdown
# Learnings

## Patterns
| Pattern | Use When |
|---------|----------|

## Do / Don't
| Do | Don't |
|----|-------|
```

### 1-ERROR-PREVENTION.md (~1 KB target)

```markdown
# Error Prevention

| Error | Prevention |
|-------|------------|

## Checks
- [ ] [validation 1]
- [ ] [validation 2]
```

### 3-CURRENT-STATE.md (~1 KB target)

```markdown
# State

| Area | % | Status |
|------|---|--------|

**Done:** [list]
**In Progress:** [item]: [status]
**Blocked:** [if any]
```

### 3-OPEN-ITEMS.md (~1 KB target)

```markdown
# Open

**Questions:** [list]
**Issues:** [list]
**Tasks:** P0: [list] | P1: [list]
**Decisions needed:** [list]
```

### README.md (Package Root)

```markdown
# [Project] Snapshot
[YYDDD-HHMM]

## Setup
1. Create project
2. Upload `1-*/` to Knowledge
3. Copy `2-*/instructions.md` to Instructions  
4. Chat: upload `3-*/`, paste CONTINUATION-PROMPT.md

## Folders
1=Knowledge | 2=Instructions | 3=First chat | 4=Outputs | 5=Archive
```

---

## Checklist

- [ ] Each file under size target?
- [ ] Tables instead of prose?
- [ ] Only continuation-relevant content?
- [ ] No redundancy across files?
- [ ] Prompt is self-contained?

---

*End of Reference*
