# Corpus Detection

Detect and validate corpus status for any project directory using the CorpusHub detection API.

## Usage

```bash
# Check if project is corpus-enabled
"Check if this is corpus-enabled"
"Is /path/to/project a corpus?"
```

## What It Does

- Detects if corpus-config.json exists
- Validates configuration structure
- Checks CorpusHub registration
- Verifies infrastructure (corpus dir, database)
- Provides actionable suggestions for issues

## API Endpoint

```
GET http://localhost:3000/api/corpora/detect?path=/absolute/path
```

## Returns

- `isCorpusEnabled`: boolean
- `checks`: Object with validation results
- `config`: Parsed configuration (if valid)
- `issues`: Array of problems found
- `suggestions`: Array of recommended actions

## Used By

- corpus-init (check before initialization)
- corpus-convert (detect existing infrastructure)
- CI/CD pipelines (validate corpus health)

## See Also

- SKILL.md - Complete documentation
- C:\Program Files\CorpusHub\docs\CORPUS-DETECTION.md
