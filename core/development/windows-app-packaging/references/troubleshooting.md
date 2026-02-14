# WiX MSI Installer Troubleshooting Guide

**Quick Reference:** Common errors and their solutions

---

## Build Errors

### LGHT0094: Unresolved reference to symbol 'Component:cmpXXX'

**Full Error:**
```
error LGHT0094 : Unresolved reference to symbol 'Component:cmpA1B2C3...' in section 'Fragment:'
```

**Cause:** XSLT filter excluded a component but the ComponentRef entry still exists

**Solution:**
```batch
REM Add post-processing step after heat.exe
heat.exe dir "%SOURCE%" ... -out ApplicationFiles.wxs
python fix-wix-refs.py  # Removes invalid ComponentRef entries
candle.exe ... ApplicationFiles-Fixed.wxs
```

**Prevention:** Always run fix-wix-refs.py after harvesting

---

### HEAT5059: The file 'nul' cannot be found

**Full Error:**
```
heat.exe : error HEAT5059 : The file 'M:\Project\installer\nul' cannot be found.
```

**Cause:** Bash redirect syntax `>nul 2>&1` created a literal file named "nul"

**Bad Code (bash):**
```bash
del /Q *.wixobj >nul 2>&1  # Creates "nul" file in Windows
```

**Solution:**
```batch
REM Use proper Windows redirect syntax
del /Q *.wixobj 2>NUL

REM Or suppress errors differently
del /Q *.wixobj 2>NUL >NUL
```

**Prevention:** Use batch scripts for all Windows commands, never bash

---

### LGHT0103: The system cannot find the file 'App.msi'

**Full Error:**
```
error LGHT0103 : The system cannot find the file 'M:\Project\installer\App.msi'
```

**Cause:** Circular reference - heat.exe harvested the installer directory which contains the MSI being built

**Solution:**
```xml
<!-- Add to ExcludeFilter.xslt -->
<xsl:template match="wix:Directory[@Name='installer']" />
```

**Prevention:** Always exclude the installer directory from harvest

---

### CNDL0062: Component/@Directory attribute conflict

**Full Error:**
```
error CNDL0062 : The Component/@Directory attribute cannot be specified when the Component element is nested underneath a Directory element.
```

**Cause:** Component incorrectly nested inside Directory

**Bad Code:**
```xml
<Directory Id="INSTALLFOLDER" Name="App">
  <Component Id="..." Directory="INSTALLFOLDER">  <!-- Wrong -->
    <File Source="..." />
  </Component>
</Directory>
```

**Solution:**
```xml
<!-- Use DirectoryRef instead -->
<DirectoryRef Id="INSTALLFOLDER">
  <Component Id="..." Guid="...">
    <File Source="..." />
  </Component>
</DirectoryRef>
```

---

### LGHT1076: ICE validation warning

**Full Error:**
```
warning LGHT1076 : ICE61: This product should remove only older versions of itself...
```

**Cause:** Non-critical validation warning from Windows Installer

**Solution:** Suppress known safe warnings
```batch
light.exe ... -sice:ICE61 -sice:ICE69 ...
```

---

### Missing WixCA binary

**Full Error:**
```
error LGHT0094 : Unresolved reference to symbol 'Binary:WixCA'
```

**Cause:** WixUtilExtension not loaded (provides WixCA for WixShellExec)

**Solution:**
```batch
REM Add WixUtilExtension to both candle and light
candle.exe -ext WixUIExtension -ext WixUtilExtension ...
light.exe -ext WixUIExtension -ext WixUtilExtension ...
```

---

## PowerShell Errors

### 'Generate-SecretKey()' - An expression was expected after '('

**Full Error:**
```
At line:162 char:41
+         $secretKey = Generate-SecretKey()
+                                         ~
An expression was expected after '('.
```

**Cause:** PowerShell functions are called without parentheses

**Bad Code:**
```powershell
function Generate-SecretKey {
    # ...
}
$key = Generate-SecretKey()  # Wrong!
```

**Solution:**
```powershell
$key = Generate-SecretKey  # Correct: no parentheses
```

---

### Cannot overwrite variable $PID

**Full Error:**
```
param([int]$PID)
ParentContainsErrorRecordException: Cannot overwrite variable PID because it is read-only
```

**Cause:** $PID is a reserved automatic variable in PowerShell

