# Orchestration Patterns Reference

Advanced patterns for orchestrating multi-skill workflows and managing phase transitions.

---

## Phase Transition Logic

### Decision Tree for Phase Routing

```python
def determine_next_phase(user_input: str, current_phase: str, context: dict) -> str:
    """
    Determine which phase to load next based on user input and context.

    Phases:
    - requirements: Gathering what the app should do
    - system-design: Designing data models and architecture
    - ui-design: Designing pages and navigation
    - build: Implementing the application
    - supervision: Packaging and deploying
    """

    # Parse user input for intent
    intent = classify_intent(user_input)

    # Requirements phase triggers
    if any(keyword in user_input.lower() for keyword in [
        "i want to build", "i need an app", "requirements", "user stories",
        "what should it do", "features"
    ]):
        return "requirements"

    # System design phase triggers
    if any(keyword in user_input.lower() for keyword in [
        "data model", "database", "entities", "relationships", "schema",
        "api endpoints", "architecture"
    ]):
        return "system-design"

    # UI design phase triggers
    if any(keyword in user_input.lower() for keyword in [
        "ui design", "pages", "screens", "navigation", "user interface",
        "wireframe", "mockup"
    ]):
        return "ui-design"

    # Build phase triggers
    if any(keyword in user_input.lower() for keyword in [
        "start coding", "implement", "fix bug", "add feature", "here's the code",
        "error:", "traceback"
    ]):
        # Special case: Authentication/security triggers
        if any(keyword in user_input.lower() for keyword in [
            "authentication", "login", "oauth", "security", "csrf"
        ]):
            context["load_security_orchestrator"] = True

        return "build"

    # Supervision phase triggers
    if any(keyword in user_input.lower() for keyword in [
        "package", "deploy", "installer", "service", "production",
        "create msi", "windows service"
    ]):
        return "supervision"

    # Context-based phase continuation
    if current_phase == "requirements":
        # After requirements, usually go to system design
        if context.get("requirements_complete"):
            return "system-design"

    if current_phase == "system-design":
        # After system design, usually go to UI design
        if context.get("system_design_complete"):
            return "ui-design"

    if current_phase == "ui-design":
        # After UI design, go to build
        if context.get("ui_design_complete"):
            return "build"

    if current_phase == "build":
        # After build, go to supervision for packaging
        if context.get("build_complete"):
            return "supervision"

    # Default: Stay in current phase or start at requirements
    return current_phase or "requirements"
```

### Phase Transition Examples

```markdown
## Example 1: New Project

User: "I want to build a property management system"
→ Phase: requirements
→ Skill: windows-app-requirements

User: "Design the data model for properties and bookings"
→ Phase: system-design
→ Skill: windows-app-system-design

User: "Create the UI for the booking page"
→ Phase: ui-design
→ Skill: windows-app-ui-design

User: "Start coding the booking functionality"
→ Phase: build
→ Skill: windows-app-build

User: "Create an installer"
→ Phase: supervision
→ Skill: windows-app-supervision

## Example 2: Existing Project (Jump to Build)

User: "Fix this bug in the booking logic" + [code snippet]
→ Phase: build
→ Skill: windows-app-build
→ Rationale: Code provided, skip to implementation

## Example 3: Security Feature

User: "Add Google OAuth login"
→ Phase: build
→ Skills: windows-app-build + security-patterns-orchestrator
→ Rationale: Authentication implementation requires both build and security
```

---

## State File Management

### State File Format (claude-state.json)

```json
{
  "project_name": "PropertyManagementSystem",
  "current_phase": "build",
  "phases_completed": ["requirements", "system-design", "ui-design"],
  "requirements": {
    "user_stories_count": 15,
    "p0_stories_count": 8,
    "nfrs_defined": true,
    "last_updated": "2026-01-27T14:00:00Z"
  },
  "system_design": {
    "entities_count": 6,
    "api_endpoints_count": 12,
    "auth_strategy": "oauth-google",
    "last_updated": "2026-01-27T14:30:00Z"
  },
  "ui_design": {
    "pages_count": 10,
    "navigation_complete": true,
    "last_updated": "2026-01-27T15:00:00Z"
  },
  "build": {
    "build_id": "26027-1500",
    "features_implemented": 12,
    "tests_passing": true,
    "last_package_created": "2026-01-27T15:30:00Z"
  },
  "files": {
    "requirements": "docs/REQUIREMENTS.md",
    "system_design": "docs/DESIGN.md",
    "ui_design": "docs/UI-GUIDE.md",
    "changelog": "CHANGELOG.md",
    "build_package": "packages/PropertyManagementSystem-v1.0-26027-1500.zip"
  },
  "metadata": {
    "created": "2026-01-20T10:00:00Z",
    "last_modified": "2026-01-27T15:30:00Z",
    "claude_version": "claude-sonnet-4-5-20250929"
  }
}
```

### State Management Functions

