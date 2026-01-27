# Plugin Ecosystem Integration

**Purpose:** Unified registry and integration guide for all installed plugins
**Size:** ~10 KB
**Philosophy:** Know what's available, when to use it, how it integrates

---

## LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "What plugins are available?"
- "Which agent should I use for..."
- "How do I review code?"
- "Help me with feature development"
- "Run a PR review"
- "Simplify this code"

**Context Indicators:**
- User needs code review or simplification
- Feature development workflow needed
- PR preparation or review
- Security concerns
- Need to understand available tooling

## DO NOT LOAD WHEN

- Already using a specific plugin (load that instead)
- Simple single-file edits
- No plugin/agent context needed

---

## Plugin Registry

### Development Workflow Plugins

| Plugin | Type | Purpose | Trigger |
|--------|------|---------|---------|
| **feature-dev** | Command | 7-phase feature development | `/feature-dev [description]` |
| **code-simplifier** | Agent | Simplify/refine code | `Task(subagent_type="code-simplifier:code-simplifier")` |
| **code-review** | Command | Automated PR review | `/code-review` |
| **pr-review-toolkit** | Agents | 6 specialized review agents | See agents below |
| **commit-commands** | Commands | Git workflow automation | `/commit`, `/commit-push-pr` |

### PR Review Toolkit Agents

| Agent | Focus | Trigger Phrase |
|-------|-------|----------------|
| `comment-analyzer` | Comment accuracy | "Check if comments are accurate" |
| `pr-test-analyzer` | Test coverage | "Check if tests are thorough" |
| `silent-failure-hunter` | Error handling | "Check for silent failures" |
| `type-design-analyzer` | Type design quality | "Review the type design" |
| `code-reviewer` | General code review | "Review my changes" |
| `code-simplifier` | Code clarity | "Simplify this code" |

### Security & Quality Plugins

| Plugin | Type | Purpose |
|--------|------|---------|
| **security-guidance** | Hook | Security warnings on file edits |
| **hookify** | Commands | Configure custom hooks |

### Plugin Development

| Plugin | Type | Purpose |
|--------|------|---------|
| **plugin-dev** | Skills/Agents | Create new plugins |
| **agent-sdk-dev** | Agents | Build SDK-based agents |

### Language Server Plugins (LSP)

| Plugin | Language |
|--------|----------|
| typescript-lsp | TypeScript/JavaScript |
| pyright-lsp | Python |
| rust-analyzer-lsp | Rust |
| gopls-lsp | Go |
| clangd-lsp | C/C++ |
| csharp-lsp | C# |
| jdtls-lsp | Java |
| kotlin-lsp | Kotlin |
| swift-lsp | Swift |
| php-lsp | PHP |
| lua-lsp | Lua |

### External Service Plugins

| Plugin | Service | Requires |
|--------|---------|----------|
| github | GitHub API | API token |
| gitlab | GitLab API | API token |
| slack | Slack | Workspace token |
| linear | Linear | API key |
| asana | Asana | API key |
| stripe | Stripe | API key |
| firebase | Firebase | Project config |
| supabase | Supabase | Project config |
| playwright | Browser testing | Node.js |

---

## Integration with Skills

### Windows App Development Ecosystem

| Phase | Skill | Complementary Plugin |
|-------|-------|---------------------|
| Requirements | windows-app-requirements | - |
| UI Design | windows-app-ui-design | frontend-design |
| System Design | windows-app-system-design | - |
| Build | windows-app-build | code-simplifier, security-guidance |
| Review | - | pr-review-toolkit, code-review |
| Supervision | windows-app-supervision | - |

### Recommended Workflow Integration

```
1. Requirements Phase
   ├── Skill: windows-app-requirements
   └── Plugin: - (requirements only)

2. Design Phase
   ├── Skill: windows-app-ui-design OR windows-app-system-design
   └── Plugin: frontend-design (for UI work)

3. Implementation Phase
   ├── Skill: windows-app-build
   ├── Plugin: feature-dev (for complex features)
   ├── Plugin: security-guidance (auto-enabled)
   └── Plugin: code-simplifier (after implementation)

4. Review Phase
   ├── Plugin: code-review (quick review)
   ├── Plugin: pr-review-toolkit (thorough review)
   └── Plugin: commit-commands (git workflow)

5. Deployment Phase
   ├── Skill: windows-app-supervision
   └── Plugin: - (supervision only)
```

