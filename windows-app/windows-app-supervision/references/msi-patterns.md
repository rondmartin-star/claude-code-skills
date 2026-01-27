# MSI Packaging Patterns

Complete WiX Toolset templates and MSI packaging patterns for Windows applications.

---

## WiX Toolset Setup

### Installation

```batch
:: Download and install WiX Toolset 3.11
:: https://wixtoolset.org/releases/

:: Verify installation
candle.exe -?
light.exe -?
```

### Project Structure

```
installer/
├── Product.wxs          # Main product definition
├── Files.wxs            # File components
├── UI.wxs               # Custom UI (optional)
├── build.bat            # Build script
└── output/
    └── Setup.msi        # Final MSI package
```

---

## Basic MSI Template (Product.wxs)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*"
           Name="Property Management System"
           Language="1033"
           Version="1.0.0"
           Manufacturer="Your Company Name"
           UpgradeCode="PUT-GUID-HERE">

    <!-- Package properties -->
    <Package InstallerVersion="200"
             Compressed="yes"
             InstallScope="perMachine"
             Description="Property Management System Installer"
             Comments="Installs and configures Property Management System" />

    <!-- Media (embedded CAB) -->
    <MediaTemplate EmbedCab="yes" />

    <!-- Upgrade logic (major upgrade pattern) -->
    <MajorUpgrade DowngradeErrorMessage="A newer version of [ProductName] is already installed."
                  Schedule="afterInstallExecute" />

    <!-- Installation directory structure -->
    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="PropertyManagementSystem" />
      </Directory>

      <Directory Id="ProgramMenuFolder">
        <Directory Id="ApplicationProgramsFolder" Name="Property Management System" />
      </Directory>
    </Directory>

    <!-- Features to install -->
    <Feature Id="MainApplication" Title="Property Management System" Level="1">
      <ComponentGroupRef Id="ApplicationFiles" />
      <ComponentGroupRef Id="PythonFiles" />
      <ComponentRef Id="ApplicationShortcut" />
    </Feature>

    <!-- User interface -->
    <UIRef Id="WixUI_InstallDir" />
    <Property Id="WIXUI_INSTALLDIR" Value="INSTALLFOLDER" />

    <!-- License agreement -->
    <WixVariable Id="WixUILicenseRtf" Value="License.rtf" />

    <!-- Installation icons -->
    <Icon Id="ProductIcon" SourceFile="app.ico" />
    <Property Id="ARPPRODUCTICON" Value="ProductIcon" />

  </Product>
