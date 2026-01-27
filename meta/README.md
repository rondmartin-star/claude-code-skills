# Meta Skills - Ecosystem Management

Skills for managing and maintaining the Claude Code skills ecosystem itself.

**Category:** Meta
**Skills:** 4
**Total Size:** ~26KB

---

## Skills in This Category

### skill-ecosystem-manager (~8KB)
**Purpose:** Create, maintain, and improve skills based on error-driven development

**When to use:**
- Creating new skills
- Refactoring existing skills
- Improving skills based on logged errors
- Managing multi-skill workflows

**Key features:**
- Skill design philosophy
- Ecosystem architecture patterns
- Error-driven improvement workflow
- Continuous refinement process

### conversation-snapshot (~6KB + refs)
**Purpose:** Create portable snapshots of chats or entire projects for seamless continuation

**When to use:**
- Approaching context limits
- Completing a work phase
- Archiving progress
- Preparing to continue work in a new chat or project

**Key features:**
- Captures state, outputs, decisions, learnings
- Portable format for context transfer
- Minimal overhead (<10KB typically)
- Includes continuation instructions

### navigation-auditor (~7KB + 15KB ref)
**Purpose:** Verify that all features have complete navigation paths

**When to use:**
- After adding new features
- Validating CLAUDE.md navigation documentation
- Generating navigation tests
- Auditing feature reachability

**Key features:**
- Navigation registry validation
- Multi-level navigation (sidebar → tabs → cards)
- Breadcrumb pattern generation
- Navigation testing templates

**References:**
- navigation-patterns.md (15KB) - Complete navigation implementation patterns

### plugin-ecosystem (~5KB)
**Purpose:** Manage integration with external skills and plugins

**When to use:**
- Integrating third-party skills
- Managing plugin dependencies
- Coordinating with external ecosystems

**Key features:**
- Plugin discovery and loading
- Dependency management
- Version compatibility checking

---

## Usage Patterns

### Pattern 1: Creating a New Skill

```
User: "Create a new skill for testing FastAPI applications"
→ Load skill-ecosystem-manager
→ Follow skill design philosophy
→ Create SKILL.md with proper structure
→ Add reference files as needed
→ Validate with quick_validate.py
→ Update category README
```

### Pattern 2: Improving Existing Skill

```
User: "Update windows-app-build based on recent errors"
→ Load skill-ecosystem-manager
→ Review ERROR-AND-FIXES-LOG.md
→ Identify patterns in errors
→ Update SKILL.md or reference files
→ Add regression tests
→ Document in CHANGELOG.md
```

### Pattern 3: Context Preservation

```
User: "Save current project state before switching contexts"
→ Load conversation-snapshot
→ Capture current work (code, decisions, next steps)
→ Generate portable snapshot file
→ User can resume in new chat with snapshot
```

### Pattern 4: Navigation Audit

```
User: "Verify all features are reachable from main navigation"
→ Load navigation-auditor
→ Read CLAUDE.md navigation section
→ Check all routes defined
→ Verify entry points exist
→ Generate navigation tests
→ Report any unreachable features
```

---

## Meta Skill Coordination

Meta skills often work together:

**Skill creation workflow:**
1. skill-ecosystem-manager → Design and create new skill
2. navigation-auditor → Verify skill is discoverable
3. conversation-snapshot → Archive creation session

**Skill improvement workflow:**
1. skill-ecosystem-manager → Analyze errors and improve
2. conversation-snapshot → Save improved skill state

**Ecosystem migration:**
1. conversation-snapshot → Capture current ecosystem state
2. skill-ecosystem-manager → Apply to new environment
3. navigation-auditor → Verify all skills accessible

---

## Best Practices

### When Creating Skills

1. **Follow 15KB guideline** - Keep SKILL.md concise
2. **Use reference files** - Detailed content in separate files
3. **Document triggers** - Clear "when to load" criteria
4. **Add README** - Skill-level README for quick reference
5. **Test thoroughly** - Validate with quick_validate.py

### When Improving Skills

1. **Log errors first** - Document in ERROR-AND-FIXES-LOG.md
2. **Create regression tests** - Prevent re-occurrence
3. **Update incrementally** - Small, focused changes
4. **Version tracking** - Increment version numbers
5. **Document changes** - Update CHANGELOG.md

### When Managing Ecosystem

1. **Regular audits** - Periodic navigation and size checks
2. **Dependency tracking** - Document skill relationships
3. **Archive snapshots** - Before major refactoring
4. **Version control** - Use git for skill files

---

## Related Skills

- **windows-app-orchestrator** - Coordinates development workflow
- **security-patterns-orchestrator** - Coordinates security skills
- **publishing-orchestrator** - Coordinates content creation

---

*Meta Skills Category - Ecosystem Management and Maintenance*
