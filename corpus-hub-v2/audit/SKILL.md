# CorpusHub Traceability Audit

## Purpose
Comprehensive bidirectional traceability verification across the entire software development lifecycle. Verifies completeness, identifies gaps, and validates consistency between requirements, design, implementation, tests, documentation, security, and operations.

## Core Audit Capabilities

### 1. Requirements Traceability

#### Forward Traceability (Requirements → Implementation)
```
GET /api/ontology/traverse?from={requirementId}&relationship=implements&depth=3

Verifies:
- Every requirement has at least one implementation
- Implementation is tested
- Tests validate the original requirement (loop closure)
```

**Example Audit:**
```javascript
// For each requirement, verify implementation chain
const requirements = await getAllBits({ type: 'requirement' });

for (const req of requirements) {
  // Find implementations
  const implementations = await traverse(req.id, 'implements', 2);

  if (implementations.length === 0) {
    report.gaps.push({
      type: 'unimplemented-requirement',
      requirement: req.id,
      severity: 'high'
    });
  }

  // For each implementation, verify tests exist
  for (const impl of implementations) {
    const tests = await getIncomingEdges(impl.id, 'tests');

    if (tests.length === 0) {
      report.gaps.push({
        type: 'untested-implementation',
        implementation: impl.id,
        requirement: req.id,
        severity: 'high'
      });
    }

    // Verify tests validate the requirement (loop closure)
    for (const test of tests) {
      const validatedReqs = await getOutgoingEdges(test.source_bit_id, 'validates');

      if (!validatedReqs.find(e => e.target_bit_id === req.id)) {
        report.warnings.push({
          type: 'test-requirement-gap',
          test: test.source_bit_id,
          implementation: impl.id,
          requirement: req.id,
          message: 'Test tests implementation but does not explicitly validate requirement'
        });
      }
    }
  }
}
```

#### Backward Traceability (Implementation → Requirements)
```
GET /api/ontology/traverse?from={implementationId}&relationship=implements&depth=3&direction=incoming

Verifies:
- Every implementation traces back to a requirement
- No orphaned code
- Implementation addresses documented needs
```

**Example Audit:**
```javascript
// For each implementation, verify requirement exists
const implementations = await getAllBits({ type: 'implementation' });

for (const impl of implementations) {
  // Find requirements this implements
  const requirements = await getOutgoingEdges(impl.id, 'implements');

  if (requirements.length === 0) {
    report.warnings.push({
      type: 'orphaned-implementation',
      implementation: impl.id,
      severity: 'medium',
      message: 'Implementation exists without documented requirement'
    });
  }
}
```

### 2. Test Coverage Audit

#### Implementation Test Coverage
```javascript
// Verify all implementations have test coverage
const implementations = await getAllBits({
  type: ['implementation', 'code-module', 'code-function', 'code-class']
});

const coverageReport = {
  total: implementations.length,
  tested: 0,
  untested: [],
  coverage: {}
};

for (const impl of implementations) {
  const tests = await getIncomingEdges(impl.id, 'tests');
  const testCases = await getIncomingEdges(impl.id, 'covers');

  const allTests = [...tests, ...testCases];

  if (allTests.length > 0) {
    coverageReport.tested++;
    coverageReport.coverage[impl.id] = {
      testCount: allTests.length,
      tests: allTests.map(t => t.source_bit_id)
    };
  } else {
    coverageReport.untested.push({
      id: impl.id,
      title: impl.title,
      severity: 'high'
    });
  }
}

coverageReport.percentage = (coverageReport.tested / coverageReport.total) * 100;
```

#### Requirement Validation Coverage
```javascript
// Verify all requirements have validating tests
const requirements = await getAllBits({ type: 'requirement' });

for (const req of requirements) {
  const validatingTests = await getIncomingEdges(req.id, 'validates');

  if (validatingTests.length === 0) {
    report.gaps.push({
      type: 'unvalidated-requirement',
      requirement: req.id,
      severity: 'high',
      message: 'Requirement has no validating tests'
    });
  }
}
```

### 3. User Story → Workflow → Implementation Chain

