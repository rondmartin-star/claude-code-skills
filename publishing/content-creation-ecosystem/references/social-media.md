# Social Media Content Reference

**Supported Platforms:** Bluesky, Twitter/X, LinkedIn  
**Load when:** User mentions social posts, Bluesky, Twitter, LinkedIn, or thread creation

---

## Bluesky Specifications

### Character Limits

| Element | Limit |
|---------|-------|
| Post body | 300 characters |
| Display name | 64 characters |
| Handle | 253 characters |
| Alt text | 2000 characters |
| Links | Count against limit |

### Thread Architecture

For content exceeding 300 characters:

```
Thread Structure:
├── Post 1 (hook) - strongest statement
├── Post 2-N (body) - key points
└── Final post (CTA) - engagement driver

Numbering: "1/5", "2/5", etc. at end of each post
```

### Bluesky Best Practices

| Do | Don't |
|----|----|
| Front-load key message | Bury the lede |
| Use line breaks for readability | Wall of text |
| Include relevant hashtags (2-3) | Hashtag spam |
| End threads with engagement hook | Trail off |
| Alt text for all images | Leave images undescribed |

### Thread Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Bluesky Thread Preview</title>
  <style>
    :root {
      --bluesky-blue: #0085ff;
      --text-dark: #1a1a1a;
      --text-light: #687684;
      --bg-white: #ffffff;
      --border: #e0e0e0;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      max-width: 600px;
      margin: 2rem auto;
      padding: 1rem;
      background: #f7f9fa;
    }
    .thread-post {
      background: var(--bg-white);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1rem;
      margin-bottom: 0.5rem;
      position: relative;
    }
    .thread-post::before {
      content: '';
      position: absolute;
      left: 28px;
      top: 100%;
      width: 2px;
      height: 0.5rem;
      background: var(--border);
    }
    .thread-post:last-child::before {
      display: none;
    }
    .post-header {
      display: flex;
      align-items: center;
      margin-bottom: 0.5rem;
    }
    .avatar {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: var(--bluesky-blue);
      margin-right: 0.75rem;
    }
    .display-name {
      font-weight: 600;
      color: var(--text-dark);
    }
    .handle {
      color: var(--text-light);
      font-size: 0.9rem;
    }
    .post-content {
      font-size: 1rem;
      line-height: 1.5;
      color: var(--text-dark);
      white-space: pre-wrap;
    }
    .char-count {
      text-align: right;
      font-size: 0.8rem;
      color: var(--text-light);
      margin-top: 0.5rem;
    }
    .char-count.over {
      color: #dc2626;
      font-weight: bold;
    }
    .hashtag {
      color: var(--bluesky-blue);
    }
    .controls {
      background: var(--bg-white);
      padding: 1rem;
      border-radius: 8px;
      margin-bottom: 1rem;
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .controls button {
      padding: 0.5rem 1rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: white;
      cursor: pointer;
      font-size: 0.9rem;
    }
    .controls button:hover {
      background: #f0f0f0;
    }
    .thread-number {
      font-size: 0.85rem;
      color: var(--text-light);
    }
  </style>
</head>
<body>
  <div class="controls" id="content-controls">
    <button onclick="window.print()">Print</button>
    <button onclick="copyThread()">Copy All</button>
    <button onclick="toggleSource()">View Source</button>
  </div>
  
  <div class="thread" id="thread-container">
    <!-- Posts inserted here -->
  </div>
  
  <script>
    function countChars(text) {
      return text.length;
    }
    
    function copyThread() {
      const posts = document.querySelectorAll('.post-content');
      let text = '';
      posts.forEach((post, i) => {
        text += post.textContent.trim() + '\n\n---\n\n';
      });
      navigator.clipboard.writeText(text.trim());
      alert('Thread copied to clipboard!');
    }
    
    function toggleSource() {
      const container = document.getElementById('thread-container');
      if (container.style.whiteSpace === 'pre') {
        container.style.whiteSpace = '';
        container.innerHTML = container.dataset.rendered;
      } else {
        container.dataset.rendered = container.innerHTML;
        container.style.whiteSpace = 'pre';
        container.textContent = container.innerHTML;
      }
    }
  </script>
</body>
</html>
```

---

## Single Post Template

```html
<div class="thread-post" data-line="{{line}}">
  <div class="post-header">
    <div class="avatar"></div>
    <div>
      <div class="display-name">{{display_name}}</div>
      <div class="handle">@{{handle}}</div>
    </div>
  </div>
  <div class="post-content">{{content}}</div>
  <div class="char-count {{over_class}}">{{char_count}}/300</div>
</div>
```

---

## Content Patterns

### Hook Types (First Post)

| Type | Pattern | Example |
|------|---------|---------|
| Contrarian | Challenge assumption | "Most advice about X is wrong..." |
| Question | Engage curiosity | "What if Y could do Z?" |
| Stat/Fact | Authority signal | "87% of A don't know B..." |
| Story | Human connection | "Yesterday I discovered..." |
| List preview | Promise value | "5 things I learned about X:" |

### Body Patterns (Middle Posts)

| Type | Use When |
|------|----------|
| Numbered list | Sequential points |
| Parallel structure | Comparison |
| Problem → Solution | Teaching |
| Before → After | Transformation |
| Evidence chain | Building argument |

### CTA Patterns (Final Post)

| Goal | Pattern |
|------|---------|
| Discussion | "What's your experience with X?" |
| Sharing | "Share if this resonated" |
| Follow | "Follow for more on X" |
| Link | "Full article: [link]" |
| Community | "Tag someone who needs this" |

---

## LinkedIn Adaptations

LinkedIn allows longer posts (3000 chars) and different formatting:

| Element | Bluesky | LinkedIn |
|---------|---------|----------|
| Length | 300 chars | 3000 chars |
| Tone | Casual/punchy | Professional |
| Hashtags | 2-3 | 3-5 |
| Formatting | Line breaks | Line breaks + emojis |
| Links | In post | Comment or post |

---

## Validation Checklist

### Before Posting

- [ ] Each post ≤ 300 characters (Bluesky)
- [ ] Hook post captures attention
- [ ] Thread numbering correct
- [ ] Hashtags relevant (not spammy)
- [ ] Links shortened if needed
- [ ] Images have alt text
- [ ] CTA clear and specific

### Quality Checks

- [ ] Read aloud for flow
- [ ] Remove filler words
- [ ] Each post can stand alone
- [ ] No typos or grammar errors
- [ ] Formatting displays correctly

---

## Export Options

### Plain Text (Copy/Paste)

```bash
python scripts/bundle_content.py thread.html --format text
```

Outputs each post with `---` separators.

### Image Cards

For visual threads, generate preview images:

```bash
python scripts/bundle_content.py thread.html --format images
```

Creates PNG for each post.

---

*End of Social Media Content Reference*
