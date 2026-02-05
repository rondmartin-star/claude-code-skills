# Changelog - Windows App Supervision Skill

All notable changes to this skill will be documented in this file.

---

## [1.1] - 2026-02-05

### Added - MSI Installer Enhancements

**Code Signing (Prevents Windows Defender Warnings):**
- Step-by-step guide for obtaining code signing certificates
- SignTool integration in build process
- Automatic signing during MSI compilation
- Certificate verification commands
- Best practices for certificate storage
- Environment variable configuration

**Installer UI Improvements:**
- Keep installer window on top during execution
- Launch option checkbox on exit dialog
- Launch option checked by default
- Custom actions for launching application after install
- Alternative launch methods (script-based)
- Modal dialog configuration

**Build Process Updates:**
- Enhanced build-msi.bat with signing step
- Certificate path environment variables
- Automatic signature verification
- Build script error handling

**Documentation:**
- MSI Best Practices Summary section
- Three Critical Requirements quick reference
- Certificate sources and costs
- Code examples for WiX configuration
- signtool command reference
- Integration checklist updated

### Changed
- Version updated from 1.0 to 1.1
- Skill size: ~8 KB → ~11 KB
- Integration checklist expanded with MSI requirements

### Impact
- **Security:** Signed installers trusted by Windows Defender
- **User Experience:** Seamless installation and launch
- **Deployment:** Professional-grade installer behavior
- **Trust:** No SmartScreen warnings for end users

---

## [1.0] - 2026-01-27

### Added
- Initial windows-app-supervision skill
- Task Scheduler auto-start with SYSTEM account
- Health check with database verification
- Restart throttling (exponential backoff)
- Graceful shutdown for Windows
- File change watching with debounce
- SQLite WAL mode for database protection
- Supervisor configuration template
- MSI installer build with WiX Toolset
- Custom actions for install/uninstall
- Automated builds after git commits

### Features
- **Auto-Start:** Task Scheduler integration
- **Health Monitoring:** HTTP health endpoint checking
- **Hot Reload:** File change detection and restart
- **Crash Recovery:** Automatic restart with throttling
- **Database Safety:** WAL mode prevents corruption
- **Production Deploy:** Complete MSI packaging

---

*Part of v4.0 Universal Skills Ecosystem - Windows Application Development*
