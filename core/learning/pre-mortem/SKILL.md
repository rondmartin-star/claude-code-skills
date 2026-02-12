---
name: pre-mortem
description: >
  Pre-mortem analysis for anticipating failures before they happen. Imagine the task
  has failed and work backwards to identify risks, blockers, and preventive measures.
  Use when: starting complex tasks, planning implementations, before major changes.
---

# Pre-Mortem Analysis

**Purpose:** Anticipate and prevent failures before they occur
**Type:** Learning Skill (Proactive Risk Analysis)

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Run a pre-mortem"
- "What could go wrong?"
- "Anticipate failures"
- Before starting complex implementations

**Context Indicators:**
- Beginning a multi-step task
- Planning a complex refactoring
- Before making architectural changes
- Starting a new feature implementation

---

## Pre-Mortem Process

### The Core Concept

**Traditional Post-Mortem:** Analyze what went wrong after failure
**Pre-Mortem:** Imagine failure has occurred, then identify what caused it

**Why It Works:**
- Overcomes optimism bias
- Surfaces hidden concerns
- Enables proactive prevention
- Team members share doubts they might otherwise suppress

---

## Implementation Steps

### 1. Set the Future Failure State

**Technique: Prospective Hindsight**

```javascript
async function setFailureScenario(task, timeframe = "completion") {
  const scenario = {
    task: task.description,
    assumedOutcome: "COMPLETE FAILURE",
    timepoint: timeframe,
    prompt: `It is now ${timeframe} and the task has failed spectacularly.
             Nothing works. Users are frustrated. The code is broken.
             Time and resources were wasted.`
  };

  return scenario;
}
```

**Example:**
```
Task: Implement user authentication system

Pre-mortem scenario:
"It is now 3 months from now. The authentication system has failed completely.
Users cannot log in. Sessions are broken. Security vulnerabilities exist.
The team has spent weeks debugging. Customer trust is damaged."
```

### 2. Generate Failure Causes

**Brainstorm what led to failure (in parallel for 6x speedup):**

```javascript
// Category-specific generation functions
async function generateTechnicalCauses(scenario) {
  // Analyze technical architecture, dependencies, implementation
  return [
    "Database not properly configured",
    "Third-party OAuth provider rate limits hit",
    "Password hashing algorithm too slow, timeouts",
    "Session storage fills up, memory leak",
    "CSRF tokens not properly validated",
    "Cookie security flags missing"
  ];
}

async function generateProcessCauses(scenario) {
  // Analyze workflow, methodology, testing practices
  return [
    "No testing of edge cases (expired tokens, concurrent logins)",
    "Security audit skipped due to time pressure",
    "No load testing performed",
    "Migration plan for existing users inadequate"
  ];
}

async function generateAssumptionCauses(scenario) {
  // Identify unverified beliefs and invalid assumptions
  return [
    "Assumed third-party library was secure (it had CVE)",
    "Thought existing database could handle sessions (it couldn't)",
    "Believed users would accept password requirements (too strict)",
    "Expected 1000 users, got 10,000 on day one"
  ];
}

async function generateExternalCauses(scenario) {
  // Consider dependencies, third-party services, environment
  return [
    "OAuth provider changed their API without notice",
    "Regulatory requirements changed (GDPR, password rules)",
    "DDoS attack overwhelmed auth endpoints",
    "Browser updates broke session handling"
  ];
}

async function generateCommunicationCauses(scenario) {
  // Assess clarity, stakeholder alignment, documentation
  return [
    "Frontend team didn't understand token refresh flow",
    "Security requirements not clearly documented",
    "User support not trained on auth issues",
    "Migration communication to users failed"
  ];
}

async function generateScopeCauses(scenario) {
  // Evaluate scope creep, missing requirements, underestimation
  return [
    "Scope creep: Added SSO, 2FA, biometrics mid-project",
    "Underestimated complexity of password reset flow",
    "Didn't account for multi-device sessions",
    "Forgot about API authentication for mobile app"
  ];
}

async function generateFailureCauses(scenario, context) {
  // Generate all categories in parallel (6x speedup: 25ms vs 150ms)
  const [technical, process, assumptions, external, communication, scope] =
    await Promise.all([
      generateTechnicalCauses(scenario),      // 25ms
      generateProcessCauses(scenario),        // 25ms
      generateAssumptionCauses(scenario),     // 25ms
      generateExternalCauses(scenario),       // 25ms
      generateCommunicationCauses(scenario),  // 25ms
      generateScopeCauses(scenario)           // 25ms
    ]);

  // Aggregate results
  return {
    technical,
    process,
    assumptions,
    external,
    communication,
    scope
  };
}
```

### 3. Assign Likelihood and Impact

**Prioritize risks:**

