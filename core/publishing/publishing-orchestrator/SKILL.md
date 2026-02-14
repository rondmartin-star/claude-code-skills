---
name: publishing-orchestrator
description: >
  Route publishing and content creation operations to specialized skills. Detects publishing intent,
  assesses complexity, and delegates to content-creation or other publishing workflows.
  Use when: user mentions publishing, content creation, or multi-platform distribution.
---

# Publishing Orchestrator

**Purpose:** Route publishing operations to appropriate specialized skills
**Size:** ~10 KB
**Type:** Core Orchestrator (Universal)
**Status:** Production

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Publish this content"
- "Create content for..."
- "Generate blog post"
- "Write documentation"
- "Multi-platform publishing"
- "Create social media content"

**Context Indicators:**
- Publishing-related request
- Content creation needed
- Multiple platform targeting
- User unsure which publishing skill to use

## ❌ DO NOT LOAD WHEN

- Specific operation clear:
  - "Create blog post" → content-creation directly
  - Content editing (use review-edit-author)
  - Corpus configuration (use corpus-config)

---

## Routing Decision Tree

### Step 1: Detect Publishing Intent

**Analyze user request to determine publishing operation:**

```javascript
function analyzePublishingIntent(userMessage) {
  const intentPatterns = {
    'create-content': [
      /create.*(?:blog|article|post|documentation)/i,
      /write.*(?:content|guide|tutorial)/i,
      /generate.*(?:documentation|content)/i
    ],
    'multi-platform': [
      /publish.*(?:everywhere|multiple platforms)/i,
      /cross-platform.*publish/i,
      /distribute.*content/i
    ],
    'social-media': [
      /(?:twitter|linkedin|facebook|social).*post/i,
      /social media content/i
    ],
    'blog': [
      /blog post/i,
      /article.*publish/i
    ],
    'documentation': [
      /(?:api|technical).*documentation/i,
      /(?:readme|guide).*create/i
    ]
  };

  for (const [intent, patterns] of Object.entries(intentPatterns)) {
    for (const pattern of patterns) {
      if (pattern.test(userMessage)) {
        return intent;
      }
    }
  }

  return 'unknown';
}
```

### Step 2: Route to Appropriate Skill

```javascript
async function routePublishingOperation(intent, context) {
  const routingMap = {
    'create-content': 'content-creation',
    'multi-platform': 'content-creation',
    'social-media': 'content-creation',
    'blog': 'content-creation',
    'documentation': 'content-creation'
  };

  const targetSkill = routingMap[intent];

  if (!targetSkill) {
    return providePublishingGuidance(context);
  }

  console.log(`Routing to: ${targetSkill}`);
  return loadSkill(targetSkill, context);
}
```

---

## Intent Detection Patterns

### Content Creation Intent

**Trigger Patterns:**
```
- "Create [a] blog post about..."
- "Write documentation for..."
- "Generate article on..."
- "Draft content for..."
```

**Route To:** content-creation

**Conditions:**
- User wants to create new content
- May target multiple platforms
- Requires content generation

### Multi-Platform Publishing

**Trigger Patterns:**
```
- "Publish to [multiple platforms]"
- "Distribute this content"
- "Cross-post to..."
- "Share on [platforms]"
```

**Route To:** content-creation (multi-platform mode)

**Conditions:**
- Content exists or will be created
- Target multiple platforms
- May need format adaptation

### Documentation Intent

**Trigger Patterns:**
```
- "Create API documentation"
- "Generate README"
- "Write technical guide"
- "Document this feature"
```

**Route To:** content-creation (documentation mode)

**Conditions:**
- Technical content
- May extract from code
- Structured format needed

---

## Routing Examples

### Example 1: Blog Post Creation

```
User: "Create a blog post about our new feature release"

Analysis:
  - Intent: create-content (blog)
  - Platform: Blog
  - Content type: Article

Routing Decision:
  → content-creation

Execution:
  - Load content-creation skill
  - Mode: blog-post
  - Gather feature information
  - Generate structured content
  - Format for publishing
```

### Example 2: Multi-Platform Publishing

