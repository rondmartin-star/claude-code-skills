# Installer Patterns Reference

Load this file when creating batch scripts, building installers, or configuring installation workflows.

---

## Batch Script Patterns

### Batch Script Boilerplate

Every .bat file MUST start with:

```batch
@echo off
setlocal EnableDelayedExpansion
title [AppName] v[X.Y.Z] Build [YYDDD-HHMM]
cd /d "%~dp0"
```

**Why:** Without `cd /d "%~dp0"`, scripts fail when run from different directories.

**Explanation of each line:**
- `@echo off` - Suppresses command echo (cleaner output)
- `setlocal EnableDelayedExpansion` - Allows !VAR! expansion in loops
- `title` - Sets window title (helps users identify the script)
- `cd /d "%~dp0"` - Changes to script directory (critical for relative paths)

### Auto-Elevation for Admin Scripts

Scripts requiring Administrator (hosts file, Caddy, ports 80/443) MUST auto-elevate:

```batch
@echo off
setlocal EnableDelayedExpansion
title [AppName] Setup (Administrator Required)
cd /d "%~dp0"

:: Check for Administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process -Verb RunAs -FilePath '%~f0' -ArgumentList '%*'"
    exit /b
)

:: Rest of script runs as Administrator
echo Running with Administrator privileges...
```

**When to use auto-elevation:**

| Task | Requires Admin |
|------|----------------|
| Modify hosts file | Yes |
| Install Caddy as service | Yes |
| Bind to ports 80/443 | Yes |
| Create Windows service | Yes |
| Modify Program Files | Yes |
| Install to user directory | No |
| Run Python/venv | No |
| Start app on port 8008+ | No |

**Testing auto-elevation:**
1. Run script as normal user
2. UAC prompt should appear
3. Script continues with admin rights
4. If no UAC, script already had admin rights

### Hosts File Modification Pattern

```batch
:: Auto-elevate first, then:
set "HOSTS_FILE=%SystemRoot%\System32\drivers\etc\hosts"
set "DOMAIN=pms.ucc-austin.org"
set "IP=192.168.0.132"

:: Check if entry already exists
findstr /C:"%DOMAIN%" "%HOSTS_FILE%" >nul 2>&1
if %errorlevel% equ 0 (
    echo Hosts entry already exists for %DOMAIN%
) else (
    echo Adding hosts entry: %IP% %DOMAIN%
    echo %IP%    %DOMAIN% >> "%HOSTS_FILE%"
    if %errorlevel% equ 0 (
        echo Successfully added hosts entry
    ) else (
        echo ERROR: Failed to modify hosts file
    )
)
```

**Important notes:**
- Always check for existing entry before adding
- Use `/C:"exact string"` for findstr (not `/C:"partial"`)
- Append with `>>` not `>`  (preserve existing entries)
- Verify with `type "%HOSTS_FILE%"` after modification

### Variable Prompts with Defaults

```batch
REM Pattern for user input with smart defaults
set "DEFAULT_PORT=8008"
set /p PORT="Server port [%DEFAULT_PORT%]: "
if "!PORT!"=="" set "PORT=%DEFAULT_PORT%"

REM Validate numeric input
echo !PORT! | findstr "^[0-9][0-9]*$" >nul
if !errorlevel! neq 0 (
    echo ERROR: Port must be numeric
    pause
    exit /b 1
)

REM Check port range
if !PORT! lss 1024 (
    echo WARNING: Ports below 1024 require Administrator privileges
)
if !PORT! gtr 65535 (
    echo ERROR: Port must be between 1 and 65535
    pause
    exit /b 1
)
```

### Path Input with Auto-Creation

```batch
REM Accept file path and create parent directory
set "DEFAULT_PATH=%USERPROFILE%\Documents\AppData\config.txt"
set /p USER_PATH="Config file path [%DEFAULT_PATH%]: "
if "!USER_PATH!"=="" set "USER_PATH=%DEFAULT_PATH%"

REM Extract directory from path
for %%F in ("!USER_PATH!") do set "DIR_PATH=%%~dpF"

REM Create directory if it doesn't exist
if not "!DIR_PATH!"=="" (
    if not exist "!DIR_PATH!" (
        echo Creating directory: !DIR_PATH!
        mkdir "!DIR_PATH!" 2>nul
        if !errorlevel! neq 0 (
            echo ERROR: Failed to create directory
            pause
            exit /b 1
        )
    )
)
```

