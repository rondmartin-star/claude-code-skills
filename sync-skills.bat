@echo off
setlocal EnableDelayedExpansion
title Claude Code Skills Sync - v4.0 Universal Ecosystem
color 0A

echo ============================================
echo   Claude Code Skills Sync - v4.0
echo ============================================
echo.

set "SKILLS_DIR=%USERPROFILE%\.claude\skills"

:: Check if skills directory exists
if not exist "%SKILLS_DIR%" (
    echo Skills directory not found. Cloning from GitHub...
    echo Repository: rondmartin-star/claude-code-skills
    echo.
    git clone https://github.com/rondmartin-star/claude-code-skills.git "%SKILLS_DIR%"
    if !errorlevel! neq 0 (
        echo ERROR: Failed to clone repository
        pause
        exit /b 1
    )
    echo.
    echo Skills repository cloned successfully!
    goto :ShowSkills
)

:: Check if it's a git repo
if not exist "%SKILLS_DIR%\.git" (
    echo ERROR: Skills directory exists but is not a git repository
    echo Please backup and remove %SKILLS_DIR% then run this script again
    pause
    exit /b 1
)

echo Syncing skills from GitHub...
echo Repository: rondmartin-star/claude-code-skills
echo.
cd /d "%SKILLS_DIR%"

:: Check current branch
for /f "tokens=*" %%B in ('git branch --show-current') do set CURRENT_BRANCH=%%B
echo Current branch: %CURRENT_BRANCH%

:: Stash any local changes
git diff-index --quiet HEAD
if !errorlevel! neq 0 (
    echo Stashing local changes...
    git stash
)

:: Pull updates from main
echo Pulling latest changes...
git pull origin main
if !errorlevel! neq 0 (
    echo ERROR: Failed to pull updates
    pause
    exit /b 1
)

echo.
echo Skills synced successfully to v4.0!

:ShowSkills
echo.
echo ============================================
echo   v4.0 Universal Skills Ecosystem
echo ============================================
echo.

:: Count skills
set /a TOTAL_SKILLS=0
set /a CORPUS_SKILLS=0
set /a AUDIT_SKILLS=0
set /a CONTENT_SKILLS=0
set /a UTILITY_SKILLS=0

:: Core Orchestrator
if exist "%SKILLS_DIR%\core\core-orchestrator\SKILL.md" (
    echo [ORCHESTRATOR]
    echo   - core-orchestrator ^(main navigation^)
    echo.
    set /a TOTAL_SKILLS+=1
)

:: Corpus Management
echo [CORPUS MANAGEMENT]
for /d %%D in ("%SKILLS_DIR%\core\corpus\*") do (
    if exist "%%D\SKILL.md" (
        echo   - %%~nxD
        set /a CORPUS_SKILLS+=1
        set /a TOTAL_SKILLS+=1
    )
)
echo.

:: Audit System
echo [AUDIT SYSTEM]
if exist "%SKILLS_DIR%\core\audit\audit-orchestrator\SKILL.md" (
    echo   - audit-orchestrator ^(routing^)
    set /a AUDIT_SKILLS+=1
    set /a TOTAL_SKILLS+=1
)
for /d %%D in ("%SKILLS_DIR%\core\audit\audits\*") do (
    if exist "%%D\SKILL.md" (
        echo   - %%~nxD
        set /a AUDIT_SKILLS+=1
        set /a TOTAL_SKILLS+=1
    )
)
if exist "%SKILLS_DIR%\core\audit\convergence-engine\SKILL.md" (
    echo   - convergence-engine
    set /a AUDIT_SKILLS+=1
    set /a TOTAL_SKILLS+=1
)
if exist "%SKILLS_DIR%\core\audit\fix-planner\SKILL.md" (
    echo   - fix-planner
    set /a AUDIT_SKILLS+=1
    set /a TOTAL_SKILLS+=1
)
echo.

:: Content Management
echo [CONTENT MANAGEMENT]
for /d %%D in ("%SKILLS_DIR%\core\content\*") do (
    if exist "%%D\SKILL.md" (
        echo   - %%~nxD
        set /a CONTENT_SKILLS+=1
        set /a TOTAL_SKILLS+=1
    )
)
echo.

:: Utilities
echo [UTILITIES]
for /d %%D in ("%SKILLS_DIR%\core\utilities\*") do (
    if exist "%%D\SKILL.md" (
        echo   - %%~nxD
        set /a UTILITY_SKILLS+=1
        set /a TOTAL_SKILLS+=1
    )
)
echo.

:: Summary
echo ============================================
echo   Summary
echo ============================================
echo   Total Skills: !TOTAL_SKILLS!
echo   - Corpus Management: !CORPUS_SKILLS!
echo   - Audit System: !AUDIT_SKILLS!
echo   - Content Management: !CONTENT_SKILLS!
echo   - Utilities: !UTILITY_SKILLS!
echo   - Orchestrator: 1
echo.

:: Configuration Templates
set /a TEMPLATE_COUNT=0
if exist "%SKILLS_DIR%\config\templates" (
    for %%F in ("%SKILLS_DIR%\config\templates\*.json") do (
        set /a TEMPLATE_COUNT+=1
    )
    echo   Configuration Templates: !TEMPLATE_COUNT!
)

:: Examples
set /a EXAMPLE_COUNT=0
if exist "%SKILLS_DIR%\config\examples" (
    for %%F in ("%SKILLS_DIR%\config\examples\*.json") do (
        set /a EXAMPLE_COUNT+=1
    )
    echo   Example Configs: !EXAMPLE_COUNT!
)

echo.
echo ============================================
echo   Quick Start
echo ============================================
echo   Initialize corpus: claude "Initialize this as a corpus"
echo   Run audit: claude "Audit code quality"
echo   Export: claude "Export to PDF"
echo   Backup: claude "Create backup"
echo.
echo   See ARCHITECTURE-v4.md for complete documentation
echo ============================================
echo.

pause
