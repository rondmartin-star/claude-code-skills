#!/bin/bash
# Seed Pattern Library from Existing Skills
# Extracts antipatterns from ERROR-AND-FIXES-LOG.md files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Seeding pattern library from existing skills..."
echo "Skills root: $SKILLS_ROOT"
echo

# Find all ERROR-AND-FIXES-LOG.md files
ERROR_LOGS=$(find "$SKILLS_ROOT" -name "ERROR-AND-FIXES-LOG.md" -type f)

if [ -z "$ERROR_LOGS" ]; then
    echo "No ERROR-AND-FIXES-LOG.md files found - will create example patterns"
    echo
fi

echo "Found ERROR-AND-FIXES-LOG.md files:"
echo "$ERROR_LOGS" | while read -r file; do
    skill_name=$(basename "$(dirname "$file")")
    echo "  - $skill_name"
done
echo

# Create seed data file
SEED_FILE="$SCRIPT_DIR/antipatterns/general/seeded-from-existing-skills.json"

cat > "$SEED_FILE" <<'EOF'
{
  "category": "general",
  "subcategory": "seeded",
  "description": "Antipatterns extracted from existing ERROR-AND-FIXES-LOG.md files",
  "antipatterns": [
EOF

# Counter for antipatterns
count=0

# Process each ERROR-AND-FIXES-LOG.md file
echo "$ERROR_LOGS" | while read -r log_file; do
    if [ ! -f "$log_file" ]; then
        continue
    fi

    skill_name=$(basename "$(dirname "$log_file")")
    echo "Processing: $skill_name"

    # Extract error patterns (simplified - would need more sophisticated parsing)
    # For now, just note that the files exist for manual review
    echo "  Found log file (manual review needed)"
done

# Close the JSON file
cat >> "$SEED_FILE" <<'EOF'
    {
      "id": "manual-review-required",
      "name": "Manual Review Required",
      "problem": "ERROR-AND-FIXES-LOG.md files exist but require manual review to extract patterns",
      "prevention": "Review existing ERROR-AND-FIXES-LOG.md files and extract antipatterns manually",
      "occurrences": 0,
      "tags": ["meta", "manual-review"],
      "sources": []
    }
  ]
}
EOF

echo
echo "✓ Created seed file: $SEED_FILE"
echo

# Create example patterns for demonstration
echo "Creating example patterns..."

cat > "$SCRIPT_DIR/patterns/audit-operations/eslint-auto-fix.json" <<'EOF'
{
  "id": "eslint-auto-fix",
  "name": "ESLint Auto-Fix Pattern",
  "category": "audit-operations",
  "subcategory": "code-quality",
  "description": "Automatically fix ESLint issues using eslint --fix",
  "solution": "Run 'eslint --fix' on target files, verify tests still pass",
  "applicability": "When ESLint issues are auto-fixable",
  "metrics": {
    "applications": 0,
    "successes": 0,
    "failures": 0,
    "successRate": 0.0
  },
  "tags": ["eslint", "auto-fix", "code-quality"],
  "relatedAntipatterns": ["manual-fix-auto-fixable"]
}
EOF

cat > "$SCRIPT_DIR/antipatterns/audit-operations/fix-symptom-not-cause.json" <<'EOF'
{
  "id": "fix-symptom-not-cause",
  "name": "Fix Symptom Not Root Cause",
  "category": "audit-operations",
  "problem": "Fixing surface-level symptoms instead of root causes leads to issues reappearing",
  "examples": [
    "Suppressing warning instead of fixing underlying issue",
    "Adding eslint-disable comments instead of fixing code",
    "Clearing cache instead of fixing caching logic"
  ],
  "prevention": "Always identify root cause with 5 Whys before implementing fix",
  "occurrences": 0,
  "tags": ["convergence", "root-cause", "anti-pattern"],
  "severity": "high"
}
EOF

cat > "$SCRIPT_DIR/patterns/corpus-operations/backup-before-conversion.json" <<'EOF'
{
  "id": "backup-before-conversion",
  "name": "Backup Before Conversion",
  "category": "corpus-operations",
  "subcategory": "conversion",
  "description": "Always create backup before converting existing project to corpus",
  "solution": "Create timestamped backup in .corpus/backups/ before any conversion",
  "applicability": "All corpus-convert operations",
  "metrics": {
    "applications": 0,
    "successes": 0,
    "failures": 0,
    "successRate": 1.0
  },
  "tags": ["safety", "backup", "conversion"],
  "relatedAntipatterns": ["no-backup-before-migration"]
}
EOF

cat > "$SCRIPT_DIR/antipatterns/corpus-operations/wrong-directory-init.json" <<'EOF'
{
  "id": "wrong-directory-init",
  "name": "Initialize in Wrong Directory",
  "category": "corpus-operations",
  "problem": "Initializing corpus in wrong directory leads to confusion and wasted setup",
  "examples": [
    "Running corpus-init in parent directory instead of project root",
    "Initializing in temporary directory",
    "Not verifying pwd before initialization"
  ],
  "prevention": "Always show full path and require user confirmation before initialization",
  "occurrences": 0,
  "tags": ["initialization", "user-error"],
  "severity": "medium"
}
EOF

echo "✓ Created example patterns and antipatterns"
echo

echo "==================================================="
echo "Pattern library seeding complete!"
echo "==================================================="
echo
echo "Seeded patterns:"
echo "  - audit-operations/eslint-auto-fix"
echo "  - corpus-operations/backup-before-conversion"
echo
echo "Seeded antipatterns:"
echo "  - audit-operations/fix-symptom-not-cause"
echo "  - corpus-operations/wrong-directory-init"
echo
echo "These patterns will be used during battle-plan execution."
echo "Metrics will accumulate as patterns are applied."
echo