**Solution:** Use different parameter name
```powershell
# Wrong
param([int]$PID)

# Right
param([int]$ProcessId)
```

**Other reserved variables to avoid:**
- $PID (current process ID)
- $PWD (current directory)
- $HOME (user home directory)
- $HOST (host program info)
- $PSScriptRoot (script directory)
- $TRUE, $FALSE, $NULL

---

### $PSScriptRoot is empty

**Full Error:** Script fails with paths like `\scripts\wizard.ps1` (missing drive)

**Cause:** $PSScriptRoot is not set when PowerShell is called with `-File` from bash

**Bad Code (bash):**
```bash
powershell -File build-msi.ps1
# Inside script: $PSScriptRoot is empty
```

**Solution:**
```batch
REM Use batch wrapper
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0build-msi.ps1"
```

Or pass explicit paths:
```powershell
powershell -Command "& { Set-Location 'C:\Project'; .\script.ps1 -Path 'C:\Project' }"
```

---

### Start-Process fails silently with paths containing spaces

**Symptom:** Start-Process returns success but nothing happens

**Cause:** Path escaping issues with paths like "C:\Program Files\App"

**Bad Code:**
```powershell
Start-Process -FilePath $pythonExe -ArgumentList $script -WindowStyle Hidden
# Fails silently if $pythonExe or $script contain spaces
```

**Solution:**
```powershell
# Wrap in cmd /c with proper escaping
$cmd = "cmd"
$args = "/c `"cd /d `"$ProjectDir`" && `"$pythonExe`" `"$script`"`""
Start-Process -FilePath $cmd -ArgumentList $args -WindowStyle Hidden
```

---

## Installer Behavior Issues

### Script launches before exit dialog is shown

**Symptom:** CONFIGURE.bat runs during installation, before user sees the checkbox

**Cause:** Custom action in InstallExecuteSequence runs during install, not after

**Bad Code:**
```xml
<InstallExecuteSequence>
  <Custom Action="LaunchConfig" After="InstallFinalize">...</Custom>
</InstallExecuteSequence>
```

**Solution:**
```xml
<!-- Use UI sequence publish event instead -->
<UI>
  <Publish Dialog="ExitDialog"
           Control="Finish"
           Event="DoAction"
           Value="LaunchApplication">WIXUI_EXITDIALOGOPTIONALCHECKBOX = 1</Publish>
</UI>
```

---

### Launch checkbox doesn't work

**Symptom:** Checkbox shows but script doesn't launch when checked

**Cause:** Missing UI publish event or wrong WixShellExecTarget syntax

**Solution:**
```xml
<!-- Set the target (use file ID from ApplicationFiles.wxs) -->
<Property Id="WixShellExecTarget" Value="[#filCONFIGURE_BAT_ID]" />

<!-- Define the custom action -->
<CustomAction Id="LaunchApplication"
              BinaryKey="WixCA"
              DllEntry="WixShellExec"
              Impersonate="yes" />

<!-- Wire to exit dialog Finish button -->
<UI>
  <Publish Dialog="ExitDialog"
           Control="Finish"
           Event="DoAction"
           Value="LaunchApplication">WIXUI_EXITDIALOGOPTIONALCHECKBOX = 1</Publish>
</UI>
```

**Finding file ID:**
```bash
grep "CONFIGURE.bat" ApplicationFiles.wxs
# Output: <File Id="filD896..." Source="...\CONFIGURE.bat" />
# Use: [#filD896...]
```

---

### License.rtf not found during build

**Full Error:**
```
error LGHT0001: Cannot open file 'License.rtf'
```

**Cause:** License file not in correct location relative to .wxs file

**Solution:**
```
installer/
├── App.wxs          ← WiX source
├── License.rtf      ← Must be in same directory
└── rebuild-msi.bat
```

Reference in WiX:
```xml
<WixVariable Id="WixUILicenseRtf" Value="License.rtf" />
<!-- Not: Value="installer\License.rtf" -->
```

---

### MSI is 40+ MB (expected 1-5 MB)

**Symptom:** Source-only installer is huge

**Cause:** Exclusion filter failed to exclude development files

**Diagnosis:**
```powershell
# Extract MSI to verify contents
msiexec /a App.msi /qb TARGETDIR="C:\Temp\Verify"
dir "C:\Temp\Verify\App" /s

