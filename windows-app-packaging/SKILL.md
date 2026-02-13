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
**Size:** ~15 KB
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

## Quick Start: Create MSI in 5 Steps

### Step 1: Create WiX Source File

Use template from `references/wix-templates.md` → Minimal installer.

Key sections:
```xml
<Product Id="*" Name="YourApp" Version="1.0.0.0" ...>
  <Package .../>
  <MajorUpgrade .../>
  <MediaTemplate EmbedCab="yes" />

  <!-- UI with license -->
  <UIRef Id="WixUI_InstallDir" />
  <WixVariable Id="WixUILicenseRtf" Value="License.rtf" />

  <!-- Directory structure -->
  <Directory Id="TARGETDIR" Name="SourceDir">
    <Directory Id="ProgramFiles64Folder">
      <Directory Id="INSTALLFOLDER" Name="YourApp" />
    </Directory>
  </Directory>

  <!-- Components -->
  <ComponentGroupRef Id="ApplicationFiles" />
</Product>
```

### Step 2: Create Exclusion Filter

Use template from `references/exclusion-filters.md`.

Critical exclusions:
- venv/, .git/, __pycache__/
- instance/, deployment-data/
- installer/ (to avoid circular reference)
- *.db, *.sqlite3, *.log
- Build artifacts

### Step 3: Create Build Script

Use template from `references/build-scripts.md` → rebuild-msi.bat.

Script does:
1. Clean build artifacts
2. Harvest files with heat.exe
3. Fix component references (Python script)
4. Compile with candle.exe
5. Link with light.exe
6. Verify size (should be < 5 MB for source-only)

### Step 4: Create Post-Install Wizard

Use template from `references/post-install-wizard.md`.

PowerShell wizard handles:
- Dependency checks
- Virtual environment setup
- Configuration prompts
- Database initialization
- Server startup

### Step 5: Build and Test

```batch
cd installer
.\rebuild-msi.bat
```

**Verification checklist:**
- [ ] MSI size < 5 MB (for source-only apps)
- [ ] License agreement shows
- [ ] Directory selection works
- [ ] Files install to correct location
- [ ] Start Menu shortcuts created
- [ ] Exit dialog checkbox shows
- [ ] Config wizard launches after clicking Finish
- [ ] Wizard completes without errors
- [ ] Application runs after configuration

---

## Critical Patterns

### Pattern 1: Use Batch Scripts for WiX Tools

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

### Pattern 2: Post-Process Component References

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

### Pattern 3: Aggressive Exclusions

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

### Pattern 4: Exit Dialog Launch (CRITICAL - Multi-Step Process)

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

### Pattern 5: Auto-Elevation for Configuration Script

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

### Pattern 6: PowerShell Function Calls (No Parentheses)

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

---

## Post-Install Wizard Pattern

**Purpose:** Handle configuration that MSI cannot do during installation

**Responsibilities:**
1. Check dependencies (Python, Node.js, etc.)
2. Create virtual environment
3. Install dependencies (pip, npm)
4. Prompt for configuration (keys, URLs, domains)
5. Generate secrets automatically
6. Initialize database / run migrations
7. Collect static files
8. Offer to start application

**Template:** `references/post-install-wizard.md`

**Key Functions:**

```powershell
function Generate-SecretKey {
    $bytes = New-Object byte[] 32
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    $rng.GetBytes($bytes)
    return [Convert]::ToBase64String($bytes)
}

function Test-PythonInstalled {
    try {
        $version = python --version 2>&1
        return $version -match "Python 3\.\d+"
    } catch {
        return $false
    }
}

function Create-VirtualEnvironment {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Virtual environment created" -ForegroundColor Green
        return $true
    } else {
        Write-Host "[ERROR] Failed to create virtual environment" -ForegroundColor Red
        return $false
    }
}

function Install-Dependencies {
    Write-Host "Installing dependencies (this may take 10-15 minutes)..." -ForegroundColor Yellow
    .\venv\Scripts\pip install -r requirements.txt --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Dependencies installed" -ForegroundColor Green
        return $true
    } else {
        Write-Host "[ERROR] Dependency installation failed" -ForegroundColor Red
        return $false
    }
}
```

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

## Troubleshooting Guide

### Error: LGHT0094 - Unresolved reference to Component 'cmpXXX'

**Cause:** XSLT excluded component but ComponentRef still exists

**Fix:** Run fix-wix-refs.py after heat.exe

```batch
"%WIX_BIN%\heat.exe" ... -out ApplicationFiles.wxs
python fix-wix-refs.py  # Cleans invalid references
"%WIX_BIN%\candle.exe" ... ApplicationFiles-Fixed.wxs
```

### Error: HEAT5059 - File 'nul' cannot be found

**Cause:** Bash redirect syntax created literal "nul" file

