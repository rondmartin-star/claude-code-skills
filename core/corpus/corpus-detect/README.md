# Corpus Detection

**Purpose:** Detect and validate corpus status for any project directory

**Size:** 8.4 KB

---

## Quick Start

```javascript
// Check if project is corpus-enabled
const status = await detectCorpus('/path/to/project');

if (status.isCorpusEnabled) {
  console.log(`✓ Corpus: ${status.config.name}`);
  console.log(`✓ Registered: ${status.isRegistered}`);
  console.log(`✓ Bits: ${status.infrastructure.bitCount}`);
} else {
  console.log('✗ Not corpus-enabled');
}
```

## What It Does

- Wraps CorpusHub detection API
- Checks for corpus-config.json
- Validates configuration schema
- Verifies CorpusHub registration
- Inspects .corpus/ infrastructure
- Counts indexed bits

## When to Use

✅ Checking if project is corpus-enabled
✅ Validating corpus setup
✅ Diagnosing corpus issues

❌ Initializing new corpus (use corpus-init)
❌ Modifying configuration (use corpus-config)

## API Integration

**Endpoint:** `GET /api/corpora/detect?path=/project/path`

**Response:**
```json
{
  "isCorpusEnabled": true,
  "isRegistered": true,
  "config": {
    "name": "Project Name"
  },
  "infrastructure": {
    "bitCount": 47
  }
}
```

---

**Part of:** v4.0.0 Universal Skills  
**Category:** Core Corpus Management  
**Dependencies:** CorpusHub API
