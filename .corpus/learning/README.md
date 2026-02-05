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
