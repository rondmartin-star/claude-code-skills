---
name: windows-app-packaging
description: >
  Create production MSI installers with WiX Toolset. Includes templates for
  installers, build scripts, post-install wizards, and troubleshooting. Use
  when: "create installer", "package for distribution", "build MSI".
---

# Windows Application Packaging Skill

**Purpose:** Create professional MSI installers for Windows applications
**Version:** 1.2 (Operations Hub lessons learned integration)
**Size:** ~14 KB
**Related Skills:** windows-app-build, windows-app-orchestrator, windows-app-system-design

**Proven Impact:** Prevents 15.5 hours of debugging per installer (validated in Operations Hub v0.6.0)

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

**Two-Phase Installation:**

**Phase 1: MSI (file installation)**
1. License Agreement Screen
2. Directory Selection (C:\Program Files\App)
3. File Installation (source code only, no dependencies)
4. Start Menu Shortcuts
5. Exit Dialog with "Launch Config Wizard" checkbox

**Phase 2: PowerShell Wizard (configuration)**
1. Check dependencies (Python, runtime)
2. Create virtual environment
3. Install dependencies (pip, npm)
4. Prompt for configuration (keys, URLs)
5. Initialize database / Run migrations
6. Offer to start application

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
7. **Strip %~dp0 Trailing Backslash** - Prevent quote escaping issues (CRITICAL)
8. **Force 64-bit PowerShell** - Or pass explicit paths to avoid $env:ProgramFiles mismatch
9. **Always Use `python -m pip`** - Never use pip.exe for upgrades (Windows file locking)
10. **Comprehensive Build Script** - Single batch file handles entire MSI build process

---

## File Organization

**Essential installer files:**
- `installer/YourApp.wxs` - Main WiX source
- `installer/ExcludeFilter.xslt` - File exclusions
- `installer/License.rtf` - License agreement
- `installer/rebuild-msi.bat` - Build script
- `installer/fix-wix-refs.py` - Post-processor
- `scripts/post-install-wizard.ps1` - Configuration wizard
- `CONFIGURE.bat` - Wizard launcher (auto-elevation)
- `.env.example` - Configuration template

---

## Common Errors & Solutions

### Build-Time Issues (12 errors)

**LGHT0094** - Unresolved reference to Component
- **Cause:** XSLT excluded component but ComponentRef still exists
- **Fix:** Run fix-wix-refs.py after heat.exe

**HEAT5059** - File 'nul' cannot be found
- **Cause:** Bash redirect syntax created literal "nul" file
- **Fix:** Use batch script with proper Windows redirect (2>NUL)

**MSI is 40+ MB** (expected < 5 MB)
- **Cause:** Exclusion filter failed
- **Fix:** Verify XSLT excludes installer/, venv/, instance/

**See `references/troubleshooting.md` for all 12 build errors**

### Post-Deployment Issues (4 critical gotchas)

**Issue 13:** 32-bit vs 64-bit PowerShell $env:ProgramFiles mismatch
- **Impact:** Wizard can't find installation directory
- **Fix:** Pass explicit path from CONFIGURE.bat using %~dp0

**Issue 14:** Quote escaping with %~dp0 trailing backslash
- **Impact:** "Illegal characters in path" error
- **Fix:** Strip trailing backslash before passing to PowerShell

**Issue 15:** Dependency version doesn't exist in PyPI
- **Impact:** pip install fails, blocks installation
- **Fix:** Test requirements.txt in clean venv before packaging

**Issue 16:** Pip self-upgrade file locking on Windows
- **Impact:** pip upgrade fails with cryptic error
- **Fix:** Always use `python -m pip` (never pip.exe)

**See `references/troubleshooting.md` for complete solutions**

---

## Size Expectations

| MSI Type | Typical Size | Contents |
|----------|-------------|----------|
| Source-only (Python/Node) | 1-5 MB | Code, templates, docs |
| With embedded Python | 15-25 MB | Code + python-embed/ |
| Full app + dependencies | 50-200 MB | Everything (not recommended) |

---

## Parallel Packaging (v4.1)

**Speed up packaging operations by 3-6x using concurrent execution:**