```javascript
function assessRisks(failureCauses) {
  const assessedRisks = [];

  failureCauses.forEach(cause => {
    const risk = {
      cause,
      likelihood: calculateLikelihood(cause),  // 1-5
      impact: calculateImpact(cause),          // 1-5
      riskScore: 0
    };

    risk.riskScore = risk.likelihood * risk.impact;
    assessedRisks.push(risk);
  });

  // Sort by risk score (highest first)
  return assessedRisks.sort((a, b) => b.riskScore - a.riskScore);
}

function calculateLikelihood(cause) {
  // Based on historical data, project context, complexity
  const indicators = {
    hasHappenedBefore: +2,
    highComplexity: +2,
    externalDependency: +1,
    tightTimeline: +1,
    newTechnology: +1
  };

  // Return 1-5 scale
  return Math.min(5, Object.values(indicators).reduce((a, b) => a + b, 1));
}

function calculateImpact(cause) {
  // Based on severity if failure occurs
  const severity = {
    dataLoss: 5,
    securityBreach: 5,
    serviceDown: 4,
    userFrustration: 3,
    performanceDeg: 2,
    minorBug: 1
  };

  // Match cause to severity
  return determineSeverity(cause, severity);
}
```

### 4. Develop Preventive Measures

**For each high-risk item:**

```javascript
async function developPreventiveMeasures(risks) {
  const measures = [];

  for (const risk of risks.filter(r => r.riskScore >= 12)) {
    const prevention = {
      risk: risk.cause,
      riskScore: risk.riskScore,
      preventions: [],
      detections: [],
      mitigations: []
    };

    // Preventions: Stop it from happening
    prevention.preventions = generatePreventions(risk);

    // Detections: Notice if it's happening
    prevention.detections = generateDetections(risk);

    // Mitigations: Reduce impact if it happens
    prevention.mitigations = generateMitigations(risk);

    measures.push(prevention);
  }

  return measures;
}

function generatePreventions(risk) {
  // Example for "Third-party OAuth rate limits"
  return [
    {
      action: "Add caching layer for OAuth tokens",
      effort: "medium",
      effectiveness: "high"
    },
    {
      action: "Implement exponential backoff",
      effort: "low",
      effectiveness: "medium"
    },
    {
      action: "Set up rate limit monitoring in dev/staging",
      effort: "low",
      effectiveness: "high"
    },
    {
      action: "Use OAuth refresh tokens properly",
      effort: "medium",
      effectiveness: "high"
    }
  ];
}

function generateDetections(risk) {
  // How to detect if this is starting to happen
  return [
    {
      metric: "OAuth API response time > 2s",
      alert: "Slack + PagerDuty",
      threshold: "5 occurrences in 10 minutes"
    },
    {
      metric: "401 errors spike",
      alert: "Dashboard + email",
      threshold: "> 5% of requests"
    }
  ];
}

function generateMitigations(risk) {
  // Reduce damage if it happens
  return [
    {
      action: "Fallback to local session store",
      triggerCondition: "OAuth provider down > 5 min",
      recoveryTime: "automatic"
    },
    {
      action: "Display user-friendly error message",
      triggerCondition: "Authentication fails",
      recoveryTime: "immediate"
    },
    {
      action: "Queue authentication requests",
      triggerCondition: "Rate limit hit",
      recoveryTime: "gradual (backlog processes)"
    }
  ];
}
```

### 5. Create Pre-Mortem Report

**Document findings:**

```javascript
async function generatePreMortemReport(task, risks, measures) {
  const report = {
    task: task.description,
    date: new Date().toISOString(),
    summary: {
      totalRisksIdentified: risks.length,
      highRisks: risks.filter(r => r.riskScore >= 15).length,
      mediumRisks: risks.filter(r => r.riskScore >= 9).length,
      lowRisks: risks.filter(r => r.riskScore < 9).length
    },
    topRisks: risks.slice(0, 5),
    preventiveMeasures: measures,
    goNoGoRecommendation: assessGoNoGo(risks, measures)
  };

  // Save to .corpus/pre-mortems/
  await savePreMortem(report);

  return report;
}

function assessGoNoGo(risks, measures) {
  const criticalRisks = risks.filter(r => r.riskScore >= 20);

  if (criticalRisks.length === 0) {
    return {
      decision: "GO",
      confidence: "high",
      reasoning: "No critical risks identified"
    };
  }

  const mitigatedCritical = criticalRisks.filter(r =>
    measures.some(m => m.risk === r.cause && m.preventions.length > 0)
  );

  if (mitigatedCritical.length === criticalRisks.length) {
    return {
      decision: "GO WITH CAUTION",
      confidence: "medium",
      reasoning: `${criticalRisks.length} critical risks, all have preventions`,
      conditions: measures.map(m => m.preventions).flat()
    };
  }

  return {
    decision: "NO GO / REVISE PLAN",
    confidence: "high",
    reasoning: `${criticalRisks.length - mitigatedCritical.length} critical risks unaddressed`,
    unblockers: criticalRisks.filter(r =>
      !mitigatedCritical.includes(r)
    )
  };
}
```