**Fix:** Use batch script with proper Windows redirect
```batch
REM WRONG (in bash): del /Q *.obj >nul 2>&1
REM RIGHT (in batch): del /Q *.obj 2>NUL
```

### Error: $PSScriptRoot is empty

**Cause:** PowerShell script called with -File from bash

**Fix:** Pass explicit paths or use batch wrapper
```batch
REM Batch wrapper
powershell -ExecutionPolicy Bypass -File "%~dp0scripts\wizard.ps1"
```

### Error: MSI is 40+ MB (expected < 5 MB)

**Cause:** Exclusion filter failed to exclude directories

**Fix:**
1. Verify XSLT syntax
2. Check that installer/ itself is excluded (prevents circular reference)
3. Exclude entire directories, not just files
4. Extract MSI to verify contents

```powershell
# Verify exclusions worked
msiexec /a YourApp.msi /qb TARGETDIR="C:\Temp\Verify"
dir "C:\Temp\Verify" /s  # Should NOT see venv, instance, .git, *.db
```

### Error: Generate-SecretKey() - Expression expected after '('

**Cause:** PowerShell functions don't use parentheses

**Fix:** Remove parentheses from function call
```powershell
$key = Generate-SecretKey  # NOT Generate-SecretKey()
```

### Error: Configuration script launches during installation

**Cause:** Custom action in InstallExecuteSequence

**Fix:** Remove from InstallExecuteSequence, use WixShellExecTarget
```xml
<!-- Remove these -->
<InstallExecuteSequence>
  <Custom Action="LaunchConfig" After="InstallFinalize">...</Custom>
</InstallExecuteSequence>

<!-- Use this instead -->
<Property Id="WixShellExecTarget" Value="[#filCONFIGURE_BAT_ID]" />
```

### Error: License.rtf not found during build

**Cause:** License file not in installer/ directory

**Fix:** Place License.rtf in same directory as .wxs file
```
installer/
├── YourApp.wxs
├── License.rtf       ← Must be here
└── rebuild-msi.bat
```

### Error: LGHT0103 - The system cannot find the file (circular reference)

**Cause:** heat.exe harvested the installer directory itself

**Fix:** Exclude installer/ directory in XSLT
```xml
<xsl:template match="wix:Directory[@Name='installer']" />
```

---

## WixUI Templates

### WixUI_InstallDir (Recommended)

Professional installer with:
- Welcome screen
- License agreement (must accept)
- Installation folder selection
- Progress bar
- Exit dialog with launch option

```xml
<UIRef Id="WixUI_InstallDir" />
<Property Id="WIXUI_INSTALLDIR" Value="INSTALLFOLDER" />
<WixVariable Id="WixUILicenseRtf" Value="License.rtf" />
```

### WixUI_Minimal

Bare bones installer (not recommended for production):
- Install immediately
- No license, no directory choice
- No exit dialog customization

---

## License File Format

WiX requires **RTF format** (not .txt or .md) for license agreement.

**Create from Word:**
1. Write license in Microsoft Word
2. Save As → Rich Text Format (.rtf)
3. Place in installer/ directory

**Or convert from text:**
```powershell
# Basic RTF wrapper
$licenseText = Get-Content LICENSE.txt -Raw
$rtf = "{\rtf1\ansi\deff0 {\fonttbl {\f0 Courier New;}}\f0\fs20 " +
       $licenseText.Replace("`n", "\par`n") +
       "}"
Set-Content -Path installer\License.rtf -Value $rtf -Encoding ASCII
```

---

## Size Expectations

| MSI Type | Typical Size | Contents |
|----------|-------------|----------|
| Source-only (Python/Node) | 1-5 MB | Code, templates, docs |
| With embedded Python | 15-25 MB | Code + python-embed/ |
| Full app + dependencies | 50-200 MB | Everything (not recommended) |

**If MSI > 5 MB for source-only app:**
- Exclusions probably failed
- Extract MSI and inspect contents
- Check for venv/, instance/, *.db files

---

## Checklist: Production-Ready Installer

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

## Integration with windows-app-build

When packaging is complete:

1. Update APP-STATE.yaml with installer version
2. Create release tag in Git
3. Document in CHANGELOG.md
4. Test on clean VM before distribution

**Cross-reference:**
- Build patterns: `/mnt/skills/user/windows-app-build/SKILL.md`
- System design: `/mnt/skills/user/windows-app-system-design/SKILL.md`

---

## Full Templates

**Complete templates in references:**

1. **wix-templates.md** - Full WiX installer examples
2. **build-scripts.md** - Batch script templates
3. **exclusion-filters.md** - XSLT filter library
4. **post-install-wizard.md** - PowerShell wizard template
5. **troubleshooting.md** - Detailed error solutions

---

*End of Windows Application Packaging Skill*