# Check for files that should be excluded:
# - venv/           (Python virtual environment)
# - instance/       (database, logs)
# - .git/           (Git repository)
# - __pycache__/    (Python bytecode)
# - *.db, *.sqlite3 (database files)
# - deployment-data/ (data packages)
# - installer/      (MSI and build artifacts)
```

**Solution:**
```xml
<!-- ExcludeFilter.xslt must exclude entire directories -->
<xsl:template match="wix:Directory[@Name='venv']" />
<xsl:template match="wix:Directory[@Name='instance']" />
<xsl:template match="wix:Directory[@Name='installer']" />
<xsl:template match="wix:Directory[@Name='deployment-data']" />
<xsl:template match="wix:Directory[@Name='.git']" />

<!-- Also exclude by file extension -->
<xsl:template match="wix:Component[contains(wix:File/@Source, '.db')]" />
<xsl:template match="wix:Component[contains(wix:File/@Source, '.sqlite3')]" />
```

**Verification:**
```powershell
# After rebuild, check size
$msi = Get-Item App.msi
$msi.Length / 1MB  # Should be < 5 MB for source-only
```

---

## Configuration Wizard Issues

### "Not running as Administrator" error blocks wizard

**Symptom:** Wizard exits immediately with admin check error

**Cause:** Wizard requires admin but user didn't run as admin

**Bad Code:**
```batch
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Not running as Administrator
    exit /b 1  # Blocks user
)
```

**Solution:** Auto-elevate instead of blocking
```batch
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b  # Exit non-elevated instance
)
# Script continues as admin after UAC prompt
```

---

### Python not found after installation

**Symptom:** Wizard fails with "python: command not found"

**Cause:** Python not in PATH or not installed

**Solution:**
```powershell
function Test-PythonInstalled {
    try {
        $version = python --version 2>&1
        if ($version -match "Python 3\.\d+") {
            Write-Host "[OK] Python found: $version" -ForegroundColor Green
            return $true
        }
    } catch {
        # Python not found
    }

    Write-Host "[ERROR] Python 3.x not found" -ForegroundColor Red
    Write-Host "Please install Python from: https://www.python.org/" -ForegroundColor Yellow
    return $false
}

# In main wizard flow
if (-not (Test-PythonInstalled)) {
    pause
    exit 1
}
```

---

### Dependency installation fails

**Symptom:** `pip install -r requirements.txt` fails

**Common Causes:**

**1. No internet connection**
```powershell
# Test connectivity
Test-NetConnection pypi.org -Port 443
```

**2. pip not up-to-date**
```powershell
# Upgrade pip first
.\venv\Scripts\python -m pip install --upgrade pip
.\venv\Scripts\pip install -r requirements.txt
```

**3. Compilation requirements (Visual C++)**
```powershell
# Some packages need Visual C++ build tools
# Provide alternative wheels or instruct user to install:
# https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

