# How to Update to Skills v3.0

**Target Audience:** All users of the Claude Code Skills Ecosystem
**Current Version:** 3.0
**Previous Version:** 2.0
**Update Type:** Major release with 13 new learning skills

---

## ✅ For This Machine (Already Updated)

**Status:** ✅ You already have v3.0

Since you pushed the changes, your local machine is automatically on v3.0. No action needed.

---

## 🔄 For Other Machines/Sessions

### Option 1: Use Sync Script (Easiest)

**Windows:**
```batch
REM Double-click or run from command prompt
C:\Users\[YourName]\.claude\skills\sync-skills.bat
```

This will:
1. Pull latest changes from GitHub
2. Show what's new
3. Display skill count

**Linux/Mac:**
```bash
cd ~/.claude/skills
git pull origin main
```

### Option 2: Manual Git Pull

```bash
# Navigate to skills directory
cd ~/.claude/skills  # Linux/Mac
cd %USERPROFILE%\.claude\skills  # Windows

# Pull latest changes
git pull origin main

# Verify version
grep "Version:" README.md
# Should show: **Version:** 3.0
```

### Option 3: Fresh Clone (Clean Install)

If you encounter issues or want a fresh start:

```bash
# Backup existing skills (optional)
mv ~/.claude/skills ~/.claude/skills.backup

# Clone latest version
git clone https://github.com/rondmartin-star/claude-code-skills.git ~/.claude/skills

# Verify installation
cd ~/.claude/skills
ls core/learning/
# Should see learning skills directories
```

---

## 🔍 Verify Update

After pulling/cloning, verify v3.0 is installed:

### 1. Check Version

```bash
cd ~/.claude/skills
grep "Version:" README.md
```

**Expected output:**
```
**Version:** 3.0
```

### 2. Verify Learning Skills Exist

```bash
ls core/learning/
```

**Expected directories:**
```
convergence/
during-execution/
error-reflection/
orchestrators/
pattern-library/
phase-transition/
post-execution/
pre-execution/
pre-mortem/
```

### 3. Check Specific New Files

```bash
# Battle-plan Phase 5.5
grep "Phase 5.5" core/learning/orchestrators/battle-plan/SKILL.md

# Windows-app gates
grep "GATE 1" windows-app/windows-app-orchestrator/SKILL.md

# MSI signing
grep "Code Signing" windows-app/windows-app-supervision/SKILL.md
```

All should return matches if v3.0 is installed correctly.

---

## 🔄 Refresh Claude Code Sessions

### How Claude Code Detects Skills

**Automatic Detection:**
- Claude Code monitors `~/.claude/skills/` directory
- Skills are automatically discovered on load
- No manual registration needed
- No cache clearing required (usually)

### Refresh Methods

**Method 1: Restart Claude Code (Recommended)**

Simply close and reopen Claude Code CLI:
```bash
# Exit current session
exit

# Start new session
claude
```

New skills will be automatically detected.

**Method 2: Use skills-version-manager (NEW in v3.0)**

In your Claude Code session:
```
"update skills"
```

This new meta skill will:
1. Check your current version
2. Pull latest from GitHub
3. Show what's new
4. Notify you to restart (if needed)

**Method 3: No Action (Skills Load On Demand)**

Claude Code loads skills on demand when triggered. Simply start using new trigger phrases:

```
"Run battle-plan for: Add health check endpoint"
→ Will load new battle-plan with Phase 5.5

"Review requirements"
→ Will load windows-app gate reviewer
```

---

## 🎯 Test New Features

After updating, test the new v3.0 features:

### 1. Test Battle-Plan Phase 5.5

```
User: "Run battle-plan for: Add health check endpoint"
```

**Expected behavior:**
- Executes Phases 1-5 (normal)
- **NEW:** Executes Phase 5.5 (Iterative Phase Review)
- Reviews deliverables with multi-methodology convergence
- Proceeds to Phase 6 (Reflection)

### 2. Test Windows-App Phase Gates

```
User: "Complete requirements phase"
User: "Review requirements"
```

**Expected behavior:**
- GATE 1 prompt appears
- Options: run now, skip, or defer
- Multi-methodology review if chosen
- State tracking in APP-STATE.yaml

### 3. Test skills-version-manager

```
User: "Check skills version"
```

**Expected output:**
```
✓ Skills up-to-date (v3.0)
```

---

## 📝 Configure Auto-Update (Optional)

Create `~/.claude/skills-config.json`:

```json
{
  "skills": {
    "autoCheckUpdates": true,
    "autoUpdate": false,
    "checkIntervalHours": 24,
    "repository": "rondmartin-star/claude-code-skills",
    "branch": "main"
  }
}
```

**Configuration Options:**

**autoCheckUpdates: true**
- Check for updates at session start
- Shows notification if update available
- Does not auto-install

**autoUpdate: false** (recommended)
- Requires manual "update skills" command
- Prevents unexpected changes
- Safe for production use