---

## Quick Reference: Common Tasks

### "I want to review code"

**Quick review:**
```
/code-review
```

**Thorough review (multiple agents):**
```
Ask: "Run comprehensive PR review with test coverage, error handling, and code quality checks"
```

**Specific concerns:**
- Comments: "Check if comments are accurate"
- Tests: "Check if tests are thorough"
- Errors: "Check for silent failures"
- Types: "Review the type design"

### "I want to simplify code"

**Use code-simplifier agent:**
```
Ask: "Simplify the recently modified code"
```
Or via Task tool:
```python
Task(subagent_type="code-simplifier:code-simplifier", prompt="...")
```

### "I want to build a new feature"

**Use feature-dev workflow:**
```
/feature-dev Add [feature description]
```

This triggers 7-phase workflow:
1. Discovery - Clarify requirements
2. Exploration - Understand codebase
3. Questions - Fill knowledge gaps
4. Architecture - Design approaches
5. Implementation - Build feature
6. Review - Quality check
7. Summary - Document changes

### "I want to commit and push"

**Simple commit:**
```
/commit
```

**Commit, push, and create PR:**
```
/commit-push-pr
```

---

## Plugin Activation Status

Plugins are activated when:
1. Installed in marketplace cache
2. Referenced in settings or CLAUDE.md
3. Triggered by matching context/phrases

### Check Installed Plugins

```bash
ls ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/
ls ~/.claude/plugins/cache/
```

### Plugin Locations

| Type | Path |
|------|------|
| Marketplace | `~/.claude/plugins/marketplaces/claude-plugins-official/` |
| Cache (active) | `~/.claude/plugins/cache/` |
| External | `~/.claude/plugins/marketplaces/.../external_plugins/` |

---

## Agent Types for Task Tool

When using the Task tool, these `subagent_type` values are available:

| subagent_type | Purpose |
|---------------|---------|
| `code-simplifier:code-simplifier` | Simplify and refine code |
| `code-review:code-review` | Code review a pull request |
| `Explore` | Codebase exploration |
| `Plan` | Implementation planning |
| `Bash` | Command execution |
| `general-purpose` | Multi-step tasks |

### Example Usage

```python
# Simplify code
Task(
    subagent_type="code-simplifier:code-simplifier",
    prompt="Simplify the auth module for clarity"
)

# Code review
Task(
    subagent_type="code-review:code-review",
    prompt="Review changes in the last commit"
)
```

---

## Security Integration

The **security-guidance** plugin provides automatic security warnings when editing files. It checks for:

- Command injection risks
- XSS vulnerabilities
- SQL injection patterns
- Unsafe code patterns

This integrates with the **secure-coding-patterns** skill for comprehensive security coverage.

---

## Error Handling

### Plugin Not Found

**Symptom:** "Unknown skill" or "Plugin not available"

**Solutions:**
1. Check plugin is installed: `ls ~/.claude/plugins/cache/`
2. Use correct name format (e.g., `code-simplifier:code-simplifier`)
3. Try the /plugins command to browse available plugins

### Agent Fails to Trigger

**Symptom:** Requested agent doesn't run

**Solutions:**
1. Be more specific in request
2. Use explicit agent name
3. Check if plugin is in active cache

---

## Creating New Plugins

Use the **plugin-dev** plugin:

```
/create-plugin
```

Or load the skill:
```
Load skill: plugin-dev/skills/plugin-structure
```

Key components:
- `.claude-plugin/plugin.json` - Manifest
- `commands/*.md` - Slash commands
- `agents/*.md` - Agent definitions
- `skills/*/SKILL.md` - Skill definitions
- `hooks/hooks.json` - Hook configurations

---

*End of Plugin Ecosystem Integration*
