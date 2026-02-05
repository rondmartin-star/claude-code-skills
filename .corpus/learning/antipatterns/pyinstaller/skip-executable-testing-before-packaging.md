# Antipattern: Skip Executable Testing Before Packaging

**Category:** PyInstaller / Build Process
**Severity:** High
**First Seen:** 2026-02-05

---

## Problem

Creating installer packages (MSI, DMG, etc.) without first testing the portable executable can hide critical runtime errors that only appear when users install the application.

## Symptoms

- Application installs successfully but fails to launch
- ModuleNotFoundError or ImportError at runtime
- Missing dependencies only discovered after distribution
- Users report "Application won't start" issues

## Consequences

**Severity:** High
- **User Impact:** Application appears to install but is completely broken
- **Business Impact:** Loss of user trust, support burden, rushed patches
- **Development Impact:** Emergency fixes, hotfix releases, reputation damage

## Root Cause

PyInstaller builds can succeed even when dependencies are missing because the build process only checks import-time dependencies, not runtime dependencies. Testing the portable executable reveals these issues before packaging.

## Prevention

### Rule
**Always test the PyInstaller executable before creating installer packages**

### Implementation

```bash
# Build Script Order
1. Run tests (pytest)
2. Build PyInstaller executable
3. TEST THE EXECUTABLE ← Critical step
4. Create installer package (MSI/DMG)
5. Test installer
```

### Testing Steps

```bash
# After PyInstaller build
cd dist/AppName
./AppName.exe

# Let it run for 5-10 seconds
# Try to:
# 1. Launch the application
# 2. Navigate to main features
# 3. Import major dependencies
# 4. Check for error dialogs

# Only proceed to MSI creation if executable works
```

### Automation

```yaml
# .github/workflows/build.yml
- name: Build PyInstaller executable
  run: pyinstaller app.spec

- name: Test portable executable
  run: |
    cd dist/App
    timeout 10 ./App.exe || exit 1
    # Add smoke tests here

- name: Create MSI
  if: success()
  run: ./build_msi.bat
```

## Detection

### Metrics to Monitor
- Executable launch success rate
- Time between build and first runtime error
- Support tickets: "App won't start"

### Alerts
- Build succeeds but executable test fails
- MSI created without executable test passing

## Related Patterns

**Patterns:**
- `test-before-package` - Always test intermediate artifacts
- `smoke-test-builds` - Quick runtime validation

**Antipatterns:**
- `trust-build-success` - Assuming successful build = working app
- `package-first-test-later` - Creating installers before validation

## Examples

### What NOT to do ❌

```bash
pyinstaller app.spec
# Build succeeded! ✓
# Ship it!
build_msi.bat
# MSI created! ✓
# Users install...
# "App won't start" 💥
```

### What TO do ✅

```bash
# 1. Build
pyinstaller app.spec --clean

# 2. Test executable FIRST
cd dist/App
./App.exe
# Verified it launches ✓

# 3. Only then create installer
cd ../..
build_msi.bat

# 4. Test installer
msiexec /i App.msi
# Test installed version ✓
```

## Occurrences

- **2026-02-05:** RecipeManager v2.0 - Missing pydantic_settings discovered post-MSI creation

---

*Part of Learning Skills Ecosystem*
*Category: Build Process / PyInstaller*
