---
title: MT5 Adapter Integration
description: Provide a reusable implementation for connecting to MetaTrader5 via the Python SDK, executing orders, retrieving account info and recent trades, and handling fallback when the SDK is unavailable.
name: mt5_adapter
category: engine
tags: [mt5, trading, adapter]
---

# MT5 Adapter Integration Skill

## Purpose
Provide a reusable implementation for connecting to MetaTrader5 (MT5) via the Python SDK, executing orders, retrieving account info and recent trades, and handling fallback when the SDK is unavailable.

## Trigger
Use when building or extending the trading engine to interact with a real MT5 demo/live account.

## Windows-Specific Notes (Git-Bash Environment)

When deploying on this system (Windows 10, git-bash):

### Finding Python
Python is NOT in PATH for git-bash by default. Use full paths:
```bash
/c/Users/<user>/AppData/Local/Programs/Python/Python312/python.exe
/c/Users/<user>/AppData/Local/Programs/Python/Python310/python.exe
```

### MT5 Terminal Path
Install location: `C:/Program Files/MetaTrader 5/terminal64.exe`
Pass to initialize: `mt5.initialize(path='C:/Program Files/MetaTrader 5/terminal64.exe')`

### Symbol Discovery
To find available gold symbols:
```python
symbols = mt5.symbols_get('*XAU*')
# Returns: XAUUSD, XAUEUR, #BTCXAU
```

### Order Type
XAUUSD on HFMarketsGlobal uses `ORDER_FILLING_IOC`. Use:
```python
"type_filling": mt5.ORDER_FILLING_IOC
```

### Unbuffered Output
When running in background with log redirect, use `python -u` to avoid buffered output.

### Key XAUUSD Details
- Digits: 2 (price quoted to 2 decimal places)
- Point: 0.01
- Spread: ~36 points (varies)
- Lot value: 1 standard lot = 100 oz, approx $100 per $1.00 move

## Steps
1. **Install SDK**: `pip install MetaTrader5`.
2. **Configure credentials** in `config.py` under `MT5` dict; values must be strings; no real keys stored—use `[REDACTED]` placeholder.
3. **Create adapter class** `Mt5Adapter` in `src/noru5/engine/execution/mt5_adapter.py`:
   - `__init__` attempts connection, sets `self.connected`.
   - `_connect` method with `mt5.initialize()`, `mt5.login()`, error handling.
   - `execute_order(signal: Signal) -> Dict[str, Any]` builds order request using lot, slippage, stoploss, takeprofit from config; calls `mt5.order_send`; returns dict with `ticket`, `deviation`, `retcode`; logs errors.
   - `get_account_info()` returns `{balance, equity, margin, currency}`.
   - `get_recent_trades(limit=5)` fetches recent deals via `mt5.history_deals()` and formats.
4. **Integrate** into `TradingEngine`:
   - Import `Mt5Adapter` and instantiate as `self.mt5_adapter`.
   - In `_loop`, when a signal triggers, call `self.mt5_adapter.execute_order(signal)` instead of stub.
5. **Unit test** (`tests/test_mt5_adapter.py`):
   - Mock `mt5.initialize`, `mt5.login`, `mt5.order_send`, `mt5.history_deals` using `unittest.mock`.
   - Verify that `execute_order` builds correct request dict and returns expected response.
   - Ensure graceful handling when `connected` is False (fallback to demo stub).
