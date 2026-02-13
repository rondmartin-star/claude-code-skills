# Quick Start: Create MSI in 5 Steps

## Step 1: Create WiX Source File

Use template from `wix-templates.md` → Minimal installer.

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

## Step 2: Create Exclusion Filter

Use template from `exclusion-filters.md`.

Critical exclusions:
- venv/, .git/, __pycache__/
- instance/, deployment-data/
- installer/ (to avoid circular reference)
- *.db, *.sqlite3, *.log
- Build artifacts

## Step 3: Create Build Script

Use template from `build-scripts.md` → rebuild-msi.bat.

Script does:
1. Clean build artifacts
2. Harvest files with heat.exe
3. Fix component references (Python script)
4. Compile with candle.exe
5. Link with light.exe
6. Verify size (should be < 5 MB for source-only)

## Step 4: Create Post-Install Wizard

Use template from `post-install-wizard.md`.

PowerShell wizard handles:
- Dependency checks
- Virtual environment setup
- Configuration prompts
- Database initialization
- Server startup

## Step 5: Build and Test

```batch
cd installer
.\rebuild-msi.bat
```

**Pre-Build Validation Checklist:**
- [ ] License.rtf exists in installer/ directory
- [ ] Version number updated in .wxs file
- [ ] ExcludeFilter.xslt excludes installer/ directory
- [ ] fix-wix-refs.py script exists
- [ ] requirements.txt versions verified in PyPI
- [ ] CONFIGURE.bat strips %~dp0 trailing backslash

**Build Verification Checklist:**
- [ ] MSI size < 5 MB (for source-only apps)
- [ ] No LGHT0094 errors (unresolved component references)
- [ ] No circular reference errors
- [ ] heat.exe completed without warnings
- [ ] candle.exe completed without errors
- [ ] light.exe completed without errors

**Installation Testing Checklist:**
- [ ] License agreement shows correctly
- [ ] Directory selection works
- [ ] Files install to correct location (C:\Program Files\App)
- [ ] Start Menu shortcuts created
- [ ] No venv/ or instance/ in installed files
- [ ] No .db or .sqlite3 files in installed files
- [ ] Uninstall works cleanly

**Exit Dialog & Launch Checklist:**
- [ ] Exit dialog appears after installation
- [ ] "Launch configuration wizard" checkbox shows
- [ ] Checkbox is checked by default
- [ ] CONFIGURE.bat launches when Finish clicked
- [ ] Auto-elevation UAC prompt appears
- [ ] Script runs as Administrator

**Wizard Validation Checklist (10 Patterns):**
- [ ] Python version check (3.11+ required)
- [ ] Write permission validation passes
- [ ] Virtual environment creates successfully
- [ ] pip upgrade uses `python -m pip` (not pip.exe)
- [ ] Dependencies install without errors
- [ ] .env file created from template
- [ ] Secret key generated with entropy validation
- [ ] Static files collect without errors
- [ ] Database migrations apply successfully
- [ ] Port 8000 availability checked

**Post-Configuration Testing:**
- [ ] Application starts without errors
- [ ] Can access http://localhost:8000
- [ ] No permission errors in logs
- [ ] Database initialized with tables
- [ ] Static files served correctly

**Deployment Issues Prevention (Issues 13-16):**
- [ ] Tested on 32-bit PowerShell environment
- [ ] Tested on 64-bit PowerShell environment
- [ ] %~dp0 trailing backslash stripped in CONFIGURE.bat
- [ ] All requirements.txt versions exist in PyPI
- [ ] Wizard uses `python -m pip` exclusively

**Clean Machine Test:**
- [ ] Test on Windows 10 (64-bit)
- [ ] Test on Windows 11 (64-bit)
- [ ] Test with fresh Python install
- [ ] Test with no previous application version
- [ ] Test uninstall leaves no orphaned files

**Estimated Time:**
- Build: 2-5 minutes
- Installation test: 3-5 minutes
- Configuration wizard: 2-3 minutes
- Full validation: 10-15 minutes

**With validation patterns:** Prevents 15+ hours of debugging per installer
