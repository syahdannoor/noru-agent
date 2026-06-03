---
name: smart_money
description: "Smart Money pattern detector – stub implementation loading config.SMART_MONEY parameters and emitting neutral placeholder signals, augmented with live detection notes for XAUUSD M5."
version: 0.1.0
author: Hermes Agent
license: MIT
tags: [trading, strategy, smart-money, placeholder, xauusd, noru5]
---
# Smart Money Strategy – NORU5 Implementation

This skill encapsulates the **SmartMoneyStrategy** that detects Smart Money Concept patterns (order blocks, Break of Structure, liquidity sweeps) and emits a `Signal`. The current implementation is a **placeholder** that loads parameters from `config.SMART_MONEY` and returns a neutral signal with the pattern list in the comment field.

## File Locations

| File | Description |
|------|-------------|
| `src/noru5/engine/strategies/smart_money.py` | Strategy module |
| `tests/test_smart_money.py` | Unit test |

## Purpose

- Load detection patterns from `config.SMART_MONEY` (order_block_body_gt_60_range, bos_atr_factor_0.5, liquidity_pool_initial_sweep, fib_50_retrace_mitigation).
- Accept `df: pandas.DataFrame` (OHLCV) and `state: dict` as inputs.
- Return a `Signal` (direction, source, confidence, comment) or `None`.
- Be auto‑discovered by `StrategyManager` via its `pkgutil`‑based import scan.

## Implementation Details

The class `SmartMoneyStrategy` inherits from `BaseStrategy` and provides a minimal `generate_signal`:

```python
from ..config import SMART_MONEY
from ..base import BaseStrategy, Signal

class SmartMoneyStrategy(BaseStrategy):
    def generate_signal(self, df, state) -> Signal | None:
        pattern_count = len(SMART_MONEY["patterns"])
        confluence = SMART_MONEY["confluence_window"]
        comment = f"Matched {pattern_count} pattern(s); confluence window = {confluence}"
        return Signal(direction="NEUTRAL", source="smart_money", confidence=0.5, comment=comment)
```

The detection logic is intentionally a **placeholder**. Replace the method body with real pattern detection (e.g., order‑block candle identification, liquidity‑sweep detection) while preserving the same signature.

## Unit Test

The file `tests/test_smart_money.py` contains a minimal test that creates a mock DataFrame and asserts `generate_signal` returns a non‑`None` `Signal` with the expected attributes (`signal_type`, `confidence`).

```python
import pandas as pd
from src.noru5.engine.strategies.smart_money import SmartMoneyStrategy

def test_generate_signal_returns_signal():
    strategy = SmartMoneyStrategy()
    df = pd.DataFrame({
        'open': [100, 101, 102, 103],
        'high': [102, 103, 104, 105],
        'low': [99, 100, 101, 102],
        'close': [101, 102, 103, 104],
        'volume': [1000, 1100, 1200, 1300],
    })
    signal = strategy.generate_signal(df, {})
    assert signal is not None
    assert hasattr(signal, 'direction')
    assert hasattr(signal, 'confidence')
```

## Integration

The strategy is auto‑discovered by `StrategyManager` because:

1. The file `smart_money.py` is placed under `src/noru5/engine/strategies/`.
2. The class name `SmartMoneyStrategy` matches the module mapping rule in `manager.py` (`if name == "smart_money": strategy_class_name = "SmartMoneyStrategy"`).
3. `StrategyManager._discover_strategies()` scans package modules and instantiates any class that subclasses `BaseStrategy`.

## Pitfalls

- The placeholder always returns `NEUTRAL`; a real implementation must differentiate `BUY`/`SELL`/`NEUTRAL`.
- Parameters (patterns list, confluence window) are static; volatility‑adaptive thresholds are left for future extensions.
- The auto‑discovery expects a corresponding `__init__.py` in the strategies folder (already present).
- If the class name convention changes (e.g., renaming the file), update the mapping in `manager.py`.

## Live Implementation Reference

A working, production-verified Order Block detection function is available in:
**`references/xauusd_order_block_live.py`**

This is NOT a placeholder. It was built and tested live on XAUUSD (HFMarketsGlobal-Demo, 2026-05-25) and correctly detected a bearish OB at $4,559 resistance. Use it as:
```python
from references.xauusd_order_block_live import detect_order_blocks
signal = detect_order_blocks(df_h1)
```

The function scans `lookback` candles for large-range candles (body/range ≥ `body_ratio`), then checks if price retraced into the OB zone (mitigation). Direction is inferred from candle color.

## Live Detection Notes

See `references/smart_money_live_detection.md` for condensed notes from live testing of Smart Money Concept patterns on XAUUSD M5, including validity criteria, implementation tips, and performance snapshot.

## Dependencies

- Python 3.10+
- pandas
- Access to `config.SMART_MONEY` dict (defined in `src/noru5/config.py`)