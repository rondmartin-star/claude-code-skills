---
name: windows-app-requirements
description: >
  Capture user intentions through structured requirements gathering. Produces
  user stories with acceptance criteria, prioritized feature lists, and 
  non-functional requirements. Use when: "I want to build...", "I need an app
  that...", "help me define requirements", "write user stories".
---

# Windows Application Requirements Skill

**Purpose:** Transform vague notions into clear, testable requirements  
**Output:** User stories, acceptance criteria, prioritized features, NFRs  
**Size:** ~8 KB  
**Related Skills:** windows-app-system-design (next), windows-app-ui-design

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "I want to build an app that..."
- "I need a system that..."
- "What should the application do?"
- "Help me define requirements"
- "Write user stories for..."
- "What features do I need?"
- "Let's plan a new application"

**Context Indicators:**
- User describes a problem without a solution
- No existing code or package mentioned
- Discussion is about "what" not "how"
- Starting a brand new project

## ❌ DO NOT LOAD WHEN

- User has existing code/package (use build skill)
- User is asking about data model (use system-design skill)
- User is asking about UI/screens (use ui-design skill)
- User wants to fix a bug (use build skill)

---

## When to Use This Skill

| User Says... | Action |
|--------------|--------|
| "I want to build..." | Start requirements discovery |
| "I need an app that..." | Start requirements discovery |
| "Help me define what I need" | Requirements gathering |
| "Write user stories for..." | Skip to Step 4 |
| "What should the requirements include?" | Explain process |

---

## Discovery Process

### Step 1: Understand the Problem

**Questions to Ask:**

1. What problem does this solve?
2. What happens today without this system? (Pain points)
3. What would success look like?
4. Who asked for this / who will benefit?

**Capture Format:**

```markdown
## Problem Statement

**Current State:** [How things work now]
**Pain Points:** [What's wrong with the current state]
**Desired State:** [What the user wants instead]
**Success Criteria:** [How we'll know it's working]
```

### Step 2: Identify Users and Roles

**Questions to Ask:**

1. Who will use this system?
2. Are there different types of users with different permissions?
3. Who can see what? Who can change what?
4. Is there an administrator role?

**Common Role Patterns:**

| Pattern | Roles | Use When |
|---------|-------|----------|
| Single User | User | Personal tool, one person |
| Admin + Users | Admin, User | Shared tool, someone manages it |
| Multi-Role | Admin, Manager, User | Different permission levels needed |
| Public + Private | Anonymous, Authenticated | Some content is public |

**Role Documentation Format:**

```markdown
## User Roles

### [Role Name]
- **Description:** [Who this is]
- **Can View:** [What they see]
- **Can Edit:** [What they change]
- **Can Delete:** [What they remove]
- **Special Abilities:** [Unique permissions]
```

### Step 3: Define Core Capabilities

**Questions to Ask:**

1. What's the ONE thing this system must do? (Core action)
2. What are the main things users will do? (Primary workflows)
3. What information do users need to see? (Views/reports)
4. What triggers actions? (User clicks, schedules, events)

**Prioritization Framework:**

| Priority | Meaning | Criteria |
|----------|---------|----------|
| P0 - Critical | Must have for v1.0 | System is useless without it |
| P1 - High | Should have for v1.0 | Significant value, not blocking |
| P2 - Medium | Nice to have | Can wait for v1.1+ |
| P3 - Low | Future consideration | Good idea, not now |

### Step 4: Write User Stories

**User Story Template:**

```markdown
## US-[XXX]: [Brief Title]

**Priority:** P0/P1/P2/P3

As a [role],
I want to [action],
so that [value/benefit].

### Acceptance Criteria

**Given** [precondition]
**When** [action taken]
**Then** [expected result]

### Notes
- [Additional context]
- [Edge cases to consider]
- [Related stories: US-XXX]
```

**Example User Story:**

```markdown
## US-001: User Login

**Priority:** P0

As a user,
I want to log in with my username and password,
so that I can access my personal data securely.

### Acceptance Criteria

**Given** I am on the login page
**When** I enter valid credentials and click Login
**Then** I am redirected to the dashboard

**Given** I am on the login page
**When** I enter invalid credentials and click Login
**Then** I see an error message and remain on the login page

**Given** I am already logged in
**When** I navigate to the login page
**Then** I am redirected to the dashboard

### Notes
- Password must be at least 8 characters
- Lock account after 5 failed attempts (P2)
- Related: US-002 (Logout), US-003 (Password Reset)
```

### Step 5: Define Non-Functional Requirements

**Categories to Consider:**

**Performance:**
- How many users will use this simultaneously?
- How much data will be stored?
- What response time is acceptable?

**Security:**
- What data is sensitive?
- Who should NOT be able to see what?
- Are there compliance requirements?

**Usability:**
- Who are the users? (Technical level)
- What devices will they use?
- Accessibility requirements?

**Deployment:**
- Where will this run? (Desktop, server, cloud)
- Who will install and maintain it?
- How will updates be delivered?

**NFR Template:**

