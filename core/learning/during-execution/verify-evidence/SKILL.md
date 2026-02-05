---
name: verify-evidence
description: >
  Combat hallucination by demanding proof before declaring things done or true.
  Verifies claims against actual codebase, config files, test results, and command output.
  Provides confidence levels and flags uncertain statements. Use when: making claims,
  declaring completion, stating facts about code.
---

# Verify Evidence

**Purpose:** Demand proof before declaring done/true (combat hallucination)
**Type:** Learning Skill (During-Execution / Verification)
**Origin:** "Trust, but verify" - Ronald Reagan

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Verify this claim"
- "Prove it"
- "Show evidence"
- Before declaring something complete

**Context Indicators:**
- Declarative statements about code
- Completion claims
- Configuration assertions
- Test result claims
- File existence claims

---

## Core Concept

**The Problem:**
- Claude makes confident statements without verification
- "The function returns X" (didn't check actual code)
- "Tests pass" (didn't run tests)
- "File exists at path/to/file" (didn't verify)
- Hallucination looks identical to truth

**The Solution:**
- Intercept declarative statements
- Require evidence (file contents, command output, test results)
- Verify against actual codebase/config
- Provide confidence levels
- Flag uncertain claims

**Article Quote:** *"prove-it (demands proof before declaring done)"* - Listed as key skill for hallucination prevention

---

## Verification Process

### 1. Detect Claims Requiring Evidence

```javascript
function detectClaims(statement) {
  const claimPatterns = {
    completion: [
      /complete/i,
      /done/i,
      /finished/i,
      /implemented/i,
      /ready/i
    ],
    existence: [
      /file.*exists/i,
      /created.*at/i,
      /located.*in/i,
      /found.*in/i
    ],
    behavior: [
      /function.*returns/i,
      /code.*does/i,
      /system.*will/i,
      /api.*responds/i
    ],
    testing: [
      /tests.*pass/i,
      /all.*tests/i,
      /verified.*by/i,
      /validated/i
    ],
    configuration: [
      /configured.*to/i,
      /settings.*are/i,
      /environment.*is/i
    ]
  };

  const claims = [];

  for (const [type, patterns] of Object.entries(claimPatterns)) {
    for (const pattern of patterns) {
      if (pattern.test(statement)) {
        claims.push({
          type,
          statement,
          requiresEvidence: true
        });
      }
    }
  }

  return claims;
}
```

**Example:**
```
Statement: "OAuth implementation is complete"

Detected claims:
- Type: completion
- Statement: "OAuth implementation is complete"
- Requires evidence: YES

Sub-claims to verify:
1. OAuth config file exists with provider settings
2. OAuth routes defined in API
3. Token caching implemented
4. Session integration working
5. Tests pass for OAuth flow
```

### 2. Define Required Evidence

```javascript
async function defineRequiredEvidence(claim) {
  const evidenceRequirements = {
    completion: [
      "All specified files exist",
      "Code implements required functionality",
      "Tests pass",
      "No compiler/linter errors"
    ],
    existence: [
      "File exists at claimed path",
      "File contents match description"
    ],
    behavior: [
      "Code inspection confirms behavior",
      "Test demonstrates behavior",
      "Runtime output confirms"
    ],
    testing: [
      "Test output shown",
      "All tests passed",
      "No skipped/pending tests",
      "Coverage meets threshold"
    ],
    configuration: [
      "Config file exists",
      "Settings present and correct",
      "Environment variables set"
    ]
  };

  return evidenceRequirements[claim.type] || ["Evidence required"];
}
```

**Example:**
```
Claim: "OAuth implementation is complete"

Required Evidence:
1. File Evidence:
   - [x] src/config/oauth.js exists
   - [x] src/routes/auth.js exists
   - [ ] src/middleware/oauth-cache.js exists

2. Code Evidence:
   - [x] OAuth provider configured (check config file)
   - [x] Routes defined (check routes file)
   - [ ] Token caching implemented (NOT FOUND)
   - [ ] Session integration (NOT VERIFIED)

3. Test Evidence:
   - [ ] OAuth flow tests pass (NOT RUN)
   - [ ] Token caching tests pass (NOT RUN)
   - [ ] Session tests pass (NOT RUN)

4. Runtime Evidence:
   - [ ] Can authenticate with OAuth (NOT TESTED)
   - [ ] Tokens cached correctly (NOT TESTED)
   - [ ] Sessions persist (NOT TESTED)
```

### 3. Gather Evidence

```javascript
async function gatherEvidence(claim, requirements) {
  const evidence = {
    fileEvidence: [],
    codeEvidence: [],
    testEvidence: [],
    runtimeEvidence: [],
    verified: [],
    missing: [],
    confidence: 0
  };

  for (const requirement of requirements) {
    try {
      const proof = await findProof(requirement);
      evidence.verified.push({
        requirement,
        proof,
        verified: true
      });
    } catch (error) {
      evidence.missing.push({
        requirement,
        error: error.message,
        verified: false
      });
    }
  }

  evidence.confidence = evidence.verified.length / requirements.length;

  return evidence;
}

async function findProof(requirement) {
  if (requirement.includes("file exists")) {
    const path = extractPath(requirement);
    return await verifyFileExists(path);
  }

  if (requirement.includes("tests pass")) {
    return await runTestsAndCapture();
  }

  if (requirement.includes("code implements")) {
    const func = extractFunction(requirement);
    return await verifyCodeImplementation(func);
  }

  if (requirement.includes("config")) {
    const config = extractConfigKey(requirement);
    return await verifyConfigSetting(config);
  }

  throw new Error(`Don't know how to verify: ${requirement}`);
}
```

**Example Evidence Gathering:**
```javascript
// Verify file exists
const fileProof = await verifyFileExists("src/config/oauth.js");
// Returns: {
//   exists: true,
//   path: "src/config/oauth.js",
//   size: 1234,
//   modified: "2026-02-04T10:30:00Z"
// }

// Verify code implements functionality
const codeProof = await verifyCodeImplementation({
  file: "src/config/oauth.js",
  expectedContent: "clientId, clientSecret, redirectUri"
});
// Returns: {
//   found: true,
//   file: "src/config/oauth.js",
//   lines: [15-25],
//   content: "module.exports = {clientId, clientSecret, redirectUri}"
// }

// Verify tests pass
const testProof = await runTestsAndCapture({
  pattern: "oauth",
  suite: "auth"
});
// Returns: {
//   ran: true,
//   passed: 8,
//   failed: 2,
//   skipped: 0,
//   output: "..."
// }
```

### 4. Calculate Confidence Level

```javascript
function calculateConfidence(evidence) {
  const weights = {
    fileEvidence: 0.2,      // Files exist (necessary but not sufficient)
    codeEvidence: 0.3,      // Code implements logic
    testEvidence: 0.3,      // Tests pass
    runtimeEvidence: 0.2    // Actually works when run
  };

  let confidence = 0;

  for (const [type, weight] of Object.entries(weights)) {
    const typeEvidence = evidence[type] || [];
    const verifiedCount = typeEvidence.filter(e => e.verified).length;
    const totalCount = typeEvidence.length || 1;
    const typeConfidence = verifiedCount / totalCount;

    confidence += typeConfidence * weight;
  }

  return {
    score: confidence,
    level: getConfidenceLevel(confidence),
    reasoning: explainConfidence(evidence)
  };
}

function getConfidenceLevel(score) {
  if (score >= 0.9) return 'VERIFIED';
  if (score >= 0.7) return 'HIGH';
  if (score >= 0.5) return 'MEDIUM';
  if (score >= 0.3) return 'LOW';
  return 'UNVERIFIED';
}
```

**Confidence Levels:**
- **VERIFIED (90-100%):** All evidence gathered and confirmed
- **HIGH (70-89%):** Most evidence confirmed, minor gaps
- **MEDIUM (50-69%):** Some evidence, significant gaps
- **LOW (30-49%):** Little evidence, mostly unverified
- **UNVERIFIED (0-29%):** Cannot verify claim

### 5. Report Verification Results

```javascript
async function reportVerification(claim, evidence, confidence) {
  const report = {
    claim: claim.statement,
    confidence: confidence,
    verified: evidence.verified,
    missing: evidence.missing,
    recommendation: generateRecommendation(confidence),
    status: determineStatus(confidence)
  };

  // Format for display
  console.log(formatVerificationReport(report));

  return report;
}
```

**Example Report:**
```
╔════════════════════════════════════════════════════════════════╗
║                   EVIDENCE VERIFICATION                        ║
╚════════════════════════════════════════════════════════════════╝

Claim: "OAuth implementation is complete"

Confidence: 40% (LOW)
Status: ⚠️ INCOMPLETE

───────────────────────────────────────────────────────────────

VERIFIED EVIDENCE (4/10):

✓ File exists: src/config/oauth.js
  Proof: File found, 1,234 bytes, modified 2h ago

✓ File exists: src/routes/auth.js
  Proof: File found, 2,456 bytes, modified 1h ago

✓ OAuth provider configured
  Proof: Found clientId, clientSecret in config (lines 15-25)

✓ Routes defined
  Proof: Found /auth/oauth/callback route (line 42)

───────────────────────────────────────────────────────────────

MISSING EVIDENCE (6/10):

✗ Token caching implemented
  Error: No cache module found in src/middleware/

✗ Session integration working
  Error: Cannot verify without runtime test

✗ OAuth flow tests pass
  Error: Tests not run (use: npm test)

✗ Token caching tests pass
  Error: Tests not run

✗ Session persistence tests pass
  Error: Tests not run

✗ Can authenticate with OAuth
  Error: No runtime verification performed

───────────────────────────────────────────────────────────────

RECOMMENDATION:

⚠️ Cannot confirm completion - 6 critical items unverified

Next steps:
1. Implement token caching (src/middleware/oauth-cache.js)
2. Integrate with session system
3. Run test suite: npm test
4. Verify OAuth flow works end-to-end

Status: INCOMPLETE (40% confidence)
Do not proceed until confidence >= 80%
```

---

## Integration with Battle-Plan

**Position:** During Execution (Phase 5) - Checkpoints

**Flow:**
```
Execute Task:
├─ Implement OAuth config ✓
├─ Implement OAuth routes ✓
│
├─ [VERIFY-EVIDENCE checkpoint]
│  Claim: "OAuth routes implemented"
│  Evidence: ✓ Routes file exists, routes defined
│  Confidence: 80% (HIGH) → PROCEED
│
├─ Implement token caching
│
├─ [VERIFY-EVIDENCE checkpoint]
│  Claim: "Token caching implemented"
│  Evidence: ✗ No cache module found
│  Confidence: 20% (UNVERIFIED) → BLOCK
│
└─ [Cannot proceed until caching verified]
```

**Checkpoints:**
- After each major subtask
- Before declaring completion
- When making claims about code
- Before moving to next phase

---

## Verification Strategies

### File Verification
```javascript
async function verifyFile(path, expectedContent = null) {
  // Check existence
  const exists = await fileExists(path);
  if (!exists) {
    throw new Error(`File not found: ${path}`);
  }

  // Check content (if specified)
  if (expectedContent) {
    const content = await readFile(path);
    const matches = content.includes(expectedContent);
    if (!matches) {
      throw new Error(`File missing expected content: ${expectedContent}`);
    }
  }

  return {verified: true, path, content: await readFile(path)};
}
```

### Code Verification
```javascript
async function verifyCodeImplementation(spec) {
  const file = await readFile(spec.file);

  // Check for expected functions/classes
  for (const expected of spec.expectedElements) {
    if (!file.includes(expected)) {
      throw new Error(`Code missing: ${expected}`);
    }
  }

  // Check for antipatterns
  for (const antipattern of spec.antipatterns || []) {
    if (file.includes(antipattern)) {
      throw new Error(`Antipattern found: ${antipattern}`);
    }
  }

  return {verified: true, file: spec.file};
}
```

### Test Verification
```javascript
async function verifyTests(pattern) {
  const result = await runCommand(`npm test -- ${pattern}`);

  if (result.exitCode !== 0) {
    throw new Error(`Tests failed: ${result.stderr}`);
  }

  const parsed = parseTestOutput(result.stdout);

  if (parsed.failed > 0) {
    throw new Error(`${parsed.failed} tests failed`);
  }

  if (parsed.skipped > 0) {
    console.log(`⚠️ ${parsed.skipped} tests skipped`);
  }

  return {
    verified: true,
    passed: parsed.passed,
    failed: parsed.failed,
    output: result.stdout
  };
}
```

### Runtime Verification
```javascript
async function verifyRuntime(endpoint, expectedResponse) {
  const response = await fetch(endpoint);

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  const data = await response.json();

  if (expectedResponse) {
    const matches = objectMatches(data, expectedResponse);
    if (!matches) {
      throw new Error(`Response doesn't match expected`);
    }
  }

  return {verified: true, response: data};
}
```

---

## Common Verification Patterns

### OAuth Implementation
```javascript
const oauthVerification = {
  claims: [
    "OAuth provider configured",
    "Routes defined",
    "Token caching implemented",
    "Session integration working",
    "Tests pass"
  ],
  evidence: [
    {claim: "OAuth provider configured", verify: () =>
      verifyFile("src/config/oauth.js", "clientId")
    },
    {claim: "Routes defined", verify: () =>
      verifyCode("src/routes/auth.js", {expectedElements: ["/oauth/callback"]})
    },
    {claim: "Token caching implemented", verify: () =>
      verifyFile("src/middleware/oauth-cache.js")
    },
    {claim: "Session integration working", verify: () =>
      verifyTests("session.*oauth")
    },
    {claim: "Tests pass", verify: () =>
      verifyTests("oauth")
    }
  ]
};
```

### Database Migration
```javascript
const migrationVerification = {
  claims: [
    "Migration file created",
    "Up migration defined",
    "Down migration defined",
    "Idempotent (can run multiple times)",
    "Tests pass"
  ],
  evidence: [
    {claim: "Migration file created", verify: () =>
      verifyFile("migrations/20260204_add_oauth_table.js")
    },
    {claim: "Up migration defined", verify: () =>
      verifyCode("migrations/20260204_add_oauth_table.js", {
        expectedElements: ["exports.up"]
      })
    },
    {claim: "Down migration defined", verify: () =>
      verifyCode("migrations/20260204_add_oauth_table.js", {
        expectedElements: ["exports.down"]
      })
    },
    {claim: "Idempotent", verify: () =>
      verifyCode("migrations/20260204_add_oauth_table.js", {
        expectedElements: ["IF NOT EXISTS"]
      })
    },
    {claim: "Tests pass", verify: () =>
      verifyTests("migration")
    }
  ]
};
```

---

## Configuration

```json
{
  "verifyEvidence": {
    "enabled": true,
    "strictMode": true,  // Require all evidence before proceeding
    "thresholds": {
      "proceed": 0.8,    // 80% confidence to proceed
      "warn": 0.5,       // 50% confidence shows warning
      "block": 0.3       // <30% confidence blocks
    },
    "autoVerify": {
      "fileExists": true,
      "runTests": false,  // Don't auto-run tests (user triggers)
      "codeInspection": true
    },
    "reporting": {
      "verbose": true,
      "showProof": true,
      "logVerifications": true
    }
  }
}
```

---

## Quick Reference

**Verify claim manually:**
```javascript
const verification = await verifyEvidence.verify({
  claim: "OAuth implementation complete",
  requiredEvidence: [
    "File: src/config/oauth.js",
    "Code: OAuth provider configured",
    "Tests: OAuth flow tests pass",
    "Runtime: Can authenticate"
  ]
});

if (verification.confidence < 0.8) {
  throw new Error(`Insufficient evidence: ${verification.confidence}`);
}
```

**Add verification checkpoint:**
```javascript
async function implementFeature() {
  await doImplementation();

  // Checkpoint
  await verifyEvidence.checkpoint({
    claim: "Feature implemented",
    verify: [
      () => verifyFile("src/feature.js"),
      () => verifyTests("feature"),
      () => verifyNoErrors()
    ]
  });

  return {complete: true};
}
```

---

## Benefits

**Prevents:**
- Hallucination going undetected
- False completion claims
- Unverified assumptions
- Proceeding with incomplete work

**Provides:**
- Evidence-based confidence
- Clear verification status
- Missing evidence list
- Actionable next steps

**Enables:**
- Trust in completion claims
- Reliable progress tracking
- Quality gates
- Evidence audit trail

---

*End of Verify-Evidence*
*Part of v4.0.0 Universal Skills Ecosystem*
*Category: Learning / During-Execution (Verification)*
*"Trust, but verify"*
