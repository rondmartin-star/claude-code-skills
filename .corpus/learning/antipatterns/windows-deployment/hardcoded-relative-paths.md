# Antipattern: Hardcoded Relative Paths in Installed Applications

**Category:** Windows Deployment / File Paths
**Severity:** Critical
**First Seen:** 2026-02-05

---

## Problem

Using relative file paths (like `./data/recipes.db`) for user data in applications that will be installed via MSI/installer packages. Relative paths work during development but fail catastrophically when the application is installed in protected directories.

## Symptoms

- Application works perfectly during development
- Portable executable (in `dist/`) works fine
- **MSI-installed application fails with database/file errors**
- Errors like:
  - `sqlite3.OperationalError: unable to open database file`
  - `FileNotFoundError: [Errno 2] No such file or directory: './data'`
  - `PermissionError: [Errno 13] Permission denied`

## Consequences

**Severity:** Critical
- **User Impact:** Application completely broken after installation
- **Business Impact:** Professional distribution impossible, user trust destroyed
- **Development Impact:** Emergency hotfix required, installer rebuild

## Root Cause

**Why Relative Paths Fail:**

1. **Development:** Current directory = project root (`G:\Projects\App\`)
   - `./data/recipes.db` → `G:\Projects\App\data\recipes.db` ✅
   - Full control, writable

2. **Portable Executable:** Running from `dist/App/`
   - `./data/recipes.db` → `G:\Projects\App\dist\App\data\recipes.db` ✅
   - Still writable during testing

3. **MSI Installation:** Installed in `C:\Program Files\App\`
   - `./data/recipes.db` → `C:\Program Files\App\data\recipes.db` ❌
   - **Read-only for standard users**
   - Requires admin elevation to write
   - Windows UAC blocks writes

**The Assumption:** "If it works on my machine, it works installed" ← WRONG!

## Prevention

### Rule
**Never use relative paths for user data in applications that will be installed**

### Correct Approach: Platform-Aware Paths

```python
import os
import sys
from pathlib import Path

def get_data_directory() -> Path:
    """Get platform-appropriate data directory"""

    if getattr(sys, 'frozen', False):
        # Running as installed/compiled executable
        if os.name == 'nt':  # Windows
            # Use %LOCALAPPDATA%\AppName
            appdata = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
            data_dir = Path(appdata) / 'MyApp'
        elif sys.platform == 'darwin':  # macOS
            # Use ~/Library/Application Support/AppName
            data_dir = Path.home() / 'Library' / 'Application Support' / 'MyApp'
        else:  # Linux
            # Use ~/.config/appname or ~/.local/share/appname
            data_dir = Path.home() / '.config' / 'myapp'
    else:
        # Running as Python script (development)
        data_dir = Path('./data')

    # Create if doesn't exist
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

# Usage
database_path = get_data_directory() / 'app.db'
```

### Windows Standard Locations

| Data Type | Windows Path | macOS Path | Linux Path |
|-----------|--------------|------------|------------|
| User data | `%LOCALAPPDATA%\AppName` | `~/Library/Application Support/AppName` | `~/.local/share/appname` |
| User config | `%APPDATA%\AppName` | `~/Library/Preferences/AppName` | `~/.config/appname` |
| Cache | `%LOCALAPPDATA%\AppName\Cache` | `~/Library/Caches/AppName` | `~/.cache/appname` |
| Logs | `%LOCALAPPDATA%\AppName\Logs` | `~/Library/Logs/AppName` | `~/.local/share/appname/logs` |

**Windows Examples:**
- `C:\Users\JohnDoe\AppData\Local\RecipeManager\recipes.db` ✅
- `C:\Users\JohnDoe\AppData\Roaming\RecipeManager\config.json` ✅

## Detection

### How to Detect This Issue

**1. Code Review:**
```python
# BAD - Hardcoded relative paths ❌
database_path = Path("./data/app.db")
config_path = Path("./config.json")
images_dir = Path("./data/images")

# GOOD - Environment-aware paths ✅
data_dir = get_data_directory()
database_path = data_dir / "app.db"
config_path = data_dir / "config.json"
images_dir = data_dir / "images"
```

**2. Runtime Testing:**
```cmd
# Don't just test portable executable!
cd dist/App
App.exe  # ❌ This isn't how users will run it

# Test actual MSI installation
msiexec /i App.msi
# Launch from Start Menu
# Verify database created in AppData ✅
```

**3. Static Analysis:**
```bash
# Search for problematic patterns
grep -r "Path(\"\./" src/
grep -r "\"\.\/data" src/
grep -r "Path('\./" src/
```

## Related Patterns

**Patterns:**
- `platform-aware-paths` - Detect OS and use appropriate directories
- `appdirs-library` - Use appdirs or platformdirs Python package
- `sys-frozen-detection` - Detect if running as compiled executable

**Antipatterns:**
- `works-on-my-machine` - Testing only in development environment
- `assume-write-permissions` - Assuming current directory is writable
- `skip-msi-testing` - Only testing portable executable

## Examples

### What NOT to do ❌

```python
# config.py - WRONG!
class Settings:
    database_path = Path("./data/recipes.db")  # ❌ Relative path
    backup_dir = Path("./data/backups")        # ❌ Relative path
    images_dir = Path("./data/images")         # ❌ Relative path
```

**Result after MSI install:**
```
C:\Program Files\RecipeManager\
  RecipeManager.exe
  # Tries to create: C:\Program Files\RecipeManager\data\recipes.db
  # ERROR: Permission denied! ❌
```

### What TO do ✅

```python
# config.py - CORRECT!
import os
import sys
from pathlib import Path

def get_default_data_dir() -> Path:
    """Get environment-appropriate data directory"""
    if getattr(sys, 'frozen', False):
        # Installed - use AppData
        if os.name == 'nt':
            appdata = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
            data_dir = Path(appdata) / 'RecipeManager'
        else:
            data_dir = Path.home() / '.recipemanager'
    else:
        # Development - use local dir
        data_dir = Path('./data')

    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

class Settings:
    database_path = get_default_data_dir() / "recipes.db"  # ✅
    backup_dir = get_default_data_dir() / "backups"        # ✅
    images_dir = get_default_data_dir() / "images"         # ✅
```

**Result after MSI install:**
```
Installation:
  C:\Program Files\RecipeManager\RecipeManager.exe  (read-only)

User Data:
  C:\Users\JohnDoe\AppData\Local\RecipeManager\
    recipes.db         ✅ Works!
    backups\           ✅ Works!
    images\            ✅ Works!
```

## Detection via sys.frozen

**How to detect if running as installed executable:**

```python
import sys

if getattr(sys, 'frozen', False):
    print("Running as compiled executable (PyInstaller/cx_Freeze)")
    print("Location:", sys.executable)
    # Use AppData paths
else:
    print("Running as Python script")
    print("Location:", __file__)
    # Can use relative paths
```

**PyInstaller sets:**
- `sys.frozen = True`
- `sys._MEIPASS` = temp extraction dir

## Platform Detection

```python
import sys
import os

def get_platform_data_dir(app_name: str) -> Path:
    """Get platform-specific data directory"""

    if sys.platform == 'win32' or os.name == 'nt':
        # Windows
        base = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
        return Path(base) / app_name

    elif sys.platform == 'darwin':
        # macOS
        return Path.home() / 'Library' / 'Application Support' / app_name

    else:
        # Linux/Unix
        # Follow XDG Base Directory specification
        xdg_data = os.environ.get('XDG_DATA_HOME')
        if xdg_data:
            return Path(xdg_data) / app_name.lower()
        else:
            return Path.home() / '.local' / 'share' / app_name.lower()
```

## Testing Checklist

Before releasing MSI installer:

- [ ] Test portable executable from dist/
- [ ] **Test actual MSI installation in clean VM** ← Critical!
- [ ] Verify app launches after MSI install
- [ ] Check database created in AppData (not Program Files)
- [ ] Verify user can create/modify data without admin
- [ ] Test upgrade: MSI v2 over v1 (data preserved?)
- [ ] Test uninstall: User data optionally preserved

**Critical:** Always test the actual distribution method, not just development/portable!

## Using Libraries

**Recommended:** Use `platformdirs` library for standard paths

```python
from platformdirs import user_data_dir, user_config_dir, user_cache_dir

# Automatically handles Windows/macOS/Linux correctly
data_dir = Path(user_data_dir("RecipeManager", "MyCompany"))
config_dir = Path(user_config_dir("RecipeManager", "MyCompany"))
cache_dir = Path(user_cache_dir("RecipeManager", "MyCompany"))

# Windows result:
#   data_dir:   C:\Users\User\AppData\Local\MyCompany\RecipeManager
#   config_dir: C:\Users\User\AppData\Roaming\MyCompany\RecipeManager
#   cache_dir:  C:\Users\User\AppData\Local\MyCompany\RecipeManager\Cache
```

Install: `pip install platformdirs`

## Occurrences

- **2026-02-05:** RecipeManager v2.0 - Database path failure after MSI install

---

*Part of Learning Skills Ecosystem*
*Category: Windows Deployment / File Paths*
*Always test installed applications, not just portable executables!*