**4. Firewall blocking**
```powershell
# Use trusted host if corporate firewall blocks HTTPS
.\venv\Scripts\pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

---

## Runtime Issues

### Application doesn't start after configuration

**Diagnostic Steps:**

**1. Check if venv was created**
```powershell
Test-Path "venv\Scripts\python.exe"  # Should be True
```

**2. Check if dependencies installed**
```powershell
.\venv\Scripts\pip list  # Should show all requirements
```

**3. Check if database initialized**
```powershell
Test-Path "instance\app.db"  # Should exist
```

**4. Check if .env file created**
```powershell
Test-Path ".env"  # Should exist
Get-Content .env  # Verify SECRET_KEY, etc.
```

**5. Try manual start**
```powershell
.\venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
# Check error output
```

---

### Database migrations fail silently

**Symptom:** Application starts but shows no data or errors about missing tables

**Cause:** Django migrations not applied during setup

**Solution:**
```powershell
# In post-install wizard
Write-Host "[5/8] Running database migrations..." -ForegroundColor Cyan
$migrateOutput = & "venv\Scripts\python.exe" manage.py migrate 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Failure "Database migration failed"
    $migrateOutput | Write-Host
    exit 1
}
```

---

## Post-Deployment Issues

### Issue 13: 32-bit vs 64-bit PowerShell $env:ProgramFiles Mismatch

**Symptom:** Wizard fails with "Installation directory not found: C:\Program Files (x86)\Operations Hub" when MSI installed to "C:\Program Files\Operations Hub"

**Root Cause:**
- MSI installs to 64-bit Program Files
- CONFIGURE.bat may launch 32-bit PowerShell
- `$env:ProgramFiles` on 32-bit = `C:\Program Files (x86)`
- `$env:ProgramW6432` = `C:\Program Files` (64-bit location)

**Wrong Approach:**
```powershell
# Wizard default path
param([string]$InstallPath = "$env:ProgramFiles\Operations Hub")
# On 32-bit PowerShell: C:\Program Files (x86)\Operations Hub ❌
# On 64-bit PowerShell: C:\Program Files\Operations Hub ✓
```

**Solution 1: Pass explicit path from batch file**
```batch
REM CONFIGURE.bat - Strip trailing backslash then pass path
set "INSTALL_DIR=%~dp0"
if "%INSTALL_DIR:~-1%"=="\" set "INSTALL_DIR=%INSTALL_DIR:~0,-1%"
powershell -File scripts\wizard.ps1 -InstallPath "%INSTALL_DIR%"
```

**Solution 2: Force 64-bit PowerShell**
```batch
%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -File ...
```

**Prevention:** Always pass installation path explicitly from MSI environment, never rely on environment variables in PowerShell

**Time Lost:** 30 minutes
**Impact:** Critical - Blocks entire configuration wizard on 32-bit PowerShell

---

### Issue 14: Quote Escaping with %~dp0 Trailing Backslash

**Symptom:** PowerShell error: "Illegal characters in path" - path contains literal quote character

**Root Cause:**
- `%~dp0` always ends with backslash: `C:\Program Files\Operations Hub\`
- When used in quotes: `"%~dp0"`
- Backslash escapes the closing quote: `"C:\Program Files\Operations Hub\"`
- PowerShell receives: `C:\Program Files\Operations Hub"` (quote becomes part of string)

**Wrong Approach:**
```batch
REM Backslash escapes the quote!
powershell -File wizard.ps1 -InstallPath "%~dp0"
REM PowerShell sees: -InstallPath "C:\Program Files\Operations Hub\"
REM Which becomes: C:\Program Files\Operations Hub" (malformed)
```

**Correct Solution:**
```batch
REM Strip trailing backslash before passing to PowerShell
set "INSTALL_DIR=%~dp0"
if "%INSTALL_DIR:~-1%"=="\" set "INSTALL_DIR=%INSTALL_DIR:~0,-1%"
powershell -File wizard.ps1 -InstallPath "%INSTALL_DIR%"
REM PowerShell sees: -InstallPath "C:\Program Files\Operations Hub" ✓
```

**Key Insight:** This is a critical Windows batch scripting gotcha that affects all paths with spaces when using `%~dp0` in quoted arguments.

**Prevention:** Always strip trailing backslash from `%~dp0` before passing to PowerShell

**Time Lost:** 45 minutes
**Impact:** Critical - Causes cryptic "illegal characters" error

---

### Issue 15: Dependency Version Doesn't Exist in PyPI

**Symptom:** `pip install` fails: "No matching distribution found for BAC0==24.9.6"

**Root Cause:**
- `requirements.txt` specified non-existent version
- Package uses different versioning scheme (e.g., calendar versioning)
- Version typo or version removed from PyPI

**Wrong Approach:**
```txt
# requirements.txt - Version doesn't exist
BAC0==24.9.6
```

**Correct Solution:**
```txt
# Verify version exists in PyPI before packaging
BAC0==2024.9.20  # Latest stable 2024.9 release
```

**Verification:**
```bash
# Check available versions
pip index versions BAC0

# Or search PyPI
curl https://pypi.org/pypi/BAC0/json | jq '.releases | keys'
```

**Prevention:**
1. Test `pip install -r requirements.txt` in clean virtualenv before creating MSI
2. Use version ranges for flexibility: `BAC0>=2024.9.0,<2025.0.0`
3. Pin exact versions only after verification

**Key Insight:** MSI testing must include full dependency installation, not just file packaging

**Time Lost:** 15 minutes
**Impact:** High - Blocks entire installation

---

### Issue 16: Pip Self-Upgrade File Locking on Windows

**Symptom:** PowerShell wizard fails during pip upgrade with "ERROR: To modify pip, please run the following command..."

