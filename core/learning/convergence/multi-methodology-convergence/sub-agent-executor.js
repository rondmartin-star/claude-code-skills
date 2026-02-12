/**
 * Sub-Agent Executor for Multi-Methodology Convergence
 *
 * Implements parallel methodology execution with:
 * - Model selection strategy (Opus vs Sonnet)
 * - Context optimization per methodology
 * - Token budget validation
 * - Result aggregation
 *
 * Version: 1.0.0
 * Date: 2026-02-12
 */

// ============================================================================
// MODEL ASSIGNMENTS
// ============================================================================

const MODEL_ASSIGNMENTS = {
  // Opus models (6) - High-stakes, user-facing, complex analysis
  'User-Experience': 'claude-opus-4-5',
  'User-Accessibility': 'claude-opus-4-5',
  'Lateral-UX': 'claude-opus-4-5',
  'Top-Down-Requirements': 'claude-opus-4-5',
  'Bottom-Up-Quality': 'claude-opus-4-5',
  'Technical-Security': 'claude-opus-4-5',

  // Sonnet models (9) - Technical analysis, pattern matching
  'Technical-Quality': 'claude-sonnet-4-5',
  'Technical-Performance': 'claude-sonnet-4-5',
  'Holistic-Consistency': 'claude-sonnet-4-5',
  'Holistic-Integration': 'claude-sonnet-4-5',
  'Top-Down-Architecture': 'claude-sonnet-4-5',
  'Bottom-Up-Consistency': 'claude-sonnet-4-5',
  'Lateral-Integration': 'claude-sonnet-4-5',
  'Lateral-Security': 'claude-sonnet-4-5',
  'Lateral-Performance': 'claude-sonnet-4-5'
};

// ============================================================================
// CONTEXT RELEVANCE MAP
// ============================================================================

const METHODOLOGY_CONTEXT_MAP = {
  'Technical-Security': ['files', 'authConfig', 'apiEndpoints', 'envVars', 'dependencies'],
  'Technical-Quality': ['sourceFiles', 'testFiles', 'complexityMetrics', 'lintResults'],
  'Technical-Performance': ['sourceFiles', 'bundleStats', 'networkCalls', 'renderMetrics'],
  'User-Accessibility': ['htmlFiles', 'cssFiles', 'ariaUsage', 'semanticStructure', 'colorContrast'],
  'User-Experience': ['componentFiles', 'routeDefinitions', 'userFlows', 'interactionPatterns'],
  'Holistic-Consistency': ['allFiles', 'namingPatterns', 'frameworkTerms', 'styleGuides'],
  'Holistic-Integration': ['apiDefinitions', 'interfaceFiles', 'documentation', 'integrationTests'],
  'Top-Down-Requirements': ['requirements', 'deliverables', 'specs', 'acceptanceCriteria'],
  'Top-Down-Architecture': ['architectureDocs', 'designDocs', 'implementation', 'adrs'],
  'Bottom-Up-Quality': ['codeArtifacts', 'qualityStandards', 'metrics', 'testCoverage'],
  'Bottom-Up-Consistency': ['deliverables', 'internalReferences', 'crossReferences'],
  'Lateral-Integration': ['componentInterfaces', 'integrationPoints', 'dataFlow'],
  'Lateral-Security': ['securityConfig', 'authFlows', 'apiSecurity', 'cryptography'],
  'Lateral-Performance': ['performanceMetrics', 'loadTests', 'bundleAnalysis', 'caching'],
  'Lateral-UX': ['uxComponents', 'interactionFlows', 'userJourneys', 'feedback']
};

// ============================================================================
// TOKEN BUDGETS
// ============================================================================

const TOKEN_BUDGETS = {
  'claude-opus-4-5': {
    total: 100000,
    context: 30000,
    analysis: 70000
  },
  'claude-sonnet-4-5': {
    total: 50000,
    context: 15000,
    analysis: 35000
  }
};

// ============================================================================
// SUB-AGENT EXECUTION
// ============================================================================

/**
 * Execute methodology as sub-agent with optimized context
 *
 * @param {Object} methodology - Methodology definition
 * @param {Object} subject - Full subject data
 * @param {Object} options - Execution options
 * @returns {Promise<Object>} Methodology results
 */
