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
