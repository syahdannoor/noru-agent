# XAUUSD Auto-Trade Engine Architecture

## System Overview

A fully autonomous trading engine for XAUUSD on MetaTrader 5, built for the Indonesian Rupiah (IDR) demo account on HFMarketsGlobal. Designed to turn IDR 300K → $1,000 (~IDR 16.5M) via aggressive compounding.

### Module Structure

```
auto-trade-noru/
├── run.py                  # Entry point — initializes and starts the engine
├── auto_trade.py           # Main loop — tick cycle, signal evaluation, position management
├── mt5_connector.py        # MT5 connection with blackout recovery
├── strategy.py             # Signal generation (Smart Money + Technical confluence)
├── risk_manager.py         # Position sizing, SL/TP, drawdown guard, trailing stop
├── executor.py             # Order execution, modification, closing
├── config.py               # All parameters (risk, strategy, monitoring)
├── start_noru.bat          # Startup + auto-restart loop (for Windows)
├── watchdog.py             # Silent guardian process
├── noru_startup.vbs        # VBS launcher (silent, no console)
└── live_trade.log          # Running log
```

### Data Flow

```
MT5 Terminal
    ↕ mt5.initialize(path=...)
MT5Connector (ensure_connection → retry → backoff)
    ↓
Account Info → RiskManager (check_drawdown, daily_loss)
    ↓
StrategyEngine (D1 trend → H1 structure → M15 entry)
    ↓
Signal → RiskManager (position_size via order_calc_margin)
    ↓
Executor (market_order with IOC/FOK fallback)
    ↓
MT5 (position open)
    ↓
Loop (every 30s):
    check positions → trailing stop → PnL monitor → wait for new signals
```

## Blackout Recovery System

### Three Protection Layers

#### Layer 1 — MT5Connector with Retry

```python
def connect(self, max_retries=10):
    for attempt in range(1, max_retries+1):
        if attempt > 1:
            time.sleep(min(attempt * 3, 30))  # 3s, 6s, 9s, ... 30s
        if mt5.initialize(path=self.path):
            # Retry symbol_select (terminal may be syncing)
            for _ in range(3):
                if mt5.symbol_select(symbol, True):
                    return True
                time.sleep(1)
```

Every method calls `ensure_connection()` first, which checks `mt5.terminal_info()` and reconnects if False. After a power outage, `mt5.initialize(path=...)` can restart the MT5 terminal process from the installed path.

#### Layer 2 — Engine Crash Recovery

The main loop wraps each tick in a try/except so errors don't kill the engine:

```python
while self.is_running:
    try:
        self._tick()
    except Exception as e:
        print(f"[TICK ERROR] {e}")
        time.sleep(15)  # Brief pause, then continue
```

#### Layer 3 — Windows Startup Auto-Run

| File | Function |
|------|----------|
| `NoruAutoTrade.vbs` | Silent VBS launcher — placed in `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\` |
| `start_noru.bat` | Checks MT5 is running, starts engine, loops forever on crash |
| `watchdog.py` | Python guardian — ensures MT5 is running before engine start |

**Boot-to-Trade flow:**
1. PC power-on → Windows login
2. `NoruAutoTrade.vbs` auto-launches from Startup folder
3. `start_noru.bat` starts MT5 (`taskkill` stale Pythons → `start terminal64.exe` → wait 15s)
4. `python -u run.py` starts → `ensure_connection()` retries until MT5 is ready
5. On any crash, `start_noru.bat` restarts after 10s delay (infinite loop)

## Key MT5 Implementation Details

### Account Info (IDR Currency)

Account ID: 49753341 (HFMarketsGlobal-Demo, XAUUSD)
Currency: IDR (Indonesian Rupiah)
Leverage: 1:1000

Balance in IDR means:
- `mt5.account_info().balance` returns IDR value (e.g., 300,000.61)
- Margin calculations: `mt5.order_calc_margin()` returns IDR amount
- Profit values from positions: returns IDR
- Tick value from `symbol_info().trade_tick_value` is in IDR

### Order Execution Pattern

```python
# Build request
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": "XAUUSD",
    "volume": lot,
    "type": order_type,  # ORDER_TYPE_BUY or ORDER_TYPE_SELL
    "price": tick.ask if BUY else tick.bid,
    "deviation": 50,
    "magic": 123456,
    "comment": "Noru Auto",
    "type_time": mt5.ORDER_TIME_GTC,
}
# Only add SL/TP if non-zero (MT5 rejects 0 values on some brokers)
if sl > 0: request["sl"] = sl
if tp > 0: request["tp"] = tp

