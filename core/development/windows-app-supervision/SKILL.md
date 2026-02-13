---
name: windows-app-supervision
description: >
  Production-grade Windows process supervision with auto-start on boot, health
  monitoring, file change detection, and graceful restart. Use when: "auto-start",
  "boot on startup", "health checks", "watchdog", "supervisor daemon".
---

# Windows Application Supervision Skill

**Purpose:** Production-ready process supervision for Windows applications
**Version:** 1.0
**Size:** ~8 KB
**Related Skills:** windows-app-build (deployment section)

---

## LOAD THIS SKILL WHEN

**Trigger Phrases:**
- "Auto-start on boot" / "Start on reboot"
- "Add health checks" / "Monitor server health"
- "Restart on file change" / "Hot reload supervision"
- "Add supervisor" / "Process manager" / "Daemon"
- "Application didn't start after reboot"

**Context Indicators:**
- User has working FastAPI/uvicorn application
- Application needs production deployment on Windows
- User reports server not starting after reboot
- User wants automatic recovery from crashes

## DO NOT LOAD WHEN

- Still designing/building the application (use build skill)
- Linux/macOS deployment (different patterns)
- No working application yet

---

## Core Components

### 1. Task Scheduler Auto-Start (SYSTEM Account)

**Why SYSTEM:** No password prompt, runs before login, full access to Program Files.

```python
def install_task_scheduler(config):
    """Install Task Scheduler entry for boot-time auto-start."""
    python_exe = config.project_dir / "python" / "python.exe"
    script_path = config.project_dir / "scripts" / "supervisor.py"

    result = subprocess.run(
        [
            "schtasks", "/create",
            "/tn", "AppName\\Supervisor",
            "/tr", f'"{python_exe}" "{script_path}"',
            "/sc", "ONSTART",           # Run at system startup
            "/delay", "0001:00",        # 1 minute delay
            "/ru", "SYSTEM",            # No password needed
            "/rl", "HIGHEST",           # Admin privileges
            "/f"                        # Force overwrite
        ],
        capture_output=True,
        text=True,
        shell=True
    )
    return result.returncode == 0
```

**Uninstall:**
```python
subprocess.run(
    ["schtasks", "/delete", "/tn", "AppName\\Supervisor", "/f"],
    capture_output=True, shell=True
)
```

### 2. Health Check with Database Verification

```python
@app.get("/health")
async def health_check():
    """Health endpoint with database connectivity check."""
    from sqlalchemy import text

    db_status = "connected"
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
    except Exception as e:
        db_status = f"error: {str(e)}"

    overall_status = "healthy" if db_status == "connected" else "degraded"

    return {
        "status": overall_status,
        "app": APP_NAME,
        "version": APP_VERSION,
        "database": db_status
    }
```

**Health Checker Class:**
```python
class HealthChecker:
    def __init__(self, url, timeout=10, max_failures=3):
        self.url = url
        self.timeout = timeout
        self.max_failures = max_failures
        self.consecutive_failures = 0

    def check(self) -> bool:
        try:
            response = httpx.get(self.url, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                status = data.get("status")
                if status in ("healthy", "degraded"):
                    self.consecutive_failures = 0
                    return True
        except Exception:
            pass

        self.consecutive_failures += 1
        return False

    def should_restart(self) -> bool:
        return self.consecutive_failures >= self.max_failures
```

### 3. Restart Throttling (Prevent Crash Loops)

```python
class RestartThrottler:
    """Exponential backoff to prevent restart loops."""

    def __init__(self, backoff_seconds=None, stable_period=600):
        self.backoff_seconds = backoff_seconds or [0, 30, 60, 120, 300]
        self.stable_period = stable_period  # 10 minutes = reset
        self.restart_times = []

    def get_wait_time(self) -> int:
        """Return seconds to wait before next restart."""
        now = time.time()
        # Keep only recent restarts
        self.restart_times = [t for t in self.restart_times
                             if now - t < self.stable_period]

        if not self.restart_times:
            return 0

        idx = min(len(self.restart_times), len(self.backoff_seconds) - 1)
        return self.backoff_seconds[idx]

    def record_restart(self):
        self.restart_times.append(time.time())
```

### 4. Graceful Shutdown (Windows)

```python
class GracefulShutdown:
    @staticmethod
    def shutdown_process(process, timeout=30, logger=None):
        """Windows graceful shutdown sequence."""
        if process.poll() is not None:
            return True  # Already terminated

        pid = process.pid
        kernel32 = ctypes.windll.kernel32

        # Step 1: CTRL_BREAK_EVENT
        kernel32.GenerateConsoleCtrlEvent(1, pid)

        start = time.time()
        while time.time() - start < timeout:
            if process.poll() is not None:
                return True
            time.sleep(0.5)

        # Step 2: CTRL_C_EVENT fallback
        kernel32.GenerateConsoleCtrlEvent(0, pid)
        time.sleep(5)

        if process.poll() is not None:
            return True

        # Step 3: Force terminate
        process.terminate()
        process.wait(timeout=5)
        return False
```

### 5. File Change Watching with Debounce

```python
class CodeChangeHandler(PatternMatchingEventHandler):
    def __init__(self, callback, debounce=2.0):
        super().__init__(
            patterns=["*.py", "*.html", "*.js", "*.css"],
            ignore_patterns=["*.pyc", "*__pycache__*", "*.log", "*.db*"],
            ignore_directories=True
        )
        self.callback = callback
        self.debounce = debounce
        self._timer = None
        self._lock = threading.Lock()

    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.event_type not in ('modified', 'created', 'deleted'):
            return

        with self._lock:
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(
                self.debounce,
                self.callback,
                args=[event.src_path]
            )
            self._timer.start()
```

