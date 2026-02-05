---
name: rubber-duck
description: >
  Force problem articulation before execution. Clarifies scope, identifies assumptions,
  lists unknowns, and generates clarifying questions. Use when: starting unclear tasks,
  ambiguous requirements, complex feature requests.
---

# Rubber-Duck Debugging

**Purpose:** Clarify scope and requirements through forced articulation
**Type:** Learning Skill (Pre-Execution / Clarification)
**Origin:** Rubber duck debugging - explain problem to rubber duck, solution becomes clear

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Clarify this task"
- "What are we actually building?"
- "Help me understand the requirements"
- Before starting unclear tasks

**Context Indicators:**
- Ambiguous user request
- Multiple possible interpretations
- Unclear scope or requirements
- Complex feature request
- First time implementing something

---

## Core Concept

**The Problem:**
- Jump straight to implementation
- Assumptions buried in mental model
- Unknowns not identified
- Requirements drift during execution

**The Solution:**
- Force explicit articulation
- Surface hidden assumptions
- Identify what's known vs. unknown
- Generate clarifying questions upfront

**Article Quote:** *"Clarify scope (what are we actually building?)"* - First step in battle-plan

---

## Rubber-Duck Process

### 1. Plain Language Explanation

```javascript
async function explainTaskPlainly(task) {
  const explanation = {
    whatWeAreBuilding: "",
    why: "",
    who: "",
    when: "",
    how: "",
    success: ""
  };

  // Force plain language (no jargon allowed)
  explanation.whatWeAreBuilding = explainLikeImFive(task.description);
  explanation.why = explainPurpose(task);
  explanation.who = identifyStakeholders(task);
  explanation.when = identifyTimeline(task);
  explanation.how = identifyApproach(task);
  explanation.success = defineSuccess(task);

  return explanation;
}
```

**Example:**
```
User: "Add OAuth login"

Plain Language Explanation:
- What: A way for users to log in using their Google/GitHub/etc. account
  instead of creating a new username/password
- Why: Users prefer not creating yet another password
- Who: End users logging into the application
- When: Before MVP launch (blocking other features)
- How: Third-party OAuth 2.0 flow with token management
- Success: Users can log in with their existing accounts, sessions work reliably
```

### 2. Identify Assumptions

```javascript
async function identifyAssumptions(task, explanation) {
  const assumptions = {
    stated: [],      // Explicitly stated
    implicit: [],    // Implied but not stated
    risky: []        // Potentially problematic
  };

  // Extract implicit assumptions
  assumptions.implicit = extractImplicitAssumptions(explanation);

  // Flag risky assumptions
  assumptions.risky = assumptions.implicit.filter(a => a.risk === 'high');

  return assumptions;
}
```

**Example:**
```
Assumptions in "Add OAuth login":

Stated:
- Using OAuth 2.0 (not OAuth 1.0)
- Third-party provider (not implementing OAuth server)

Implicit (HIDDEN):
- Provider is Google/GitHub/similar (which one?)
- Existing user system needs integration (or fresh start?)
- Web application (what about mobile?)
- Users will link OAuth to existing accounts (or new accounts only?)
- Session management already exists (or build from scratch?)

Risky Assumptions:
⚠️ "Existing session system compatible with OAuth" (HIGH RISK)
  → May need complete session rewrite
⚠️ "Provider APIs are stable" (MEDIUM RISK)
  → Provider could change API without notice
```

### 3. Known vs. Unknown Analysis

```javascript
async function analyzeKnowledge(task, assumptions) {
  const knowledge = {
    known: [],
    unknown: [],
    needsResearch: [],
    needsUserInput: []
  };

  // Categorize what we know
  knowledge.known = identifyKnownFacts(task);

  // Identify unknowns
  knowledge.unknown = identifyUnknowns(task, assumptions);

  // Separate unknowns by resolution method
  knowledge.needsResearch = knowledge.unknown.filter(u =>
    u.resolvableBy === 'research'
  );

  knowledge.needsUserInput = knowledge.unknown.filter(u =>
    u.resolvableBy === 'user-decision'
  );

  return knowledge;
}
```

**Example:**
```
Known:
✓ OAuth 2.0 is the standard approach
✓ Third-party libraries exist (Passport.js, etc.)
✓ Flow: redirect → authorize → callback → token
✓ Need to store tokens securely

Unknown (Research):
? What OAuth library is best for our stack?
? How to handle token refresh?
? Rate limits for OAuth providers?
? PKCE required for our use case?

Unknown (User Decision):
? Which OAuth provider(s)? (Google, GitHub, both?)
? Replace existing auth or supplement?
? What happens to existing user accounts?
? Mobile app support required?
? SSO across multiple apps?
```