### Python Environment Setup

```batch
REM Check if Python is installed
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo Creating Python virtual environment...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if !errorlevel! neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install requirements
if exist "requirements.txt" (
    echo Installing Python dependencies...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)
```

---

## Interactive Installer Design

### Smart Defaults Implementation

Provide sensible defaults that work out-of-the-box:

| Setting | Default | Why |
|---------|---------|-----|
| Port | 8008 | Unlikely to conflict, doesn't need admin |
| Base URL | http://localhost:8008 | Works immediately for testing |
| Database | {AppName}.db in script directory | Simple, portable |
| Response file | %USERPROFILE%\Documents\{AppName}_response.enc | User-accessible, backed up |
| OAuth domain | Empty | Force user to configure (security) |

### User Input Validation

Validate all user input before proceeding:

```batch
REM Example: Validate email format
echo !EMAIL! | findstr /R "^[a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]*\.[a-zA-Z][a-zA-Z]*$" >nul
if !errorlevel! neq 0 (
    echo ERROR: Invalid email format
    goto :prompt_email
)

REM Example: Validate URL format
echo !BASE_URL! | findstr "^http" >nul
if !errorlevel! neq 0 (
    echo ERROR: URL must start with http:// or https://
    goto :prompt_base_url
)

REM Example: Validate directory exists
if not exist "!INSTALL_DIR!\" (
    echo ERROR: Directory does not exist: !INSTALL_DIR!
    goto :prompt_install_dir
)
```

### Progress Indicators

Keep users informed during long operations:

```batch
echo.
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if !errorlevel! neq 0 goto :error_python

echo [2/5] Creating virtual environment...
python -m venv venv
if !errorlevel! neq 0 goto :error_venv

echo [3/5] Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install -r requirements.txt >nul
if !errorlevel! neq 0 goto :error_pip

echo [4/5] Generating encryption key...
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" > .encryption_key
if !errorlevel! neq 0 goto :error_key

echo [5/5] Saving configuration...
call :save_response_file
if !errorlevel! neq 0 goto :error_config

echo.
echo ========================================
echo Installation complete!
echo ========================================
```

---

## Silent Install Mode

### Response File Format

Create encrypted response file for non-interactive installs:

```batch
REM Generate response file during interactive install
(
    echo PORT=!PORT!
    echo BASE_URL=!BASE_URL!
    echo OAUTH_DOMAIN=!OAUTH_DOMAIN!
    echo OAUTH_CLIENT_ID=!OAUTH_CLIENT_ID!
    echo OAUTH_CLIENT_SECRET=!OAUTH_CLIENT_SECRET!
    echo SMTP_SERVER=!SMTP_SERVER!
    echo SMTP_PORT=!SMTP_PORT!
    echo SMTP_USERNAME=!SMTP_USERNAME!
    echo SMTP_PASSWORD=!SMTP_PASSWORD!
    echo DATABASE_PATH=!DATABASE_PATH!
) > temp_response.txt

REM Encrypt response file
python -c "from cryptography.fernet import Fernet; import sys; key=open('.encryption_key','rb').read(); f=Fernet(key); encrypted=f.encrypt(open('temp_response.txt','rb').read()); open('!RESPONSE_PATH!','wb').write(encrypted)"

REM Clean up temp file
del temp_response.txt
```

### Silent Install Usage

```batch
REM Check for response file argument
if "%~1" neq "" (
    if exist "%~1" (
        echo Loading configuration from: %~1
        call :load_response_file "%~1"
        set "SILENT_MODE=true"
    ) else (
        echo ERROR: Response file not found: %~1
        exit /b 1
    )
)

REM In silent mode, skip all prompts
if "!SILENT_MODE!"=="true" (
    echo Running in silent mode...
    goto :install
)

REM Interactive mode - prompt for all settings
call :prompt_all_settings
goto :install
```

### Non-Interactive Validation