```python
import json
from pathlib import Path
from datetime import datetime

class ProjectState:
    """Manage orchestrator state across sessions."""

    def __init__(self, state_file: Path = Path("claude-state.json")):
        self.state_file = state_file
        self.state = self.load()

    def load(self) -> dict:
        """Load state from file or create new state."""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        else:
            return self._create_initial_state()

    def save(self):
        """Save current state to file."""
        self.state["metadata"]["last_modified"] = datetime.utcnow().isoformat() + "Z"

        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def _create_initial_state(self) -> dict:
        """Create initial state for new project."""
        return {
            "project_name": None,
            "current_phase": None,
            "phases_completed": [],
            "requirements": {},
            "system_design": {},
            "ui_design": {},
            "build": {},
            "files": {},
            "metadata": {
                "created": datetime.utcnow().isoformat() + "Z",
                "last_modified": datetime.utcnow().isoformat() + "Z",
                "claude_version": "claude-sonnet-4-5-20250929"
            }
        }

    def update_phase(self, phase: str, data: dict):
        """Update state for a specific phase."""
        self.state[phase].update(data)
        self.state[phase]["last_updated"] = datetime.utcnow().isoformat() + "Z"

        if phase not in self.state["phases_completed"]:
            self.state["phases_completed"].append(phase)

        self.save()

    def get_current_phase(self) -> str:
        """Get current phase."""
        return self.state.get("current_phase")

    def set_current_phase(self, phase: str):
        """Set current phase."""
        self.state["current_phase"] = phase
        self.save()

    def is_phase_complete(self, phase: str) -> bool:
        """Check if a phase is complete."""
        return phase in self.state.get("phases_completed", [])

    def get_phase_data(self, phase: str) -> dict:
        """Get data for a specific phase."""
        return self.state.get(phase, {})
```

---

## Multi-Skill Coordination

### Loading Multiple Skills

```python
def coordinate_multi_skill_task(task: str, context: dict) -> list[str]:
    """
    Determine which skills to load for multi-skill tasks.

    Returns: List of skill paths to load
    """

    skills_to_load = []

    # Example: OAuth implementation requires build + security
    if "oauth" in task.lower() or "authentication" in task.lower():
        skills_to_load.append("~/.claude/skills/windows-app/windows-app-build/SKILL.md")
        skills_to_load.append("~/.claude/skills/windows-app/security/security-patterns-orchestrator/SKILL.md")

    # Example: Form with file upload requires build + security
    if "form" in task.lower() and "upload" in task.lower():
        skills_to_load.append("~/.claude/skills/windows-app/windows-app-build/SKILL.md")
        skills_to_load.append("~/.claude/skills/windows-app/security/secure-coding-patterns/SKILL.md")

    # Example: Full audit requires build + all reference files
    if "audit" in task.lower() or "validate" in task.lower():
        skills_to_load.append("~/.claude/skills/windows-app/windows-app-build/SKILL.md")
        skills_to_load.append("~/.claude/skills/windows-app/windows-app-build/references/audit-checklists.md")

    # Example: Packaging requires build + supervision
    if "package" in task.lower() or "installer" in task.lower():
        skills_to_load.append("~/.claude/skills/windows-app/windows-app-build/SKILL.md")
        skills_to_load.append("~/.claude/skills/windows-app/windows-app-supervision/SKILL.md")

    return skills_to_load
```

### Coordination Patterns

```markdown
## Pattern 1: Sequential Skills (One After Another)

**Scenario:** User completes requirements and wants to start design

**Orchestration:**
1. Load requirements skill → gather user stories
2. User approves requirements
3. Unload requirements skill
4. Load system-design skill → design data model
5. Continue...

## Pattern 2: Parallel Skills (Multiple Simultaneously)

**Scenario:** User wants to implement OAuth (authentication + security)

**Orchestration:**
1. Load windows-app-build skill (core implementation)
2. Load security-patterns-orchestrator skill (security guidance)
3. Both skills active during implementation
4. Build skill handles routes, security skill validates patterns

## Pattern 3: Primary + Reference Skills

**Scenario:** User debugging specific error from catalog

**Orchestration:**
1. Load windows-app-build skill (primary)
2. Load error-catalog.md reference (supporting)
3. Use catalog to identify root cause
4. Build skill implements fix

## Pattern 4: Hierarchical Skills (Orchestrator → Specialized)

**Scenario:** User wants to add OAuth

**Orchestration:**
1. Windows-app-orchestrator determines task is "build + authentication"
2. Load windows-app-build skill
3. Load security-patterns-orchestrator skill
4. Security orchestrator determines "authentication-patterns" needed
5. Load authentication-patterns skill
6. Three skills active: build, security-orchestrator, authentication-patterns
```

---

## Error Recovery Patterns

### Pattern 1: Wrong Skill Loaded

**Problem:** User loaded UI design skill but wants to write code.

**Recovery:**
```markdown
1. Detect mismatch:
   - User input contains code
   - Current skill is "ui-design"

2. Inform user:
   "I notice you want to implement code, but I'm currently in UI design mode. Let me switch to the build skill."

3. Transition:
   - Save UI design state
   - Load windows-app-build skill
   - Continue with implementation
```

