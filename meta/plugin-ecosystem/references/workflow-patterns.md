# Plugin + Skill Workflow Patterns

Detailed patterns for combining plugins and skills effectively.

---

## Pattern 1: Complete Feature Development

**Scenario:** Building a new feature from scratch

### Phase 1: Requirements (Skill)
```
Load skill: windows-app-requirements
"Help me define requirements for [feature]"
```

### Phase 2: UI Design (Skill + Plugin)
```
Load skill: windows-app-ui-design
# For frontend-heavy features:
Load plugin skill: frontend-design
```

### Phase 3: System Design (Skill)
```
Load skill: windows-app-system-design
"Design the architecture for [feature]"
```

### Phase 4: Implementation (Plugin Workflow)
```
/feature-dev [feature description]
```

This runs the 7-phase feature-dev workflow:
1. Discovery
2. Codebase Exploration (launches code-explorer agents)
3. Clarifying Questions
4. Architecture Design (launches code-architect agents)
5. Implementation
6. Quality Review (launches code-reviewer agents)
7. Summary

### Phase 5: Simplification (Plugin Agent)
```
Task(subagent_type="code-simplifier:code-simplifier",
     prompt="Simplify the [feature] implementation")
```

### Phase 6: Review (Plugin)
```
/code-review
```

Or for thorough review:
```
"Run pr-test-analyzer, silent-failure-hunter, and code-reviewer"
```

### Phase 7: Commit (Plugin)
```
/commit-push-pr
```

---

## Pattern 2: Quick Code Quality Check

**Scenario:** Just finished coding, want quick feedback

### Option A: Single Agent
```
Task(subagent_type="code-review:code-review",
     prompt="Review changes in the last commit")
```

### Option B: Targeted Review
```
"Check for silent failures in the error handling"
→ Triggers: silent-failure-hunter

"Check if tests are thorough"
→ Triggers: pr-test-analyzer

"Check if comments are accurate"
→ Triggers: comment-analyzer
```

### Option C: Full PR Review
```
/code-review
```

---

## Pattern 3: Code Cleanup Sprint

**Scenario:** Code works but needs polish

### Step 1: Identify Complexity
```
Task(subagent_type="code-simplifier:code-simplifier",
     prompt="Analyze [module] for simplification opportunities")
```

### Step 2: Apply Simplifications
Agent automatically:
- Removes duplicate code
- Consolidates related logic
- Improves naming
- Reduces nesting
- Follows project standards

### Step 3: Verify
```
"Review my changes"
→ Triggers: code-reviewer
```

---

## Pattern 4: Security-First Development

**Scenario:** Building security-sensitive features

### Step 1: Load Security Skill
```
Load skill: secure-coding-patterns
```

### Step 2: Enable Security Plugin
security-guidance plugin automatically warns about:
- Command injection
- XSS vulnerabilities
- SQL injection
- Unsafe patterns

### Step 3: Implementation with Guards
Use windows-app-build skill which includes:
- Input validation patterns
- Output encoding
- Parameterized queries
- Safe file handling

### Step 4: Security Review
```
"Check for security issues in [files]"
```

---

## Pattern 5: Exploratory Development

**Scenario:** Need to understand codebase before changes

### Option A: Feature-Dev Exploration Phases
```
/feature-dev [feature]
# Let it run through Discovery and Exploration phases
# Answer clarifying questions
# Review architecture options
```

### Option B: Direct Exploration
```
Task(subagent_type="Explore",
     prompt="How does [feature] work in this codebase?")
```

### Option C: Code Explorer Agent
```
"Launch code-explorer to trace how [feature] works"
```

---

## Pattern 6: Test Coverage Improvement

**Scenario:** Tests exist but may have gaps

### Step 1: Analyze Coverage
```
"Check if tests are thorough"
→ Triggers: pr-test-analyzer
```

Agent analyzes:
- Behavioral vs line coverage
- Critical gaps
- Edge cases
- Error conditions

### Step 2: Review Findings
Agent returns:
- Gap severity ratings (1-10)
- Specific missing tests
- Priority recommendations

### Step 3: Add Tests
Implement based on recommendations

### Step 4: Re-verify
```
"Check test coverage again"
```

---

## Pattern 7: Type System Review

**Scenario:** Added new types, want design review

### Trigger Type Analyzer
```
"Review the [TypeName] type design"
→ Triggers: type-design-analyzer
```

Agent rates (1-10):
- Type encapsulation
- Invariant expression
- Type usefulness
- Invariant enforcement

### Review and Iterate
Based on ratings, improve:
- Low encapsulation → Add private fields
- Low invariants → Add validation
- Low usefulness → Reconsider API

---

## Pattern 8: Comment Maintenance

**Scenario:** Major refactoring, comments may be stale

### Analyze Comments
```
"Check if comments are accurate"
→ Triggers: comment-analyzer
```

Agent checks:
- Comment accuracy vs code
- Documentation completeness
- Comment rot
- Misleading info

### Fix Issues
Update based on findings:
- Remove outdated comments
- Fix inaccurate descriptions
- Add missing documentation

---

## Pattern 9: Error Handling Audit

**Scenario:** Ensure robust error handling

### Hunt Silent Failures
```
"Check for silent failures"
→ Triggers: silent-failure-hunter
```

Agent finds:
- Silent catch blocks
- Inadequate error handling
- Bad fallback behavior
- Missing logging

### Fix Patterns
Common fixes:
- Add error logging
- Propagate important errors
- Remove silent swallows
- Add user feedback

---

## Pattern 10: Pre-PR Checklist

**Scenario:** About to create PR, need comprehensive check

### Run All Relevant Agents
```
"I'm ready to create this PR. Please:
1. Review test coverage
2. Check for silent failures
3. Verify comments are accurate
4. Review any new types
5. General code review
6. Simplify if needed"
```

### Commit Workflow
After all checks pass:
```
/commit-push-pr
```

This:
1. Stages changes
2. Creates commit
3. Pushes to remote
4. Creates pull request

---

## Anti-Patterns to Avoid

### Don't: Skip Exploration
```
# Bad: Jump straight to coding
"Implement [complex feature]"

# Good: Use feature-dev workflow
/feature-dev [complex feature]
```

### Don't: Over-Review Simple Changes
```
# Bad: Full PR review for typo fix
/code-review  # For one-line fix

# Good: Just commit
/commit
```

### Don't: Ignore Agent Recommendations
```
# Bad: Dismiss all findings
"Proceed anyway"

# Good: Address or consciously defer
"Fix the critical issues now, defer medium priority"
```

### Don't: Run Agents on Entire Codebase
```
# Bad: Review everything
"Review all code in the project"

# Good: Focus on changes
"Review my recent changes"
"Review changes in the last commit"
```

---

*End of Workflow Patterns*
