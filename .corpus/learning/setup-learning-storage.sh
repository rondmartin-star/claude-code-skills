#!/bin/bash
# Setup Learning Storage Infrastructure
# Creates directory structure and seeds pattern library from existing skills

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Setting up learning storage infrastructure..."
echo "Skills root: $SKILLS_ROOT"
echo "Storage location: $SCRIPT_DIR"
echo

# Create directory structure
echo "Creating directory structure..."

# Root directories
mkdir -p "$SCRIPT_DIR/patterns"
mkdir -p "$SCRIPT_DIR/antipatterns"
mkdir -p "$SCRIPT_DIR/risks"
mkdir -p "$SCRIPT_DIR/pre-mortems/recent"
mkdir -p "$SCRIPT_DIR/checkpoints"
mkdir -p "$SCRIPT_DIR/metrics"

# Category-specific pattern directories
categories=("corpus-operations" "audit-operations" "content-operations" "general")

for category in "${categories[@]}"; do
    mkdir -p "$SCRIPT_DIR/patterns/$category"
    mkdir -p "$SCRIPT_DIR/antipatterns/$category"
    echo "✓ Created directories for category: $category"
done

echo

# Create initial pattern files
echo "Creating initial pattern files..."

# Corpus operations patterns
cat > "$SCRIPT_DIR/patterns/corpus-operations/initialization.json" <<'EOF'
{
  "category": "corpus-operations",
  "subcategory": "initialization",
  "patterns": []
}
EOF

# Audit operations patterns
cat > "$SCRIPT_DIR/patterns/audit-operations/code-quality-fixes.json" <<'EOF'
{
  "category": "audit-operations",
  "subcategory": "code-quality",
  "patterns": []
}
EOF

# Content operations patterns
cat > "$SCRIPT_DIR/patterns/content-operations/newsletter-patterns.json" <<'EOF'
{
  "category": "content-operations",
  "subcategory": "newsletter",
  "patterns": []
}
EOF

echo "✓ Created initial pattern files"
echo

# Create risk databases
echo "Creating risk databases..."

cat > "$SCRIPT_DIR/risks/corpus-risks.json" <<'EOF'
{
  "initialization": [
    {
      "risk": "Initialize in wrong directory",
      "likelihood": 3,
      "impact": 4,
      "prevention": "Verify pwd, show full path, ask user to confirm"
    },
    {
      "risk": "Overwrite existing corpus",
      "likelihood": 2,
      "impact": 5,
      "prevention": "Check for existing .corpus/, require explicit confirmation"
    }
  ],
  "conversion": [
    {
      "risk": "Lose existing project files",
      "likelihood": 2,
      "impact": 5,
      "prevention": "Create backup before conversion"
    }
  ]
}
EOF

cat > "$SCRIPT_DIR/risks/audit-risks.json" <<'EOF'
{
  "code-quality": [
    {
      "risk": "Fixes break existing functionality",
      "likelihood": 4,
      "impact": 5,
      "prevention": "Run tests after each fix, verify no new issues"
    }
  ],
  "convergence": [
    {
      "risk": "GATE never converges (same issues reappear)",
      "likelihood": 3,
      "impact": 4,
      "prevention": "Fix root cause, not symptoms. Use detect-infinite-loop."
    }
  ]
}
EOF

cat > "$SCRIPT_DIR/risks/content-risks.json" <<'EOF'
{
  "newsletter": [
    {
      "risk": "Broken links in newsletter",
      "likelihood": 3,
      "impact": 3,
      "prevention": "Validate all links before publishing"
    }
  ],
  "blog": [
    {
      "risk": "Poor SEO (title, meta, headings)",
      "likelihood": 3,
      "impact": 4,
      "prevention": "Apply blog-seo-optimization pattern"
    }
  ]
}
EOF

echo "✓ Created risk databases"
echo

# Create README
cat > "$SCRIPT_DIR/README.md" <<'EOF'
# Learning Storage Infrastructure

This directory contains the learning system's pattern library, antipatterns, risks, and execution history.

## Directory Structure

```
.corpus/learning/
├── patterns/{category}/           # Proven solutions
├── antipatterns/{category}/       # Known failures
├── risks/{category}-risks.json    # Pre-mortem risk databases
├── pre-mortems/recent/            # Pre-mortem reports
├── checkpoints/                   # Context checkpoints
└── metrics/                       # Effectiveness tracking
```

## Categories

- **corpus-operations**: corpus-init, corpus-convert, corpus-config
- **audit-operations**: audits, fixes, convergence
- **content-operations**: newsletters, blogs, websites
- **general**: Cross-cutting patterns

## Pattern Format

```json
{
  "id": "pattern-unique-id",
  "name": "pattern-name",
  "category": "category-name",
  "description": "What this pattern solves",
  "solution": "How to implement",
  "applicability": "When to use",
  "metrics": {
    "applications": 0,
    "successes": 0,
    "failures": 0,
    "successRate": 0.0
  },
  "tags": ["tag1", "tag2"]
}
```

## Antipattern Format

```json
{
  "id": "antipattern-unique-id",
  "name": "antipattern-name",
  "category": "category-name",
  "problem": "What goes wrong",
  "occurrences": 0,
  "prevention": "How to avoid",
  "tags": ["tag1", "tag2"]
}
```

## Usage

The pattern library is automatically queried during battle-plan execution (Phase 2: Knowledge Check).

New patterns and antipatterns are automatically saved during battle-plan completion (Phase 8: Pattern Update).

## Seeding Data

Run `./seed-from-existing-skills.sh` to extract patterns and antipatterns from existing ERROR-AND-FIXES-LOG.md files.
EOF

echo "✓ Created README.md"
echo

echo "==================================================="
echo "Learning storage infrastructure setup complete!"
echo "==================================================="
echo
echo "Next steps:"
echo "1. Run seed-from-existing-skills.sh to populate patterns"
echo "2. Patterns will automatically accumulate as skills are used"
echo "3. Check metrics/ directory for effectiveness tracking"
echo

ls -lah "$SCRIPT_DIR"
