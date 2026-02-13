---
name: windows-app-packaging
description: >
  Create production MSI installers with WiX Toolset. Includes templates for
  installers, build scripts, post-install wizards, and troubleshooting. Use
  when: "create installer", "package for distribution", "build MSI".
---

# Windows Application Packaging Skill

**Purpose:** Create professional MSI installers for Windows applications
**Version:** 1.0
**Size:** ~12 KB
**Related Skills:** windows-app-build, windows-app-system-design

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Create an installer"
- "Package for distribution"
- "Build MSI"
- "Make installable package"
- "Production installer"
- "Distribution package"

**Context Indicators:**
- Application is complete and tested
- Ready for deployment to other machines
- Need professional installation experience
- Require license agreement
- Post-install configuration needed

## ❌ DO NOT LOAD WHEN

- Still developing the application
- Just need to run locally
- Working on features/fixes (use windows-app-build)
- Designing data model or UI

---

## Golden Rules

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   1. NEVER RUN WIX TOOLS FROM BASH                          │
│      Always use batch scripts                               │
│                                                             │
│   2. MSI = SOURCE CODE ONLY                                 │
│      Dependencies installed on target machine               │
│                                                             │
│   3. POST-INSTALL WIZARD FOR CONFIGURATION                  │
│      MSI cannot prompt during installation                  │
│                                                             │
│   4. TEST INSTALLER SIZE                                    │
│      If > 5 MB, exclusions probably failed                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## MSI Installer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         MSI INSTALLER                       │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 1. License Agreement Screen (WixUI_InstallDir)        │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 2. Directory Selection (default: C:\Program Files\App)│ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 3. File Installation (source code, templates, docs)  │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 4. Start Menu Shortcuts (app, configure, readme)     │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 5. Exit Dialog with "Launch Config Wizard" checkbox  │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               POST-INSTALL CONFIGURATION WIZARD              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 1. Check dependencies (Python, runtime, etc.)        │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 2. Create virtual environment                         │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 3. Install dependencies (pip, npm, etc.)             │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 4. Prompt for configuration (keys, URLs, etc.)       │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 5. Initialize database / Run migrations               │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 6. Offer to start application                         │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start

See `references/quick-start.md` for complete 5-step workflow:
1. Create WiX source file (.wxs)
2. Create exclusion filter (XSLT)
3. Create build script (rebuild-msi.bat)
4. Create post-install wizard (PowerShell)
5. Build and test

---

## Critical Patterns

**See `references/critical-patterns.md` for detailed examples of:**

1. **Use Batch Scripts for WiX Tools** - Never run from bash
2. **Post-Process Component References** - Fix XSLT cleanup issues
3. **Aggressive Exclusions** - Keep MSI size under 5MB
4. **Exit Dialog Launch** - Launch config wizard after install
5. **Auto-Elevation** - Request admin rights automatically
6. **PowerShell Function Calls** - No parentheses on function calls

---

## File Organization

```
YourApp/
├── installer/
│   ├── YourApp.wxs              # Main WiX source
│   ├── ExcludeFilter.xslt       # File exclusions
│   ├── License.rtf              # License agreement (RTF format)
│   ├── rebuild-msi.bat          # Build script
│   ├── fix-wix-refs.py          # Post-processor
│   └── .gitignore               # Exclude *.wixobj, *.msi, ApplicationFiles*.wxs
├── scripts/
│   └── post-install-wizard.ps1  # Configuration wizard
├── CONFIGURE.bat                # Wizard launcher (with auto-elevation)
├── POST-INSTALL-README.md       # Manual setup instructions
├── LICENSE.txt                  # Plain text license
└── .env.example                 # Configuration template
```

---

## Common Errors & Solutions

### LGHT0094 - Unresolved reference to Component

**Cause:** XSLT excluded component but ComponentRef still exists

**Fix:** Run fix-wix-refs.py after heat.exe (see `references/critical-patterns.md`)

### HEAT5059 - File 'nul' cannot be found

**Cause:** Bash redirect syntax created literal "nul" file

**Fix:** Use batch script with proper Windows redirect (2>NUL not >nul 2>&1)

### MSI is 40+ MB (expected < 5 MB)

**Cause:** Exclusion filter failed

**Fix:** Verify XSLT syntax, exclude installer/ directory, test with:
```powershell
msiexec /a App.msi /qb TARGETDIR="C:\Temp\Verify"
dir "C:\Temp\Verify" /s  # Should NOT see venv, instance, .git, *.db
```

**See `references/troubleshooting.md` for complete error reference**

---

## Size Expectations

| MSI Type | Typical Size | Contents |
|----------|-------------|----------|
| Source-only (Python/Node) | 1-5 MB | Code, templates, docs |
| With embedded Python | 15-25 MB | Code + python-embed/ |
| Full app + dependencies | 50-200 MB | Everything (not recommended) |

---

## Production Checklist

Before releasing MSI:

- [ ] License agreement shows (License.rtf exists)
- [ ] Version number updated in .wxs
- [ ] Company/product name correct
- [ ] Start Menu shortcuts created
- [ ] Uninstall works (test via Control Panel)
- [ ] Installer size reasonable (< 5 MB for source-only)
- [ ] Post-install wizard tested on clean machine
- [ ] All dependencies install correctly
- [ ] Configuration prompts work
- [ ] Database initializes
- [ ] Application starts after configuration
- [ ] Admin elevation works
- [ ] Works on Windows 10 and 11
- [ ] Tested fresh install (not upgrade)
- [ ] Tested uninstall (no orphaned files)

---

## References

**Complete templates and guides:**

1. **quick-start.md** - 5-step MSI creation workflow
2. **critical-patterns.md** - 6 essential patterns with code examples
3. **troubleshooting.md** - Detailed error solutions
4. **wix-templates.md** - Full WiX installer examples (see legacy skills)
5. **build-scripts.md** - Batch script templates (see legacy skills)
6. **exclusion-filters.md** - XSLT filter library (see legacy skills)
7. **post-install-wizard.md** - PowerShell wizard template (see legacy skills)

---

## Integration with Other Skills

**windows-app-build:**
- Build application before packaging
- Update APP-STATE.yaml with installer version
- Document in CHANGELOG.md

**windows-app-system-design:**
- Plan installer requirements
- Design post-install configuration flow
- Plan dependency installation strategy

---

*End of Windows Application Packaging Skill*
