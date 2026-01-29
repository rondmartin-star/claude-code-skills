# Framework Context Skill

## Purpose

Provides consistent access to America 4.0 framework canonical definitions, ensuring all skills reference the authoritative sources for principles, roles, and key terms.

## Canonical Sources

### Primary Documents

```
G:\My Drive\Projects\America 4.0\03-specifications\v1.0\
├── america40.comprehensive-framework-synthesis-streamlined.md  # 7 Principles
├── america40.stakeholder-roles.md                              # 14 Roles
└── core-specification.md                                       # Full spec
```

### Style and Voice

```
G:\My Drive\Projects\America 4.0\04-marketing\messaging\
├── america40-style-guide.md
└── america40-content-strategy.md
```

## The Seven Principles

| # | Principle | Core Concept |
|---|-----------|--------------|
| 1 | Human Dignity and Inclusion | Equal worth, diversity as resource |
| 2 | Social and Ecological Interconnection | Complex relational webs, stewardship |
| 3 | Economic Justice and Opportunity | Reward aligned with contribution |
| 4 | Democratic Governance and Rule of Law | Equal application regardless of power |
| 5 | Global Citizenship and Leadership | Interconnected world participation |
| 6 | Creative and Cultural Flourishing | Cultural resources for democratic imagination |
| 7 | Evidence-Based Decision Making | Rigorous evidence + inclusive deliberation |

## The Fourteen Stakeholder Roles

| Role | Function |
|------|----------|
| Citizen | Democratic participation and voice |
| Representative | Elected governance on behalf of constituents |
| Expert | Technical knowledge and evidence provision |
| Educator | Knowledge transmission and civic learning |
| Facilitator | Process design and neutral moderation |
| Democracy Auditor | Distributed accountability function |
| Communicator | Information synthesis and distribution |
| Contributor | Resource and effort provision |
| Community Builder | Social fabric cultivation |
| Bridge Builder | Cross-boundary connection |
| Cultural Creator | Narrative and meaning-making |
| Protector | Rights and institution defense |
| Systems Designer | Structure and process architecture |
| Implementer | Operational execution |

## Key Terms and Concepts

### Variable Geometry
Principles are immutable; implementation varies by context, scale, and domain.

### Attractor Theory
Elite governance is a structural attractor requiring continuous countervailing energy.

### Curated Failure
Deliberate creation of small-scale, recoverable failures to stress-test systems.

### Democracy Auditor
Distributed accountability function with anti-capture design (sortition, rotation, federated oversight).

### Historical Epochs
- **America 1.0** (1787): Constitutional Convention, federal/state balance
- **America 2.0** (1865-1870): Civil War amendments, expanded participation
- **America 3.0** (Progressive/New Deal): Individual vs. corporate power balance
- **America 4.0** (Current): Interconnectedness vs. individualism in networked world

## Voice Guidelines

### Use This Language
- "Democratic renewal" (not "saving democracy")
- "Civic engagement" (not "political activism")
- "Democratic evolution" (not "revolution")
- "Equal dignity" (not just "equality")
- "Shared purpose" (not "unity")
- "Evidence-based governance" (not "expert rule")

### Brand Attributes
- **Evolutionary** not revolutionary
- **Integrative** not partisan
- **Practical** not merely theoretical
- **Hopeful** but realistic
- **Accessible** without sacrificing depth

### Avoid
- Partisan framing that creates tribal sorting
- Academic jargon creating barriers
- Conspiratorial thinking
- Fatalistic language
- Technocratic solutions ignoring politics
- Uncritical nationalism or cynical dismissal

## Loading Context

When a skill needs framework context:

```javascript
// Load principles
const principles = await loadDocument('03-specifications/v1.0/america40.comprehensive-framework-synthesis-streamlined.md');

// Load roles
const roles = await loadDocument('03-specifications/v1.0/america40.stakeholder-roles.md');

// Load style guide
const style = await loadDocument('04-marketing/messaging/america40-style-guide.md');
```

## Validation

All generated content should be validated against:
1. Does it align with one or more of the 7 principles?
2. Does it use appropriate stakeholder role language?
3. Does it follow voice guidelines (bridge-building, practical idealism)?
4. Does it avoid partisan framing?
5. Does it maintain factual accuracy and avoid unsubstantiated claims?