</Wix>
```

---

## File Components (Files.wxs)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Fragment>
    <!-- Application files -->
    <ComponentGroup Id="ApplicationFiles" Directory="INSTALLFOLDER">

      <!-- Main scripts -->
      <Component Id="InstallScript" Guid="PUT-GUID-HERE">
        <File Id="InstallAndRun" Source="INSTALL-AND-RUN.bat" KeyPath="yes" />
      </Component>

      <Component Id="UpdateScript" Guid="PUT-GUID-HERE">
        <File Id="UpdateBat" Source="UPDATE.bat" KeyPath="yes" />
      </Component>

      <!-- Scripts directory -->
      <Component Id="ScriptsDir" Guid="PUT-GUID-HERE">
        <CreateFolder />
        <File Id="RunBat" Source="scripts\run.bat" KeyPath="yes" />
        <File Id="RunTestsBat" Source="scripts\run-tests.bat" />
        <File Id="BackupBat" Source="scripts\backup.bat" />
        <File Id="ConfigCrypto" Source="scripts\config_crypto.py" />
      </Component>

      <!-- Documentation -->
      <Component Id="Documentation" Guid="PUT-GUID-HERE">
        <File Id="ReadmeMd" Source="README.md" KeyPath="yes" />
        <File Id="InstallMd" Source="INSTALL.md" />
        <File Id="ChangelogMd" Source="CHANGELOG.md" />
      </Component>

      <!-- Environment template -->
      <Component Id="EnvExample" Guid="PUT-GUID-HERE">
        <File Id="EnvExample" Source=".env.example" KeyPath="yes" />
      </Component>

      <!-- Requirements -->
      <Component Id="Requirements" Guid="PUT-GUID-HERE">
        <File Id="RequirementsTxt" Source="requirements.txt" KeyPath="yes" />
      </Component>

      <!-- Tools -->
      <Component Id="NSSM" Guid="PUT-GUID-HERE">
        <CreateFolder Directory="ToolsFolder" />
        <File Id="NssmExe" Source="tools\nssm.exe" KeyPath="yes" />
      </Component>

    </ComponentGroup>

    <!-- Python application files -->
    <ComponentGroup Id="PythonFiles" Directory="INSTALLFOLDER">
      <Component Id="AppInit" Guid="PUT-GUID-HERE">
        <CreateFolder Directory="AppFolder" />
        <File Id="AppInit" Source="app\__init__.py" KeyPath="yes" />
        <File Id="AppMain" Source="app\main.py" />
        <File Id="AppConfig" Source="app\config.py" />
        <File Id="AppDatabase" Source="app\database.py" />
      </Component>

      <!-- Models -->
      <Component Id="AppModels" Guid="PUT-GUID-HERE">
        <File Id="ModelsInit" Source="app\models.py" KeyPath="yes" />
      </Component>

      <!-- Routes -->
      <Component Id="AppRoutes" Guid="PUT-GUID-HERE">
        <CreateFolder Directory="RoutesFolder" />
        <File Id="RoutesInit" Source="app\routes\__init__.py" KeyPath="yes" />
        <File Id="RoutesAuth" Source="app\routes\auth.py" />
        <File Id="RoutesIndex" Source="app\routes\index.py" />
      </Component>

      <!-- Templates -->
      <Component Id="AppTemplates" Guid="PUT-GUID-HERE">
        <CreateFolder Directory="TemplatesFolder" />
        <File Id="TemplateBase" Source="app\templates\base.html" KeyPath="yes" />
        <File Id="TemplateIndex" Source="app\templates\index.html" />
      </Component>

      <!-- Static files -->
      <Component Id="AppStatic" Guid="PUT-GUID-HERE">
        <CreateFolder Directory="StaticFolder" />
        <File Id="StaticCss" Source="app\static\style.css" KeyPath="yes" />
      </Component>
    </ComponentGroup>

    <!-- Shortcuts -->
    <DirectoryRef Id="ApplicationProgramsFolder">
      <Component Id="ApplicationShortcut" Guid="PUT-GUID-HERE">
        <Shortcut Id="ApplicationStartMenuShortcut"
                  Name="Property Management System"
                  Description="Launch Property Management System"
                  Target="[INSTALLFOLDER]scripts\run.bat"
                  WorkingDirectory="INSTALLFOLDER" />

        <Shortcut Id="UninstallShortcut"
                  Name="Uninstall Property Management System"
                  Description="Uninstalls Property Management System"
                  Target="[SystemFolder]msiexec.exe"
                  Arguments="/x [ProductCode]" />

        <RemoveFolder Id="ApplicationProgramsFolder" On="uninstall" />
        <RegistryValue Root="HKCU"
                       Key="Software\PropertyManagementSystem"
                       Name="installed"
                       Type="integer"
                       Value="1"
                       KeyPath="yes" />
      </Component>
    </DirectoryRef>

    <!-- Directory structure -->
    <DirectoryRef Id="INSTALLFOLDER">
      <Directory Id="ToolsFolder" Name="tools" />
      <Directory Id="AppFolder" Name="app">
        <Directory Id="RoutesFolder" Name="routes" />
        <Directory Id="TemplatesFolder" Name="templates" />
        <Directory Id="StaticFolder" Name="static" />
      </Directory>
    </DirectoryRef>

  </Fragment>
</Wix>
```

---

