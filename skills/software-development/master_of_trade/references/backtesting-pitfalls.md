# Backtesting Gold Tsunami — Detailed Findings

## Session Context

Backtest of Gold Tsunami strategy on XAUUSD M15 data (Oct 2025 → May 2026, 15,000 bars).
Parameters: 50% risk/trade, 1.5× ATR SL, 2.5/4.0/7.0× ATR TP, 40/30/20/10% partial closes.

## Evolution of Results

| Version | Trades | Entry Logic | Notes |
|---------|--------|-------------|-------|
| v1 | 2 | NHITS-scoring proxy (threshold 65) | Way too strict, no NHITS |
| v2 | 298 | Loose same-direction filter | P&L over-inflated by buggy multiplier |
| v3 | 8 | Strict EMA cross + RSI extremes | Correct P&L but too few trades |
| v4 | 5→9 | Score-based (threshold 5→4) | Regime tracking broken by kill switch |

## Bug #1: Kill Switch Blocks Per-Bar Collection

### Discovery
Regime distribution showed 99.9% RNG despite ADX > 22 at 57.3% of bars.

### Root Cause
In `_go()` loop, regime tracking was placed AFTER the kill switch (DD ≥ 60%) check:

```python
for i in range(n):
    dd = 1 - eq / peak
    if dd >= 0.60:
        close_all()
        continue  # ← skips _regime(i) for this bar!
    
    _ = _regime(i)  # ← never reached after account blow
```

With 50% risk/trade, 2 losses → equity 25% of peak → DD 75% → ALL subsequent bars skip regime.

### Stats
- Total bars: 14,900 (post-warmup)
- Bars before blow: ~105 (immediately after warmup)
- Bars after blow with skipped regime: ~14,795

### Fix
```python
for i in range(n):
    _ = _regime(i)   # ← ALWAYS track first
    
    dd = 1 - eq / peak
    if dd >= 0.60:
        close_all()
        continue      # OK to skip trade logic, but data saved
```

## Bug #2: P&L Over-Inflation in v2

### Root Cause
Using `entry_equity * pnl_pct * t.volume * 100` instead of proper risk-reward ratios inflated returns to 15,740× unrealistically.

### Correct Formula
```
eq_delta = current_equity * total_pnl_fraction

Where:
  total_pnl_fraction = sum of each partial close's contribution
  
  TP1 hit:  pnl1 = init_risk × (tp1_dist/sl_dist) × 0.40
  TP2 hit:  pnl2 = init_risk × (tp2_dist/sl_dist) × 0.30
  TP3 hit:  pnl3 = init_risk × (tp3_dist/sl_dist) × 0.20
  SL hit:   if no TP hit: -init_risk
            else: remaining_risk × -1.0 (remaining portion hits SL)
  Trail:    remaining_risk × (trail_exit_move / sl_dist)
```

### Multiple Account Currency Pitfall
Never multiply equity by abstract factors. Use actual risk-reward ratios from ATR distances.

## Bug #3: ADX Regime vs Entry Logic Misalignment

### Root Cause
`_regime()` used `adx_trend = 22` while `_sig()` (entry signals) used hardcoded `25` and `18`.

### Fix
Consolidate all ADX thresholds to use the config value:
```python
if ax >= self.cfg.adx_trend + 3:   # strong trend (25)
    ...
elif ax < self.cfg.adx_trend - 4:   # range (18)
    ...
```

## Statistical Validity

### Minimum Trade Count
Using binomial confidence interval for winrate:
- 5 trades: WR could be 20-80% even with true WR of 50%
- 20 trades: ±20% margin of error at 95% CI
- 50 trades: ±14% margin of error
- 100 trades: ±10% margin of error

9 trades with 66.7% WR → true WR could be 30-92% → meaningless.

### How to Get Enough Trades
- Backtest 3+ years of M15 data (200,000+ bars)
- Or use lower timeframe (M5) for more bars
- Or use lower entry threshold to generate more signals
- Or use walk-forward cross-validation on shorter windows

## ADX Breakout Momentum — Validated Proxy Strategy

Tested as a pure ADX+DI strategy (no EMA/BB/NHITS) on XAUUSD M15, 15,000 bars, 15% risk/trade.

### Entry Logic
```
if ADX_i > 22 AND ADX_{i-5} < 22:    # ADX breakout from range
    if +DI > -DI: LONG
    if -DI > +DI: SHORT
```
SL = 1.5× ATR, TP = 2.5× ATR (close 50%, trail 50% at 1.2× ATR).

### Key Finding: LONG-Only Bias
| Filter | Trades | WR | Net Return |
|--------|--------|----|-----------|
| All signals | 34 | 32.4% | -29.2% |
| LONG only | 7 | 57.1% | +21.0% |
| SHORT only | 27 | 29.2% | -28.3% |

SELL signals dominate volume (27/34 = 79%) but are net negative. LONG signals have positive expectancy despite small sample. Gold's structural upward bias on M15 makes short ADX breakout entries unreliable without ensemble confirmation.

### Risk Scaling for Backtest Validity
With 50% risk/trade: 2 losses → equity at 25% of peak → kill switch kills ALL data. Solution:
1. Use 10-15% risk during backtesting to survive 6+ consecutive losses
2. Validate signal WR and R:R FIRST (without risk scaling)
3. Apply risk model mathematically after signal quality is proven
4. Scale results proportionally: 15% risk with 34 trades → 50% risk would produce same WR but fewer trades (account blows faster)

## Verification Checklist

Before trusting backtest results:
- [ ] Regime distribution matches external ADX stats (>22 in ~50-60% of bars)
- [ ] Trade count ≥ 50
- [ ] No kill switch blocking per-bar data collection
- [ ] P&L formula verified with manual calculation of 3 sample trades
- [ ] Entry threshold calibrated for proxy (no NHITS = lower threshold)
- [ ] No multiple consecutive identical P&L entries (indicates formula bug)
- [ ] Avg Loss % is NOT larger than risk_per_trade (indicates scaling bug)
- [ ] Max DD never exceeds kill switch threshold if kill switch is active
