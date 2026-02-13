# Critical Packaging Patterns

## Pattern 1: Use Batch Scripts for WiX Tools

**❌ WRONG: Run WiX tools from bash**
```bash
# Fails: path quoting, redirects, $PSScriptRoot issues
heat.exe dir "C:\App" -out files.wxs
candle.exe -arch x64 app.wxs
```

**✅ RIGHT: Comprehensive batch script**
```batch
@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

set "WIX_BIN=C:\Program Files (x86)\WiX Toolset v3.14\bin"
set "SOURCE_DIR=%~dp0.."

REM Clean
del /Q *.wixobj *.wixpdb ApplicationFiles*.wxs 2>NUL

REM Harvest
"%WIX_BIN%\heat.exe" dir "%SOURCE_DIR%" ^
    -cg ApplicationFiles ^
    -gg -sfrag -srd -sreg ^
    -dr INSTALLFOLDER ^
    -var var.SourceDir ^
    -out ApplicationFiles.wxs ^
    -t ExcludeFilter.xslt

REM Fix references (Python post-processor)
python fix-wix-refs.py

REM Compile
"%WIX_BIN%\candle.exe" ^
    -dSourceDir="%SOURCE_DIR%" ^
    -arch x64 ^
    -ext WixUIExtension ^
    -ext WixUtilExtension ^
    -out App.wixobj ^
    App.wxs

"%WIX_BIN%\candle.exe" ^
    -dSourceDir="%SOURCE_DIR%" ^
    -arch x64 ^
    -ext WixUIExtension ^
    -ext WixUtilExtension ^
    -out ApplicationFiles.wixobj ^
    ApplicationFiles-Fixed.wxs

REM Link
"%WIX_BIN%\light.exe" ^
    -ext WixUIExtension ^
    -ext WixUtilExtension ^
    -cultures:en-US ^
    -out App-1.0.0.msi ^
    -spdb ^
    -sice:ICE61 ^
    -sice:ICE69 ^
    App.wixobj ^
    ApplicationFiles.wixobj

echo MSI built successfully
dir /-C App-1.0.0.msi | find ".msi"
```

## Pattern 2: Post-Process Component References

**Problem:** XSLT excludes components but leaves ComponentRef entries → linker errors

**Solution:** Python script validates and cleans

```python
# fix-wix-refs.py
import xml.etree.ElementTree as ET

tree = ET.parse("ApplicationFiles.wxs")
root = tree.getroot()
ns = {"wix": "http://schemas.microsoft.com/wix/2006/wi"}

# Find all existing components
existing_components = set()
for component in root.findall(".//wix:Component", ns):
    comp_id = component.get("Id")
    if comp_id:
        existing_components.add(comp_id)

# Remove ComponentRef entries for non-existent components
removed_count = 0
for component_group in root.findall(".//wix:ComponentGroup", ns):
    refs_to_remove = []
    for ref in component_group.findall("wix:ComponentRef", ns):
        ref_id = ref.get("Id")
        if ref_id and ref_id not in existing_components:
            refs_to_remove.append(ref)

    for ref in refs_to_remove:
        component_group.remove(ref)
        removed_count += 1

tree.write("ApplicationFiles-Fixed.wxs", encoding="UTF-8", xml_declaration=True)
print(f"Found {len(existing_components)} existing components")
print(f"Removed {removed_count} invalid component references")
```

## Pattern 3: Aggressive Exclusions

**Problem:** MSI includes development artifacts → 40+ MB bloated installer

**Solution:** Exclude entire directories, all database files

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:wix="http://schemas.microsoft.com/wix/2006/wi">

  <!-- Identity template -->
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()" />
    </xsl:copy>
  </xsl:template>

  <!-- Exclude development directories -->
  <xsl:template match="wix:Directory[@Name='venv']" />
  <xsl:template match="wix:Directory[@Name='.git']" />
  <xsl:template match="wix:Directory[@Name='__pycache__']" />
  <xsl:template match="wix:Directory[@Name='.pytest_cache']" />

  <!-- Exclude data directories -->
  <xsl:template match="wix:Directory[@Name='instance']" />
  <xsl:template match="wix:Directory[@Name='deployment-data']" />
  <xsl:template match="wix:Directory[@Name='temp_energy_images']" />

  <!-- CRITICAL: Exclude installer directory (prevents circular reference) -->
  <xsl:template match="wix:Directory[@Name='installer']" />

  <!-- Exclude database files -->
  <xsl:template match="wix:Component[contains(wix:File/@Source, '.db')]" />
  <xsl:template match="wix:Component[contains(wix:File/@Source, '.sqlite3')]" />
  <xsl:template match="wix:Component[contains(wix:File/@Source, '.db-journal')]" />

  <!-- Exclude log files -->
  <xsl:template match="wix:Component[contains(wix:File/@Source, '.log')]" />

  <!-- Exclude Python bytecode -->
  <xsl:template match="wix:Component[substring(wix:File/@Source, string-length(wix:File/@Source) - 3) = '.pyc']" />
  <xsl:template match="wix:Component[substring(wix:File/@Source, string-length(wix:File/@Source) - 3) = '.pyo']" />

  <!-- Exclude .env file (user must create) -->
  <xsl:template match="wix:Component[wix:File/@Name='.env']" />