## Custom Actions (Actions.wxs)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Fragment>

    <!-- Custom action: Run post-install configuration -->
    <CustomAction Id="RunPostInstall"
                  FileKey="InstallAndRun"
                  ExeCommand=""
                  Execute="deferred"
                  Return="check"
                  Impersonate="no" />

    <!-- Custom action: Create virtual environment -->
    <CustomAction Id="CreateVirtualEnv"
                  Directory="INSTALLFOLDER"
                  ExeCommand='cmd.exe /c "python -m venv venv"'
                  Execute="deferred"
                  Return="check"
                  Impersonate="no" />

    <!-- Custom action: Install requirements -->
    <CustomAction Id="InstallRequirements"
                  Directory="INSTALLFOLDER"
                  ExeCommand='cmd.exe /c "venv\Scripts\pip.exe install -r requirements.txt"'
                  Execute="deferred"
                  Return="check"
                  Impersonate="no" />

    <!-- Custom action: Stop service before uninstall -->
    <CustomAction Id="StopService"
                  Directory="INSTALLFOLDER"
                  ExeCommand='cmd.exe /c "nssm.exe stop PropertyManagementSystem"'
                  Execute="deferred"
                  Return="ignore"
                  Impersonate="no" />

    <!-- Custom action: Remove service before uninstall -->
    <CustomAction Id="RemoveService"
                  Directory="INSTALLFOLDER"
                  ExeCommand='cmd.exe /c "nssm.exe remove PropertyManagementSystem confirm"'
                  Execute="deferred"
                  Return="ignore"
                  Impersonate="no" />

    <!-- Execution sequence -->
    <InstallExecuteSequence>
      <!-- Post-install actions (after files copied) -->
      <Custom Action="CreateVirtualEnv" After="InstallFiles">NOT Installed</Custom>
      <Custom Action="InstallRequirements" After="CreateVirtualEnv">NOT Installed</Custom>

      <!-- Pre-uninstall actions (before files removed) -->
      <Custom Action="StopService" Before="RemoveFiles">Installed AND REMOVE="ALL"</Custom>
      <Custom Action="RemoveService" After="StopService">Installed AND REMOVE="ALL"</Custom>
    </InstallExecuteSequence>

  </Fragment>
</Wix>
```

---

## Build Script (build.bat)

```batch
@echo off
setlocal EnableDelayedExpansion
title MSI Build Script
cd /d "%~dp0"

:: Set variables
set "VERSION=1.0.0"
set "OUTPUT_DIR=output"
set "WXS_FILES=Product.wxs Files.wxs Actions.wxs"
set "MSI_NAME=PropertyManagementSystem-%VERSION%.msi"

echo ========================================
echo Building MSI Installer
echo ========================================
echo Version: %VERSION%
echo Output: %OUTPUT_DIR%\%MSI_NAME%
echo ========================================
echo.

:: Create output directory
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

:: Compile WiX source files
echo [1/3] Compiling WiX source files...
for %%f in (%WXS_FILES%) do (
    echo   - Compiling %%f
    candle.exe -nologo "%%f" -out "%OUTPUT_DIR%\%%~nf.wixobj"
    if !errorlevel! neq 0 (
        echo ERROR: Failed to compile %%f
        pause
        exit /b 1
    )
)

:: Link WiX object files
echo [2/3] Linking WiX object files...
set "WIXOBJ_FILES="
for %%f in (%WXS_FILES%) do (
    set "WIXOBJ_FILES=!WIXOBJ_FILES! %OUTPUT_DIR%\%%~nf.wixobj"
)

light.exe -nologo -ext WixUIExtension -cultures:en-us !WIXOBJ_FILES! -out "%OUTPUT_DIR%\%MSI_NAME%"
if !errorlevel! neq 0 (
    echo ERROR: Failed to link
    pause
    exit /b 1
)

:: Verify output
echo [3/3] Verifying output...
if exist "%OUTPUT_DIR%\%MSI_NAME%" (
    echo.
    echo ========================================
    echo Build successful!
    echo ========================================
    echo MSI: %OUTPUT_DIR%\%MSI_NAME%
    echo Size:
    dir "%OUTPUT_DIR%\%MSI_NAME%" | findstr "%MSI_NAME%"
    echo ========================================
) else (
    echo ERROR: MSI file not created
    pause
    exit /b 1
)

pause
```

---

## Advanced Patterns

### Pattern 1: Property Prompts

```xml
<!-- Ask user for custom properties during installation -->
<Property Id="SERVER_PORT" Value="8008" />
<Property Id="BASE_URL" Value="http://localhost:8008" />

<!-- Custom dialog for properties -->
<UI>
  <Dialog Id="ConfigDialog" Width="370" Height="270" Title="Configuration">
    <Control Id="ServerPortLabel" Type="Text" X="20" Y="60" Width="100" Height="17" Text="Server Port:" />
    <Control Id="ServerPortEdit" Type="Edit" X="120" Y="60" Width="150" Height="17" Property="SERVER_PORT" />

    <Control Id="BaseUrlLabel" Type="Text" X="20" Y="90" Width="100" Height="17" Text="Base URL:" />
    <Control Id="BaseUrlEdit" Type="Edit" X="120" Y="90" Width="150" Height="17" Property="BASE_URL" />

    <Control Id="Next" Type="PushButton" X="236" Y="243" Width="56" Height="17" Default="yes" Text="Next">
      <Publish Event="NewDialog" Value="VerifyReadyDlg">1</Publish>
    </Control>
  </Dialog>
