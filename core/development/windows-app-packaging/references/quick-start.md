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
