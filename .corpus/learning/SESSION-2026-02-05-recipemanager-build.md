# Learning Session: RecipeManager v2.0 Build & Deployment

**Date:** 2026-02-05
**Project:** RecipeManager v2.0
**Task:** Create MSI installer with PyInstaller
**Duration:** ~3 hours
**Outcome:** ✅ Success (with learnings extracted)

---

## Summary

Built and deployed RecipeManager v2.0 as a Windows MSI installer. Encountered 3 critical errors during the build-test-package cycle, each revealing important antipatterns for PyInstaller and GUI development.

---

## Errors Encountered & Fixed

### 1. Missing pydantic_settings Module ⚠️

**Error:** `ModuleNotFoundError: No module named 'pydantic_settings'`

**Root Cause:** PyInstaller didn't auto-detect pydantic_settings as a hidden import

**Fix:** Added to hiddenimports in RecipeManager.spec
```python
hiddenimports=[
    'pydantic',
    'pydantic_settings',  # Added
    'pydantic_core',      # Added
]
```

**Time to Fix:** 5 minutes

**Antipattern Extracted:** `skip-executable-testing-before-packaging`
- Location: `.corpus/learning/antipatterns/pyinstaller/`
- Prevention: Always test portable executable before creating installer

---

### 2. Missing mf2py Data Files ⚠️

**Error:** `FileNotFoundError: mf2py\backcompat-rules`

**Root Cause:** PyInstaller doesn't auto-detect non-Python data files in transitive dependencies (recipe-scrapers → extruct → mf2py → backcompat-rules/)

**Fix:** Added data directory to datas in RecipeManager.spec
```python
datas=[
    ('src', 'src'),
    ('data', 'data'),
    (r'...\site-packages\mf2py\backcompat-rules', 'mf2py/backcompat-rules'),
]
```

**Investigation Steps:**
1. Located mf2py package in site-packages
2. Found backcompat-rules directory with 11 JSON files
3. Added to PyInstaller spec
4. Rebuilt and verified

**Time to Fix:** 10 minutes

**Antipattern Extracted:** `assume-pyinstaller-finds-all-dependencies`
- Location: `.corpus/learning/antipatterns/pyinstaller/`
- Prevention: Check each dependency for data files before building

---

### 3. Status Bar Initialization Order Bug ⚠️

**Error:** `AttributeError: 'RecipeManagerWindow' object has no attribute 'status_bar'`

**Root Cause:** status_bar created AFTER main content, but meal plan tab initialization tried to use it

**Fix:** Moved status_bar creation before _create_main_content()
```python
# Before:
_create_main_content()  # Creates tabs
self.status_bar = QStatusBar()  # TOO LATE

# After:
self.status_bar = QStatusBar()  # CREATE FIRST
_create_main_content()          # Tabs can now use it
```

**Time to Fix:** 3 minutes

**Antipattern Extracted:** `late-dependency-initialization`
- Location: `.corpus/learning/antipatterns/gui/`
- Prevention: Create shared resources before child widgets

---

## Learnings Extracted

### PyInstaller Best Practices

1. **Always test the portable executable before packaging**
   - Build → Test → Package (not Build → Package → Test)
   - Saves time catching issues early

2. **Don't trust auto-detection for dependencies**
   - Check each package in site-packages
   - Look for: JSON, XML, templates, images, data dirs
   - Explicitly add to datas or hiddenimports

3. **Common packages with data files:**
   - certifi (cacert.pem)
   - mf2py (backcompat-rules/)
   - babel (locale-data/)
   - jinja2 (ext/)

### GUI Development (PyQt6) Best Practices

1. **Initialization order matters**
   - Map dependencies before writing __init__
   - Create shared resources before child widgets
   - Pattern: Resources → UI → Signals → Data

2. **PyQt6-specific behavior:**
   - Adding tabs to QTabWidget triggers immediate initialization
   - Child __init__ methods run immediately
   - Can't defer widget creation

