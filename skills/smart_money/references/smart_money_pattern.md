# Smart Money Pattern – Detectable Order‑Block Signals

## Overview
An **order‑block (OB)** is a candlestick (or small cluster of candles) that
represents a strong directional move detected by institutional participants.
When price later retraces only a fraction of that move before resuming the
original direction, the pattern is said to be **mitigated** – a key signal
for Smart Money entry/exit zones.

## Core Conditions (implemented in `smart_money.py`)

| Step | Condition | Parameter (config) | Typical Range |
|------|-----------|--------------------|---------------|
| 1️⃣ | **Body‑to‑Range Ratio** – The candle’s body must occupy a configurable fraction of its total range (high‑low). | `body_ratio` | **≥ 0.6** (default) |
| 2️⃣ | **Look‑back Window** – Scan the last *N* candles to locate the most recent OB. | `lookback` | **20‑40** candles |
| 3️⃣ | **Mitigation Check** – The following candle must retrace **no more than** `confluence_window` of the OB body. | `confluence_window` | **≤ 0.5** (50 % of OB body) |
| 4️⃣ | **Minimum OB Size** – The OB body must be larger than `min_ob_size` × recent average body. | `min_ob_size` | **≥ 0.02** (2 % of avg body) |
| 5️⃣ | **Directional Signal** – Bullish OB → `BUY`; Bearish OB → `SELL`. | – | – |
| 6️⃣ | **Confidence** – `confidence = min(OB_body / (avg_body × min_ob_size), 1.0)`. | – | **[0, 1]** |

## Visual Sketch

```
   High
    |
    |        ┌─────────────┐   ← Bullish OB (large body)
    |        │           │
Low ────┼──────│───────────│─────► Time →
    |        │           │
    └────────└───────────┘
          ↑   Retrace ≤ confluence_window ?
```

- If the next candle’s low (for a bullish OB) is within `confluence_window` of the OB’s close,
  the pattern is considered **mitigated** and a trade signal is emitted.

## Configuration (`config.SMART_MONEY`)

```yaml
SMART_MONEY:
  patterns:               # list of OB pattern identifiers (currently unused)
    - order_block_body_gt_60_range
    - bos_atr_factor_0.5
    - liquidity_pool_initial_sweep
    - fib_50_retrace_mitigation
  confluence_window: 0.5   # max retrace (fraction of OB body)
  lookback: 30             # candles to scan back for candidate OB
  body_ratio: 0.6          # min body / range ratio
  min_ob_size: 0.02        # min OB size relative to recent avg body
```

## Extending the Stub

When a full‑featured Smart Money model becomes available (e.g., LSTM, Gradient
Boosting, or a footprint‑analysis library), replace `SmartMoneyStrategy` with
the real implementation **while preserving** the same public signature:

```python
def generate_signal(self, df: pd.DataFrame, state: dict) -> Signal | None:
    ...
```

All other components (StrategyManager auto‑discovery, signal formatting,
confidence scoring) remain unchanged, ensuring zero ripple effects across the
codebase.

--- 
*This reference document is intentionally concise – it captures only the
essential logic and configuration needed for future developers to understand,
audit, or replace the placeholder detector.*