### 4. Generate Clarifying Questions

```javascript
async function generateQuestions(knowledge, assumptions) {
  const questions = {
    critical: [],    // Must answer before starting
    important: [],   // Should answer soon
    optional: []     // Nice to know
  };

  // Critical: Blocks implementation
  questions.critical = knowledge.needsUserInput.filter(u => u.blocking);

  // Important: Affects approach
  questions.important = knowledge.needsUserInput.filter(u =>
    !u.blocking && u.impact === 'high'
  );

  // Optional: Nice to clarify
  questions.optional = knowledge.needsUserInput.filter(u =>
    u.impact === 'low'
  );

  return prioritizeQuestions(questions);
}
```

**Example:**
```
Critical Questions (MUST answer):
1. Which OAuth provider(s) should we support?
   Impact: Determines implementation approach
   Options: Google only, GitHub only, both, others?

2. How do existing users migrate?
   Impact: May require database migration
   Options: Force re-registration, link accounts, both?

3. What happens to existing password authentication?
   Impact: Determines if we keep old system
   Options: Deprecate, keep alongside, phase out?

Important Questions (SHOULD answer):
4. Mobile app support needed?
   Impact: Affects token storage approach

5. Session duration preferences?
   Impact: Affects refresh token strategy

6. Admin/service accounts use OAuth too?
   Impact: May need separate auth system

Optional Questions (NICE to answer):
7. OAuth button styling preferences?
8. Remember me checkbox needed?
9. Login analytics requirements?
```

### 5. Validate Understanding

```javascript
async function validateUnderstanding(task, analysis) {
  const validation = {
    summary: "",
    assumptions: analysis.assumptions.implicit,
    unknowns: analysis.knowledge.needsUserInput,
    questions: analysis.questions.critical,
    nextSteps: []
  };

  // Generate summary
  validation.summary = generateSummary(task, analysis);

  // Determine next steps
  if (validation.questions.critical.length > 0) {
    validation.nextSteps.push("Get answers to critical questions");
  }

  if (validation.assumptions.risky.length > 0) {
    validation.nextSteps.push("Validate risky assumptions");
  }

  if (validation.unknowns.needsResearch.length > 0) {
    validation.nextSteps.push("Research technical unknowns");
  }

  return validation;
}
```

**Example Output:**
```
Understanding Validation:

Summary:
We're adding third-party OAuth authentication to allow users to log in
with existing accounts (Google/GitHub/etc.). This may replace or supplement
the current password-based system. Implementation complexity depends on
answers to critical questions below.

Implicit Assumptions (⚠️ need validation):
- Existing session system is compatible with OAuth
- Provider APIs are stable
- Users want this feature
- OAuth is more secure than current system

Critical Questions Blocking Start:
1. Which OAuth provider(s)?
2. Migrate existing users how?
3. Keep password auth or deprecate?

Next Steps:
1. Get answers to 3 critical questions from user
2. Validate assumption about session system compatibility
3. Research OAuth libraries for our stack

Ready to proceed? NO - awaiting answers to critical questions
```

---

## Integration with Battle-Plan

**Position:** Phase 1 - First step in battle-plan

**Flow:**
```
User Request →
├─ RUBBER-DUCK (you are here) →
│  ├─ Plain language explanation
│  ├─ Identify assumptions
│  ├─ Known vs. unknown
│  ├─ Generate questions
│  └─ Validate understanding
│
├─ [USER ANSWERS CRITICAL QUESTIONS]
│
├─ PATTERN-LIBRARY (with clarified scope) →
├─ PRE-MORTEM (with validated assumptions) →
└─ ...
```

**Why First:**
- Can't check patterns without knowing what we're building
- Can't run pre-mortem without understanding requirements
- Can't get user approval without clear scope

**Article Quote:** *"rubber-duck (clarify scope)"* - Listed as first skill in battle-plan sequence

---

## Output Format

