---
name: content-creation
description: >
  Create high-quality content for multiple platforms including blog posts, technical documentation,
  social media, and multi-platform distribution. Adapts content format, length, and style for each
  target platform while maintaining message consistency.
---

# Content Creation

**Purpose:** Generate and adapt content for publishing across multiple platforms
**Size:** ~14 KB
**Type:** Core Publishing Skill (Universal)
**Status:** Production

---

## ⚡ LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Create a blog post about..."
- "Write documentation for..."
- "Generate social media content"
- "Publish to multiple platforms"
- "Draft an article on..."

**Context Indicators:**
- Need to create new content
- Multi-platform distribution required
- Content format adaptation needed
- SEO optimization desired

## ❌ DO NOT LOAD WHEN

- Editing existing content (use review-edit-author)
- Reviewing content (use review-edit-author in reviewer mode)
- Managing corpus documentation (use corpus-config)

---

## Content Types

### Blog Posts

**Characteristics:**
- Length: 800-2000 words
- Format: HTML/Markdown
- Structure: Title, intro, body sections, conclusion
- SEO: Meta description, keywords, internal links
- Images: Featured image, inline images
- Voice: Engaging, informative

**Template:**
```markdown
# [Compelling Title]

[Meta Description: 150-160 chars summary]

## Introduction
[Hook + problem statement + what reader will learn]

## [Section 1: Main Point]
[Content with examples, data, visuals]

## [Section 2: Supporting Point]
[Content with practical application]

## [Section 3: Advanced Insights]
[Deeper dive, edge cases, best practices]

## Conclusion
[Summary + call-to-action]

**Key Takeaways:**
- [Bullet point 1]
- [Bullet point 2]
- [Bullet point 3]
```

### Technical Documentation

**Characteristics:**
- Length: Variable (500-5000+ words)
- Format: Markdown
- Structure: Overview, installation, usage, API, examples
- Code: Syntax-highlighted examples
- Navigation: Table of contents, cross-links
- Voice: Clear, precise, professional

**Template:**
```markdown
# [Feature/API Name]

## Overview
[Brief description, purpose, use cases]

## Installation
```bash
[Installation commands]
```

## Quick Start
[Minimal example to get started]

## API Reference
### [Method/Function Name]
**Parameters:**
- `param1` (type): Description
- `param2` (type): Description

**Returns:** Description

**Example:**
```javascript
[Code example]
```

## Advanced Usage
[Complex scenarios, best practices]

## Troubleshooting
[Common issues and solutions]
```

### Social Media Content

**Platform-Specific Guidelines:**

#### Twitter/X
- **Length:** 280 characters max
- **Format:** Plain text + links
- **Structure:** Hook + value + CTA
- **Hashtags:** 1-3 relevant hashtags
- **Threads:** Break long content into connected tweets

**Template:**
```
[Hook sentence]

[Value proposition]

[Call-to-action]

#hashtag1 #hashtag2
```

#### LinkedIn
- **Length:** 1300 characters max (first 140 visible in feed)
- **Format:** Rich text with line breaks
- **Structure:** Professional hook + insights + CTA
- **Tone:** Professional, thought-leadership
- **Hashtags:** 3-5 professional hashtags

**Template:**
```
[Professional hook - first 140 chars crucial]

[Key insight #1 with data/example]

[Key insight #2 with practical application]

[Call-to-action]

#Industry #Topic #Skill #ProfessionalDevelopment
```

#### Medium
- **Length:** 1000-2000 words (7-minute read)
- **Format:** Markdown/Rich text
- **Structure:** Story-driven narrative
- **Images:** Header image + inline visuals
- **Tone:** Personal, narrative-driven

---

## Content Generation Workflow

### Phase 1: Requirements Gathering

```javascript
async function gatherRequirements(userRequest) {
  const requirements = {
    contentType: detectContentType(userRequest),
    targetPlatforms: extractPlatforms(userRequest),
    topic: extractTopic(userRequest),
    audience: determineAudience(userRequest),
    tone: determineTone(userRequest),
    length: determinateLength(userRequest),
    seoKeywords: extractKeywords(userRequest)
  };

  // Validate requirements
  if (!requirements.topic) {
    console.log('❓ What topic should the content cover?');
    requirements.topic = await promptUser();
  }

  if (!requirements.targetPlatforms.length) {
    console.log('❓ Which platforms should we target?');
    console.log('   1. Blog only');
    console.log('   2. Social media (Twitter, LinkedIn)');
    console.log('   3. Both blog and social');
    console.log('   4. Documentation site');
    requirements.targetPlatforms = await promptPlatformChoice();
  }

  return requirements;
}
```

