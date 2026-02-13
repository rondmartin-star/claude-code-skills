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
# Should match ID in OperationsHub-Minimal.wxs
```

---

*End of Troubleshooting Guide*