```javascript
// Verify user stories flow through workflows to implementation
const userStories = await getAllBits({ type: 'user-story' });

for (const story of userStories) {
  // Check if story has associated workflows
  const workflows = await getIncomingEdges(story.id, 'fulfills');

  if (workflows.length === 0) {
    report.gaps.push({
      type: 'story-without-workflow',
      story: story.id,
      severity: 'medium'
    });
    continue;
  }

  // For each workflow, verify implementation exists
  for (const workflow of workflows) {
    const implementations = await getIncomingEdges(workflow.source_bit_id, 'implements');

    if (implementations.length === 0) {
      report.gaps.push({
        type: 'workflow-without-implementation',
        workflow: workflow.source_bit_id,
        story: story.id,
        severity: 'high'
      });
    }

    // Verify workflow is tested via use cases
    const useCases = await getIncomingEdges(workflow.source_bit_id, 'describes');
    const testScenarios = await getIncomingEdges(workflow.source_bit_id, 'validates');

    if (useCases.length === 0 && testScenarios.length === 0) {
      report.warnings.push({
        type: 'workflow-not-tested',
        workflow: workflow.source_bit_id,
        story: story.id,
        severity: 'medium'
      });
    }
  }
}
```

### 4. API Contract Traceability

```javascript
// Verify API specs → implementation → tests → documentation
const apiSpecs = await getAllBits({ type: 'api-spec' });

for (const spec of apiSpecs) {
  const auditResult = {
    spec: spec.id,
    implementation: null,
    tests: [],
    documentation: [],
    issues: []
  };

  // Find implementation
  const implementations = await getIncomingEdges(spec.id, 'implements');
  if (implementations.length === 0) {
    auditResult.issues.push({
      type: 'api-not-implemented',
      severity: 'critical'
    });
  } else {
    auditResult.implementation = implementations[0].source_bit_id;

    // Find tests
    const tests = await getIncomingEdges(auditResult.implementation, 'tests');
    auditResult.tests = tests.map(t => t.source_bit_id);

    if (tests.length === 0) {
      auditResult.issues.push({
        type: 'api-not-tested',
        severity: 'high'
      });
    }
  }

  // Find documentation
  const docs = await getIncomingEdges(spec.id, 'documents');
  auditResult.documentation = docs.map(d => d.source_bit_id);

  if (docs.length === 0) {
    auditResult.issues.push({
      type: 'api-not-documented',
      severity: 'medium'
    });
  }

  report.apiAudit.push(auditResult);
}
```

### 5. Security Traceability

```javascript
// Verify threat model → security controls → implementation
const threats = await getAllBits({ type: 'threat-model' });

for (const threat of threats) {
  // Find mitigating controls
  const controls = await getIncomingEdges(threat.id, 'mitigates');

  if (controls.length === 0) {
    report.security.unmitigated.push({
      threat: threat.id,
      severity: 'critical',
      message: 'Threat has no mitigating controls'
    });
    continue;
  }

  // For each control, verify implementation
  for (const control of controls) {
    const implementations = await getIncomingEdges(control.source_bit_id, 'implements');

    if (implementations.length === 0) {
      report.security.unimplemented.push({
        control: control.source_bit_id,
        threat: threat.id,
        severity: 'high'
      });
    } else {
      // Verify security testing
      for (const impl of implementations) {
        const securityTests = await getIncomingEdges(impl.source_bit_id, 'tests');
        const filtered = securityTests.filter(async (test) => {
          const testBit = await getBitById(test.source_bit_id);
          return testBit.tags && testBit.tags.includes('security');
        });

        if (filtered.length === 0) {
          report.security.warnings.push({
            implementation: impl.source_bit_id,
            control: control.source_bit_id,
            threat: threat.id,
            message: 'Security control implementation not security-tested'
          });
        }
      }
    }
  }
}
```

### 6. Data Model Traceability

```javascript
// Verify data models → implementation → tests
const dataModels = await getAllBits({ type: 'data-model' });

for (const model of dataModels) {
  // Find schema implementations
  const schemas = await getIncomingEdges(model.id, 'implements');

  if (schemas.length === 0) {
    report.data.gaps.push({
      type: 'model-not-implemented',
      model: model.id,
      severity: 'high'
    });
    continue;
  }

  // For each schema, verify validation tests
  for (const schema of schemas) {
    const tests = await getIncomingEdges(schema.source_bit_id, 'validates');

    if (tests.length === 0) {
      report.data.warnings.push({
        type: 'schema-not-validated',
        schema: schema.source_bit_id,
        model: model.id,
        severity: 'medium'
      });
    }
  }
}
```

