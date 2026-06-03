# PID Lock & Singleton Enforcement (Windows)

## Problem: Bot Instance Accumulation

Each Hermes background process (`terminal(background=true)`) is tied to a Hermes session context. When context compresses or rotates, the agent loses the `session_id` handle — but the Windows Python process continues running indefinitely.

### Actual Damage Found (May 2026)

In one cleanup session:
- **14× orphaned** `auto_trade.py` instances (all with live MT5 connections)
- **2× orphaned** `_ensemble_train.py` processes (training models against live data)
- **1× `terminal64.exe`** (MT5) kept alive by the Python parent processes
- Total: 17 rogue processes consuming memory, API quota, and broker connections

### Root Cause

Every time the bot was restarted via `terminal(background=true)`, a **new** Python process was spawned. The old `session_id` callback was lost on context compression, but the old process was never terminated because:
1. Hermes doesn't track spawned processes across compressed contexts
2. Windows doesn't automatically orphan-kill process trees
3. No PID lock file existed to prevent double-starts
4. `signal.SIGKILL` does NOT exist on Windows Python — old code's `os.kill(pid, signal.SIGKILL)` would silently crash with `AttributeError`, leaving the stale instance alive

## Solution: WMIC-Based Singleton (Rewrite)

Replaced the broken `os.kill(pid, signal.SIGTERM/SIGKILL)` chain with a WMIC process scan + `taskkill /F`. Located in:

| File | Method | Detects |
|------|--------|---------|
| `auto_trade.py` | `_lock_pid()` | Both `auto_trade.py` AND `run.py` instances |
| `run.py` | `enforce_singleton()` | Only `run.py` instances (defense-in-depth, runs before import) |

### How the WMIC Scan Works

```python
import subprocess

result = subprocess.run(
    ["wmic", "process", "where", "name like '%python%'",
     "get", "ProcessId,CommandLine,CreationDate", "/format:csv"],
    capture_output=True, text=True, timeout=10
)

# Parse CSV output: Node,CommandLine,CreationDate,ProcessId
for line in result.stdout.strip().split("\n"):
    if not any(t in line for t in ("auto_trade.py", "run.py")):
        continue
    parts = [p.strip() for p in line.split(",")]
    pid = int(parts[2])
    epoch = int(parts[3][:14])  # YYYYMMDDHHMMSS
    if pid != my_pid:
        rivals.append((pid, epoch))

# Kill ALL rivals (they are older since we just started)
for pid, epoch in rivals:
    subprocess.run(["taskkill", "/F", "/PID", str(pid)], timeout=5)
```

### Why WMIC + taskkill vs Old os.kill Approach

| Aspect | Old (os.kill) | New (WMIC + taskkill) |
|--------|---------------|----------------------|
| Detection | File-based `.noru.pid` only | Active WMIC scan — finds all instances even if lock file is missing |
| Kill reliability | `os.kill(pid, signal.SIGTERM)` may fail silently on Windows | `taskkill /F /PID` — guaranteed force-kill |
| `signal.SIGKILL` | **Does not exist on Windows** — `AttributeError` crash, exception NOT caught (caught OSError/ValueError only) | N/A — uses `taskkill` which always works |
| False positives | Only detected same-PID via lock file | Filters by script name in command line (`auto_trade.py` / `run.py`) |
| Cross-script detection | Only detects same process | Detects BOTH `run.py` AND `auto_trade.py` as the same bot |

### Important: Don't Use signal.SIGKILL on Windows

```python
# ❌ BROKEN on Windows — AttributeError, not caught by OSError/ValueError
os.kill(pid, signal.SIGKILL)

# ✅ WORKS on Windows
subprocess.run(["taskkill", "/F", "/PID", str(pid)], timeout=5)
```

Python's `signal` module on Windows only defines: `SIGABRT`, `SIGFPE`, `SIGILL`, `SIGINT`, `SIGSEGV`, `SIGTERM`. **No SIGKILL, no SIGQUIT, no SIGHUP.** Using any of these raises `AttributeError`.

### Lock File Cleanup

Lock file `.noru.pid` is still written as a secondary guard AND for verification. Cleanup now verifies ownership before deleting:

```python
def _unlock_pid(self):
    try:
        if os.path.exists(self._lock_path):
            with open(self._lock_path) as f:
                if f.read().strip() == str(os.getpid()):
                    os.remove(self._lock_path)
                    print("[LOCK] 🔓 Lock released")
    except Exception:
        pass
```

This prevents the wrong instance from deleting another instance's lock.

