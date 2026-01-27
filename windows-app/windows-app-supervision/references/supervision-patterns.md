# Windows Process Supervision Patterns

Complete patterns for supervising Windows applications with NSSM, health monitoring, and automated restarts.

---

## NSSM (Non-Sucking Service Manager) Setup

### Installation

```batch
@echo off
setlocal EnableDelayedExpansion
title Service Installation
cd /d "%~dp0"

:: Check for Administrator privileges (auto-elevate if needed)
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process -Verb RunAs -FilePath '%~f0' -ArgumentList '%*'"
    exit /b
)

echo Installing application as Windows service...

:: Set variables
set "SERVICE_NAME=PropertyManagementSystem"
set "APP_DIR=%~dp0"
set "PYTHON_EXE=%APP_DIR%venv\Scripts\python.exe"
set "APP_SCRIPT=%APP_DIR%app\main.py"
set "NSSM_EXE=%APP_DIR%tools\nssm.exe"

:: Check if NSSM exists
if not exist "%NSSM_EXE%" (
    echo ERROR: NSSM not found at %NSSM_EXE%
    echo Please download NSSM from https://nssm.cc/download
    pause
    exit /b 1
)

:: Check if service already exists
sc query "%SERVICE_NAME%" >nul 2>&1
if %errorlevel% equ 0 (
    echo Service %SERVICE_NAME% already exists.
    echo Removing old service...
    "%NSSM_EXE%" stop "%SERVICE_NAME%"
    "%NSSM_EXE%" remove "%SERVICE_NAME%" confirm
    timeout /t 2 /nobreak >nul
)

:: Install service
echo Creating service: %SERVICE_NAME%
"%NSSM_EXE%" install "%SERVICE_NAME%" "%PYTHON_EXE%" "-m" "uvicorn" "app.main:app" "--host" "0.0.0.0" "--port" "8008"

:: Configure service
echo Configuring service parameters...

:: Set working directory
"%NSSM_EXE%" set "%SERVICE_NAME%" AppDirectory "%APP_DIR%"

:: Set startup type (automatic with delayed start)
"%NSSM_EXE%" set "%SERVICE_NAME%" Start SERVICE_DELAYED_AUTO_START

:: Set display name and description
"%NSSM_EXE%" set "%SERVICE_NAME%" DisplayName "%SERVICE_NAME%"
"%NSSM_EXE%" set "%SERVICE_NAME%" Description "Property Management System FastAPI application"

:: Set log file paths
"%NSSM_EXE%" set "%SERVICE_NAME%" AppStdout "%APP_DIR%logs\service.log"
"%NSSM_EXE%" set "%SERVICE_NAME%" AppStderr "%APP_DIR%logs\service-error.log"

:: Enable log rotation (10MB max, keep 5 files)
"%NSSM_EXE%" set "%SERVICE_NAME%" AppStdoutCreationDisposition 4
"%NSSM_EXE%" set "%SERVICE_NAME%" AppStderrCreationDisposition 4
"%NSSM_EXE%" set "%SERVICE_NAME%" AppRotateFiles 1
"%NSSM_EXE%" set "%SERVICE_NAME%" AppRotateOnline 1
"%NSSM_EXE%" set "%SERVICE_NAME%" AppRotateBytes 10485760
"%NSSM_EXE%" set "%SERVICE_NAME%" AppRotateFiles 5

:: Set restart behavior
"%NSSM_EXE%" set "%SERVICE_NAME%" AppExit Default Restart
"%NSSM_EXE%" set "%SERVICE_NAME%" AppRestartDelay 5000

:: Set process priority (normal)
"%NSSM_EXE%" set "%SERVICE_NAME%" AppPriority NORMAL_PRIORITY_CLASS

:: Set shutdown timeout (30 seconds)
"%NSSM_EXE%" set "%SERVICE_NAME%" AppStopMethodSkip 0
"%NSSM_EXE%" set "%SERVICE_NAME%" AppStopMethodConsole 5000
"%NSSM_EXE%" set "%SERVICE_NAME%" AppStopMethodWindow 5000
"%NSSM_EXE%" set "%SERVICE_NAME%" AppStopMethodThreads 5000
"%NSSM_EXE%" set "%SERVICE_NAME%" AppKillConsoleDelay 1500

:: Create logs directory if it doesn't exist
if not exist "%APP_DIR%logs" mkdir "%APP_DIR%logs"

:: Start the service
echo Starting service...
"%NSSM_EXE%" start "%SERVICE_NAME%"

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Service installed successfully!
    echo ========================================
    echo Service Name: %SERVICE_NAME%
    echo Status: Started
    echo Logs: %APP_DIR%logs\
    echo.
    echo To check status: nssm status %SERVICE_NAME%
    echo To stop: nssm stop %SERVICE_NAME%
    echo To start: nssm start %SERVICE_NAME%
    echo ========================================
) else (
    echo ERROR: Failed to start service
    echo Check logs at: %APP_DIR%logs\service-error.log
)

pause
```

