# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

---

## 🚨 CRITICAL OPERATIONAL RULES (READ FIRST)

You must follow these rules before writing a single line of code.

### 1. Infrastructure Lock
You are **STRICTLY FORBIDDEN** from modifying infrastructure files without explicit, written user permission:
- `.env` (environment variables)
- `docker-compose.yml` (container configuration)
- `terraform/` (infrastructure as code)
- Database connection strings
- Port configurations (localhost:3000, localhost:8000, etc.)

**Drift Prevention:** If a code change requires an infrastructure change, STOP and propose the plan first.

### 2. No "Flailing" - Three Strikes Rule
- If a fix fails **twice**, STOP immediately
- Do NOT guess a third time
- Report the error clearly
- Restore the previous working state
- Ask the user for guidance

**Apply the Three Strikes Rule:**
```
Attempt 1 fails → Try different approach
Attempt 2 fails → STOP and analyze
Is this a hard blocker? (permission, file lock, environment)
  YES → Request user action, WAIT
  NO  → Try one more targeted approach with user approval
```

### 3. Do No Harm
**NEVER** fix a bug by:
- Deleting a feature
- Downgrading a requirement
- Removing functionality
- Disabling critical components

Example of harm: "I disabled the database to fix the loading spinner" ❌

### 4. Plan → Act
For any task involving:
- More than 1 file
- Cross-stack logic (Frontend ↔ Backend)
- Database schema changes
- API modifications

You MUST:
1. Outline your plan in bullet points
2. Wait for confirmation
3. Then proceed with implementation

### 5. Never Downgrade Tools
Do NOT downgrade versions without explicit user request:
- LLM models (e.g., GPT-4 → GPT-3.5)
- Dependencies (e.g., React 18 → React 17)
- Paid services or APIs
- Database engines

If downgrade seems necessary, make a recommendation and consult first.

### 6. Never Modify Production Data
**NEVER** without explicit permission:
- Delete database entries
- Modify existing user data
- Clear caches that contain user content
- Truncate tables
- Drop indexes

### 7. Test Before Complete
**NEVER** say a task is complete until you:
1. Test the change end-to-end
2. Verify both frontend and backend (if applicable)
3. Run relevant test suites
4. Check for regressions

Use Playwright for UI testing when available.

### 8. Commit Every Change
**Commit ALL changes immediately:**
- After each logical unit of work
- After each feature implementation
- After each bug fix
- Before and after risky operations

Do NOT batch commits. Do NOT skip commits.

### 9. Never Downgrade UI
Assume the current UI is the **final approved design**.
- Do NOT revert to previous commits
- Do NOT "simplify" existing styling
- Do NOT remove animations or interactions
- Do NOT change color schemes

Only modify UI when explicitly requested.

### 10. Memory-Conscious Operations
On resource-constrained environments:
- Check available RAM before Docker rebuilds
- Use memory-efficient algorithms
- Stream large datasets instead of loading into memory
- Clean up resources after operations

**Prompt awareness:** "I only have 4GB RAM on this VPS, do it in memory-efficient manner"

### 11. Context Management
**To maintain quality across long sessions:**
- Save every changelog step to `milestone.md`
- Update key summary after significant changes
- When reopened, study `milestone.md` to regain full context
- Keep `milestone.md` concise (key decisions, not play-by-play)

### 12. Playwright for UI Debugging
For pixel-perfect UI work:
1. Spin up Playwright browser instance
2. Open localhost
3. Iterate based on visual feedback (not code inspection)

**Do NOT** try to fix UI issues by staring at code. Look at the rendered page.

---

## 📋 Project-Specific Rules

*Add your project-specific imperatives here (limit to 20 total rules)*

Example project rules:
```
13. Supabase database uses port 6543 (Pooler mode). Never change to 5432 (Session mode).
14. All API endpoints must include rate limiting
15. Never expose internal IDs in public APIs (use UUIDs)
16. All user input must be sanitized before database queries
```

---

## 🎯 Effort Level Management

Use `/model` to control effort level:
- **low** - Simple tasks, quick fixes, known patterns
- **medium** - Most development work (default)
- **high** - Complex refactoring, architectural changes, debugging

**Guideline:** Don't use "high" effort for simple problems (wastes tokens). Don't use "low" effort for complex problems (poor quality).

---

## 🧠 Memory Management Patterns

### Milestone Tracking
Automatically maintain `milestone.md` with:
- Session summaries
- Key architectural decisions
- Major feature completions
- Breaking changes introduced
- Known issues and workarounds

