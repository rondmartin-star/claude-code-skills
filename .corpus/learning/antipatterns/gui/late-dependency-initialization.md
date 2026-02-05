# Antipattern: Late Dependency Initialization

**Category:** GUI / Initialization
**Severity:** High
**First Seen:** 2026-02-05

---

## Problem

Creating child widgets or components BEFORE initializing the shared resources they depend on. This causes AttributeError when child initialization methods try to use parent resources that don't exist yet.

Common in GUI frameworks (PyQt, Tkinter, etc.) where adding widgets to containers triggers immediate initialization.

## Symptoms

- AttributeError: 'ClassName' object has no attribute 'dependency_name'
- Widgets fail to initialize properly
- Intermittent errors depending on initialization timing
- Errors only appear when specific tabs/panels load

## Consequences

**Severity:** High
- **User Impact:** Application launches but features fail with error dialogs
- **Business Impact:** Poor first impressions, support burden
- **Development Impact:** Hard-to-debug timing issues, refactoring overhead

## Root Cause

**Initialization Dependency Order Not Considered:**

In PyQt6/PyQt5, adding a tab to QTabWidget immediately creates and initializes the widget:

```python
def __init__(self):
    super().__init__()

    # 1. Create tabs container
    self.tabs = QTabWidget()

    # 2. Create meal plan tab
    self._create_meal_plan_tab()  # ← Runs immediately!
    # Inside this method:
    #   - Tab widget created
    #   - _load_meal_plans() called
    #   - _update_status() called
    #   - self.status_bar.showMessage() ← ERROR! status_bar doesn't exist yet

    # 3. Create status bar (TOO LATE!)
    self.status_bar = QStatusBar()  # ← Created after tabs tried to use it
```

## Prevention

### Rule
**Create all shared dependencies BEFORE creating child components that use them**

### Implementation

```python
# CORRECT Initialization Order
def __init__(self):
    super().__init__()

    # 1. Initialize shared resources FIRST
    self.status_bar = QStatusBar()
    self.setStatusBar(self.status_bar)

    self.service = ServiceClass()
    self.state = AppState()

    # 2. Create UI components that depend on resources
    self._create_menu_bar()      # Might use status_bar
    self._create_main_content()  # Tabs use status_bar, services
    self._create_toolbar()       # Uses services

    # 3. Connect signals
    self._connect_signals()

    # 4. Load initial data
    self._load_initial_data()
```

### Dependency Mapping

Before writing `__init__`, map out dependencies:

```
Dependencies:
  status_bar ← [meal_plan_tab, grocery_tab]
  recipe_service ← [recipe_tab, meal_plan_tab, grocery_tab]
  meal_plan_service ← [meal_plan_tab, grocery_tab]

Initialization Order:
  1. status_bar (no dependencies)
  2. recipe_service (no dependencies)
  3. meal_plan_service (no dependencies)
  4. tabs (depend on above)
```

### Pattern Template

```python
def __init__(self):
    """
    Initialization Order:
    1. Parent class initialization
    2. Instance variables
    3. Shared resources (services, state, status bar)
    4. UI structure (menus, toolbars, main widget)
    5. Signal connections
    6. Initial data loading
    """
    super().__init__()

    # Instance variables
    self.current_recipes = []
    self.current_meal_plan = None

    # Shared resources (CREATE FIRST)
    self._init_services()
    self._create_status_bar()
    self._init_state()

    # UI components (can now use resources)
    self._create_menu_bar()
    self._create_main_content()
    self._create_toolbar()

    # Connect signals
    self._connect_signals()

    # Load data
    self._load_initial_data()
```

## Detection

### Runtime Errors
```
AttributeError: 'RecipeManagerWindow' object has no attribute 'status_bar'
  File "main_window.py", line 287, in _create_meal_plan_tab
    self._load_meal_plans()
  File "main_window.py", line 629, in _load_meal_plans
    self._update_status(f"Loaded {len(plans)} meal plans")
  File "main_window.py", line 596, in _update_status
    self.status_bar.showMessage(message)
```

### Static Analysis

```python
# Linter rule idea: Check __init__ method structure
def check_init_order(cls):
    """Ensure dependencies created before use"""
    init_method = cls.__init__
    # Parse AST to find:
    # 1. All self.attr assignments
    # 2. All self.attr accesses
    # Flag if access comes before assignment
```

## Related Patterns

**Patterns:**
- `dependency-injection` - Inject dependencies rather than create in __init__
- `initialization-order-pattern` - Systematic approach to __init__
- `factory-pattern` - Centralize creation logic

**Antipatterns:**
- `create-on-demand` - Creating dependencies when first needed (lazy init)
- `no-init-order` - Random initialization without dependency consideration

## Framework-Specific Notes

### PyQt6 / PyQt5
- Adding widgets to containers triggers immediate initialization
- QTabWidget creates tab widgets when added
- Child widgets' `__init__` and load methods run immediately

### Tkinter
- Similar issue with Frame creation and pack/grid
- Child frames initialize when added to parent

### General GUI Frameworks
- Most GUI frameworks initialize child components immediately
- Assume child __init__ runs as soon as widget is created
- Plan initialization order accordingly

## Examples

### What NOT to do ❌

```python
def __init__(self):
    super().__init__()

    # Create tabs FIRST (BAD!)
    self.tabs = QTabWidget()
    self._create_meal_plan_tab()  # Tries to use status_bar ← ERROR!

    # Create status bar LATER (TOO LATE!)
    self.status_bar = QStatusBar()  # ← Should be before tabs!
```

### What TO do ✅

```python
def __init__(self):
    super().__init__()

    # Create dependencies FIRST ✓
    self.status_bar = QStatusBar()
    self.setStatusBar(self.status_bar)

    self.recipe_service = RecipeService()
    self.meal_plan_service = MealPlanService()

    # NOW create tabs ✓
    self.tabs = QTabWidget()
    self._create_meal_plan_tab()  # Can safely use status_bar ✓
```

### Refactoring Checklist

When hitting this error:

1. **Identify the missing dependency**
   - What attribute is missing? (e.g., status_bar)

2. **Find where it's created**
   - Search __init__ for: `self.status_bar = ...`

3. **Find where it's used**
   - Search for all uses: `self.status_bar.`

4. **Move creation earlier**
   - Move dependency creation before first use

5. **Test**
   - Verify application initializes without errors

## Occurrences

- **2026-02-05:** RecipeManager v2.0 - status_bar created after tabs, causing AttributeError in _load_meal_plans()

---

*Part of Learning Skills Ecosystem*
*Category: GUI / Initialization*
