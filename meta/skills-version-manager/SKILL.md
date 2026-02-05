---
name: skills-version-manager
description: >
  Check skills ecosystem version, pull latest updates from GitHub, and show
  what's new. Runs at session initialization or on demand. Use when: session
  starts, "update skills", "check skills version", "pull latest skills".
---

# Skills Version Manager

**Purpose:** Keep skills ecosystem up-to-date with latest versions from GitHub
**Size:** ~8 KB
**Auto-Run:** Can run at session initialization (configurable)

---

## LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Update skills" / "Pull latest skills"
- "Check skills version" / "What's my skills version"
- "Sync skills from GitHub"
- "Show what's new in skills"
- At session initialization (if configured)

**Context Indicators:**
- User wants to know current version
- User wants to see release notes
- User wants latest features
- Session just started and auto-update enabled

---

## Core Features

### 1. Version Detection

```javascript
async function getCurrentVersion() {
  const readmePath = path.join(SKILLS_DIR, 'README.md');
  const content = await fs.readFile(readmePath, 'utf8');

  // Extract version from README
  const match = content.match(/\*\*Version:\*\* ([\d.]+)/);
  return match ? match[1] : 'unknown';
}

async function getRemoteVersion() {
  // Fetch remote README to check version
  const url = 'https://raw.githubusercontent.com/rondmartin-star/claude-code-skills/main/README.md';
  const response = await fetch(url);
  const content = await response.text();

  const match = content.match(/\*\*Version:\*\* ([\d.]+)/);
  return match ? match[1] : 'unknown';
}

async function checkVersion() {
  const current = await getCurrentVersion();
  const remote = await getRemoteVersion();

  return {
    current,
    remote,
    updateAvailable: compareVersions(remote, current) > 0,
    upToDate: current === remote
  };
}
```

### 2. Update Detection

```javascript
function compareVersions(v1, v2) {
  // Compare semantic versions (e.g., "3.0" vs "2.0")
  const parts1 = v1.split('.').map(Number);
  const parts2 = v2.split('.').map(Number);

  for (let i = 0; i < Math.max(parts1.length, parts2.length); i++) {
    const a = parts1[i] || 0;
    const b = parts2[i] || 0;
    if (a > b) return 1;
    if (a < b) return -1;
  }
  return 0;
}

async function checkForUpdates() {
  console.log("Checking for skills updates...");

  const version = await checkVersion();

  if (version.upToDate) {
    console.log(`✓ Skills up-to-date (v${version.current})`);
    return { needsUpdate: false, version };
  }

  if (version.updateAvailable) {
    console.log(`📦 Update available: v${version.current} → v${version.remote}`);
    return { needsUpdate: true, version };
  }

  return { needsUpdate: false, version };
}
```

### 3. Git Pull Updates

```javascript
async function pullLatestSkills() {
  const SKILLS_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.claude', 'skills');

  console.log("Pulling latest skills from GitHub...");
  console.log(`Repository: rondmartin-star/claude-code-skills`);

  // Check if directory exists
  if (!fs.existsSync(SKILLS_DIR)) {
    throw new Error('Skills directory not found. Run initial setup first.');
  }

  // Check if it's a git repo
  if (!fs.existsSync(path.join(SKILLS_DIR, '.git'))) {
    throw new Error('Skills directory is not a git repository.');
  }

  // Change to skills directory
  process.chdir(SKILLS_DIR);

  // Check current branch
  const branch = await execCommand('git branch --show-current');
  console.log(`Current branch: ${branch}`);

  // Stash local changes if any
  const hasChanges = await hasUncommittedChanges();
  if (hasChanges) {
    console.log("Stashing local changes...");
    await execCommand('git stash');
  }

  // Pull from main
  console.log("Pulling from origin/main...");
  const pullResult = await execCommand('git pull origin main');

  if (pullResult.includes('Already up to date')) {
    console.log("✓ Already up-to-date");
    return { updated: false, message: 'Already up-to-date' };
  }

  console.log("✓ Skills updated successfully!");
  return { updated: true, message: 'Updated to latest version' };
}

async function hasUncommittedChanges() {
  const result = await execCommand('git diff-index --quiet HEAD');
  return result.exitCode !== 0;
}

async function execCommand(cmd) {
  return new Promise((resolve, reject) => {
    exec(cmd, (error, stdout, stderr) => {
      if (error && error.code !== 1) {
        reject(error);
      } else {
        resolve(stdout.trim());
      }
    });
  });
}
```

### 4. Show What's New

