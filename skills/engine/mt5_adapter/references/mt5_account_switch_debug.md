# MT5 Account Switch Procedure — Debug Notes

## Scenario
Switch auto-trade bot from old demo account (49753341) to new one (235001316).

## Steps Taken (after failed attempts)

### 1. Update config.py
Add `password` field to ACCOUNT dict:
```python
ACCOUNT = {
    "login": 235001316,
    "password": "Noru1369!",
    "server": "HFMarketsGlobal-Demo 4",  # exact string including " 4"
}
```

### 2. Update mt5_connector.py
Replace separate `mt5.initialize(path)` + `mt5.login()` with single call:
```python
init_result = mt5.initialize(
    path=self.path,
    login=ACCOUNT["login"],
    password=ACCOUNT["password"],
    server=ACCOUNT["server"],
    timeout=30000  # 30 seconds
)
```
Import `ACCOUNT` from config.

### 3. Kill all terminal64.exe processes
Before starting, ensure no MT5 terminal is running:
```bash
cmd //c "taskkill /F /IM terminal64.exe"
# repeat until tasklist | grep -i terminal64 returns nothing
```

### 4. Delete PID lock file
The `.noru.pid` lock file may have stale PID:
```bash
rm -f /c/auto-trade-noru/.noru.pid
```

### 5. Run with unbuffered output + pty
```bash
cd /c/auto-trade-noru && python -u run.py
```
Use `pty=True` and `timeout=90` minimum — first launch starts terminal which takes 30-60s.

## Error Messages Encountered

### `(-6, 'Terminal: Authorization failed')`
- **Cause**: Server name incorrect. The user provided "HFMarketsGlobal-Demo 4" but I tried "HFMarketsGlobal-Demo" (without the " 4").
- **Fix**: Use the exact server string, including spaces and numbers. The MT5 Python API connects to this server name during `mt5.initialize()`.

### Infinite hang at mt5.initialize() with no output
- **Cause 1**: Existing terminal64.exe was still logged into old account. `mt5.initialize()` connected to it and ignored new credentials.
- **Cause 2**: `mt5.login()` called after `mt5.initialize()` could hang indefinitely if server name was wrong.
- **Fix**: Kill all terminal64.exe first, use `mt5.initialize()` with inline credentials + timeout.

### Output empty despite process running
- **Cause**: Python buffered output. Use `python -u` (unbuffered) flag.
- **Note**: Even with `-u`, the MT5 init/login phase produces no output until after connect succeeds. The first output is `[MT5] Connected | Login: ...`. Wait up to 60s for terminal launch.

## Verification
After successful connection, the log shows:
```
[MT5] Logged in to 235001316 @ HFMarketsGlobal-Demo 4
[MT5] Connected | Login: 235001316 | Server: HFMarketsGlobal-Demo4 | Balance: $678129.01
```
Note: The server appears with "Demo4" (no space) in the connected line — MT5 normalizes it.
