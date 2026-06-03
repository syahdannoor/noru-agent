# Pine Script: Indicator to Strategy Conversion

## When to Convert
A Pine indicator produces visual signals (plots, lines, shapes, alerts). A Pine strategy wraps those signals with `strategy.entry()` / `strategy.exit()` for backtesting and automated execution. Convert when:
- The indicator generates clear long/short conditions (trend direction, momentum release, MA cross, structure break).
- You need P&L, winrate, drawdown, equity curve.
- You want to auto-trade the signal with TP/SL.

## Conversion Recipe

### 1. Change Declaration
```
indicator(...)  →  strategy(...)
```
Add `default_qty_type`, `default_qty_value`, `initial_capital`, `commission_value`, `pyramiding`.

### 2. Entry Conditions — Extract from Indicator
Every indicator signal maps to a boolean condition. Examples from V6.0a:

| Signal | Var | Convert |
|--------|-----|---------|
| Supertrend direction | `os` (0/1) | `upT = os == 1`, `dnT = os == 0` |
| Squeeze release up | `triangUp` | `sqzOff and dir > dir[1] and dir >= threshold` |
| Squeeze release down | `triangDown` | `sqzOff and dir < dir[1] and dir <= threshold` |
| EMA filter | `saveEntryBuy/saveEntrySell` | `MA2 < MA1` for buy, `MA2 > MA1` for sell |
| Structure break | `isStructureHighBroken/isStuctureLowBroken` | `close > structHigh` / `close < structLow` |

Combine with AND: `entryCond = trendUp and momentumUp and (filter or not filterEnabled)`

### 3. Strategy Exit with TP/SL
Always use `strategy.exit()` for risk management:
```
if entryCond
    strategy.entry("Long", strategy.long)
    strategy.exit("Long Exit", "Long",
     limit=close + atr * tpMult,    // take-profit
     stop=close - atr * slMult)     // stop-loss
```
Key: `limit` and `stop` are absolute price levels, not offsets.

### 4. Keep Visuals Intact
The strategy overlay can still show:
- **Plots**: `plot()` for ST, MA lines
- **Shapes**: `plotshape()` for entry/squeeze markers
- **Boxes**: `box.new()` for FVG zones
- **Lines**: `line.new()` for structure levels
- **Labels**: `label.new()` for BOS/CHoCH annotations

No need to remove visual code — the strategy simply layers execution on top.

### 5. SMC Structures in Strategy Context
SMC (BOS/CHoCH/FVG) are market-context visuals. They do NOT need to drive entry logic — keep them as overlay reference. The code that detects swing highs/lows and structure breaks is the same; just don't route them into `strategy.entry()` unless desired.

### 6. Alerts
Convert `alert()` calls to `alertcondition()` so the strategy can fire TradingView webhooks:
```
alertcondition(longEntry, 'Long Entry', '{{ticker}} {{interval}} LONG {{close}}')
```

## Pitfalls

### Indicator-vs-Strategy Discrepancy
- `indicator` executes on every tick; `strategy` respects `process_orders_on_close` / `calc_on_every_tick`.
- `plotshape` in indicator uses `location.bottom`/`location.abovebar` — these work identically in strategy.
- `strategy.exit()` SL/TP lines are NOT plotted by default — you must draw them manually if you want visual SL/TP lines like V6.0a did.

### K-Means Clustering in Strategy
V6.0a's clustering (`perfClusters`, `factorsClusters`) is computationally heavy. Strategy backtests re-run the clustering on every historical bar within `maxData`. This can be slow — consider simplifying or constraining `maxData` / `maxIter` for backtesting speed.

### Browser-based Pine Editor
When editing via browser tools (Monaco editor on TradingView):
- The page's accessibility tree can go empty randomly — navigate fresh if snapshot shows 0 elements.
- `browser_type` only works after a fresh `browser_snapshot` and clicking the editor textbox.
- The `editors` global object may or may not be available depending on page load.
- Monaco editor accepts plain text through its textbox role element.
- Long scripts must be typed in segments — no paste/load from file via API.

### Name Conflicts
Indicator uses `sources`, `length`, `basis`, `dev` — these are Pine built-ins or common names. Strategy should rename:
- `sources` → `src`
- `length` → `atrLen` (since `ta.atr(length)` shadows Pine's `length` constant)
- `val` → `sqzVal` (to avoid confusion with Pine's `val`)

## Strategy Template
```
//@version=6
strategy(title="Strategy Name", overlay=true,
 initial_capital=1000, default_qty_type=strategy.percent_of_equity,
 default_qty_value=5, pyramiding=0, commission_value=0.03,
 commission_type=strategy.commission.percent)

// --- INPUTS ---
// (mirror indicator inputs, rename to avoid conflicts)

// --- CALCULATIONS ---
// (copy indicator math verbatim)

// --- CONDITIONS ---
longEntry = trendUp and momentumUp and (filterOK or not filterEnabled)
shortEntry = trendDown and momentumDown and (filterOK or not filterEnabled)

// --- EXECUTION ---
if longEntry
    strategy.entry("L", strategy.long)
    strategy.exit("LX", "L", limit=close+atr*tp, stop=close-atr*sl)
if shortEntry
    strategy.entry("S", strategy.short)
    strategy.exit("SX", "S", limit=close-atr*tp, stop=close+atr*sl)

// --- VISUALS (optional) ---
// plots, shapes, FVG boxes, structure lines, labels

// --- ALERTS ---
alertcondition(longEntry, 'L Entry', '{{ticker}} LONG {{close}}')
```
