# Skills Version Manager

**Category:** Meta - Ecosystem Management
**Purpose:** Keep skills ecosystem up-to-date automatically
**Status:** Active (v1.0.0)

---

## Quick Reference

Check if your skills are up-to-date and pull latest updates from GitHub.

### Commands

```
"check skills version"     - Check current vs remote version
"update skills"            - Pull latest updates from GitHub
"show what's new"          - Display release notes
```

### Auto-Update Configuration

Create `~/.claude/skills-config.json`:

```json
{
  "skills": {
    "autoCheckUpdates": true,
    "autoUpdate": false
  }
}
```

**autoCheckUpdates: true** - Check at session start (notify only)
**autoUpdate: true** - Automatically pull updates (use with caution)

---

## How It Works

1. **Version Detection**
   - Reads version from local README.md
   - Fetches remote README.md from GitHub
   - Compares versions

2. **Update Notification**
   - At session start (if configured)
   - Shows "v2.0 → v3.0" notification
   - Suggests update command

3. **Git Pull**
   - Stashes local changes if any
   - Pulls from origin/main
   - Shows what's new

4. **Release Notes**
   - Displays key highlights
   - Links to full RELEASE-NOTES file

---

## Files

- `SKILL.md` - Full documentation with implementation code
- `README.md` - This file (quick reference)

---

*Part of v3.0 Universal Skills Ecosystem - Meta Skills*