</UI>

<!-- Insert dialog into sequence -->
<InstallUISequence>
  <Show Dialog="ConfigDialog" After="LicenseAgreementDlg" />
</InstallUISequence>

<!-- Use properties to create .env file -->
<CustomAction Id="CreateEnvFile"
              Directory="INSTALLFOLDER"
              ExeCommand='cmd.exe /c "echo SERVER_PORT=[SERVER_PORT]>.env &amp; echo BASE_URL=[BASE_URL]>>.env"'
              Execute="deferred"
              Return="check" />
```

### Pattern 2: Conditional Installation

```xml
<!-- Check if Python is installed -->
<Property Id="PYTHONINSTALLED">
  <DirectorySearch Id="SearchForPython" Path="[ProgramFilesFolder]">
    <DirectorySearch Id="SearchPython3" Path="Python*">
      <FileSearch Id="FindPython" Name="python.exe" />
    </DirectorySearch>
  </DirectorySearch>
</Property>

<!-- Show error if Python not found -->
<Condition Message="Python 3.8+ must be installed first. Download from https://www.python.org/">
  <![CDATA[Installed OR PYTHONINSTALLED]]>
</Condition>
```

### Pattern 3: Upgrade Logic

```xml
<!-- Minor upgrade (files replaced, settings preserved) -->
<Upgrade Id="PUT-UPGRADE-CODE-GUID-HERE">
  <UpgradeVersion Minimum="1.0.0"
                  Maximum="1.1.0"
                  Property="PREVIOUSVERSIONSINSTALLED"
                  IncludeMinimum="yes"
                  IncludeMaximum="no" />
</Upgrade>

<!-- Major upgrade (complete reinstall) -->
<MajorUpgrade DowngradeErrorMessage="A newer version of [ProductName] is already installed."
              Schedule="afterInstallExecute" />

<!-- Preserve user data during upgrade -->
<Component Id="UserData" Guid="PUT-GUID-HERE" Permanent="yes">
  <CreateFolder Directory="InstanceFolder" />
  <!-- Files marked permanent are not removed on upgrade -->
</Component>
```

---

## Testing MSI

### Manual Testing Checklist

- [ ] **Install:** Fresh install completes without errors
- [ ] **Shortcuts:** Start menu shortcuts created and work
- [ ] **Files:** All files copied to install directory
- [ ] **Custom Actions:** Post-install scripts executed
- [ ] **Upgrade:** Minor upgrade preserves settings
- [ ] **Major Upgrade:** Uninstalls old version first
- [ ] **Uninstall:** Complete removal, no orphaned files
- [ ] **Rollback:** Failed install rolls back cleanly

### Automated Testing

```batch
:: Install silently
msiexec /i PropertyManagementSystem.msi /qn /l*v install.log

:: Verify installation
if exist "C:\Program Files\PropertyManagementSystem\app\main.py" (
    echo Install successful
) else (
    echo Install failed
    exit /b 1
)

:: Uninstall silently
msiexec /x PropertyManagementSystem.msi /qn /l*v uninstall.log

:: Verify removal
if not exist "C:\Program Files\PropertyManagementSystem\" (
    echo Uninstall successful
) else (
    echo Uninstall failed
    exit /b 1
)
```

---

## MSI Properties Reference

### Standard Properties

| Property | Description | Example |
|----------|-------------|---------|
| ProductName | Application name | "Property Management System" |
| ProductVersion | Version number | "1.0.0" |
| Manufacturer | Company name | "Your Company" |
| UpgradeCode | GUID for upgrades | "{12345678-1234-...}" |
| INSTALLFOLDER | Installation directory | "[ProgramFilesFolder]AppName" |
| ARPPRODUCTICON | Add/Remove Programs icon | "app.ico" |

### Custom Properties

| Property | Description | Default |
|----------|-------------|---------|
| SERVER_PORT | Application port | "8008" |
| BASE_URL | Application URL | "http://localhost:8008" |
| ADMIN_EMAIL | Admin email | "admin@example.com" |

---

*End of MSI Patterns Reference*
