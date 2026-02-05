# Antipattern: Assume PyInstaller Finds All Dependencies

**Category:** PyInstaller / Dependency Management
**Severity:** Critical
**First Seen:** 2026-02-05

---

## Problem

Assuming PyInstaller will automatically detect and bundle ALL dependencies, including:
- Hidden imports (dynamic imports, plugins)
- Data files (JSON, XML, templates, images)
- Non-Python assets in packages

This leads to "works on my machine" but fails when bundled.

## Symptoms

- FileNotFoundError for data files at runtime
- ModuleNotFoundError for dynamically imported modules
- Missing templates, config files, or assets
- Application works in development but breaks in PyInstaller build

## Consequences

**Severity:** Critical
- **User Impact:** Complete application failure in specific features
- **Business Impact:** Broken deployments, loss of functionality
- **Development Impact:** Time wasted debugging packaging issues

## Root Cause

**PyInstaller's Auto-Detection Limitations:**

1. **Only detects import-time dependencies**
   - Misses: `importlib.import_module()`, `__import__()`, `exec()`

2. **Only bundles .py files by default**
   - Misses: JSON, XML, templates, images, data directories

3. **Doesn't analyze transitive dependency data needs**
   - Package A imports Package B, Package B needs data files
   - PyInstaller bundles Package B's code but not its data

## Prevention

### Rule
**For each dependency, explicitly check for hidden imports and data files**

### Implementation

#### Step 1: Identify All Dependencies

```bash
# List all installed packages
pip freeze > requirements.txt

# Check each package's site-packages directory
cd venv/lib/python3.12/site-packages/
ls -la <package-name>/
```

#### Step 2: Check for Data Files

```bash
# Look for non-Python files
find <package-dir> -type f ! -name "*.py" ! -name "*.pyc"

# Common data file patterns:
# - *.json, *.xml, *.yaml, *.yml
# - *.txt, *.md, *.rst
# - templates/, data/, config/, resources/
# - *.so, *.dll (binary dependencies)
```

#### Step 3: Update PyInstaller Spec

```python
# RecipeManager.spec
a = Analysis(
    ['src/main.py'],
    datas=[
        ('src', 'src'),
        ('data', 'data'),
        # Explicitly add dependency data files
        (site_packages / 'mf2py/backcompat-rules', 'mf2py/backcompat-rules'),
        (site_packages / 'certifi/cacert.pem', 'certifi/'),
        # Add any other discovered data files
    ],
    hiddenimports=[
        # Explicitly add dynamic imports
        'pydantic_settings',
        'pydantic_core',
        # Any plugins or dynamically loaded modules
    ],
)
```

### Automated Detection Script

```python
# check_dependency_data.py
import os
from pathlib import Path
import site

def find_data_files():
    site_packages = Path(site.getsitepackages()[0])

    with open('requirements.txt') as f:
        packages = [line.split('==')[0] for line in f]

    data_files = []

    for package in packages:
        pkg_dir = site_packages / package.replace('-', '_')
        if not pkg_dir.exists():
            continue

        # Find non-Python files
        for file in pkg_dir.rglob('*'):
            if file.is_file() and file.suffix not in ['.py', '.pyc', '.pyo']:
                rel_path = file.relative_to(site_packages)
                data_files.append(str(rel_path))

    print("Data files found:")
    for f in data_files:
        print(f"  {f}")

    return data_files

if __name__ == '__main__':
    find_data_files()
```

## Detection

### Runtime Testing

```bash
# After PyInstaller build, test each major feature
cd dist/App

# Test imports of all major dependencies
python -c "
import recipe_scrapers  # Tests mf2py data files
import pydantic_settings  # Tests hidden imports
import certifi  # Tests SSL certificates
"

# If any fail, investigate and update spec
```

### Build Validation

```yaml
# CI/CD Pipeline Check
- name: Validate PyInstaller Build
  run: |
    # Build executable
    pyinstaller app.spec

    # Test all imports
    cd dist/App
    ./App.exe --test-imports

    # Check for common data file patterns
    find _internal -name "*.json" -o -name "*.xml"
```

## Related Patterns

**Patterns:**
- `explicit-dependency-declaration` - List all dependencies explicitly
- `dependency-audit` - Regular review of dependency data needs
- `build-smoke-test` - Quick runtime validation after build

**Antipatterns:**
- `trust-auto-detection` - Relying solely on automatic tools
- `fix-it-in-production` - Discovering missing dependencies after deployment

## Examples

### What NOT to do ❌

```python
# Just trust PyInstaller will find everything
a = Analysis(['main.py'])
# Build and ship!
# Runtime: FileNotFoundError: mf2py/backcompat-rules 💥
```

### What TO do ✅

```python
# Step 1: Research dependencies
# Check recipe-scrapers in site-packages
# Found: depends on mf2py
# Found: mf2py has backcompat-rules/ directory with JSON files

# Step 2: Explicitly include
import site
site_packages = Path(site.getsitepackages()[0])

a = Analysis(
    ['main.py'],
    datas=[
        ('src', 'src'),
        # Explicitly add discovered data files
        (site_packages / 'mf2py/backcompat-rules', 'mf2py/backcompat-rules'),
    ],
    hiddenimports=[
        'pydantic_settings',  # Dynamic import
        'pydantic_core',      # Required by pydantic_settings
    ],
)

# Step 3: Test before packaging
# Verify executable runs with all features
```

## Common Packages with Data Files

```python
# Known packages that need explicit data inclusion:
datas = [
    # SSL certificates
    ('certifi/cacert.pem', 'certifi/'),

    # Jinja2 templates (if using template loaders)
    ('jinja2/ext', 'jinja2/ext/'),

    # Babel localization data
    ('babel/locale-data', 'babel/locale-data/'),

    # Requests CA bundle
    ('requests/cacert.pem', 'requests/'),

    # Microformats parser rules (mf2py)
    ('mf2py/backcompat-rules', 'mf2py/backcompat-rules/'),
]
```

## Occurrences

- **2026-02-05:** RecipeManager v2.0 - mf2py backcompat-rules missing

---

*Part of Learning Skills Ecosystem*
*Category: PyInstaller / Dependency Management*