### Build Pipeline Improvements

**Current Build Process:**
```bash
1. Run tests (pytest)
2. Build PyInstaller executable
3. ❌ Create MSI (WRONG - skips testing)
```

**Improved Build Process:**
```bash
1. Run tests (pytest)
2. Build PyInstaller executable
3. ✅ TEST PORTABLE EXECUTABLE ← Added!
4. Create MSI installer
5. Test MSI installation
```

---

## Metrics

### Error Resolution

| Error | Severity | Detection | Time to Fix | Preventable? |
|-------|----------|-----------|-------------|--------------|
| Missing pydantic_settings | Critical | Runtime | 5 min | Yes |
| Missing mf2py data | Critical | Runtime | 10 min | Yes |
| Status bar init order | High | Runtime | 3 min | Yes |

**Total Errors:** 3
**Total Time Lost:** 18 minutes
**All Preventable:** Yes

### Effectiveness of Error Reflection

- **Patterns Identified:** 0 (errors were preventable, not patterns to reuse)
- **Antipatterns Identified:** 3 (all documented)
- **Prevention Rules Generated:** 3
- **Pre-Mortem Updated:** Yes (will catch these in future)

---

## Prevention Rules for Future Projects

### Rule 1: PyInstaller Testing Gate
```bash
# Add to build scripts
if [ ! -f "dist/App/App.exe" ]; then
    echo "Executable not found!"
    exit 1
fi

# Test executable
cd dist/App
timeout 10 ./App.exe || exit 1

# Only proceed if successful
echo "Executable test passed ✓"
```

### Rule 2: Dependency Data File Scan
```python
# check_deps.py - Run before PyInstaller build
def scan_dependencies_for_data():
    for package in requirements:
        pkg_dir = site_packages / package
        data_files = find_non_python_files(pkg_dir)
        if data_files:
            print(f"⚠️ {package} has data files: {data_files}")
            print(f"   Add to spec: ('{pkg_dir}', '{package}')")
```

### Rule 3: GUI Initialization Checklist
```python
# Before writing GUI __init__:
# 1. List all shared resources (status bar, services, state)
# 2. List all child widgets and their dependencies
# 3. Order: Resources → UI → Signals → Data
# 4. Verify with dependency graph
```

---

## Files Created

### Error Reports
- `errors/2026-02-05-pyinstaller-missing-pydantic-settings.json`
- `errors/2026-02-05-pyinstaller-missing-mf2py-data.json`
- `errors/2026-02-05-pyqt6-initialization-order.json`

### Antipatterns
- `antipatterns/pyinstaller/skip-executable-testing-before-packaging.md`
- `antipatterns/pyinstaller/assume-pyinstaller-finds-all-dependencies.md`
- `antipatterns/gui/late-dependency-initialization.md`

### Updated Documentation
- RecipeManager: `BUILD_SUCCESS.md` (added troubleshooting section)
- RecipeManager: `RecipeManager.spec` (fixed hiddenimports and datas)
- RecipeManager: `src/views/main_window.py` (fixed initialization order)

---

## Success Metrics

✅ **Build Complete:** RecipeManager.msi (82 MB)
✅ **All Tests Passing:** 32/32 tests
✅ **Application Launches:** Successfully
✅ **Features Working:** All tabs load without errors
✅ **Learnings Documented:** 3 antipatterns extracted
✅ **Prevention Rules Created:** 3 new rules for future

---

## Next Session Improvements

**Apply Learnings:**
1. Add executable testing to build script
2. Create dependency data scanner
3. Review GUI initialization patterns
4. Update pre-mortem checklist with new antipatterns

**Pattern Library:**
- No new patterns (errors were preventable)
- 3 antipatterns to avoid
- Build process improvements identified

---

*Session completed successfully with institutional memory built*
*Error Reflection skill applied ✓*
*Pattern library updated ✓*