</xsl:stylesheet>
```

**Verification:**
```powershell
# Extract MSI and verify
msiexec /a App.msi /qb TARGETDIR="C:\Temp\Verify"
dir "C:\Temp\Verify\App\" /s  # Check contents
```

## Pattern 4: Exit Dialog Launch (CRITICAL - Multi-Step Process)

**This is the most error-prone part of MSI creation. Follow exactly:**

**Step 1: Find the CONFIGURE.bat file ID**
```bash
grep "CONFIGURE.bat" ApplicationFiles-Fixed.wxs
# Output: <File Id="filD89685035D6AFFAB7EBB90E93B5DB01B" KeyPath="yes" Source="$(var.SourceDir)\CONFIGURE.bat" />
# Copy the file ID: filD89685035D6AFFAB7EBB90E93B5DB01B
```

**Step 2: Configure the exit dialog properties**
```xml
<!-- Checkbox text and default state -->
<Property Id="WIXUI_EXITDIALOGOPTIONALCHECKBOXTEXT"
          Value="Launch configuration wizard (recommended)" />
<Property Id="WIXUI_EXITDIALOGOPTIONALCHECKBOX" Value="1" />
```

**Step 3: Set WixShellExecTarget with file reference**
```xml
<!-- CRITICAL: Use [#fileID] syntax with exact file ID from Step 1 -->
<Property Id="WixShellExecTarget" Value="[#filD89685035D6AFFAB7EBB90E93B5DB01B]" />
```

**Step 4: Define the launch custom action**
```xml
<CustomAction Id="LaunchApplication"
              BinaryKey="WixCA"
              DllEntry="WixShellExec"
              Impersonate="yes" />
```

**Step 5: Wire to exit dialog Finish button**
```xml
<UI>
  <Publish Dialog="ExitDialog"
           Control="Finish"
           Event="DoAction"
           Value="LaunchApplication">WIXUI_EXITDIALOGOPTIONALCHECKBOX = 1</Publish>
</UI>
```

**Complete example:**
```xml
<Product ...>
  <!-- Properties -->
  <Property Id="WIXUI_EXITDIALOGOPTIONALCHECKBOXTEXT"
            Value="Launch configuration wizard (recommended)" />
  <Property Id="WIXUI_EXITDIALOGOPTIONALCHECKBOX" Value="1" />
  <Property Id="WixShellExecTarget" Value="[#filD89685035D6AFFAB7EBB90E93B5DB01B]" />

  <!-- Custom Action -->
  <CustomAction Id="LaunchApplication"
                BinaryKey="WixCA"
                DllEntry="WixShellExec"
                Impersonate="yes" />

  <!-- UI Wiring -->
  <UI>
    <Publish Dialog="ExitDialog"
             Control="Finish"
             Event="DoAction"
             Value="LaunchApplication">WIXUI_EXITDIALOGOPTIONALCHECKBOX = 1</Publish>
  </UI>
</Product>
```

**❌ WRONG APPROACHES (Don't use these):**

**1. InstallExecuteSequence (runs during install, not after)**
```xml
<InstallExecuteSequence>
  <Custom Action="LaunchConfig" After="InstallFinalize">...</Custom>
</InstallExecuteSequence>
<!-- This runs BEFORE exit dialog, bad UX -->
```

**2. Hardcoded path without file reference**
```xml
<Property Id="WixShellExecTarget" Value="[INSTALLFOLDER]CONFIGURE.bat" />
<!-- Doesn't work - use [#fileID] syntax -->
```

**3. Missing UI Publish event**
```xml
<!-- Having WixShellExecTarget alone isn't enough -->
<!-- MUST wire to ExitDialog/Finish button via Publish event -->
```

**Debugging if launch doesn't work:**

1. **Verify file ID is correct** - Must match exactly
   ```bash
   grep "CONFIGURE.bat" ApplicationFiles-Fixed.wxs
   ```

2. **Check WixUtilExtension is loaded**
   ```batch
   candle.exe -ext WixUIExtension -ext WixUtilExtension ...
   light.exe -ext WixUIExtension -ext WixUtilExtension ...
   ```

3. **Test manually after install**
   - Navigate to installation folder
   - Double-click CONFIGURE.bat
   - Verify it runs without errors

4. **Check MSI log for launch attempt**
   ```batch
   msiexec /i App.msi /l*v install.log
   REM Search log for "LaunchApplication" and "WixShellExec"
   ```

## Pattern 5: Auto-Elevation for Configuration Script

**Problem:** Users forget to "Run as Administrator"

**Solution:** Auto-elevate at script start

```batch
@echo off
REM Check for Administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

REM Rest of script runs as Administrator
setlocal EnableDelayedExpansion
cd /d "%~dp0"

echo Running with Administrator privileges...
echo.

REM Launch PowerShell wizard
powershell -ExecutionPolicy Bypass -File "scripts\post-install-wizard.ps1"
```

## Pattern 6: PowerShell Function Calls (No Parentheses)

**❌ WRONG:**
```powershell
function Generate-SecretKey {
    # ...
}

$key = Generate-SecretKey()  # ERROR: Expression expected after '('
```

**✅ RIGHT:**
```powershell
function Generate-SecretKey {
    $bytes = New-Object byte[] 32
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    $rng.GetBytes($bytes)
    return [Convert]::ToBase64String($bytes)
}

$key = Generate-SecretKey  # Correct: no parentheses
```

## Pattern 7: Strip %~dp0 Trailing Backslash (CRITICAL)

**Problem:** `%~dp0` ends with backslash, which escapes closing quote in PowerShell arguments

**❌ WRONG:**
```batch
REM %~dp0 = "C:\Program Files\Operations Hub\"
powershell -File wizard.ps1 -InstallPath "%~dp0"
REM PowerShell receives: C:\Program Files\Operations Hub"
REM ERROR: Illegal characters in path
```

**✅ RIGHT:**
```batch
@echo off
setlocal EnableDelayedExpansion

REM Strip trailing backslash
set "INSTALL_DIR=%~dp0"
if "%INSTALL_DIR:~-1%"=="\" set "INSTALL_DIR=%INSTALL_DIR:~0,-1%"

REM Now safe to pass to PowerShell
powershell -ExecutionPolicy Bypass -File "scripts\wizard.ps1" -InstallPath "%INSTALL_DIR%"
```

**Complete CONFIGURE.bat template:**
```batch
@echo off
REM Auto-elevate
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

REM Strip trailing backslash from installation path
setlocal EnableDelayedExpansion
set "INSTALL_DIR=%~dp0"
if "%INSTALL_DIR:~-1%"=="\" set "INSTALL_DIR=%INSTALL_DIR:~0,-1%"

REM Launch wizard with explicit path
powershell -ExecutionPolicy Bypass -File "%INSTALL_DIR%\scripts\post-install-wizard.ps1" -InstallPath "%INSTALL_DIR%"

pause
```

**Why This Matters:**
- Affects ALL installers with paths containing spaces
- Error message ("Illegal characters") is cryptic
- Issue only occurs on 64-bit Windows in Program Files
- Prevents $PSScriptRoot from working correctly

**Time Saved:** 45 minutes per installer

## Pattern 8: Force 64-bit PowerShell or Pass Explicit Paths

**Problem:** 32-bit PowerShell sees different $env:ProgramFiles than 64-bit

**Context:**
- MSI installs to: `C:\Program Files\App` (64-bit)
- 32-bit PowerShell `$env:ProgramFiles` = `C:\Program Files (x86)`
- 64-bit PowerShell `$env:ProgramFiles` = `C:\Program Files`
- `$env:ProgramW6432` always = `C:\Program Files` (on 64-bit Windows)

**❌ WRONG:**
```powershell
# wizard.ps1
param([string]$InstallPath = "$env:ProgramFiles\Operations Hub")
# On 32-bit PS: C:\Program Files (x86)\Operations Hub ❌
# On 64-bit PS: C:\Program Files\Operations Hub ✓
```

**✅ RIGHT - Solution 1: Pass explicit path from batch**
```batch
REM CONFIGURE.bat knows actual install location via %~dp0
set "INSTALL_DIR=%~dp0"
if "%INSTALL_DIR:~-1%"=="\" set "INSTALL_DIR=%INSTALL_DIR:~0,-1%"
powershell -File wizard.ps1 -InstallPath "%INSTALL_DIR%"
```

**✅ RIGHT - Solution 2: Force 64-bit PowerShell**
```batch
REM Explicitly use 64-bit PowerShell
%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -File wizard.ps1
REM Now $env:ProgramFiles correctly points to C:\Program Files
```

**✅ RIGHT - Solution 3: Use ProgramW6432 in PowerShell**
```powershell
# Always use 64-bit Program Files on 64-bit Windows
param([string]$InstallPath = "$env:ProgramW6432\Operations Hub")
```

**Recommended:** Solution 1 (explicit path) - most reliable

## Pattern 9: Always Use `python -m pip` (Never pip.exe)

**Problem:** `pip.exe` can't upgrade itself on Windows due to file locking

**❌ WRONG:**
```powershell
# pip.exe tries to modify itself while running
& "venv\Scripts\pip.exe" install --upgrade pip setuptools wheel
# ERROR: To modify pip, please run the following command...
```

**✅ RIGHT:**
```powershell
# python -m pip launches new process
& "venv\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel
```

**Why This Works:**
- `python -m pip` launches new Python process
- New process loads pip as module (not pip.exe)
- pip can upgrade pip.exe because it's not running
- Recommended by pip documentation

**Apply to ALL pip operations:**
```powershell
# Create venv
python -m venv venv

# Upgrade pip
& "venv\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel

# Install dependencies
& "venv\Scripts\python.exe" -m pip install -r requirements.txt

# Install package
& "venv\Scripts\python.exe" -m pip install somepackage
```

**Time Saved:** 30 minutes debugging cryptic pip errors

## Pattern 10: Comprehensive Build Script Template

**Problem:** Manual orchestration is error-prone and not repeatable

**Solution:** Single batch script handles everything

```batch
@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"

REM Configuration
set "WIX_BIN=C:\Program Files (x86)\WiX Toolset v3.14\bin"
set "SOURCE_DIR=%~dp0.."
set "VERSION=1.0.0"
set "APP_NAME=OperationsHub"

echo ========================================
echo Building %APP_NAME% v%VERSION% MSI
echo ========================================
echo.

REM 1. Clean previous build artifacts
echo [1/6] Cleaning build artifacts...
del /Q *.wixobj *.wixpdb ApplicationFiles*.wxs 2>NUL
if exist "%APP_NAME%-*.msi" del /Q "%APP_NAME%-*.msi" 2>NUL

REM 2. Harvest files
echo [2/6] Harvesting application files...
"%WIX_BIN%\heat.exe" dir "%SOURCE_DIR%" ^
    -cg ApplicationFiles ^
    -gg -sfrag -srd -sreg ^
    -dr INSTALLFOLDER ^
    -var var.SourceDir ^
    -out ApplicationFiles.wxs ^
    -t ExcludeFilter.xslt

if %errorlevel% neq 0 (
    echo ERROR: heat.exe failed
    exit /b 1
)

REM 3. Fix component references
echo [3/6] Fixing component references...
python fix-wix-refs.py
if %errorlevel% neq 0 (
    echo ERROR: fix-wix-refs.py failed
    exit /b 1
)

REM 4. Compile
echo [4/6] Compiling WiX sources...
"%WIX_BIN%\candle.exe" ^
    -dSourceDir="%SOURCE_DIR%" ^
    -dVersion="%VERSION%" ^
    -arch x64 ^
    -ext WixUIExtension ^
    -ext WixUtilExtension ^
    -out "%APP_NAME%.wixobj" ^
    "%APP_NAME%-Minimal.wxs"

if %errorlevel% neq 0 (
    echo ERROR: candle.exe failed on main .wxs
    exit /b 1
)

"%WIX_BIN%\candle.exe" ^
    -dSourceDir="%SOURCE_DIR%" ^
    -arch x64 ^
    -ext WixUIExtension ^
    -ext WixUtilExtension ^
    -out "ApplicationFiles.wixobj" ^
    "ApplicationFiles-Fixed.wxs"

if %errorlevel% neq 0 (
    echo ERROR: candle.exe failed on ApplicationFiles.wxs
    exit /b 1
)

REM 5. Link
echo [5/6] Linking MSI...
"%WIX_BIN%\light.exe" ^
    -ext WixUIExtension ^
    -ext WixUtilExtension ^
    -cultures:en-US ^
    -out "%APP_NAME%-%VERSION%.msi" ^
    -spdb ^
    -sice:ICE61 ^
    -sice:ICE69 ^
    "%APP_NAME%.wixobj" ^
    "ApplicationFiles.wixobj"

if %errorlevel% neq 0 (
    echo ERROR: light.exe failed
    exit /b 1
)

REM 6. Verify
echo [6/6] Verifying MSI...
echo.
echo ========================================
echo MSI BUILD SUCCESSFUL
echo ========================================
dir /-C "%APP_NAME%-%VERSION%.msi" | find ".msi"
echo.

REM Check size
for %%A in ("%APP_NAME%-%VERSION%.msi") do set SIZE=%%~zA
set /A SIZE_MB=%SIZE% / 1048576
echo Size: %SIZE_MB% MB
if %SIZE_MB% GTR 10 (
    echo WARNING: MSI is larger than expected - verify exclusions
)

echo.
echo Build complete: %APP_NAME%-%VERSION%.msi
echo.
pause
```

**Benefits:**
- Repeatable builds
- Error handling at each step
- Clear progress indicators
- Automatic size validation
- Single command: `rebuild-msi.bat`