### Phase 2: Research & Outline

```javascript
async function createOutline(requirements) {
  console.log('Creating content outline...');

  const outline = {
    title: generateTitle(requirements),
    metaDescription: generateMetaDescription(requirements),
    sections: [],
    keyPoints: [],
    callToAction: determineCTA(requirements)
  };

  // Generate section structure based on content type
  switch (requirements.contentType) {
    case 'blog-post':
      outline.sections = [
        { title: 'Introduction', points: [] },
        { title: generateSectionTitle(requirements, 1), points: [] },
        { title: generateSectionTitle(requirements, 2), points: [] },
        { title: 'Conclusion', points: [] }
      ];
      break;

    case 'documentation':
      outline.sections = [
        { title: 'Overview', points: [] },
        { title: 'Installation', points: [] },
        { title: 'Usage', points: [] },
        { title: 'API Reference', points: [] },
        { title: 'Examples', points: [] }
      ];
      break;

    case 'social-media':
      outline.sections = [
        { title: 'Hook', points: [] },
        { title: 'Value', points: [] },
        { title: 'CTA', points: [] }
      ];
      break;
  }

  console.log('✓ Outline created');
  return outline;
}
```

### Phase 3: Content Generation

```javascript
async function generateContent(outline, requirements) {
  console.log('Generating content...');

  const masterContent = {
    title: outline.title,
    meta: outline.metaDescription,
    sections: []
  };

  // Generate each section
  for (const section of outline.sections) {
    const sectionContent = await generateSection(
      section,
      requirements.tone,
      requirements.audience
    );
    masterContent.sections.push(sectionContent);
  }

  console.log('✓ Master content generated');
  return masterContent;
}
```

### Phase 4: Platform Adaptation

```javascript
async function adaptForPlatforms(masterContent, platforms) {
  console.log('Adapting content for platforms...');

  const adaptedContent = {};

  for (const platform of platforms) {
    switch (platform) {
      case 'blog':
        adaptedContent.blog = formatForBlog(masterContent);
        break;

      case 'twitter':
        adaptedContent.twitter = formatForTwitter(masterContent);
        break;

      case 'linkedin':
        adaptedContent.linkedin = formatForLinkedIn(masterContent);
        break;

      case 'medium':
        adaptedContent.medium = formatForMedium(masterContent);
        break;

      case 'documentation':
        adaptedContent.docs = formatForDocs(masterContent);
        break;
    }

    console.log(`✓ Adapted for ${platform}`);
  }

  return adaptedContent;
}
```

---

## Platform Formatters

### Blog Formatter

```javascript
function formatForBlog(content) {
  return `# ${content.title}

${content.meta}

${content.sections.map(section => `
## ${section.title}

${section.content}
`).join('\n')}

## Key Takeaways

${content.keyPoints.map(point => `- ${point}`).join('\n')}

${content.callToAction}
`;
}
```

### Twitter Formatter

```javascript
function formatForTwitter(content) {
  const tweets = [];

  // Main tweet (hook)
  tweets.push({
    text: `${content.hook}\n\n${content.value}\n\n${content.cta}`,
    hashtags: content.hashtags.slice(0, 3)
  });

  // Thread expansion if content is long
  if (content.sections.length > 1) {
    for (let i = 0; i < content.sections.length; i++) {
      const section = content.sections[i];
      tweets.push({
        text: `${i + 2}/ ${section.summary}`,
        isThread: true
      });
    }
  }

  return tweets;
}
```

### LinkedIn Formatter

```javascript
function formatForLinkedIn(content) {
  // First 140 characters are crucial
  const hook = content.title;

  // Professional formatting with line breaks
  return `${hook}

${content.sections[0].summary}

Key insights:
${content.keyPoints.map((point, i) => `${i + 1}. ${point}`).join('\n\n')}

${content.callToAction}

${content.hashtags.map(tag => `#${tag}`).join(' ')}`;
}
```

### Documentation Formatter