```
User: "Write an announcement and publish it to blog, Twitter, and LinkedIn"

Analysis:
  - Intent: multi-platform
  - Platforms: [blog, twitter, linkedin]
  - Content type: Announcement

Routing Decision:
  → content-creation (multi-platform mode)

Execution:
  - Create master content
  - Adapt for each platform:
    * Blog: Full article (1000+ words)
    * Twitter: Thread (280 chars/tweet)
    * LinkedIn: Professional post (1300 chars)
  - Generate platform-specific formats
```

### Example 3: Documentation Generation

```
User: "Generate API documentation for our REST endpoints"

Analysis:
  - Intent: documentation
  - Source: Code/API specs
  - Format: Technical docs

Routing Decision:
  → content-creation (documentation mode)

Execution:
  - Scan code for endpoints
  - Extract docstrings/comments
  - Generate structured docs
  - Format in Markdown/HTML
```

---

## Guidance Mode

**When intent is unclear, provide guidance:**

```javascript
function providePublishingGuidance(context) {
  console.log('Publishing Operations Available:');
  console.log('');
  console.log('Content Creation:');
  console.log('  - Blog posts and articles');
  console.log('  - Technical documentation');
  console.log('  - Social media content');
  console.log('  - Multi-platform distribution');
  console.log('');
  console.log('What would you like to create?');
  console.log('  1. Blog post or article');
  console.log('  2. Technical documentation');
  console.log('  3. Social media content');
  console.log('  4. Multi-platform announcement');

  return promptUserChoice();
}
```

---

## Platform Support

**Supported Publishing Platforms:**

| Platform | Format | Max Length | Special Requirements |
|----------|--------|------------|---------------------|
| **Blog** | HTML/Markdown | Unlimited | SEO metadata |
| **Twitter** | Plain text | 280 chars | Hashtags, threads |
| **LinkedIn** | Rich text | 1300 chars | Professional tone |
| **Medium** | Markdown | Unlimited | Story format |
| **Dev.to** | Markdown | Unlimited | Frontmatter |
| **Hashnode** | Markdown | Unlimited | Canonical URL |
| **Documentation** | Markdown/HTML | Unlimited | Code blocks, links |

---

## Error Handling

### Invalid Platform

```javascript
if (!isSupportedPlatform(platform)) {
  console.error(`❌ Unsupported platform: ${platform}`);
  console.log('');
  console.log('Supported platforms:');
  console.log('  - Blog, Twitter, LinkedIn, Medium');
  console.log('  - Dev.to, Hashnode');
  console.log('  - Custom documentation sites');
  return;
}
```

### Missing Content

```javascript
if (!hasContent(context)) {
  console.warn('⚠️  No content provided');
  console.log('');
  console.log('Options:');
  console.log('  1. Generate new content (provide topic)');
  console.log('  2. Use existing content (provide path)');
  console.log('  3. Extract from code (provide source)');

  const choice = await promptUser();
  return handleContentSource(choice);
}
```

---

## Configuration

**Publishing Settings:**

```json
{
  "publishing": {
    "defaultPlatforms": ["blog", "twitter"],
    "contentTypes": {
      "blog-post": {
        "minWords": 500,
        "maxWords": 2000,
        "includeSEO": true
      },
      "social-media": {
        "generateHashtags": true,
        "includeCTA": true
      },
      "documentation": {
        "format": "markdown",
        "includeCodeExamples": true
      }
    }
  }
}
```

---

## Quick Reference

**Route to skill by intent:**
```javascript
const skill = routePublishingOperation(userMessage);
await loadSkill(skill);
```

**Multi-platform workflow:**
```javascript
await publishMultiPlatform({
  content: masterContent,
  platforms: ['blog', 'twitter', 'linkedin']
});
```

---

## Skill Summary

**Publishing Skills:**

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| **content-creation** | Create content for publishing | All content creation needs |
| **publishing-orchestrator** | Route publishing operations | Ambiguous or multi-step requests |

---

*End of Publishing Orchestrator*
*Part of v4.0.0 Universal Skills Ecosystem*
*Routes to: content-creation*