### 7. Documentation Completeness

```javascript
// Verify all public APIs and modules are documented
const publicBits = await getAllBits({
  type: ['api-spec', 'code-module', 'code-class'],
  tags: 'public'
});

for (const bit of publicBits) {
  const documentation = await getIncomingEdges(bit.id, 'documents');

  if (documentation.length === 0) {
    report.documentation.missing.push({
      bit: bit.id,
      type: bit.bit_type,
      severity: 'medium'
    });
  } else {
    // Verify documentation is current (hash-based)
    const docBit = await getBitById(documentation[0].source_bit_id);
    const bitHash = bit.source_hash || bit.corpus_hash;

    // Check metadata for documented version
    const docMetadata = JSON.parse(docBit.metadata || '{}');
    if (docMetadata.documentedHash !== bitHash) {
      report.documentation.outdated.push({
        bit: bit.id,
        documentation: docBit.id,
        severity: 'low'
      });
    }
  }
}
```

### 8. Dependency Traceability

```javascript
// Verify all external dependencies are documented and monitored
const dependencies = await getAllBits({ type: 'dependency' });

for (const dep of dependencies) {
  const auditResult = {
    dependency: dep.id,
    consumers: [],
    vulnerabilities: [],
    documentation: [],
    issues: []
  };

  // Find what depends on this
  const consumers = await getIncomingEdges(dep.id, 'depends-on');
  auditResult.consumers = consumers.map(c => c.source_bit_id);

  if (consumers.length === 0) {
    auditResult.issues.push({
      type: 'unused-dependency',
      severity: 'low'
    });
  }

  // Find vulnerability reports
  const vulns = await getOutgoingEdges(dep.id, 'threatens');
  auditResult.vulnerabilities = vulns.map(v => v.target_bit_id);

  if (vulns.length > 0) {
    // Verify mitigations exist
    for (const vuln of vulns) {
      const mitigations = await getIncomingEdges(vuln.target_bit_id, 'mitigates');
      if (mitigations.length === 0) {
        auditResult.issues.push({
          type: 'unmitigated-vulnerability',
          vulnerability: vuln.target_bit_id,
          severity: 'critical'
        });
      }
    }
  }

  report.dependencies.push(auditResult);
}
```

### 9. Change Impact Analysis

```javascript
// For a proposed change, analyze full impact via traceability
async function analyzeChangeImpact(changedBitId) {
  const impact = {
    direct: [],
    indirect: [],
    requiresUpdate: [],
    requiresTesting: []
  };

  // Direct dependents
  const directDeps = await getIncomingEdges(changedBitId, null); // All relationships
  impact.direct = directDeps.map(d => ({
    bit: d.source_bit_id,
    relationship: d.relationship
  }));

  // Indirect via implementation chains
  for (const dep of directDeps) {
    const secondOrder = await getIncomingEdges(dep.source_bit_id, null);
    impact.indirect.push(...secondOrder.map(d => ({
      bit: d.source_bit_id,
      via: dep.source_bit_id,
      relationship: d.relationship
    })));
  }

  // Find what needs updating
  const implementers = await getIncomingEdges(changedBitId, 'implements');
  impact.requiresUpdate.push(...implementers.map(i => i.source_bit_id));

  // Find what needs testing
  const testers = await getIncomingEdges(changedBitId, 'tests');
  impact.requiresTesting.push(...testers.map(t => t.source_bit_id));

  // Add tests of implementations
  for (const impl of implementers) {
    const implTests = await getIncomingEdges(impl.source_bit_id, 'tests');
    impact.requiresTesting.push(...implTests.map(t => t.source_bit_id));
  }

  return impact;
}
```

## Audit Reports

### Comprehensive Traceability Report
```
POST /api/audit/traceability/full

Generates complete traceability report:
- Requirements coverage
- Implementation coverage
- Test coverage
- Documentation coverage
- Security coverage
- All gaps and warnings
```

### Gap Analysis Report
```
POST /api/audit/gaps

Identifies all traceability gaps:
- Unimplemented requirements
- Untested implementations
- Unvalidated requirements
- Undocumented APIs
- Unmitigated threats
- Orphaned code
```