### Pattern 2: Missing Prerequisites

**Problem:** User wants to build but no design documents exist.

**Recovery:**
```markdown
1. Detect missing prerequisites:
   - User requests "start coding"
   - No DESIGN.md or UI-GUIDE.md found

2. Ask user:
   "I don't see design documents for this project. Would you like to:
   a) Create requirements and design first (recommended)
   b) Build directly from your description (quick prototype)"

3. Based on choice:
   a) Load requirements skill → system-design → ui-design → build
   b) Load build skill with disclaimer about lack of design
```

### Pattern 3: Context Overflow

**Problem:** Too many skills loaded, approaching token limit.

**Recovery:**
```markdown
1. Detect context pressure:
   - Token usage > 80% of limit
   - Multiple large skills loaded

2. Prioritize skills:
   - Keep primary skill (windows-app-build)
   - Unload reference-only skills
   - Keep state in claude-state.json

3. Inform user:
   "To optimize performance, I'm unloading some reference skills. I can reload them if needed."

4. Continue with essential skills only
```

### Pattern 4: Unexpected User Request

**Problem:** User asks for something unrelated to current phase.

**Recovery:**
```markdown
1. Detect phase mismatch:
   - Current phase: "build"
   - User asks: "Create user stories for reporting feature"

2. Ask for clarification:
   "You're asking about requirements, but we're currently in the build phase. Would you like to:
   a) Add requirements for a new feature (switch to requirements phase)
   b) Implement the reporting feature based on current design (stay in build)
   c) Both (gather requirements first, then implement)"

3. Transition based on user choice
```

---

## Handoff Protocol Between Skills

### Requirements → System Design Handoff

**Requirements skill delivers:**
- User stories (prioritized)
- Acceptance criteria
- Non-functional requirements
- Domain glossary

**System design skill expects:**
- List of entities (derived from user stories)
- Business rules (from acceptance criteria)
- Performance/security requirements (from NFRs)

**Handoff format:**
```json
{
  "phase": "requirements",
  "deliverables": {
    "user_stories": "docs/REQUIREMENTS.md#user-stories",
    "nfrs": "docs/REQUIREMENTS.md#non-functional-requirements",
    "glossary": "docs/REQUIREMENTS.md#glossary"
  },
  "ready_for_design": true,
  "key_entities": ["Property", "Booking", "Guest", "Payment"],
  "key_workflows": ["Create Booking", "Check-In", "Check-Out", "Process Payment"]
}
```

### System Design → UI Design Handoff

**System design skill delivers:**
- Data models (entities and relationships)
- API endpoints (routes and methods)
- Authentication strategy

**UI design skill expects:**
- Entity fields (for forms)
- Relationships (for navigation)
- Endpoints (for actions)

**Handoff format:**
```json
{
  "phase": "system-design",
  "deliverables": {
    "data_model": "docs/DESIGN.md#data-model",
    "api_endpoints": "docs/DESIGN.md#api-endpoints",
    "auth_strategy": "docs/DESIGN.md#authentication"
  },
  "ready_for_ui": true,
  "forms_needed": ["Property Form", "Booking Form", "Guest Form"],
  "pages_needed": ["Dashboard", "Properties List", "Property Detail", "Bookings Calendar"]
}
```

### UI Design → Build Handoff

**UI design skill delivers:**
- Page inventory (all pages)
- Navigation flow
- Form specifications
- Template hierarchy

**Build skill expects:**
- Route names (from pages)
- Form fields (from specifications)
- Template structure (from hierarchy)

**Handoff format:**
```json
{
  "phase": "ui-design",
  "deliverables": {
    "page_inventory": "docs/UI-GUIDE.md#page-inventory",
    "navigation": "docs/UI-GUIDE.md#navigation",
    "forms": "docs/UI-GUIDE.md#forms"
  },
  "ready_for_build": true,
  "routes_to_implement": [
    {"path": "/", "method": "GET", "template": "index.html"},
    {"path": "/properties", "method": "GET", "template": "properties/list.html"},
    {"path": "/properties/new", "method": "GET/POST", "template": "properties/form.html"}
  ]
}
```

---

## Orchestrator Exit Gates

### When to Exit Each Phase

**Requirements phase complete when:**
- [ ] At least 5 user stories documented
- [ ] P0 stories identified
- [ ] NFRs defined (performance, security, usability)
- [ ] User approves requirements

**System design phase complete when:**
- [ ] All entities modeled
- [ ] Relationships defined
- [ ] API endpoints specified
- [ ] Authentication strategy chosen
- [ ] User approves design

**UI design phase complete when:**
- [ ] Page inventory created
- [ ] Navigation flow defined
- [ ] Forms specified
- [ ] User approves UI design

**Build phase complete when:**
- [ ] All P0 stories implemented
- [ ] Tests passing
- [ ] Build validated
- [ ] Package created

**Supervision phase complete when:**
- [ ] Service installed
- [ ] Health checks working
- [ ] Auto-start configured
- [ ] Production deployment successful

---

*End of Orchestration Patterns Reference*