---

## Health Check Implementation

### Health Check Endpoint (app/routes/health.py)

```python
from fastapi import APIRouter, HTTPException
from datetime import datetime
import psutil
import os
from sqlalchemy import text

from app.database import get_db
from app.config import settings

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and auto-restart logic.

    Returns:
        - status: "healthy" or "unhealthy"
        - timestamp: Current server time
        - uptime: Seconds since process started
        - database: Database connection status
        - disk: Free disk space
        - memory: Available memory
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.BUILD_ID
    }

    # Check process uptime
    try:
        process = psutil.Process(os.getpid())
        uptime_seconds = (datetime.now() - datetime.fromtimestamp(process.create_time())).total_seconds()
        health_status["uptime_seconds"] = int(uptime_seconds)
    except Exception as e:
        health_status["uptime_error"] = str(e)

    # Check database connection
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
        health_status["database"] = "connected"
    except Exception as e:
        health_status["database"] = "disconnected"
        health_status["database_error"] = str(e)
        health_status["status"] = "unhealthy"

    # Check disk space
    try:
        disk = psutil.disk_usage('.')
        health_status["disk_free_gb"] = round(disk.free / (1024**3), 2)
        health_status["disk_percent_used"] = disk.percent

        # Alert if disk > 90% full
        if disk.percent > 90:
            health_status["disk_warning"] = "Disk usage above 90%"
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["disk_error"] = str(e)

    # Check memory
    try:
        memory = psutil.virtual_memory()
        health_status["memory_available_gb"] = round(memory.available / (1024**3), 2)
        health_status["memory_percent_used"] = memory.percent

        # Alert if memory > 90% used
        if memory.percent > 90:
            health_status["memory_warning"] = "Memory usage above 90%"
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["memory_error"] = str(e)

    # Return appropriate status code
    if health_status["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=health_status)

    return health_status


@router.get("/health/ready")
async def readiness_check():
    """
    Readiness check - is the application ready to receive traffic?

    Returns 200 only if:
    - Database connection works
    - All critical services initialized
    """
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={"status": "not ready", "error": str(e)}
        )


@router.get("/health/live")
async def liveness_check():
    """
    Liveness check - is the application still running?

    Returns 200 as long as the process is alive.
    """
    return {"status": "alive", "timestamp": datetime.utcnow().isoformat()}
```

---

## Automated Restart on File Changes

### File Watcher Service (tools/file_watcher.py)

```python
import time
import os
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AppRestartHandler(FileSystemEventHandler):
    """Restart application when Python files change."""

    def __init__(self, service_name, debounce_seconds=2):
        self.service_name = service_name
        self.debounce_seconds = debounce_seconds
        self.last_restart = 0

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        # Only restart for Python files
        if not event.src_path.endswith('.py'):
            return

        # Debounce rapid changes
        current_time = time.time()
        if current_time - self.last_restart < self.debounce_seconds:
            return

        print(f"File changed: {event.src_path}")
        print(f"Restarting service: {self.service_name}")

        try:
            # Restart service using NSSM
            subprocess.run(
                ["nssm", "restart", self.service_name],
                check=True,
                capture_output=True
            )
            self.last_restart = current_time
            print(f"Service restarted successfully at {time.ctime()}")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to restart service: {e.stderr.decode()}")


def watch_directory(directory, service_name):
    """Watch directory for changes and restart service."""
    print(f"Watching {directory} for changes...")
    print(f"Will restart service: {service_name}")

    event_handler = AppRestartHandler(service_name)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nFile watcher stopped")

    observer.join()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python file_watcher.py <directory> <service_name>")
        print("Example: python file_watcher.py ./app PropertyManagementSystem")
        sys.exit(1)

    watch_dir = Path(sys.argv[1]).resolve()
    service_name = sys.argv[2]

    if not watch_dir.exists():
        print(f"ERROR: Directory not found: {watch_dir}")
        sys.exit(1)

    watch_directory(str(watch_dir), service_name)
```

### File Watcher Batch Script (scripts/watch-and-restart.bat)

```batch
@echo off
setlocal EnableDelayedExpansion
title File Watcher - Auto Restart Service
cd /d "%~dp0\.."

set "SERVICE_NAME=PropertyManagementSystem"
set "WATCH_DIR=app"

echo ========================================
echo File Watcher for %SERVICE_NAME%
echo ========================================
echo Watching directory: %WATCH_DIR%
echo Service will restart on Python file changes
echo Press Ctrl+C to stop
echo ========================================
echo.

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run file watcher
python tools\file_watcher.py "%WATCH_DIR%" "%SERVICE_NAME%"

pause
```