async function executeMethodologyAsSubAgent(methodology, subject, options = {}) {
  const model = MODEL_ASSIGNMENTS[methodology.name] || 'claude-sonnet-4-5';
  const context = buildMinimalContext(methodology, subject);

  // Validate token budget before execution
  const budgetValid = validateTokenBudget(methodology, context, model);
  if (!budgetValid.valid) {
    console.log(`⚠️ Context too large for ${methodology.name}: ${budgetValid.estimate} tokens`);
    console.log(`   Reducing context...`);
    context.subject = reduceContextFurther(context.subject, budgetValid.limit);
    context.prompt = rebuildPrompt(methodology, context.subject);
    context.tokenEstimate = Math.ceil(context.prompt.length / 4);
  }

  console.log(`→ Launching ${methodology.name} as sub-agent`);
  console.log(`   Model: ${model}`);
  console.log(`   Context size: ~${context.tokenEstimate} tokens (${budgetValid.percentage}% of budget)`);

  // Launch as sub-agent task
  try {
    const result = await Task({
      subagent_type: 'general-purpose',
      description: `Execute ${methodology.name} methodology`,
      prompt: context.prompt,
      model: model,
      timeout: options.timeout || 300000  // 5 minutes default
    });

    return parseMethodologyResult(result, methodology);
  } catch (error) {
    console.log(`✗ ${methodology.name} execution failed: ${error.message}`);
    return {
      methodology: methodology.name,
      error: error.message,
      issues: [],
      evidence: [`Execution error: ${error.message}`],
      summary: `Failed to execute ${methodology.name}`
    };
  }
}

/**
 * Execute multiple methodologies in parallel
 *
 * @param {Array} methodologies - Methodologies to execute
 * @param {Object} subject - Subject data
 * @param {Object} options - Execution options
 * @returns {Promise<Array>} Array of results
 */
async function executeMethodologiesInParallel(methodologies, subject, options = {}) {
  console.log(`\n→ Executing ${methodologies.length} methodologies in parallel`);

  // Estimate token savings
  const savings = estimateTokenSavings(subject, methodologies);
  console.log(`   Token savings: ${savings.savingsPercentage}% (${savings.savings} tokens)`);

  const promises = methodologies.map(methodology =>
    executeMethodologyAsSubAgent(methodology, subject, options)
  );

  const results = await Promise.allSettled(promises);

  // Process results
  const successful = results.filter(r => r.status === 'fulfilled').map(r => r.value);
  const failed = results.filter(r => r.status === 'rejected');

  console.log(`✓ Parallel execution complete`);
  console.log(`   Successful: ${successful.length}/${methodologies.length}`);
  if (failed.length > 0) {
    console.log(`   Failed: ${failed.length}/${methodologies.length}`);
  }

  return successful;
}

// ============================================================================
// CONTEXT OPTIMIZATION
// ============================================================================

/**
 * Build minimal context for methodology
 *
 * @param {Object} methodology - Methodology definition
 * @param {Object} subject - Full subject data
 * @returns {Object} Minimal context with prompt and token estimate
 */
function buildMinimalContext(methodology, subject) {
  const focusedSubject = extractRelevantSubject(methodology, subject);
  const serialized = serializeMinimal(focusedSubject);

  const prompt = `
# ${methodology.name} Methodology

## Objective
${methodology.description}

## Subject Data
${serialized}

## Task
Analyze the subject data using the ${methodology.name} methodology.
Return results in JSON format:

{
  "issues": [
    {
      "type": "issue-type",
      "description": "Issue description",
      "file": "path/to/file",
      "line": 123,
      "severity": "high|medium|low",
      "evidence": "Supporting evidence"
    }
  ],
  "evidence": [
    "Evidence item 1",
    "Evidence item 2"
  ],
  "summary": "Brief summary of findings"
}

If no issues found, return empty issues array.
`.trim();

  const tokenEstimate = Math.ceil(prompt.length / 4);

  return {
    prompt,
    tokenEstimate,
    subject: focusedSubject
  };
}

/**
 * Extract relevant subject data for methodology
 *
 * @param {Object} methodology - Methodology definition
 * @param {Object} subject - Full subject data
 * @returns {Object} Filtered subject data
 */
function extractRelevantSubject(methodology, subject) {
  const relevantFields = METHODOLOGY_CONTEXT_MAP[methodology.name] || ['*'];

  if (relevantFields.includes('*')) {
    return subject;  // Needs everything
  }

  const filtered = {};

  for (const field of relevantFields) {
    if (subject.data && subject.data[field] !== undefined) {
      filtered[field] = subject.data[field];
    } else if (subject[field] !== undefined) {
      filtered[field] = subject[field];
    }
  }

  return {
    type: subject.type,
    data: filtered
  };
}

/**
 * Serialize data with minimal token usage
 *
 * @param {Object} data - Data to serialize
 * @returns {string} Minimized JSON string
 */
function serializeMinimal(data) {
  return JSON.stringify(data, (key, value) => {
    // Omit null/undefined
    if (value === null || value === undefined) {
      return undefined;
    }

    // Sample large arrays (first 25 + last 25)
    if (Array.isArray(value) && value.length > 50) {
      return [
        ...value.slice(0, 25),
        { _truncated: `... ${value.length - 50} items omitted ...` },
        ...value.slice(-25)
      ];
    }

    // Truncate long strings
    if (typeof value === 'string' && value.length > 1000) {
      return value.substring(0, 1000) + `... (${value.length - 1000} chars truncated)`;
    }

    return value;
  }, 0);  // No indentation for minimal size
}

/**
 * Further reduce context if needed
 *
 * @param {Object} subject - Subject data
 * @param {number} targetTokens - Target token count
 * @returns {Object} Reduced subject
 */