### Coverage Metrics
```
GET /api/audit/metrics

Returns quantitative metrics:
- % requirements implemented
- % implementations tested
- % requirements validated
- % APIs documented
- % threats mitigated
- % dependencies monitored
```

## Usage Patterns

### Daily Build Audit
```bash
# Run full traceability audit
POST /api/audit/traceability/full

# Check for critical gaps
GET /api/audit/gaps?severity=critical,high

# Fail build if critical gaps exist
if gaps.length > 0:
  exit 1
```

### Release Readiness Audit
```bash
# Verify all requirements for release
POST /api/audit/release-readiness
{
  "milestone": "v2.0",
  "requirements": ["req-1", "req-2", "req-3"]
}

# Returns:
# - Implementation status
# - Test coverage
# - Documentation status
# - Security audit
# - Known issues
```

### Security Audit
```bash
# Run security-focused audit
POST /api/audit/security

# Returns:
# - Unmitigated threats
# - Unimplemented security controls
# - Security tests needed
# - Vulnerability status
```

### Continuous Monitoring
```bash
# Setup webhook for traceability violations
POST /api/audit/webhooks
{
  "url": "https://slack.com/...",
  "events": ["gap-created", "coverage-decreased"],
  "severity": ["critical", "high"]
}

# Notifies team when:
# - New requirement has no implementation
# - Implementation has no tests
# - Security control removed
# - API changed without documentation update
```

## Integration with CorpusHub Workflows

### On Bit Creation
```javascript
// When new requirement is created, immediately check implementation status
eventBus.on('bit-created', async (bit) => {
  if (bit.type === 'requirement') {
    setTimeout(async () => {
      const implementations = await getIncomingEdges(bit.id, 'implements');
      if (implementations.length === 0) {
        notify({
          type: 'traceability-gap',
          message: `New requirement ${bit.id} has no implementation`,
          severity: 'medium'
        });
      }
    }, 60000); // Check after 1 minute
  }
});
```

### On Bit Update
```javascript
// When requirement changes, verify implementations are updated
eventBus.on('bit-updated', async (bit, changes) => {
  if (bit.type === 'requirement') {
    const impact = await analyzeChangeImpact(bit.id);

    if (impact.requiresUpdate.length > 0 || impact.requiresTesting.length > 0) {
      // Create propagation plan automatically
      await createPropagationPlan({
        sourceBit: bit.id,
        changes,
        impact
      });
    }
  }
});
```

### On Test Run
```javascript
// After test run, update traceability metrics
eventBus.on('test-run-completed', async (testResults) => {
  for (const test of testResults) {
    // Update coverage metrics
    const coveredBits = await getOutgoingEdges(test.id, ['tests', 'validates', 'covers']);

    for (const covered of coveredBits) {
      await updateMetrics(covered.target_bit_id, {
        lastTested: new Date(),
        testStatus: test.passed ? 'passing' : 'failing'
      });
    }
  }

  // Regenerate coverage report
  await generateCoverageReport();
});
```

## Best Practices

1. **Establish Relationships Early**: Create traceability relationships as bits are created, not retroactively
2. **Bidirectional Links**: Always create relationships in both directions (e.g., requirement→implements AND test→validates)
3. **Provenance Tracking**: Tag AI-inferred relationships with confidence scores; verify manually
4. **Continuous Auditing**: Run traceability audits on every commit
5. **Severity Levels**: Classify gaps by severity (critical, high, medium, low)
6. **Automated Notifications**: Alert teams immediately when critical gaps appear
7. **Metrics Dashboard**: Track traceability metrics over time
8. **Release Gates**: Block releases if traceability gaps exist above threshold

## API Endpoints

```
POST   /api/audit/traceability/full              - Full traceability audit
POST   /api/audit/gaps                           - Gap analysis
GET    /api/audit/metrics                        - Coverage metrics
POST   /api/audit/release-readiness              - Release audit
POST   /api/audit/security                       - Security audit
POST   /api/audit/impact/{bitId}                 - Change impact analysis
GET    /api/audit/coverage/{bitId}               - Coverage for specific bit
POST   /api/audit/webhooks                       - Configure notifications
```