**autoUpdate: true** (use with caution)
- Automatically pulls updates
- May override local changes
- Best for development/testing

---

## 🆕 What's New in v3.0

### Learning Skills (13 new skills)

**Core:**
- multi-methodology-convergence
- iterative-phase-review
- convergence-engine (forwarding)

**Pre-Execution:**
- clarify-requirements
- pre-mortem
- confirm-operation

**During-Execution:**
- verify-evidence
- detect-infinite-loop
- manage-context

**Post-Execution:**
- error-reflection
- declare-complete
- pattern-library

**Battle-Plan Orchestrators:**
- battle-plan (9 phases with Phase 5.5)
- audit-battle-plan
- content-battle-plan
- corpus-battle-plan

### Battle-Plan Phase 5.5

**New Phase:** Iterative Phase Review
- Runs after Phase 5 (Execution)
- Multi-methodology convergence on deliverables
- 8 orthogonal review approaches
- Random methodology selection
- 3 consecutive clean passes required

### Windows-App Phase Gates

**5 Quality Gates:**
- GATE 1: Requirements → System Design
- GATE 2: System Design → UI Design
- GATE 3: UI Design → Build
- GATE 4: Build → Supervision
- GATE 5: Supervision → Production

### MSI Installer Enhancements

**New Features:**
- Code signing guide (prevents Windows Defender warnings)
- Keep installer on top during execution
- Launch option (checked by default)

---

## 🔧 Troubleshooting

### "git pull" fails with merge conflicts

```bash
# Stash your local changes
git stash

# Pull updates
git pull origin main

# Restore your changes (optional)
git stash pop
```

### Skills not loading after update

**Solution 1: Restart Claude Code**
```bash
exit
claude
```

**Solution 2: Verify files exist**
```bash
ls ~/.claude/skills/core/learning/
# Should show learning skills directories
```

**Solution 3: Re-clone (fresh start)**
```bash
mv ~/.claude/skills ~/.claude/skills.backup
git clone https://github.com/rondmartin-star/claude-code-skills.git ~/.claude/skills
```

### "Not a git repository" error

Your skills directory is not tracking git. Fix:
```bash
cd ~/.claude/skills
git init
git remote add origin https://github.com/rondmartin-star/claude-code-skills.git
git fetch
git checkout main
```

### Version shows 2.0 after pulling

**Verify you pulled correctly:**
```bash
cd ~/.claude/skills
git log --oneline -1
```

Should show latest commit (5e428f0 or later).

If not:
```bash
git pull origin main --force
```

---

## 📞 Getting Help

### GitHub Repository

https://github.com/rondmartin-star/claude-code-skills

### Documentation

- **Release Notes:** RELEASE-NOTES-v3.0.md
- **Ecosystem Overview:** README.md
- **Development Guide:** CLAUDE.md
- **Individual Skills:** See SKILL.md files

### Common Questions

**Q: Will updating break my existing skills?**
A: No, v3.0 is fully backward compatible.

**Q: Do I need to reconfigure anything?**
A: No, all existing configurations work as before.

**Q: Can I roll back to v2.0?**
A: Yes, `git checkout <v2.0-commit>` or keep v2.0 backup.

**Q: Will this update other projects using skills?**
A: No, only updates the skills in `~/.claude/skills/`.

---

## ✅ Update Checklist

For users upgrading from v2.0 to v3.0:

- [ ] Pull latest changes (`git pull origin main`)
- [ ] Verify version shows 3.0 (`grep "Version:" README.md`)
- [ ] Verify learning skills exist (`ls core/learning/`)
- [ ] Restart Claude Code session
- [ ] Test battle-plan with Phase 5.5 ("run battle-plan")
- [ ] Test windows-app gates ("review requirements")
- [ ] Review RELEASE-NOTES-v3.0.md
- [ ] Configure auto-update (optional)
- [ ] Update any custom integrations (if applicable)

---

## 🎉 You're All Set!

After completing the update:

1. ✅ **Skills are v3.0**
2. ✅ **13 new learning skills available**
3. ✅ **Battle-plan has Phase 5.5**
4. ✅ **Windows-app has 5 quality gates**
5. ✅ **MSI installers enhanced**

Start using new features:
```
"Run battle-plan for: [task]"
"Review requirements"
"Update skills" (check for future updates)
```

---

## 📈 Version Comparison

| Feature | v2.0 | v3.0 |
|---------|------|------|
| Total Skills | 15 | 28 |
| Learning Integration | ❌ | ✅ |
| Battle-Plan Phases | 8 | 9 |
| Windows-App Gates | ❌ | ✅ |
| MSI Code Signing | ❌ | ✅ |
| Pattern Library | ❌ | ✅ |
| Auto-Update | ❌ | ✅ |

---

*Update Guide v1.0*
*Created: 2026-02-05*
*For Skills Ecosystem v3.0*
*GitHub: https://github.com/rondmartin-star/claude-code-skills*
