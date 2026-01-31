---
name: content
description: >
  Content quality audit checking grammar, spelling, readability, style, and voice
  alignment. Validates writing quality and framework voice consistency. Use when:
  content review, pre-publication, or part of user methodology audits.
---

# Content Audit

**Purpose:** Comprehensive content quality validation
**Size:** ~13 KB
**Type:** Audit Type (Part of User Methodology)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Audit content quality"
- "Check grammar and spelling"
- "Validate readability"
- "Review writing style"

**Context Indicators:**
- Pre-publication content review
- Part of convergence (user methodology)
- Content quality assurance
- Voice alignment validation

---

## Content Checks

### 1. Grammar

**Issues Detected:**
- Subject-verb agreement
- Verb tense consistency
- Pronoun-antecedent agreement
- Sentence fragments
- Run-on sentences

**Example Issues:**
```
✗ "The team are working on the project"
✓ "The team is working on the project"

✗ "Each of the members have their own role"
✓ "Each of the members has their own role"

✗ "She don't understand the concept"
✓ "She doesn't understand the concept"
```

**Detection:**
```javascript
const grammarRules = [
  {
    pattern: /\b(team|group|committee)\s+are\b/gi,
    suggestion: 'Use "is" with collective nouns',
    severity: 'medium'
  },
  {
    pattern: /\b(don't|doesn't)\s+(he|she|it)\b/gi,
    suggestion: 'Subject-verb disagreement',
    severity: 'high'
  }
];
```

### 2. Spelling

**Types:**
- Misspellings
- Commonly confused words
- Domain-specific terms
- Brand names

**Example Issues:**
```
✗ "recieve" → ✓ "receive"
✗ "occured" → ✓ "occurred"
✗ "its a problem" → ✓ "it's a problem"
✗ "affect the outcome" → ✓ "effect the outcome" (context-dependent)
```

**Detection:**
```javascript
async function checkSpelling(content, customDictionary = []) {
  const words = content.match(/\b[a-zA-Z]+\b/g);
  const misspellings = [];

  for (const word of words) {
    if (!isInDictionary(word) &&
        !customDictionary.includes(word.toLowerCase())) {
      const suggestions = getSuggestions(word);
      misspellings.push({
        word,
        suggestions,
        severity: 'medium'
      });
    }
  }

  return misspellings;
}
```

### 3. Readability

**Metrics:**
- Flesch Reading Ease
- Flesch-Kincaid Grade Level
- Average sentence length
- Complex word percentage
- Passive voice percentage

**Flesch Reading Ease:**
```
90-100: Very Easy (5th grade)
80-89: Easy (6th grade)
70-79: Fairly Easy (7th grade)
60-69: Standard (8th-9th grade)
50-59: Fairly Difficult (10th-12th grade)
30-49: Difficult (College)
0-29: Very Difficult (College graduate)
```

**Calculation:**
```javascript
function calculateReadability(text) {
  const sentences = text.split(/[.!?]+/).length;
  const words = text.split(/\s+/).length;
  const syllables = countSyllables(text);

  // Flesch Reading Ease
  const readingEase = 206.835 - 1.015 * (words / sentences) -
                      84.6 * (syllables / words);

  // Flesch-Kincaid Grade Level
  const gradeLevel = 0.39 * (words / sentences) +
                     11.8 * (syllables / words) - 15.59;

  return {
    readingEase: Math.round(readingEase),
    gradeLevel: Math.round(gradeLevel * 10) / 10,
    avgSentenceLength: Math.round(words / sentences),
    interpretation: getInterpretation(readingEase)
  };
}
```

**Target Levels from Config:**
```json
{
  "content": {
    "config": {
      "readability_target": "grade-10",
      "max_avg_sentence_length": 20,
      "max_passive_voice_percent": 10
    }
  }
}
```

### 4. Style Issues

**Common Problems:**
- Passive voice overuse
- Wordiness
- Redundancy
- Clichés
- Jargon without explanation

**Passive Voice Detection:**
```javascript
const passivePatterns = [
  /\b(am|is|are|was|were|be|been|being)\s+\w+ed\b/gi,
  /\b(am|is|are|was|were|be|been|being)\s+\w+en\b/gi
];

function detectPassiveVoice(text) {
  const sentences = text.split(/[.!?]+/);
  const passiveSentences = [];

  sentences.forEach((sentence, idx) => {
    passivePatterns.forEach(pattern => {
      if (pattern.test(sentence)) {
        passiveSentences.push({
          line: idx + 1,
          sentence: sentence.trim(),
          suggestion: 'Consider active voice'
        });
      }
    });
  });

  return passiveSentences;
}
```

**Wordiness Patterns:**
```javascript
const wordyPhrases = {
  'at this point in time': 'now',
  'due to the fact that': 'because',
  'in order to': 'to',
  'for the purpose of': 'to',
  'in the event that': 'if',
  'it is important to note that': '',
  'has the ability to': 'can'
};
```

### 5. Voice Alignment

**Check against corpus voice attributes:**
```json
{
  "voice": {
    "attributes": ["professional", "clear", "technical"],
    "avoid": ["marketing speak", "jargon", "vague statements"],
    "preferredTerms": {
      "OAuth 2.0": "OAuth"
    }
  }
}
```