```markdown
## Non-Functional Requirements

### Performance
- NFR-P01: Page load time < 2 seconds
- NFR-P02: Support up to [X] concurrent users
- NFR-P03: Database can grow to [X] records

### Security
- NFR-S01: All passwords hashed with salt
- NFR-S02: Session expires after [X] minutes of inactivity
- NFR-S03: [Sensitive data] encrypted at rest

### Usability
- NFR-U01: Works in Chrome, Edge, Firefox
- NFR-U02: Responsive design for tablet and desktop
- NFR-U03: All actions have visual feedback

### Deployment
- NFR-D01: Single-click installation on Windows 10/11
- NFR-D02: No administrator rights required for basic install
- NFR-D03: Updates preserve user data
```

### Step 6: Write Acceptance Test Outlines

**Acceptance Test Template:**

```markdown
## AT-[XXX]: [Test Name]

**Verifies:** US-[XXX]
**Type:** Manual / Automated

### Preconditions
- [Setup required before test]

### Test Steps
1. [Action 1]
2. [Action 2]
3. [Action 3]

### Expected Results
- [What should happen]

### Test Data
- [Specific data needed for test]
```

---

## Phase 1 Deliverables Checklist

Before proceeding to System Design (Phase 2):

- [ ] Problem statement documented
- [ ] All user roles identified with permissions
- [ ] All user stories written with acceptance criteria
- [ ] Stories prioritized (P0/P1/P2/P3)
- [ ] P0 stories are truly essential for v1.0
- [ ] Non-functional requirements documented
- [ ] Acceptance test outlines created for P0 stories
- [ ] User has reviewed and approved requirements

### Cross-Skill Validation

Before transitioning to **windows-app-system-design**:
- [ ] Each user story identifies data it creates/reads/updates/deletes
- [ ] User roles are clear enough to map to permissions
- [ ] NFRs specify authentication requirements
- [ ] NFRs specify data retention/backup requirements

**If any item fails:** Resolve before loading system-design skill.

---

## Exit Gate Questions

Ask the user:

1. "Do these user stories capture what you want to build?"
2. "Is the prioritization correct - are P0 items truly essential?"
3. "Are there any scenarios or edge cases we missed?"
4. "Do the acceptance criteria clearly define 'done'?"

**When user confirms → Proceed to windows-app-system-design skill**

---

## Common Patterns to Listen For

| User Says... | Implies... |
|--------------|------------|
| "Track" / "Log" / "Record" | CRUD operations, history |
| "Categorize" / "Group" / "Filter" | Categories, tags, relationships |
| "Report" / "Summary" / "Dashboard" | Aggregation, views, charts |
| "Assign" / "Belongs to" | Ownership, relationships |
| "Approve" / "Review" / "Status" | Workflow, state machine |
| "Schedule" / "Remind" / "Due date" | Time-based features |
| "Import" / "Export" / "Sync" | Integration, file handling |
| "Only I should see" / "Share with" | Authorization, permissions |

---

## Red Flags to Address

| Red Flag | Risk | Resolution |
|----------|------|------------|
| "And it should also..." (scope creep) | Never-ending project | Prioritize, defer to P2/P3 |
| "Like [complex product]" | Unrealistic expectations | Identify essential subset |
| No clear user role | Authorization confusion | Define roles explicitly |
| "It needs to be perfect" | Analysis paralysis | Start with MVP, iterate |
| Conflicting requirements | Design deadlock | Clarify with stakeholder |
| Single location/venue assumed | Breaks when scaled | Ask "Will there be multiple [X]?" |
| No mention of data boundaries | Multi-tenant issues | Clarify ownership/isolation |

### Critical Question: Multi-Tenant Design

**Always ask early in requirements:**

> "Will there ever be multiple [venues/locations/organizations/accounts] using this system? Even if starting with one, should we design for multiple?"

**Why this matters:**
- Single-tenant designs are expensive to retrofit
- Database queries that assume `.first()` break with multiple entities
- UI that shows "the venue" instead of "select venue" confuses users
- API endpoints need entity IDs, not assumptions

**If multi-tenant is possible:**
- Add to NFRs: "System must support multiple [entities]"
- Every user story should clarify which entity it operates on
- Data model must include proper foreign keys for isolation

---

## Requirements Document Template

```markdown
# [Application Name] Requirements

## 1. Overview
[2-3 sentence description of what the application does]

## 2. Problem Statement
**Current State:** ...
**Pain Points:** ...
**Desired State:** ...
**Success Criteria:** ...

## 3. User Roles
### 3.1 Admin
- Description: ...
- Permissions: ...

### 3.2 User
- Description: ...
- Permissions: ...

## 4. User Stories

### P0 - Critical (v1.0 Required)
[List P0 user stories]

### P1 - High (v1.0 Target)
[List P1 user stories]

### P2 - Medium (v1.1+)
[List P2 user stories]

### P3 - Low (Future)
[List P3 user stories]

## 5. Non-Functional Requirements
[NFRs organized by category]

## 6. Acceptance Test Outlines
[Test outlines for P0 stories]

## 7. Approval
- [ ] Stakeholder reviewed
- [ ] Prioritization confirmed
- [ ] Ready for design phase
```

---

*End of Windows Application Requirements Skill*
