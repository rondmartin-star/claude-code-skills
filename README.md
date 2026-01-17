# Claude Code Skills Ecosystem

A modular collection of skills for Claude Code that provide specialized guidance for Windows application development, security patterns, and workflow management.

## Skills Overview

### Core Orchestration
| Skill | Purpose |
|-------|---------|
| **windows-app-orchestrator** | Entry point that loads appropriate skills based on context |
| **skill-ecosystem-manager** | Create, maintain, and improve skills |

### Development Phases
| Skill | Purpose |
|-------|---------|
| **windows-app-requirements** | Capture user intentions, write user stories |
| **windows-app-system-design** | Design data models, architecture, technology selection |
| **windows-app-ui-design** | Design pages, workflows, navigation, brand language |
| **windows-app-build** | Implement features, fix bugs, package for delivery |

### Specialized Skills
| Skill | Purpose |
|-------|---------|
| **windows-app-supervision** | Process management, auto-start, health monitoring, MSI packaging |
| **authentication-patterns** | OAuth-first authentication, Google/Microsoft OAuth setup |
| **secure-coding-patterns** | Security guidance during implementation |
| **navigation-auditor** | Verify feature navigation paths and reachability |
| **conversation-snapshot** | Create portable snapshots for context continuity |

## Directory Structure

```
skills/
├── windows-app-orchestrator/   # Always loaded first (~4KB)
│   └── SKILL.md
├── windows-app-requirements/   # Requirements gathering (~8KB)
│   └── SKILL.md
├── windows-app-system-design/  # System architecture (~12KB)
│   ├── SKILL.md
│   └── references/
│       └── patterns.md
├── windows-app-ui-design/      # UI/UX design (~10KB)
│   ├── SKILL.md
│   └── references/
│       └── brand-language.md
├── windows-app-build/          # Implementation (~25KB)
│   ├── SKILL.md
│   └── references/
│       ├── audit-checklists.md
│       ├── security-patterns.md
│       └── templates.md
├── windows-app-supervision/    # Process management (~8KB)
│   └── SKILL.md
├── authentication-patterns/    # Auth patterns (~4KB)
│   └── SKILL.md
├── secure-coding-patterns/     # Security patterns
│   └── SKILL.md
├── navigation-auditor/         # Navigation verification
│   └── SKILL.md
├── conversation-snapshot/      # Context preservation
│   ├── SKILL.md
│   └── references/
│       └── templates.md
└── skill-ecosystem-manager/    # Skill maintenance
    ├── SKILL.md
    └── references/
        ├── design-philosophy.md
        ├── maintenance.md
        └── skill-templates.md
```

## Usage

Skills are automatically loaded by Claude Code when their trigger patterns match. The orchestrator skill determines which specialized skills to load based on context.

### Trigger Examples

```
"I want to build an app..."     → windows-app-requirements
"Design the data model..."      → windows-app-system-design
"Design the UI..."              → windows-app-ui-design
"Implement this feature..."     → windows-app-build
"Add OAuth login..."            → authentication-patterns
"Build MSI installer..."        → windows-app-supervision
```

## Installation

Place this directory at `~/.claude/skills/` for Claude Code to discover.

## License

Proprietary - Pterodactyl Holdings, LLC