```javascript
function formatForDocs(content) {
  return `# ${content.title}

## Table of Contents
${generateTOC(content.sections)}

${content.sections.map(section => `
## ${section.title}

${section.content}

${section.codeExamples ? `
\`\`\`${section.language || 'javascript'}
${section.codeExamples}
\`\`\`
` : ''}
`).join('\n')}
`;
}
```

---

## SEO Optimization

### Meta Tags Generation

```javascript
function generateSEOTags(content, requirements) {
  return {
    title: truncate(content.title, 60),
    description: truncate(content.metaDescription, 160),
    keywords: requirements.seoKeywords.join(', '),
    ogTitle: content.title,
    ogDescription: content.metaDescription,
    ogImage: content.featuredImage || generateDefaultImage(),
    twitterCard: 'summary_large_image',
    twitterTitle: truncate(content.title, 70),
    twitterDescription: truncate(content.metaDescription, 200)
  };
}
```

### Internal Linking

```javascript
function addInternalLinks(content, existingContent) {
  // Find related content
  const relatedArticles = findRelated(content.topic, existingContent);

  // Add contextual links
  content.internalLinks = relatedArticles.map(article => ({
    title: article.title,
    url: article.url,
    context: findBestInsertionPoint(content, article)
  }));

  return content;
}
```

---

## Usage Examples

### Example 1: Simple Blog Post

```
User: "Create a blog post about the benefits of TypeScript"

Execution:
  Requirements:
    - Content type: blog-post
    - Platform: blog
    - Topic: "Benefits of TypeScript"
    - Audience: JavaScript developers
    - Tone: Informative, practical

  Outline:
    - Introduction: Why type safety matters
    - Section 1: Catch errors before runtime
    - Section 2: Better IDE support
    - Section 3: Improved maintainability
    - Conclusion: Getting started

  Output:
    - 1500-word blog post
    - SEO optimized
    - Code examples included
    - Internal links to related content
```

### Example 2: Multi-Platform Launch

```
User: "Announce our new v2.0 release on blog, Twitter, and LinkedIn"

Execution:
  Requirements:
    - Content type: announcement
    - Platforms: [blog, twitter, linkedin]
    - Topic: "v2.0 Release"
    - Tone: Exciting, professional

  Master Content:
    - Core message: v2.0 features
    - Key benefits: Speed, reliability, new APIs
    - CTA: Try it now

  Platform Adaptations:
    - Blog: 1000-word detailed announcement
    - Twitter: 5-tweet thread with key features
    - LinkedIn: Professional post highlighting business value
```

### Example 3: API Documentation

```
User: "Generate API documentation for our REST endpoints"

Execution:
  Requirements:
    - Content type: documentation
    - Platform: docs site
    - Source: Extract from code
    - Format: Markdown

  Process:
    1. Scan code for endpoints
    2. Extract parameters, returns
    3. Generate usage examples
    4. Create navigation structure

  Output:
    - Structured API reference
    - Code examples for each endpoint
    - Authentication guide
    - Error handling section
```

---

## Configuration

```json
{
  "contentCreation": {
    "defaults": {
      "blogWordCount": 1500,
      "tone": "professional",
      "includeSEO": true,
      "generateImages": false
    },
    "seo": {
      "titleMaxLength": 60,
      "descriptionMaxLength": 160,
      "includeOGTags": true,
      "includeTwitterCard": true
    },
    "platforms": {
      "twitter": {
        "maxLength": 280,
        "hashtagLimit": 3,
        "createThreads": true
      },
      "linkedin": {
        "maxLength": 1300,
        "professionalTone": true,
        "hashtagLimit": 5
      }
    }
  }
}
```

---

## Quick Reference

**Create blog post:**
```javascript
await createContent({
  type: 'blog-post',
  topic: 'Your Topic',
  platform: 'blog'
});
```

**Multi-platform:**
```javascript
await createContent({
  type: 'announcement',
  topic: 'Product Launch',
  platforms: ['blog', 'twitter', 'linkedin']
});
```

**Documentation:**
```javascript
await createContent({
  type: 'documentation',
  source: 'code',
  format: 'markdown'
});
```

---

*End of Content Creation*
*Part of v4.0.0 Universal Skills Ecosystem*
*Supports: Blog, Twitter, LinkedIn, Medium, Documentation*