```javascript
async function showReleaseNotes(version) {
  const releaseNotesPath = path.join(SKILLS_DIR, `RELEASE-NOTES-v${version}.md`);

  if (fs.existsSync(releaseNotesPath)) {
    const notes = await fs.readFile(releaseNotesPath, 'utf8');
    console.log("\n" + "=".repeat(60));
    console.log(`  Release Notes - v${version}`);
    console.log("=".repeat(60) + "\n");

    // Extract key sections
    const sections = extractKeySections(notes);

    console.log("✨ What's New:");
    sections.whatsNew.forEach(item => console.log(`  - ${item}`));

    console.log("\n🎯 Key Features:");
    sections.keyFeatures.forEach(item => console.log(`  - ${item}`));

    console.log("\n📦 Files Changed:");
    console.log(`  ${sections.filesChanged}`);

    console.log("\n📖 Full release notes:");
    console.log(`  ${releaseNotesPath}`);
    console.log("\n" + "=".repeat(60) + "\n");
  } else {
    console.log(`\nRelease notes for v${version} not available.`);
  }
}

function extractKeySections(content) {
  // Parse markdown to extract key information
  const whatsNew = [];
  const keyFeatures = [];
  let filesChanged = 'Unknown';

  const lines = content.split('\n');
  let inWhatsNew = false;
  let inKeyFeatures = false;

  for (const line of lines) {
    if (line.includes('## ✨ What\'s New') || line.includes('## What\'s New')) {
      inWhatsNew = true;
      inKeyFeatures = false;
    } else if (line.includes('## 🎯 Key Features')) {
      inWhatsNew = false;
      inKeyFeatures = true;
    } else if (line.startsWith('## ')) {
      inWhatsNew = false;
      inKeyFeatures = false;
    }

    if (inWhatsNew && line.trim().startsWith('-')) {
      whatsNew.push(line.trim().substring(2));
    }
    if (inKeyFeatures && line.trim().startsWith('-')) {
      keyFeatures.push(line.trim().substring(2));
    }

    if (line.includes('files changed')) {
      filesChanged = line.trim();
    }
  }

  return { whatsNew, keyFeatures, filesChanged };
}
```

### 5. Session Initialization Hook

```javascript
async function onSessionStart() {
  // This runs at session initialization if configured
  const config = await loadConfig();

  if (!config.autoCheckUpdates) {
    return; // Auto-check disabled
  }

  console.log("Checking skills version...");

  const update = await checkForUpdates();

  if (update.needsUpdate) {
    console.log(`\n📦 Skills update available: v${update.version.current} → v${update.version.remote}`);
    console.log(`Run "update skills" to install the latest version.`);
    console.log(`Or run "show what's new" to see release notes.\n`);

    if (config.autoUpdate) {
      console.log("Auto-updating skills...");
      const result = await pullLatestSkills();

      if (result.updated) {
        console.log("✓ Skills updated to latest version!");
        await showReleaseNotes(update.version.remote);
      }
    }
  } else {
    console.log(`✓ Skills up-to-date (v${update.version.current})`);
  }
}
```

---

## Configuration

### Config File Location

`~/.claude/skills-config.json`

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

### Configuration Options

**autoCheckUpdates** (boolean, default: true)
- Check for updates at session start
- Does not automatically install

**autoUpdate** (boolean, default: false)
- Automatically pull updates if available
- Requires autoCheckUpdates: true
- Use with caution (may override local changes)

**checkIntervalHours** (number, default: 24)
- Minimum hours between update checks
- Prevents excessive GitHub API calls

**repository** (string)
- GitHub repository to pull from
- Format: "owner/repo"

**branch** (string, default: "main")
- Git branch to pull from
- Usually "main" or "master"

---

## Usage Examples

### Manual Update Check

```
User: "Check skills version"
Claude: "Checking skills version..."
✓ Skills up-to-date (v3.0)
```

### Pull Latest Updates

```
User: "Update skills"

Claude: "Pulling latest skills from GitHub..."
Repository: rondmartin-star/claude-code-skills
Current branch: main
Pulling from origin/main...
✓ Skills updated successfully!

✨ What's New in v3.0:
  - 13 new learning skills
  - Battle-plan Phase 5.5
  - Windows-app 5 phase gates
  - MSI installer enhancements
```

### Show Release Notes

```
User: "Show what's new in skills"

Claude: [Displays release notes from RELEASE-NOTES-v3.0.md]
```

### Session Initialization (Auto-Check)

```
[Claude Code starts]

Checking skills version...
📦 Skills update available: v2.0 → v3.0
Run "update skills" to install the latest version.
Or run "show what's new" to see release notes.
```

---

## Implementation Notes

### Version Storage

Version is stored in `README.md`:
```markdown
**Version:** 3.0
```

This ensures version is always in sync with the ecosystem documentation.

### GitHub API Rate Limits

- Check interval prevents excessive API calls
- Uses raw.githubusercontent.com (no auth required)
- Falls back gracefully if API unavailable

### Local Changes Handling

- Stashes local changes before pulling
- User can retrieve stash later with `git stash pop`
- Prevents conflicts during update

### Error Handling

```javascript
try {
  const result = await pullLatestSkills();
} catch (error) {
  if (error.message.includes('not a git repository')) {
    console.error("Skills directory is not a git repo.");
    console.error("Please clone from: https://github.com/rondmartin-star/claude-code-skills");
  } else {
    console.error(`Update failed: ${error.message}`);
  }
}
```

---

## Integration with Other Skills

### skill-ecosystem-manager

When creating new skills, suggest version bump:
```
"New skill created. Consider bumping version in README.md"
```

### conversation-snapshot

Include skills version in snapshot metadata:
```json
{
  "snapshot_version": "1.0",
  "skills_version": "3.0",
  "timestamp": "2026-02-05T10:30:00Z"
}
```

---

## Windows Batch Script

For users who prefer batch script over skill:

`sync-skills.bat` (already exists in repository)

```batch
@echo off
cd %USERPROFILE%\.claude\skills
git pull origin main
echo Skills updated!
pause
```

---

## Quick Reference

**Check version:**
```
"check skills version" or "what's my skills version"
```

**Update:**
```
"update skills" or "pull latest skills"
```

**See what's new:**
```
"show what's new in skills" or "skills release notes"
```

**Configure auto-update:**
Edit `~/.claude/skills-config.json` and set `autoCheckUpdates: true`

---

*End of Skills Version Manager Skill*