### Defense-in-Depth: Two Layers

```
run.py start
  ├── enforce_singleton()     ← Layer 1: kills other run.py instances
  │   └── WMIC scan for "run.py" → taskkill older
  ├── from auto_trade import ...  ← triggers auto_trade module load
  └── bot.start()
        └── _lock_pid()        ← Layer 2: kills auto_trade.py OR run.py instances
              └── WMIC scan for both scripts → taskkill older
```

Layer 1 runs before any import — catches `python run.py` duplicates immediately. Layer 2 catches `python auto_trade.py` direct runs AND any `run.py` instances that raced past Layer 1.

### Edge Cases

| Scenario | Behavior |
|----------|----------|
| `.run.pid` lock file missing | WMIC scan still finds the process via command line — kills it |
| Multiple Python versions running the script | WMIC filters by command line text, not by Python binary |
| Process started milliseconds apart | Both scan simultaneously → the one that completes `taskkill` last wins (the loser dies) |
| OS crash / power loss | On restart, `_lock_pid()` scans WMIC → finds no other instances → starts clean |
| `run.py` singleton kills `auto_trade.py` instance | ✅ Yes — `run.py`'s `enforce_singleton()` only looks for `run.py`. But `auto_trade._lock_pid()` (called inside `bot.start()`) detects `auto_trade.py` instances and kills them |

### Verification

After bot start:
```bash
# Check only one instance running:
wmic process where "name like '%python%' and (CommandLine like '%auto_trade%' or CommandLine like '%run.py%')" get ProcessId,CommandLine,CreationDate /format:csv

cat /c/Users/syahd/auto-trade-noru/.noru.pid
# Should match the Python PID
```

After bot stop:
```bash
ls /c/Users/syahd/auto-trade-noru/.noru.pid 2>&1
# Should say: No such file or directory
ls /c/Users/syahd/auto-trade-noru/.run.pid 2>&1
# Should say: No such file or directory
```

## Process Kill Chain (Full Stop)

When user says "stop bot", just killing `auto_trade.py` is NOT sufficient. Follow this chain:

### The Parent-Child Trap

```
Hermes session (background=true)
  └── Python auto_trade.py (PID X)
        └── mt5.initialize(path="terminal64.exe")
              └── terminal64.exe (PID Y)  ← MT5 GUI
```

When you kill `auto_trade.py` (PID X), `terminal64.exe` (PID Y) keeps running because:
- MT5 is a separate Windows process, not a child of Python in the traditional sense
- Python's `MetaTrader5` module initializes a separate terminal process
- The terminal can be re-parented to `winlogon.exe` or survive as orphan

**Worse**: Other orphaned Python instances (from earlier sessions) may keep terminal64.exe alive even after you kill the current one.

### Step-by-step (On This Windows System)

```bash
# 1. Kill the auto_trade process
process(action="kill", session_id="proc_xxx")  # Hermes method
# OR
kill -9 <PID>  # from ps aux

# 2. Find orphaned Python processes
powershell.exe -Command "Get-WmiObject Win32_Process -Filter \"Name='python.exe' OR Name='python3.12.exe'\" | Select-Object ProcessId, CommandLine | Format-Table -Wrap -AutoSize"

# 3. Kill bot PIDs (NOT Hermes PID 6032)
# Look for: auto_trade.py, "run.py", _ensemble_train.py
kill -9 <bot_PID_1> <bot_PID_2> ...

# 4. Kill MT5 terminal (may auto-restart from parent Python)
powershell.exe -Command "Get-Process terminal64 -ErrorAction SilentlyContinue | Stop-Process -Force"

# 5. If terminal64 keeps restarting, find parent chain:
powershell.exe -Command "Get-WmiObject Win32_Process -Filter \"Name='terminal64.exe'\" | ForEach-Object { \$parent = Get-Process -Id \$_.ParentProcessId -ErrorAction SilentlyContinue; Write-Output \"terminal64 PID=\`$(\$_.ProcessId) parent=\`$(\$_.ParentProcessId) \`$(\$parent.ProcessName)\" }"
# Kill the parent PID first, then terminal64

# 6. Final verification
ps aux | grep -E "auto_trade|ensemble_train|run\.py" | grep -v grep  # should be empty
powershell.exe -Command "Get-Process terminal64 -ErrorAction SilentlyContinue"  # should be empty
```

## Prevention (Active)

Since the WMIC-based singleton was deployed, fresh starts automatically detect and kill stale instances. The singleton renders process accumulation **impossible** — any new start kills all older instances before spawning.