```json
{
  "rubberDuckAnalysis": {
    "task": "Add OAuth login",
    "explanation": {
      "plainLanguage": "Let users log in with Google/GitHub instead of password",
      "why": "Better UX, users prefer existing accounts",
      "who": "End users",
      "when": "Before MVP launch",
      "how": "OAuth 2.0 with third-party library",
      "success": "Users can log in, sessions reliable"
    },
    "assumptions": {
      "stated": [
        "OAuth 2.0 (not 1.0)",
        "Third-party provider"
      ],
      "implicit": [
        "Provider is Google/GitHub",
        "Existing users need migration",
        "Web app only",
        "Session system compatible"
      ],
      "risky": [
        {
          "assumption": "Session system compatible",
          "risk": "high",
          "impact": "May require complete rewrite"
        }
      ]
    },
    "knowledge": {
      "known": [
        "OAuth 2.0 standard flow",
        "Libraries available",
        "Security considerations"
      ],
      "unknown": {
        "research": [
          "Best OAuth library for stack",
          "Token refresh patterns",
          "Rate limits"
        ],
        "userDecision": [
          "Which provider(s)?",
          "Migrate existing users how?",
          "Keep password auth?"
        ]
      }
    },
    "questions": {
      "critical": [
        {
          "question": "Which OAuth provider(s)?",
          "impact": "Determines implementation",
          "blocking": true,
          "options": ["Google", "GitHub", "Both", "Other"]
        },
        {
          "question": "Migrate existing users how?",
          "impact": "May require DB migration",
          "blocking": true,
          "options": ["Force re-register", "Link accounts", "Both"]
        },
        {
          "question": "Keep password auth?",
          "impact": "Determines if old system stays",
          "blocking": true,
          "options": ["Deprecate", "Keep alongside", "Phase out"]
        }
      ],
      "important": [...],
      "optional": [...]
    },
    "validation": {
      "summary": "Adding OAuth login, complexity depends on answers",
      "readyToProceed": false,
      "blockers": ["3 critical questions unanswered"],
      "nextSteps": [
        "Get answers to critical questions",
        "Validate session compatibility assumption",
        "Research OAuth libraries"
      ]
    }
  }
}
```

---

## User Interaction

**Present questions to user:**
```
I've analyzed the task "Add OAuth login" and need clarification on 3 critical points
before we can proceed:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CRITICAL QUESTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Which OAuth provider(s) should we support?
   a) Google only
   b) GitHub only
   c) Both Google and GitHub
   d) Other (specify)

   Impact: This determines which OAuth libraries we'll use and how
   we configure the authentication flow.

2. How should existing users migrate to OAuth?
   a) Force all users to re-register with OAuth
   b) Allow users to link OAuth to existing accounts
   c) Support both: OAuth for new, keep passwords for existing

   Impact: Option (b) may require database migration and account
   linking logic. Option (c) means maintaining both systems.

3. What happens to password authentication?
   a) Deprecate immediately (OAuth only)
   b) Keep both systems running indefinitely
   c) Gradual phase-out (timeline?)

   Impact: Keeping both systems doubles maintenance burden but
   provides flexibility.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I also identified these assumptions (please confirm):
⚠️ Current session system is compatible with OAuth tokens
⚠️ This is for web app only (not mobile)
⚠️ Users want this feature

Once you answer these questions, I can:
- Check pattern library for proven OAuth implementations
- Run pre-mortem to identify potential pitfalls
- Create implementation plan

Ready for your answers!
```

---

## Quick Reference

**Run rubber-duck manually:**
```javascript
const analysis = await rubberDuck.analyze({
  task: "Add OAuth login",
  description: userRequest.description
});

if (!analysis.validation.readyToProceed) {
  // Present questions to user
  await askUserQuestions(analysis.questions.critical);

  // Re-analyze with answers
  analysis = await rubberDuck.analyze({
    task: "Add OAuth login",
    answers: userAnswers
  });
}

// Proceed to next battle-plan phase
return analysis;
```

**Check if clarification needed:**
```javascript
const needsClarification = rubberDuck.needsClarification(task);
// Returns: true if task has ambiguity, unknowns, or risky assumptions
```

---

## Benefits

**Prevents:**
- Building the wrong thing
- Scope creep mid-implementation
- Assumptions causing failures
- Wasted effort on unclear requirements

**Provides:**
- Explicit scope definition
- Surfaced assumptions
- Clear list of unknowns
- Actionable questions for user

**Enables:**
- Pattern library to find relevant solutions
- Pre-mortem to assess specific risks
- Accurate time estimates
- Confident implementation

---

*End of Rubber-Duck*
*Part of v4.0.0 Universal Skills Ecosystem*
*Category: Learning / Pre-Execution*
*"Force problem articulation first"*