**Root Cause:**
- When `pip.exe install --upgrade pip` is executed, pip tries to upgrade itself
- On Windows, pip.exe is locked by the current process (can't modify running executable)
- Python prevents modifying files that are currently in use
- Error message is cryptic and doesn't explain the Windows file locking issue

**Wrong Approach:**
```powershell
# WRONG - pip.exe can't upgrade itself while running
& "venv\Scripts\pip.exe" install --upgrade pip setuptools wheel
# Error: "To modify pip, please run the following command..."
```

**Correct Solution:**
```powershell
# RIGHT - Use python -m pip to launch new process
& "venv\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel
```

**Why This Works:**
- `python -m pip` launches a new Python process
- The new process loads pip as a module (not pip.exe)
- pip can now upgrade pip.exe because it's not the currently running file
- This is the recommended approach from pip documentation

**Alternative Approach (Skip upgrade if recent):**
```powershell
$pipVersion = & "venv\Scripts\pip.exe" --version
if ($pipVersion -match "pip (\d+)\.(\d+)") {
    $major = [int]$Matches[1]
    $minor = [int]$Matches[2]
    if ($major -ge 24) {
        Write-Host "  pip $major.$minor is recent enough, skipping upgrade" -ForegroundColor Gray
        $skipPipUpgrade = $true
    }
}

if (-not $skipPipUpgrade) {
    & "venv\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel
}
```

**Prevention:**
1. **Always use** `python -m pip` for pip operations in scripts
2. **Never invoke** `pip.exe` directly for upgrade operations
3. **Test wizard** in clean environment before building MSI

**Key Insight:** Windows file locking prevents self-modification of running executables. Always use `python -m pip` for pip operations, especially upgrades.

**Time Lost:** 30 minutes
**Impact:** High - Blocks dependency installation

---

### Issue 17: MSI Only Packaged .pyc Bytecode Files, Not .py Source Files

**Symptom:** After MSI installation, application directory only contains `.pyc` bytecode files in `__pycache__/` directories, no `.py` source files

**Root Cause:**
- WiX `heat.exe` harvesting collected only bytecode files
- Likely due to harvesting from a directory where `.py` files were previously excluded or moved
- Or heat.exe was run with incorrect file pattern filters

**Diagnosis:**
```powershell
# Extract MSI to verify contents
msiexec /a App.msi /qb TARGETDIR="C:\Temp\Verify"

# Check for .py files
Get-ChildItem "C:\Temp\Verify" -Recurse -Filter "*.py" | Measure-Object
# Should return > 0 files

# Check what was actually packaged
Get-ChildItem "C:\Temp\Verify" -Recurse -Filter "*.pyc" | Measure-Object
# If .pyc > 0 but .py = 0, this issue is present
```

**Impact:**
- Application cannot run (Python needs source files)
- Debugging is impossible (no source code)
- Modifications cannot be made
- **CRITICAL BLOCKER** - Requires full MSI rebuild

**Wrong Approach:**
```batch
REM Harvesting from wrong directory or with wrong settings
heat.exe dir "%SOURCE%\__pycache__" -cg AppComponents -out AppFiles.wxs
REM This only gets bytecode!
```

**Correct Solution:**
```batch
REM Harvest from source directory, ensuring .py files are included
REM Verify SOURCE points to actual source code, not build artifacts
set "SOURCE=%~dp0.."

REM Ensure source directory has .py files
dir /s /b "%SOURCE%\*.py" | findstr /c:".py" >nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: No .py files found in %SOURCE%
    exit /b 1
)

REM Harvest with proper file pattern
heat.exe dir "%SOURCE%" ^
    -cg ApplicationComponents ^
    -dr INSTALLFOLDER ^
    -gg -g1 -sf -srd -sreg ^
    -var var.SourceDir ^
    -t ExcludeFilter.xslt ^
    -out ApplicationFiles.wxs

REM Verify .py files were captured
findstr /c:".py\"" ApplicationFiles.wxs >nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: No .py files in ApplicationFiles.wxs
    exit /b 1
)
```

**Prevention Checklist:**
- [ ] Verify SOURCE directory contains `.py` files before harvesting
- [ ] Check `ApplicationFiles.wxs` contains `.py` file references (not just `.pyc`)
- [ ] Extract and inspect MSI contents before distribution
- [ ] Test MSI installation on clean machine and verify `.py` files exist
- [ ] Add automated check to build script (see example above)

**Key Insight:** Windows file locking and Python's bytecode caching can create situations where only `.pyc` files are visible or accessible during harvesting. Always verify source files are present before and after harvest.

**Time Lost:** 2-4 hours (typically discovered during deployment testing)
**Impact:** Critical - Requires full MSI rebuild and redeployment
**Detection:** MSI installation completes but application won't start

**Automated Detection:**
```batch
REM Add to rebuild-msi.bat after heat.exe
echo Verifying .py files were harvested...
findstr /c:".py\"" ApplicationFiles.wxs | find /c ".py" > temp.txt
set /p COUNT=<temp.txt
del temp.txt

if %COUNT% LSS 10 (
    echo WARNING: Only %COUNT% .py files found in ApplicationFiles.wxs
    echo Expected at least 10 .py files. Check harvest directory.
    pause
    exit /b 1
)
echo [OK] Found %COUNT% .py files in harvest
```

---

## Preventive Checks

Before releasing installer, verify:

```powershell
# 1. MSI size check
$msi = Get-Item App.msi
if ($msi.Length -gt 10MB) {
    Write-Warning "MSI is $($msi.Length / 1MB) MB - check exclusions"
}

# 2. Extract and inspect
msiexec /a App.msi /qb TARGETDIR="C:\Temp\Verify"
$extracted = Get-ChildItem "C:\Temp\Verify" -Recurse
if ($extracted | Where-Object Name -eq "venv") {
    Write-Error "venv/ should not be in MSI"
}
if ($extracted | Where-Object Extension -eq ".db") {
    Write-Error ".db files should not be in MSI"
}

# 3. Component count
$wxs = Get-Content ApplicationFiles-Fixed.wxs
$components = ([regex]::Matches($wxs, '<Component ')).Count
Write-Host "Components in MSI: $components"
# Should be 500-800 for typical app

# 4. Verify file ID exists
$configBatId = ([regex]::Match($wxs, 'File Id="([^"]+)"[^>]*CONFIGURE\.bat')).Groups[1].Value
Write-Host "CONFIGURE.bat file ID: $configBatId"
# Should match ID in main .wxs file

# 5. Test requirements.txt in clean environment
python -m venv test-venv
& "test-venv\Scripts\python.exe" -m pip install -r requirements.txt
# Should complete without "No matching distribution" errors
Remove-Item test-venv -Recurse -Force

# 6. Verify %~dp0 trailing backslash is stripped
# In CONFIGURE.bat, ensure this pattern is used:
# set "INSTALL_DIR=%~dp0"
# if "%INSTALL_DIR:~-1%"=="\" set "INSTALL_DIR=%INSTALL_DIR:~0,-1%"
```

---

## Summary of All 17 Critical Issues

| # | Issue | Category | Time Lost | Prevention |
|---|-------|----------|-----------|------------|
| 1 | Bash redirect creates literal "nul" file | Build | 2h | Use batch scripts |
| 2 | $PSScriptRoot empty from bash | Build | 1h | Pass explicit paths |
| 3 | Component references mismatch | Build | 3h | Run fix-wix-refs.py |
| 4 | MSI included excluded files | Build | 2h | Test exclusions |
| 5 | WixShellExecTarget requires file reference | Build | 1h | Use [#fileID] syntax |
| 6 | PowerShell function call with () | Wizard | 30min | No parentheses |
| 7 | Script launched before exit dialog | Build | 1h | Use UI Publish |
| 8 | License.rtf not found | Build | 30min | Keep in installer/ |
| 9 | Missing WixUtilExtension | Build | 30min | Load both extensions |
| 10 | Circular reference | Build | 1h | Exclude installer/ |
| 11 | Admin check blocked script | Wizard | 30min | Auto-elevate |
| 12 | Path spaces in Start-Process | Wizard | 1h | Use cmd /c wrapper |
| 13 | 32/64-bit PowerShell paths | Deploy | 30min | Pass explicit path |
| 14 | %~dp0 trailing backslash | Deploy | 45min | Strip backslash |
| 15 | Non-existent PyPI version | Deploy | 15min | Test requirements.txt |
| 16 | Pip self-upgrade locking | Deploy | 30min | Use python -m pip |
| 17 | MSI only packaged .pyc files | Build | 2-4h | Verify source files |

**Total Time Lost:** ~19.5 hours
**With Skill Guidance:** ~2 hours
**Time Saved:** ~17.5 hours per installer
**Value Delivered:** Prevents 17+ hours of debugging per installer

---

*End of Troubleshooting Guide*