**Detection:**
```javascript
async function checkVoiceAlignment(content, voiceConfig) {
  const issues = [];

  // Check for avoided patterns
  voiceConfig.avoid.forEach(avoidPattern => {
    const pattern = getPatternForPhrase(avoidPattern);
    const matches = content.match(pattern);

    if (matches) {
      issues.push({
        category: 'voice_violation',
        avoided_pattern: avoidPattern,
        instances: matches.length,
        severity: 'medium'
      });
    }
  });

  // Check for preferred terms
  Object.entries(voiceConfig.preferredTerms).forEach(([full, short]) => {
    const fullCount = (content.match(new RegExp(full, 'g')) || []).length;
    const shortCount = (content.match(new RegExp(short, 'g')) || []).length;

    if (shortCount > fullCount * 2) {
      issues.push({
        category: 'preferred_term',
        message: `Overusing "${short}" instead of "${full}"`,
        severity: 'low'
      });
    }
  });

  return issues;
}
```

### 6. Style Guide Compliance

**Load external style guide:**
```javascript
async function checkStyleGuide(content, styleGuidePath) {
  const styleGuide = await loadStyleGuide(styleGuidePath);
  const issues = [];

  // Check capitalization rules
  styleGuide.capitalization?.forEach(rule => {
    if (!checkCapitalization(content, rule)) {
      issues.push({
        rule: rule.name,
        severity: 'low'
      });
    }
  });

  // Check formatting rules
  styleGuide.formatting?.forEach(rule => {
    if (!checkFormatting(content, rule)) {
      issues.push({
        rule: rule.name,
        severity: 'medium'
      });
    }
  });

  return issues;
}
```

---

## Configuration

### corpus-config.json

```json
{
  "audit": {
    "convergence": {
      "methodologies": [
        {
          "name": "user",
          "description": "How content is experienced",
          "audits": [
            {
              "id": "content",
              "config": {
                "check_grammar": true,
                "check_spelling": true,
                "check_readability": true,
                "readability_target": "grade-10",
                "max_avg_sentence_length": 20,
                "max_passive_voice_percent": 10,
                "style_guide": "voice/style-guide.md",
                "check_voice_alignment": true,
                "custom_dictionary": [
                  "OAuth",
                  "CorpusHub",
                  "parameterized"
                ]
              }
            }
          ]
        }
      ]
    }
  }
}
```

---

## Auto-Fix Capabilities

### ✓ Fully Automatic

**Spelling (obvious):**
```
Issue: "recieve"
Fix: "receive"
Strategy: Use dictionary suggestions
```

**Wordiness:**
```
Issue: "at this point in time"
Fix: "now"
Strategy: Replace with concise alternative
```

**Preferred Terms:**
```
Issue: Overusing "OAuth" instead of "OAuth 2.0 with cookie separation"
Fix: Replace some instances with full term
Strategy: Balance usage according to preferences
```

### ⚠ User Approval Required

**Grammar (context-dependent):**
```
Issue: "The data is important" vs "The data are important"
Fix: Depends on style guide (US vs UK)
Strategy: Present options to user
```

**Passive Voice:**
```
Issue: "The report was written by the team"
Fix: "The team wrote the report"
Strategy: Suggest active alternative, user approves
```

### ✗ Manual Only

**Readability (restructuring):**
```
Issue: Sentence too long (45 words)
Fix: Requires content restructuring
Strategy: Flag for manual review
```

**Voice Misalignment:**
```
Issue: Tone doesn't match voice attributes
Fix: Requires rewriting
Strategy: Provide guidance on voice attributes
```

---

## Output Format

```json
{
  "audit_type": "content",
  "timestamp": "2026-01-31T10:00:00Z",
  "project_path": "/path/to/project",
  "summary": {
    "files_scanned": 47,
    "grammar_issues": 12,
    "spelling_issues": 8,
    "readability_score": 65.2,
    "readability_target": 60,
    "style_issues": 15,
    "voice_violations": 3
  },
  "issues": [
    {
      "severity": "medium",
      "category": "grammar",
      "location": "docs/guide.md:42",
      "issue": "Subject-verb disagreement",
      "context": "The team are working on the project",
      "suggestion": "The team is working on the project",
      "auto_fixable": true
    },
    {
      "severity": "low",
      "category": "readability",
      "location": "docs/api.md",
      "readability_score": 45.3,
      "target_score": 60,
      "grade_level": 14.2,
      "message": "Content is too difficult for target audience",
      "auto_fixable": false
    }
  ]
}
```

---

## Integration with User Methodology

Content audit is part of the **user methodology** in 3-3-1 convergence:

```json
{
  "methodologies": [
    {
      "name": "user",
      "description": "How it's experienced",
      "audits": [
        "content",          // ← This audit
        "accessibility",
        "ux-performance"
      ]
    }
  ]
}
```

**User Perspective:**
- Is content clear and readable?
- Are there grammar or spelling errors?
- Does writing match expected voice?
- Is content appropriate for target audience?

---

## Quick Reference

**Run content audit:**
```javascript
const issues = await runAudit('content', projectConfig);
```

**Check readability:**
```javascript
const score = calculateReadability(content);
console.log(`Reading Ease: ${score.readingEase}`);
console.log(`Grade Level: ${score.gradeLevel}`);
```

**Check voice alignment:**
```javascript
const voiceIssues = await checkVoiceAlignment(content, voiceConfig);
```

**Generate content report:**
```javascript
const report = await generateContentReport(projectPath);
console.log(`Grammar issues: ${report.summary.grammar_issues}`);
console.log(`Readability: ${report.summary.readability_score}`);
```

---

*End of Content Audit*
*Part of v4.0.0 Universal Skills Ecosystem*
*Methodology: User (How it's experienced)*
*Supports voice-driven content quality*
