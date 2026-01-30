# Source Modes - Traditional, Corpus, and Hybrid

Understanding the three source-of-truth modes in CorpusHub.

---

## Mode 1: Traditional (Source Files are Truth)

**Use when:**
- Software project with code + documentation
- Team edits in IDE (VS Code, IntelliJ, etc.)
- Want corpus for review/comments only
- Source files are primary workflow

**How it works:**
1. Edit `.md`, `.yaml`, etc. in your IDE
2. File watchers detect changes
3. CorpusHub auto-generates HTML
4. View/comment in CorpusHub
5. Corpus is read-only representation

**Configuration:**
```json
{
  "bits": [
    {
      "id": "requirements/auth",
      "sourceFile": "docs/requirements/auth.md",
      "corpusFile": "corpus/requirements/auth.html",
      "sourceOfTruth": "source",
      "watchMode": true
    }
  ]
}
```

**Pros:**
- Team works in familiar tools
- Git workflow unchanged
- Corpus always synced

**Cons:**
- Can't edit via CorpusHub UI
- Requires file watchers running

---

## Mode 2: Corpus (Corpus is Truth)

**Use when:**
- Documentation-only project
- Browser-based editing preferred
- No code infrastructure
- Converting existing docs

**How it works:**
1. Edit HTML in CorpusHub
2. Changes saved to corpus/
3. Original files marked deprecated
4. Corpus is authoritative

**Configuration:**
```json
{
  "bits": [
    {
      "id": "specs/api",
      "corpusFile": "corpus/specs/api.html",
      "sourceFile": "docs/specs/api.md",  // Deprecated
      "sourceOfTruth": "corpus",
      "watchMode": false
    }
  ]
}
```

**Pros:**
- Edit anywhere (browser)
- No file watchers needed
- Simple workflow

**Cons:**
- Original files become stale
- IDE editing discouraged

---

## Mode 3: Hybrid (Mixed)

**Use when:**
- Complex projects
- Some docs traditional, some corpus
- Advanced users
- Specific per-artifact needs

**How it works:**
- Configure per artifact type
- Mix traditional and corpus bits
- Maximum flexibility

**Configuration:**
```json
{
  "bits": [
    {
      "id": "requirements/auth",
      "sourceOfTruth": "source",
      "watchMode": true
    },
    {
      "id": "guides/tutorial",
      "sourceOfTruth": "corpus",
      "watchMode": false
    }
  ]
}
```

**Pros:**
- Ultimate flexibility
- Best of both worlds

**Cons:**
- More complex
- Easy to confuse team

---

## Choosing a Mode

**For conversion:** Recommend **Corpus mode**
- Simpler migration
- Clear transition point
- Original files preserved but deprecated

**For new software projects:** Recommend **Traditional mode**
- Familiar IDE workflow
- Git-centric
- Corpus for review only

**For documentation projects:** Recommend **Corpus mode**
- Browser-based editing
- No toolchain needed

---

## Migration Paths

### Traditional → Corpus
1. Disable file watchers
2. Update `sourceOfTruth` to `corpus`
3. Mark source files deprecated
4. Edit via CorpusHub

### Corpus → Traditional
1. Export corpus to markdown
2. Update `sourceOfTruth` to `source`
3. Enable file watchers
4. Edit via IDE

### Hybrid Setup
Configure per artifact type based on team needs.