# Try IOC first, then FOK
for mode_name, mode in [("IOC", mt5.ORDER_FILLING_IOC), ("FOK", mt5.ORDER_FILLING_FOK)]:
    request["type_filling"] = mode
    result = mt5.order_send(request)
    if result and result.retcode == mt5.TRADE_RETCODE_DONE:
        success
```

### SL/TP Modification — Critical!

MT5's `TRADE_ACTION_SLTP` **zeros out any field not included**. Always:

```python
pos = mt5.positions_get(ticket=ticket)[0]
request = {
    "action": mt5.TRADE_ACTION_SLTP,
    "symbol": self.symbol,
    "position": ticket,
    "sl": sl if sl > 0 else (pos.sl or 0),
    "tp": tp if tp > 0 else (pos.tp or 0),
}
# Skip if nothing changed
if sl == (pos.sl or 0) and tp == (pos.tp or 0):
    return True
```

### Position Sizing for IDR Accounts

Use MT5's own margin calculator rather than manual formulas:

```python
# Find max lot affordable
lo, hi = 0.01, 1.0
for _ in range(8):
    mid = round((lo + hi) / 2, 2)
    margin = mt5.order_calc_margin(order_type, "XAUUSD", mid, entry_price)
    if margin <= free_margin * 0.95:
        lo = mid
        max_lot = mid
    else:
        hi = mid
```

### Trailing Stop Implementation

```python
min_trail_dist = 0.15  # Minimum 15 pips improvement to trail
if direction == "BUY":
    profit_pct = (current_price - entry) / entry * 100
    if profit_pct >= 0.5:  # 0.5% price activation
        new_sl = entry + (current_price - entry) * 0.3  # Lock 30% of profit
        if new_sl > current_sl + min_trail_dist:
            return round(new_sl, 2)
return 0  # No trailing needed
```

### Order Filling Modes

XAUUSD on HFMarketsGlobal supports `ORDER_FILLING_IOC`. `ORDER_FILLING_FOK` may also work but `SYMBOL_TRADE_EXECUTION` is typically `REQUEST_EXECUTION` (market execution) with `ORDER_FILLING_IOC` as primary. Always try IOC first, then FOK as fallback.

### ATR Calculation

```python
high_low = df["high"] - df["low"]
high_close = abs(df["high"] - df["close"].shift())
low_close = abs(df["low"] - df["close"].shift())
tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
atr = tr.rolling(14).mean().iloc[-1]
```

## Error Codes Encountered

| Code | Meaning | Fix |
|------|---------|-----|
| 10019 | Not enough money | Reduce lot, check margin `order_calc_margin()` |
| 10025 | Invalid stops (SL/TP) | SL/TP unchanged from current position — skip modify if same |

## XAUUSD Instrument Details (HFMarketsGlobal)

| Property | Value |
|----------|-------|
| Symbol | XAUUSD |
| Digits | 2 |
| Point | 0.01 |
| Tick Size | 0.01 |
| Tick Value | ~IDR 16,500 (varies with USD/IDR) |
| Spread | ~36 points typical |
| Lot value | 1 lot = 100 oz |
| Leverage | 1:1000 |
| Account Currency | IDR |
| Trade Mode | Market execution (REQUEST_EXECUTION) |
| Order Filling | IOC (primary), FOK (fallback) |