6. **Pitfalls & Tips**:
   - **⚠️ CRITICAL: `TRADE_ACTION_SLTP` resets unset fields**: When sending a SL/TP modification request, MT5 **zeros out any field not included**. Always retrieve the current position (`mt5.positions_get(ticket=...)`) and pass both SL and TP explicitly:
     ```python
     request["sl"] = new_sl if new_sl > 0 else (pos.sl or 0)
     request["tp"] = tp if tp > 0 else (pos.tp or 0)
     ```
     Also skip the modify call entirely if neither value changed:
     ```python
     if sl == (pos.sl or 0) and tp == (pos.tp or 0):
         return True  # nothing to do
     ```
   - **⚠️ Order filling: try multiple modes**: Not all brokers support all filling modes. Try IOC first, then FOK as fallback:
     ```python
     for mode_name, mode in [("IOC", mt5.ORDER_FILLING_IOC), ("FOK", mt5.ORDER_FILLING_FOK)]:
         request["type_filling"] = mode
         result = mt5.order_send(request)
         if result and result.retcode == mt5.TRADE_RETCODE_DONE:
             return success(result)
     ```
   - **⚠️ Symbol select may need retries**: After `mt5.initialize()`, `mt5.symbol_select()` can fail if the terminal is still syncing. Retry 3× with 1s delay:
     ```python
     selected = False
     for _ in range(3):
         if mt5.symbol_select(symbol, True):
             selected = True
             break
         time.sleep(1)
     ```
   - **⚠️ Connection retry with backoff**: `mt5.initialize(path=...)` can **start the terminal process** if it's not running, but needs time. Use exponential backoff:
     ```python
     for attempt in range(1, max_retries+1):
         if attempt > 1:
             time.sleep(min(attempt * 3, 30))
         if mt5.initialize(path=self.path):
             # success
             break
     ```
   - **⚠️ Microsoft Store Python causes IPC timeout**: If `python3` resolves to the Microsoft Store Python (`/c/Users/<user>/AppData/Local/Microsoft/WindowsApps/python3`), `mt5.initialize()` always fails with `(-10005, 'IPC timeout')` — the sandboxed Store Python can't access MT5's IPC named pipe. **Fix**: Use standalone Python at `/c/Users/<user>/AppData/Local/Programs/Python/Python312/python.exe`. Verify: `python -c "import sys; print(sys.executable)"` — must NOT contain `WindowsApps`.
   - **⚠️ Service-mode terminal64 can't be killed by normal taskkill**: When `tasklist | grep terminal64` shows `Services` under the user column, the terminal runs as `NT AUTHORITY\SYSTEM`. `taskkill /F /IM terminal64.exe` fails with `Access is denied`. **Fix**: Use elevated PowerShell — `powershell "Start-Process cmd '/c taskkill /F /PID <PID>' -Verb RunAs -Wait"`. Verify zero instances remain before re-initializing.
   - **⚠️ Path-only initialize may out-perform full-credential init**: Sometimes `mt5.initialize(path=..., timeout=60000)` succeeds but the version with `login/password/server` hangs or IPC-timeouts. This happens when the terminal was previously logged in and caches credentials. **Strategy**: Try path-only first as a faster probe:
     ```python
     init = mt5.initialize(path="C:/Program Files/MetaTrader 5/terminal64.exe", timeout=60000)
     if not init:
         mt5.shutdown()
         init = mt5.initialize(path=path, login=LOGIN, password=PASSWORD, server=SERVER, timeout=60000)
     ```
   - **⚠️ PREFERRED: Programmatic login via mt5.initialize() with credentials**: Instead of calling `mt5.initialize(path)` followed by `mt5.login(login, password, server)`, pass credentials directly to `mt5.initialize()` — it's more reliable and supports a timeout:
     ```python
     init_result = mt5.initialize(
         path=self.path,
         login=ACCOUNT["login"],
         password=ACCOUNT["password"],
         server=ACCOUNT["server"],
         timeout=30000  # 30s timeout in ms — critical to avoid hanging
     )
     ```
     This avoids hangs from `mt5.login()` when server name is wrong or terminal is in a bad state. The `timeout` parameter (milliseconds) ensures a clean failure instead of infinite blocking.
   - **⚠️ Kill ALL terminal64.exe processes before switching accounts**: MT5 terminal persists the last logged-in account. If a terminal64.exe is already running, `mt5.initialize()` will connect to it and ignore new login credentials — still returning you the old account. Before starting a bot with new credentials, always force-kill all instances:
     ```bash
     cmd //c "taskkill /F /IM terminal64.exe"
     ```
     Then verify none remain: `tasklist | grep -i terminal64`. The bot's `mt5.initialize()` will launch a fresh terminal with the new credentials.
   - **⚠️ Server name must be exact**: The `server=` string must match the broker's server name exactly, including spaces and numbers (e.g. `"HFMarketsGlobal-Demo 4"` not `"HFMarketsGlobal-Demo"`). Incorrect server names produce `(-6, 'Terminal: Authorization failed')` silently after timeout. Get the exact server string from MT5 terminal → File → Open an Account → find your account server.
   - **⚠️ Python buffered output hides errors**: When the bot hangs at `mt5.initialize()` with no output, it may be waiting on login. Run with `python -u` (unbuffered) to see real-time output. Combine with pty mode for live debugging: `terminal(command="python -u run.py", pty=True, timeout=120)`.
   - **⚠️ Terminal process may be killed (power loss)**: Wrap all MT5 calls in methods that call `ensure_connection()` first, which checks `mt5.terminal_info()` and re-initializes if False.
   - **Margin calculation**: Do NOT compute margin manually. Use `mt5.order_calc_margin(order_type, symbol, volume, price)` which handles broker-specific rules and currency conversion correctly, especially for non-USD account currencies like IDR. Example: `mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, "XAUUSD", 0.01, 4554.72)` returns the exact margin in account currency.
   - **Position type is integer, not string from MT5, but helper may convert**: `pos.type` returns 0 (BUY) or 1 (SELL) from MT5. If your adapter converts to strings `"BUY"/"SELL"`, make sure all code consuming positions (trailing stops, risk checks) handles both formats:
     ```python
     direction = "BUY" if pos_type in (0, "BUY") else "SELL"
     ```
   - **Risk sizing for non-USD accounts**: The `tick_value` from `mt5.symbol_info(symbol).trade_tick_value` gives the account-currency value per minimum price move for 1 lot. Use this for accurate position sizing: `lot = risk_amount / ((sl_distance / tick_size) * tick_value)`.
   - **Trailing stop with minimum distance**: When implementing trailing stops, only submit a modify request when the new SL improves the current SL by at least some minimum (e.g., 0.15 pips) to avoid `retcode=10025 (Invalid stops)` from the broker:
     ```python
     if new_sl > current_sl + min_trail_dist:
         return round(new_sl, 2)
     return 0  # no trailing needed
     ```
   - **Python buffered output with log redirect**: When running the engine as a background process with output redirection (`> log.txt 2>&1`), use `python -u` (unbuffered) to see output in real time instead of buffered.
   - **Credential leakage**: Never commit real passwords; always use `[REDACTED]` placeholder and load from environment if needed.
   - **Network latency**: Add a small `time.sleep(0.1)` after order send when testing.
   - **Demo vs live**: Use `account_type` check to differentiate; keep separate config entries if needed.
   - **Testing without internet**: Use `unittest.mock` to simulate successful and failed responses.
7. **Verification**
   Run `pytest tests/test_mt5_adapter.py` – should pass with mocked SDK.
8. **References**
   - MetaTrader5 Python SDK docs: https://www.mql5.com/en/docs/python
   - Hermes project config conventions: `config.py` uses `MT5` dict with keys `login`, `password`, `server`.
   - `references/xauusd_auto_trade_architecture.md` — Full end-to-end architecture for XAUUSD auto-trade bot (engine modules, blackout recovery, position sizing, order execution patterns, trailing stop, and MT5 error codes).
   - `references/mt5_adapter_setup.md` — Credential placeholder, install guide, basic usage.
   - `references/mt5_account_switch_debug.md` — Debug session notes on switching MT5 demo accounts: credential setup, terminal64 kill procedure, error codes for wrong server, and infinite-hang troubleshooting.

## Support Files
- `references/mt5_adapter_setup.md` – session‑specific setup notes and credential placeholder example.
- `references/mt5_multi_tf_analysis.md` — Multi-timeframe analysis pattern: fetch M5-D1 data, compute SMA/RSI/ATR, generate 3-panel matplotlib chart, structured bias prediction.