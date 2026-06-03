---
name: pine-script
description: Pine Script v6 development — convert indicators to strategies, manage TradingView scripts, handle Monaco editor quirks
category: trading
---

# Pine Script Development Guide

Covers converting Pine Script `indicator()` into `strategy()`, managing scripts via TradingView's web editor, and handling the Monaco/ACE editor constraints.

## Indicator → Strategy Conversion

Core recipe for turning a Pine indicator into a backtestable strategy:

### 1. Change declaration
Replace `indicator(...)` → `strategy(...)` with capital, pyramiding, and commission settings:
```pine
//@version=6
strategy(title="My Strategy", overlay=true, max_labels_count=500,
     initial_capital=1000, default_qty_type=strategy.percent_of_equity, default_qty_value=5,
     commission_type=strategy.commission.percent, commission_value=0.04)
```

### 2. Identify entry conditions
Scan the indicator for BUY/SELL signal booleans. Common patterns:
- Supertrend direction (`os == 1` for up, `os == 0` for down)
- Squeeze Momentum release (`sqzOff && dir > dir[1] && dir >= threshold`)
- Crossovers of moving averages
- RSI oversold/overbought

### 3. Add MA filter (optional)
```pine
MA1 = ta.ema(close, 9)
MA2 = ta.ema(close, 21)
saveEntryBuy = addsave ? MA2 < MA1 : false
buyCondition = baseBuyCondition and (saveEntryBuy or not addsave)
```

### 4. Entry with strategy.exit()
```pine
if buyCondition
    strategy.entry("Long", strategy.long)
    strategy.exit("XL", "Long",
         limit = close + atr * tpMultiplier,
         stop = close - atr * slMultiplier)
```

For partial TP pyramids, use multiple exit IDs per entry.

### 5. TP/SL from existing indicator logic
The indicator already calculates target/stop levels — reuse those vars. If none exist, derive from ATR:
```pine
tp = close + atr * targetMultiplier
sl = close - atr * stopLossMultiplier
```

### 6. Remove visual-only code
Strip SMC structures (BOS/CHoCH lines/labels), FVG boxes, Fibo overlays, dashboard tables — they don't affect strategy execution but consume compute.

### 7. Keep K-means / dynamic params
If the indicator uses clustering (like ST+SQZMOM's adaptive supertrend), keep it — it runs on each bar and affects signals.

## TradingView Editor Pasting

The Pine Editor uses Monaco (VS Code's editor). TEXTAREA VALUE SETTING DOES NOT WORK — Monaco owns its model and ignores programmatic textarea changes.

**Working approaches:**
- Click the editor textarea (visible as `[ref=e50]` in the a11y tree), then use Ctrl+A → Delete → type new code (works for short scripts)
- For long scripts (10K+ chars): save to local `.pine` file, tell user to open and paste manually
- Use the `navigator.clipboard` API is blocked without user gesture

**Pitfalls:**
- DO NOT try to set `textarea.value` + dispatch input event — Monaco will overwrite with spaces or corrupted content
- DO NOT try multiple appends to the same textarea — Monaco's internal model desyncs
- Opening a new "Untitled script" tab in Pine Editor gives a fresh Monaco instance

## Chart Interaction

When on a TradingView chart page (``tradingview.com/chart/...``):
- `View Only Mode` means user is not signed in; `Make a copy` (ref=e9) triggers sign-in prompt
- Click `Pine` (ref=e38) in the right toolbar to open the Pine Editor panel
- The currently-running strategy shows in the legend (`Open strategy report` button)
- To add a new script: paste in Pine Editor → click `Add to chart`

## References
- `references/strategy-conversion-details.md` — session-specific example from ST_SQZMOM_SMC V6.0a → strategy conversion