**Format:**
```markdown
# Project Milestones

## 2026-02-13 - Authentication System
- Implemented OAuth 2.0 with Google provider
- Added user session management
- Known issue: Refresh tokens not implemented yet

## 2026-02-12 - Database Schema
- Created users, posts, comments tables
- Added indexes on frequently queried columns
- Migration files: 001_initial.sql, 002_add_indexes.sql
```

### Context Preservation
Before compaction (at ~200-300k tokens):
- Ensure `milestone.md` is current
- Preserve critical architectural decisions
- Save any ongoing debugging context
- Document incomplete work clearly

---

## 🛠️ Tool-Specific Guidance

### Playwright Usage
Load Playwright MCP: `/plugin playwright`

**For UI development:**
```
Spin out an instance of Playwright browser, open http://localhost:3000
and I'll guide you from there in terms of UI improvements.
```

**For testing:**
- Use headless mode on CI/CD
- Take screenshots on test failures
- Record videos for complex interactions

### Git Workflow
**Branch strategy:**
- `main` - Production (stable, tested)
- `stage` - Development (integration testing)
- `feature/*` - Feature branches (short-lived)

**Commit messages:**
```
<type>: <description>

Types: feat, fix, docs, style, refactor, test, chore
Examples:
- feat: Add user authentication with OAuth
- fix: Resolve database connection timeout
- refactor: Extract payment processing to service layer
```

### Docker Operations
On memory-constrained systems:
```bash
# Build images one at a time
# Use --no-cache sparingly
# Clean up dangling images after builds
docker system prune -f
```

---

## 🚀 Testing Requirements

### Before Declaring Complete
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] No console errors
- [ ] No broken links
- [ ] Responsive on mobile/desktop
- [ ] Accessibility check (basic)

### Playwright End-to-End Tests
For critical flows:
- User registration/login
- Payment processing
- Data submission
- Content publishing

---

## 📊 Performance Budgets

*Define performance expectations*
- Page load time: < 2s
- API response time: < 500ms
- Bundle size: < 500KB (main)
- Lighthouse score: > 90

If changes degrade performance, report and discuss optimization.

---

## 🔒 Security Checklist

Before deploying security-sensitive changes:
- [ ] No hardcoded credentials
- [ ] No API keys in source code
- [ ] Input validation on all user data
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection implemented
- [ ] Authentication required for protected routes
- [ ] Authorization checks on all operations

---

## 📝 Documentation Requirements

Keep updated automatically:
- `CHANGELOG.md` - All user-facing changes
- `milestone.md` - Development progress
- `README.md` - Setup and usage instructions
- API docs - OpenAPI/Swagger for all endpoints

---

## 🎨 UI/UX Guidelines

*Define design system constraints*
- Color palette: [Primary, Secondary, Accent, ...]
- Typography: [Font families, sizes, weights]
- Spacing: [8px grid, margins, padding]
- Components: [Use existing component library]

**Never introduce new colors or fonts without approval.**

---

## 🔄 Release Cycle

*Define deployment cadence*
- Development: Continuous (auto-deploy to stage)
- Staging: Daily merges from feature branches
- Production: Weekly releases (Friday 5 PM)

**Pre-release checklist:**
- [ ] All tests passing
- [ ] Staging tested by QA
- [ ] Database migrations tested
- [ ] Rollback plan documented
- [ ] Monitoring alerts configured

---

## 💡 Best Practices Learned

*Track lessons from this project*

### What Works Well
- Playwright for UI iteration (saves 60% debugging time)
- Pre-startup checks catch 95% of environment issues
- Committing every change enables easy rollback
- milestone.md preserves context across sessions

### What to Avoid
- Attempting 10+ workarounds for hard blockers (use Three Strikes Rule)
- Fixing UI by reading code instead of using Playwright
- Modifying .env without explicit permission
- Declaring complete without testing

---

## 📚 Quick Reference

### Common Commands
```bash
# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build

# Database migrations
npm run migrate

# Start Playwright
/plugin playwright
```

### Debugging Workflow
1. Reproduce the issue
2. Check logs (console, server, database)
3. Use Playwright if UI-related
4. Add targeted console.log statements
5. Test fix thoroughly
6. Remove debug logging
7. Commit

### When Stuck
1. Check `milestone.md` for context
2. Review recent commits
3. Check issue tracker
4. Ask user for clarification
5. Do NOT guess blindly

---

*Last Updated: 2026-02-13*
*Template Version: 1.0*
*Based on: Claude Code Advanced Guide (Corp Waters, Feb 2026)*