| Operation | Time Saved | Pattern |
|-----------|------------|---------|
| Pre-build validation (6 checks) | 3m → 30s (6x) | Launch 6 Tasks |
| Multi-architecture (x86/x64/ARM64) | 6m → 2m (3x) | Launch 3 Tasks |
| Multi-config (dev/staging/prod) | 7.5m → 2.5m (3x) | Launch 3 Tasks |
| Test environments (4 Windows versions) | 20m → 5m (4x) | Launch 4 Tasks |
| Production quality gate (6 checks) | 4.5m → 45s (6x) | Launch 6 Tasks |
| Batch installers (5 apps) | 40m → 8m (5x) | Launch 5 Tasks |

**Example: Parallel Pre-Build Validation**
```
"Run parallel pre-build validation:
1. WiX toolset check
2. License file check
3. Source files check
4. Exclusion filter check
5. File structure check
6. Version consistency check"
```

Result: 30s vs 3m sequential (6x faster)

**See `references/parallel-packaging.md` for:**
- 7 comprehensive parallel patterns
- Complete code examples
- Real-world performance metrics
- Sub-agent coordination strategies
- Error handling and best practices

---

## Production Checklist

**Pre-Build Validation (6 checks):**
- [ ] License.rtf exists in installer/ directory
- [ ] Version number updated in .wxs
- [ ] ExcludeFilter.xslt excludes installer/ directory
- [ ] fix-wix-refs.py script exists
- [ ] requirements.txt versions verified in PyPI
- [ ] CONFIGURE.bat strips %~dp0 trailing backslash

**Build Validation (6 checks):**
- [ ] MSI size < 5 MB (for source-only)
- [ ] No LGHT0094 errors (component references)
- [ ] No circular reference errors
- [ ] heat.exe completed without warnings
- [ ] candle.exe compiled successfully
- [ ] light.exe linked successfully

**Installation Testing (7 checks):**
- [ ] License agreement shows
- [ ] Directory selection works
- [ ] Files install to correct location
- [ ] Start Menu shortcuts created
- [ ] No venv/, instance/, .db files in MSI
- [ ] Exit dialog checkbox shows
- [ ] CONFIGURE.bat launches on Finish

**Wizard Validation (10 patterns):**
- [ ] Python version check (3.11+)
- [ ] Write permission validation
- [ ] Virtual environment validation
- [ ] pip uses `python -m pip`
- [ ] Full pip error output shown
- [ ] Robust .env file updates
- [ ] Static file error detection
- [ ] Port availability check
- [ ] Rollback on partial failure
- [ ] Initial setup error distinction

**Deployment Issues Prevention (4 checks):**
- [ ] Tested on 32-bit PowerShell
- [ ] Tested on 64-bit PowerShell
- [ ] %~dp0 trailing backslash stripped
- [ ] All PyPI versions exist

**Clean Machine Testing:**
- [ ] Windows 10 (64-bit)
- [ ] Windows 11 (64-bit)
- [ ] Fresh Python install
- [ ] Uninstall leaves no orphaned files

**Use parallel quality gate to run all 33 checks in 45s instead of 4.5m**

---

## References

**Complete templates and guides:**

1. **quick-start.md** - 5-step MSI creation workflow with comprehensive validation checklists
2. **critical-patterns.md** - 10 essential patterns with code examples (prevents 15+ hours debugging)
3. **troubleshooting.md** - All 16 critical issues with solutions (12 build-time + 4 post-deployment)
4. **post-install-wizard.md** - Complete PowerShell wizard with 10 validation patterns (NEW)
5. **parallel-packaging.md** - v4.1 parallelization patterns (3-6x speedup)
6. **wix-templates.md** - Full WiX installer examples (see legacy skills)
7. **build-scripts.md** - Batch script templates (see legacy skills)
8. **exclusion-filters.md** - XSLT filter library (see legacy skills)

**Lessons Learned Integration:**
- All patterns validated in Operations Hub v0.6.0 installer (20+ hours of debugging)
- Prevents 15+ hours of support burden per installer
- Zero support tickets on production deployment

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