Validate response file before proceeding:

```batch
:validate_response_file
if "!PORT!"=="" (
    echo ERROR: Response file missing PORT
    exit /b 1
)
if "!BASE_URL!"=="" (
    echo ERROR: Response file missing BASE_URL
    exit /b 1
)
REM ... validate all required fields
goto :eof
```

---

## MSI Installer Patterns

### WiX Toolset Template

Basic WiX (.wxs) file structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*"
           Name="$(var.ProductName)"
           Language="1033"
           Version="$(var.Version)"
           Manufacturer="$(var.Manufacturer)"
           UpgradeCode="PUT-GUID-HERE">

    <Package InstallerVersion="200" Compressed="yes" InstallScope="perMachine" />

    <MajorUpgrade DowngradeErrorMessage="A newer version is already installed." />

    <MediaTemplate EmbedCab="yes" />

    <Feature Id="ProductFeature" Title="$(var.ProductName)" Level="1">
      <ComponentGroupRef Id="ProductComponents" />
    </Feature>
  </Product>

  <Fragment>
    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="$(var.ProductName)" />
      </Directory>
    </Directory>
  </Fragment>

  <Fragment>
    <ComponentGroup Id="ProductComponents" Directory="INSTALLFOLDER">
      <!-- Add files here -->
      <Component Id="MainExecutable" Guid="PUT-GUID-HERE">
        <File Source="$(var.SourceDir)\app.exe" KeyPath="yes" />
      </Component>
    </ComponentGroup>
  </Fragment>
</Wix>
```

### Custom Actions

Execute scripts during installation:

```xml
<CustomAction Id="RunPostInstall"
              FileKey="PostInstallScript"
              ExeCommand="cmd.exe /c post-install.bat"
              Execute="deferred"
              Return="check"
              Impersonate="no" />

<InstallExecuteSequence>
  <Custom Action="RunPostInstall" After="InstallFiles">NOT Installed</Custom>
</InstallExecuteSequence>
```

### Upgrade Patterns

Handle version upgrades gracefully:

```xml
<!-- Major Upgrade: Uninstall old, install new -->
<MajorUpgrade DowngradeErrorMessage="A newer version is already installed."
              Schedule="afterInstallExecute" />

<!-- Minor Update: Replace changed files only -->
<Upgrade Id="PUT-UPGRADE-CODE-GUID-HERE">
  <UpgradeVersion Minimum="1.0.0"
                  Maximum="1.1.0"
                  Property="PREVIOUSVERSIONSINSTALLED"
                  IncludeMinimum="yes"
                  IncludeMaximum="no" />
</Upgrade>

<!-- Patch: Update specific files -->
<PatchCreation Id="MyPatch"
               DisplayName="Patch for AppName"
               Description="Fixes critical bug"
               Manufacturer="$(var.Manufacturer)" />
```

---

## Testing Installer Scripts

### Manual Testing Checklist

- [ ] Run as normal user (should work or request elevation)
- [ ] Run as Administrator (should skip elevation)
- [ ] Run from different directory (should still work due to `cd /d`)
- [ ] Run with spaces in path (should handle quoted paths)
- [ ] Kill mid-execution and restart (should handle incomplete state)
- [ ] Run silent install (should complete without prompts)
- [ ] Verify all files created in correct locations
- [ ] Check that services start automatically
- [ ] Uninstall and verify cleanup

### Automated Testing

```batch
REM Test script that runs installer and verifies results
@echo off
setlocal EnableDelayedExpansion

echo Testing installer...

REM Create temp response file for silent install
call create_test_response.bat

REM Run installer in silent mode
call INSTALL-AND-RUN.bat test_response.enc
if !errorlevel! neq 0 (
    echo FAILED: Installer returned error
    exit /b 1
)

REM Verify files exist
if not exist "%INSTALL_DIR%\app\main.py" (
    echo FAILED: Main application file not found
    exit /b 1
)

REM Verify service installed
sc query "AppName" >nul 2>&1
if !errorlevel! neq 0 (
    echo FAILED: Service not installed
    exit /b 1
)

echo PASSED: All tests successful
```

---

*End of Installer Patterns Reference*
