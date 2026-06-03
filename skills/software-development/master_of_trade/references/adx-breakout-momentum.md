# ADX Breakout Momentum — Complete Strategy Spec

## Overview
Pure ADX + DI breakout strategy. No EMA, BB, NHITS, or scoring systems.
Enter when market transitions from ranging (ADX < threshold) to trending (ADX ≥ threshold).

## Entry Rules (M15)

### Condition (all must be true):
1. **ADX breakout**: `ADX[i] > threshold AND ADX[i-5] < threshold`
   - Threshold = 22 (default)
   - Breakout window: 5 bars (75 minutes on M15)
2. **DI confirmation**:
   - LONG: `+DI > -DI`
   - SHORT: `-DI > +DI`
3. **No position already open** (max 1 position)

### Cooldown:
- After loss: pause for 48 bars (12 hours on M15)
- After 3 consecutive losses: pause until manual reset
- No cooldown after wins

## Exit Rules

### Take Profit (first target):
- TP = 2.5× ATR from entry
- Close 50% of position at TP
- Move remaining SL to breakeven after TP hit

### Trailing:
- After TP hit: trail remaining 50% at 1.2× ATR
- BUY trailing: `new_sl = hi - (atr × trail_dist)` if `new_sl > old_sl`
- SELL trailing: `new_sl = lo + (atr × trail_dist)` if `new_sl < old_sl`

### Stop Loss:
- SL = 1.5× ATR from entry
- Breakeven after TP hit

## Risk Management

| State | Risk per Trade |
|-------|---------------|
| Normal | 15% |
| After 1 loss | 12% |
| After 2+ losses | 8% |
| DD ≥ 25% | 10% |
| DD ≥ 35% | 5% |
| DD ≥ 50% | STOP — manual reset |

## Backtest Results (XAUUSD M15, Oct 2025–May 2026)

### Full Results (LONG + SHORT):
- Trades: 34
- Winrate: 32.4% (11W / 23L)
- Avg Win: +10.5%
- Avg Loss: -6.0%
- Profit Factor: 0.84
- Max DD: 51.9%
- Net Return: -29.2%

### LONG Only:
- Trades: 7
- Winrate: 57.1% (4W / 3L)
- Avg Win: +10.5%
- Profit Factor: ~1.85 (est)
- Net Return: +21.0%

### SHORT Only:
- Trades: 27
- Winrate: 29.2% (7W / 20L)
- Net Return: -28.3%

## Key Insight
**LONG-only filter turns this from losing to profitable.** Gold's M15 data has strong upward structural bias. SHORT entries lose consistently. For pure ADX breakout, restrict to BUY signals only unless SHORT is confirmed by a higher timeframe (H1/H4) bearish structure.

## Configuration (backtest_adx.py template)
```python
@dataclass
class Config:
    symbol: str = "XAUUSD"
    start_balance: float = 500000
    risk_pct: float = 0.15          # 15% per trade
    max_pos: int = 1
    adx_threshold: float = 22
    adx_period: int = 14
    atr_period: int = 14
    sl_atr: float = 1.5
    tp_atr: float = 2.5
    tp_close: float = 0.50          # close 50% at TP
    trail_atr: float = 1.2          # trail at 1.2× ATR
    loss_cooldown: int = 48         # M15 bars = 12h
    consec_pause: int = 3
```

## Implementation Notes
- Use ADX(14) with smoothed DMI (not raw)
- Breakout window of 5 bars prevents re-entry during same trend
- Trail distance of 1.2× ATR allows room for pullbacks while locking profit
- 50% close at TP provides immediate P&L while runner captures extended moves