---

## Health Check Monitoring Script

### Health Monitor (tools/health_monitor.py)

```python
import requests
import time
import subprocess
from datetime import datetime

class HealthMonitor:
    """Monitor application health and restart if unhealthy."""

    def __init__(self, health_url, service_name, check_interval=60, failure_threshold=3):
        self.health_url = health_url
        self.service_name = service_name
        self.check_interval = check_interval
        self.failure_threshold = failure_threshold
        self.consecutive_failures = 0

    def check_health(self):
        """Check if application is healthy."""
        try:
            response = requests.get(self.health_url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                status = data.get("status", "unknown")

                if status == "healthy":
                    self.consecutive_failures = 0
                    print(f"[{datetime.now()}] Status: HEALTHY - Uptime: {data.get('uptime_seconds', 0)}s")
                    return True
                else:
                    print(f"[{datetime.now()}] Status: {status.upper()} - {data}")
                    self.consecutive_failures += 1
                    return False
            else:
                print(f"[{datetime.now()}] HTTP {response.status_code} - Service unhealthy")
                self.consecutive_failures += 1
                return False

        except requests.exceptions.RequestException as e:
            print(f"[{datetime.now()}] Health check failed: {e}")
            self.consecutive_failures += 1
            return False

    def restart_service(self):
        """Restart the Windows service."""
        print(f"\n{'='*50}")
        print(f"Failure threshold reached ({self.consecutive_failures}/{self.failure_threshold})")
        print(f"Restarting service: {self.service_name}")
        print(f"{'='*50}\n")

        try:
            # Stop service
            subprocess.run(["nssm", "stop", self.service_name], check=True, capture_output=True)
            time.sleep(5)

            # Start service
            subprocess.run(["nssm", "start", self.service_name], check=True, capture_output=True)

            print(f"Service restarted successfully at {datetime.now()}")
            self.consecutive_failures = 0

        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to restart service: {e.stderr.decode()}")

    def run(self):
        """Main monitoring loop."""
        print(f"Starting health monitor for {self.service_name}")
        print(f"Health URL: {self.health_url}")
        print(f"Check interval: {self.check_interval}s")
        print(f"Failure threshold: {self.failure_threshold}")
        print(f"{'='*50}\n")

        while True:
            is_healthy = self.check_health()

            if not is_healthy and self.consecutive_failures >= self.failure_threshold:
                self.restart_service()

            time.sleep(self.check_interval)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python health_monitor.py <health_url> <service_name>")
        print("Example: python health_monitor.py http://localhost:8008/health PropertyManagementSystem")
        sys.exit(1)

    health_url = sys.argv[1]
    service_name = sys.argv[2]

    monitor = HealthMonitor(health_url, service_name)
    monitor.run()
```

### Health Monitor Batch Script (scripts/monitor-health.bat)

```batch
@echo off
setlocal EnableDelayedExpansion
title Health Monitor
cd /d "%~dp0\.."

set "SERVICE_NAME=PropertyManagementSystem"
set "HEALTH_URL=http://localhost:8008/health"

echo ========================================
echo Health Monitor for %SERVICE_NAME%
echo ========================================
echo Health URL: %HEALTH_URL%
echo Auto-restart on failures
echo Press Ctrl+C to stop
echo ========================================
echo.

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run health monitor
python tools\health_monitor.py "%HEALTH_URL%" "%SERVICE_NAME%"

pause
```

---

## Graceful Shutdown Handling

### Shutdown Handler (app/main.py)

```python
from fastapi import FastAPI
import signal
import sys
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""

    # Startup
    print("Application starting...")
    # Initialize resources (database connections, etc.)
    yield

    # Shutdown
    print("\nShutdown signal received - cleaning up...")
    # Close database connections
    # Cancel background tasks
    # Flush logs
    print("Cleanup complete")


app = FastAPI(lifespan=lifespan)


def signal_handler(sig, frame):
    """Handle SIGINT (Ctrl+C) and SIGTERM."""
    print(f"\nReceived signal {sig} - initiating graceful shutdown...")
    sys.exit(0)


# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
```

---

## Log Management

### Log Rotation Configuration

```python
# app/logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app_name="app", log_dir="logs"):
    """Configure application logging with rotation."""

    # Create logs directory
    os.makedirs(log_dir, exist_ok=True)

    # Create logger
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)

    # Rotating file handler (10MB max, keep 5 files)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, f"{app_name}.log"),
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    file_handler.setFormatter(file_format)

    # Error file handler (separate file for errors)
    error_handler = RotatingFileHandler(
        os.path.join(log_dir, f"{app_name}-error.log"),
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_format)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)

    return logger
```

---

*End of Supervision Patterns Reference*
