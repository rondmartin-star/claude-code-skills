# Orchestrator Routing Rules

## Skill Detection Rules - Detailed

### STEP 1: Check for Explicit Phase Indicators

| If prompt contains... | Load skill... |
|-----------------------|---------------|
| "requirements", "user stories", "what should it do" | requirements |
| "data model", "database schema", "entities" | system-design |
| "UI", "pages", "screens", "workflows", "navigation" | ui-design |
| "logo", "brand", "colors", "styling" | ui-design |
| "OAuth", "Google login", "authentication", "login page" | authentication-patterns |
| "HTTPS", "SSL", "Caddy", "production deployment" | build (HTTPS section) |
| "code", "implement", "fix", "bug", "package", "deliver" | build |
| "form", "file upload", "user input", "CSRF" | build + secure-coding-patterns |
| "security", "XSS", "SQL injection", "authentication" | build + secure-coding-patterns |
| "audit", "check consistency", "verify codebase" | codebase-audit |
| "bulletproof", "pre-commit", "CI/CD", "type checking" | bulletproof-codebase |
| "protect database", "backup verification", "error monitoring" | bulletproof-codebase |
| "auto-start", "boot", "reboot", "supervisor", "health check", "watchdog" | supervision |
| "MSI", "installer", "WiX", "build package", "create installer" | supervision (MSI section) |

### STEP 2: Check for Project State File

If user uploads or references a state file (e.g., `APP-STATE.yaml`):
- Read the `recommended_mode` field
- Load the appropriate skill for that mode

### STEP 3: Infer from Context

| Context Clues | Likely Phase | Load |
|---------------|--------------|------|
| No existing code mentioned | Early phase | requirements |
| Discussing "what" not "how" | Requirements | requirements |
| Discussing structure/architecture | Design | system-design |
| Discussing user interaction | UI Design | ui-design |
| Has existing package/baseline | Implementation | build |
| Mentions specific files/bugs | Fix mode | build |
| "Ready to deliver" | Ship mode | build |

### STEP 4: When Uncertain

Ask the user:
> "I want to load only the skills needed for this task. Are you:
> 1. Defining requirements (what the app should do)
> 2. Designing the system (data model, architecture)
> 3. Designing the UI (pages, workflows)
> 4. Building/fixing/packaging (implementation)
>
> Or tell me what you're working on and I'll determine the right skill."

## Multi-Skill Scenarios

Some tasks may require content from multiple skills:

| Scenario | Skills to Load | Notes |
|----------|----------------|-------|
| "Design data model and plan pages" | system-design + ui-design | Design phases often overlap |
| "Implement feature from scratch" | requirements (briefly) + build | Capture intent, then implement |
| "Fix authentication bug" | build only | Auth patterns are in build |
| "Add new entity and UI" | system-design + build | Design then implement |

**When loading multiple skills:**
- Load the primary skill fully
- Reference specific sections from secondary skill
- Keep total context under 40 KB

## Validation Across Skills

Each skill has its own exit gate checklist. The orchestrator ensures:

1. **Phase transitions** only happen after exit gate passes
2. **Build skill** contains detailed coding/audit validation
3. **Cross-references** are maintained (e.g., UI must cover all user stories)

### Cross-Skill Validation Points

| Checkpoint | Validates |
|------------|-----------|
| Requirements → System Design | All user stories map to entities |
| System Design → UI Design | All entities have UI representation |
| UI Design → Build | All pages have route specifications |
| Build (SHIP) → Delivery | All audits pass |