---

## Integration with Workflow

### Before Starting Tasks

**Automatic pre-mortem for complex tasks:**

```javascript
async function shouldRunPreMortem(task) {
  const triggers = {
    multiStep: task.steps?.length > 5,
    highComplexity: task.complexity === 'high',
    architecturalChange: task.type === 'architecture',
    newTechnology: task.involves?.newTech,
    criticalPath: task.blocking?.length > 0,
    userFacing: task.userImpact === 'high'
  };

  return Object.values(triggers).some(t => t);
}

// Before task execution
async function executeTaskWithPreMortem(task) {
  if (await shouldRunPreMortem(task)) {
    console.log("Running pre-mortem analysis...");
    const preMortem = await runPreMortem(task);

    if (preMortem.goNoGo.decision === "NO GO / REVISE PLAN") {
      console.log("⚠️ Pre-mortem recommends revising plan");
      console.log(preMortem.goNoGo.reasoning);
      return { status: "blocked", preMortem };
    }

    // Add preventive measures to task plan
    task.preventiveMeasures = preMortem.preventiveMeasures;
  }

  // Continue with task
  return await executeTask(task);
}
```

### Integration with Convergence

**Add pre-mortem to Phase 1:**

```json
{
  "convergence": {
    "phase1": {
      "gate": {
        "steps": [
          "1. Run pre-mortem analysis",
          "2. Implement high-priority preventions",
          "3. Set up detection mechanisms",
          "4. Run audits",
          "5. Fix issues",
          "6. Verify 3 clean passes"
        ]
      }
    }
  }
}
```

---

## Storage and Retrieval

**Pre-mortem library:**

```javascript
// Store for future reference
const preMortemPath = '.corpus/learning/pre-mortems';

async function savePreMortem(report) {
  const filename = `${report.task.slug}-${Date.now()}.json`;
  const filepath = path.join(preMortemPath, filename);

  await fs.writeFile(filepath, JSON.stringify(report, null, 2));

  // Also update index
  await updatePreMortemIndex(report);
}

// Retrieve similar pre-mortems
async function findSimilarPreMortems(task) {
  const index = await loadPreMortemIndex();

  const similar = index.filter(pm =>
    pm.taskType === task.type ||
    pm.technologies.some(t => task.technologies?.includes(t)) ||
    pm.domain === task.domain
  );

  return similar;
}

// Learn from past pre-mortems
async function applyLearningsFromPast(task) {
  const similarPreMortems = await findSimilarPreMortems(task);

  const commonRisks = identifyCommonRisks(similarPreMortems);
  const effectivePreventions = identifyEffectivePreventions(similarPreMortems);

  return {
    suggestedRisks: commonRisks,
    provenPreventions: effectivePreventions
  };
}
```

---

## Output Format

```json
{
  "preMortemReport": {
    "task": "Implement user authentication",
    "date": "2026-02-04T10:00:00Z",
    "summary": {
      "totalRisks": 24,
      "highRisks": 5,
      "mediumRisks": 12,
      "lowRisks": 7
    },
    "topRisks": [
      {
        "cause": "OAuth provider rate limits hit",
        "likelihood": 4,
        "impact": 5,
        "riskScore": 20,
        "category": "external"
      }
    ],
    "preventiveMeasures": [
      {
        "risk": "OAuth provider rate limits hit",
        "preventions": [
          {
            "action": "Add caching layer",
            "effort": "medium",
            "effectiveness": "high"
          }
        ],
        "detections": [
          {
            "metric": "OAuth response time > 2s",
            "alert": "PagerDuty"
          }
        ]
      }
    ],
    "goNoGo": {
      "decision": "GO WITH CAUTION",
      "confidence": "medium",
      "conditions": ["Implement OAuth caching", "Set up monitoring"]
    }
  }
}
```

---

## Quick Reference

**Run pre-mortem:**
```javascript
const preMortem = await runPreMortem({
  description: "Implement user authentication",
  complexity: "high",
  type: "feature"
});
```

**Apply learnings:**
```javascript
const insights = await applyLearningsFromPast(task);
console.log("Common risks from similar tasks:", insights.suggestedRisks);
```

---

*End of Pre-Mortem Analysis*
*Part of v4.0.0 Universal Skills Ecosystem*
*Category: Learning (Proactive Risk Management)*
*Builds institutional memory through failure anticipation*