function reduceContextFurther(subject, targetTokens) {
  const reduced = JSON.parse(JSON.stringify(subject));

  for (const key in reduced.data) {
    if (Array.isArray(reduced.data[key])) {
      if (reduced.data[key].length > 20) {
        // More aggressive sampling
        reduced.data[key] = [
          ...reduced.data[key].slice(0, 10),
          { _truncated: `... ${reduced.data[key].length - 20} items ...` },
          ...reduced.data[key].slice(-10)
        ];
      }
    } else if (typeof reduced.data[key] === 'string' && reduced.data[key].length > 500) {
      // More aggressive string truncation
      reduced.data[key] = reduced.data[key].substring(0, 500) +
        `... (${reduced.data[key].length - 500} chars truncated)`;
    }
  }

  return reduced;
}

/**
 * Rebuild prompt after context reduction
 */
function rebuildPrompt(methodology, subject) {
  const serialized = serializeMinimal(subject);
  return `
# ${methodology.name} Methodology

## Objective
${methodology.description}

## Subject Data (Reduced)
${serialized}

## Task
Analyze the subject data using the ${methodology.name} methodology.
Return results in JSON format with issues, evidence, and summary.
`.trim();
}

// ============================================================================
// VALIDATION
// ============================================================================

/**
 * Validate token budget for methodology
 *
 * @param {Object} methodology - Methodology definition
 * @param {Object} context - Built context
 * @param {string} model - Model name
 * @returns {Object} Validation result
 */
function validateTokenBudget(methodology, context, model) {
  const budget = TOKEN_BUDGETS[model] || TOKEN_BUDGETS['claude-sonnet-4-5'];
  const estimate = context.tokenEstimate;
  const limit = budget.context;

  return {
    valid: estimate <= limit,
    estimate,
    limit,
    model,
    percentage: Math.round((estimate / limit) * 100),
    remaining: limit - estimate
  };
}

// ============================================================================
// RESULT PROCESSING
// ============================================================================

/**
 * Parse sub-agent result into methodology format
 *
 * @param {Object} result - Raw sub-agent result
 * @param {Object} methodology - Methodology definition
 * @returns {Object} Parsed result
 */
function parseMethodologyResult(result, methodology) {
  try {
    // Attempt to parse JSON from result
    const parsed = typeof result === 'string' ? JSON.parse(result) : result;

    return {
      methodology: methodology.name,
      issues: parsed.issues || [],
      evidence: parsed.evidence || [],
      summary: parsed.summary || '',
      success: true
    };
  } catch (error) {
    console.log(`⚠️ Failed to parse ${methodology.name} result: ${error.message}`);

    // Try to extract issues from text response
    const fallbackIssues = extractIssuesFromText(result);

    return {
      methodology: methodology.name,
      issues: fallbackIssues,
      evidence: [`Parse error: ${error.message}`, `Raw result length: ${String(result).length} chars`],
      summary: 'Failed to parse structured results, extracted from text',
      success: false,
      parseError: error.message
    };
  }
}

/**
 * Extract issues from text response (fallback)
 */
function extractIssuesFromText(text) {
  const issues = [];
  const lines = String(text).split('\n');

  // Simple pattern matching for common issue indicators
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.match(/error|issue|problem|warning|vulnerability/i)) {
      issues.push({
        type: 'extracted-issue',
        description: line.trim(),
        severity: 'medium',
        line: i + 1
      });
    }
  }

  return issues.slice(0, 20);  // Limit to 20
}

// ============================================================================
// METRICS
// ============================================================================

/**
 * Estimate token savings from context optimization
 *
 * @param {Object} fullSubject - Full subject data
 * @param {Array} methodologies - Methodologies being executed
 * @returns {Object} Savings estimate
 */
function estimateTokenSavings(fullSubject, methodologies) {
  const fullSerialized = JSON.stringify(fullSubject);
  const fullTokens = Math.ceil(fullSerialized.length / 4);
  const fullCost = fullTokens * methodologies.length;

  let optimizedCost = 0;
  for (const methodology of methodologies) {
    const context = buildMinimalContext(methodology, fullSubject);
    optimizedCost += context.tokenEstimate;
  }

  return {
    fullCost,
    optimizedCost,
    savings: fullCost - optimizedCost,
    savingsPercentage: Math.round(((fullCost - optimizedCost) / fullCost) * 100),
    perMethodology: {
      full: Math.round(fullTokens),
      optimized: Math.round(optimizedCost / methodologies.length)
    }
  };
}

// ============================================================================
// EXPORTS
// ============================================================================

module.exports = {
  // Core functions
  executeMethodologyAsSubAgent,
  executeMethodologiesInParallel,

  // Context optimization
  buildMinimalContext,
  extractRelevantSubject,
  serializeMinimal,
  reduceContextFurther,

  // Validation
  validateTokenBudget,

  // Result processing
  parseMethodologyResult,

  // Metrics
  estimateTokenSavings,

  // Configuration
  MODEL_ASSIGNMENTS,
  METHODOLOGY_CONTEXT_MAP,
  TOKEN_BUDGETS
};