### 6. SQLite WAL Mode (Database Protection)

```python
def enable_wal_mode(db_path):
    """Enable Write-Ahead Logging for safe restarts."""
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA busy_timeout=30000")  # 30 seconds
    conn.close()
```

---

## Supervisor Configuration Template

```python
@dataclass
class SupervisorConfig:
    # Paths
    project_dir: Path
    logs_dir: Path = None
    pid_file: Path = None
    database_path: Path = None

    # Server
    server_host: str = "0.0.0.0"
    server_port: int = 8004

    # Health check
    health_check_interval: int = 900  # 15 minutes
    health_check_timeout: int = 10
    health_check_max_failures: int = 3

    # File watching
    watch_patterns: list = field(default_factory=lambda:
        ["*.py", "*.html", "*.js", "*.css"])
    watch_debounce: float = 2.0

    # Restart throttling
    throttle_backoff_seconds: list = field(default_factory=lambda:
        [0, 30, 60, 120, 300])
    throttle_stable_period: int = 600  # 10 minutes

    # Shutdown
    graceful_shutdown_timeout: int = 30
```

---

## Integration Checklist

Before deploying supervision:

- [ ] Application has embedded Python at known path
- [ ] Application runs on a static port (e.g., 8004)
- [ ] Database is in SYSTEM-accessible location (e.g., Program Files)
- [ ] Logs directory exists and is writable
- [ ] Health endpoint (`/health`) is implemented
- [ ] SQLite WAL mode enabled
- [ ] Required packages installed: `watchdog`, `httpx`

## Installation Commands

```batch
REM Run as Administrator
python scripts/supervisor.py --install

REM Verify installation
schtasks /query /tn "AppName\Supervisor" /v

REM Check status
python scripts/supervisor.py --status

REM Uninstall
python scripts/supervisor.py --uninstall
```

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Task doesn't run at boot | InteractiveToken + BootTrigger conflict | Use SYSTEM account |
| Restart loop | Server keeps crashing | Add restart throttling |
| Health check fails | Database locked | Enable WAL mode |
| Files not detected | Wrong patterns | Check watch_patterns config |
| Permission denied | Not running as Admin | Run install as Administrator |

---

## MSI Installer Build (WiX Toolset)

### Prerequisites

Install WiX Toolset from: https://wixtoolset.org/releases/

```batch
REM Verify WiX installation
where candle
```

### WiX Project Structure

```
installer/
├── ServiceDirector.wxs    # Main WiX project
├── license.rtf            # License for installer UI
├── python.wxs             # Auto-generated (heat.exe)
└── app.wxs                # Auto-generated (heat.exe)
```

### Build MSI Manually

```batch
REM Run build script
scripts\build-msi.bat

REM Output: dist\ServiceDirector-X.Y.Z-YYDDD-HHMM.msi
```

### Build MSI After Git Commit (Automated)

```batch
REM Setup post-commit hook
scripts\setup-git-hooks.bat

REM Now every commit automatically builds MSI
git commit -m "Add feature"
REM -> Triggers build-msi.bat

REM Disable automatic builds
echo. > .msi-build-disabled

REM Re-enable
del .msi-build-disabled
```

### WiX Key Concepts

```xml
<!-- Product GUID: changes each build (use "*") -->
<Product Id="*" ...>

<!-- UpgradeCode: NEVER changes (enables upgrades) -->
UpgradeCode="E8F7D6C5-B4A3-9281-7069-5E4D3C2B1A00"

<!-- Major Upgrade: removes old versions automatically -->
<MajorUpgrade DowngradeErrorMessage="..." />

<!-- Heat.exe: auto-harvest directories -->
heat dir "python" -cg PythonComponents -dr PythonDir ...
```

### Custom Actions (Install/Uninstall)

```xml
<!-- Install supervisor task on install -->
<CustomAction Id="InstallSupervisor"
    ExeCommand="[INSTALLFOLDER]python\python.exe scripts\supervisor.py --install"
    Execute="deferred" Impersonate="no" />

<!-- Uninstall supervisor task on uninstall -->
<CustomAction Id="UninstallSupervisor"
    ExeCommand="[INSTALLFOLDER]python\python.exe scripts\supervisor.py --uninstall"
    Execute="deferred" Impersonate="no" />
```

### MSI Deployment Commands

```batch
REM Silent install
msiexec /i ServiceDirector-5.2.0.msi /qn

REM Install with logging
msiexec /i ServiceDirector-5.2.0.msi /l*v install.log

REM Uninstall
msiexec /x ServiceDirector-5.2.0.msi /qn

REM Repair
msiexec /fa ServiceDirector-5.2.0.msi
```

---

## Full Supervisor Script Structure

```
scripts/
├── supervisor.py           # Main supervisor daemon
├── supervisor_config.py    # Configuration dataclass
└── install-supervisor.bat  # Installation helper
```

**Key Classes:**
- `SingleInstanceLock` - PID file locking
- `GracefulShutdown` - Windows signal handling
- `CodeChangeHandler` - Watchdog file monitoring
- `HealthChecker` - HTTP health verification
- `RestartThrottler` - Exponential backoff
- `ServerSupervisor` - Main coordinator

**Entry Points:**
- `python supervisor.py` - Run daemon
- `python supervisor.py --status` - Check status
- `python supervisor.py --install` - Install auto-start
- `python supervisor.py --uninstall` - Remove auto-start

---

*End of Windows Application Supervision Skill*
