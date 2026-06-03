# Gold Tsunami — Complete Strategy Reference

> Discovered via `mixture_of_agents` (Claude Opus + Gemini Pro + GPT-5 + DeepSeek) when web research was blocked by bot detection. Captures the full strategy design for the XAUUSD 10,000% target.

## Core Thesis

**Trend + Momentum + Breakout** at 1:2000 leverage on demo. 50% risk per trade, aggressive compounding. NOT grid/martingale (guaranteed blowup at this risk level).

| Edge Source | Contribution | Why |
|-------------|-------------|-----|
| Trend Following (H1/H4/D1) | 40% | Direction filter — prevents counter-trend entries |
| Momentum Breakout (M5/M15) | 30% | Precise entry timing |
| Volatility Expansion (squeeze→breakout) | 20% | Catches explosive moves |
| Session Timing (London/NY overlap) | 10% | Gold's best liquidity window |

## Architecture

```
1-SECOND LOOP:
  Sync MT5 → Kill Switch Check → Update NHITS Forecasts (new bars only)
  → Fetch M15 Data → Detect Regime → Compute Indicators
  → Trailing Manager (all open positions) → Early Exit Check
  → Entry Scoring (0-100) → if ≥65: Execute → Log Performance (5min)
```

## Key Components

### 1. Regime Detection (2-tier filter)
- Squeeze = BB fully inside Keltner Channel = WAIT
- Ranging = ADX < 20 = NO TRADE
- Strong Trend = ADX > 30 = FULL RISK
- Breakout = squeeze release + ADX rising = HIGH CONFIDENCE
- Chaos = high ATR + low ADX = REDUCED SIZE

### 2. Multi-Level TP (the compounding engine)
After TP1 (2.5×ATR) closes 40% → SL moves to breakeven = remaining 60% is risk-free
After TP2 (4.0×ATR) closes 30% → ATR trail activates at 1.8×
After TP3 (7.0×ATR) closes 20% → trail tightens to 1.0×
Runner (10%) → trails indefinitely for outlier moves

### 3. Entry Scoring (weighted 0-100)
```
score = 0.40 * ensemble_agreement + 0.20 * regime_match + 0.25 * PA_alignment + 0.15 * session_vol
```
Threshold: 65 (1st pos), 75 (2nd pos). Below = skip.

### 4. Adaptive Risk
```
base_risk = 50%
after_1_loss → 35%
after_2_losses → 20%
after_3_losses → PAUSE 1hr
drawdown 25% → cap at 25%
drawdown 35% → cap at 15%
drawdown 40%+ → PAUSE
drawdown 60% → KILL SWITCH (close all)
```

### 5. Session Awareness
London-NY overlap (13-16 UTC) = +10 session score bonus (peak Gold)
Asian session = +1 (avoid)

## Numpy Indicator Engine Pattern

All indicators return numpy arrays. Pattern for each:

```python
def atr(high, low, close, period=14):
    tr = np.maximum(high - low,
                    np.maximum(np.abs(high - np.roll(close,1)),
                               np.abs(low - np.roll(close,1))))
    tr[0] = high[0] - low[0]  # first bar
    return ema(tr, period)     # sma also works
```

Compute once per cycle on M15 OHLCV (200 bars), index i=-1 for current value.

## ATR-Based SL/TP Formulas

```
sl_dist  = current_atr × SL_ATR_MULTIPLIER         (default 1.5)
tp1_dist = current_atr × TP1_ATR_MULTIPLIER         (default 2.5)
tp2_dist = current_atr × TP2_ATR_MULTIPLIER         (default 4.0)
tp3_dist = current_atr × TP3_ATR_MULTIPLIER         (default 7.0)

BUY:  entry = ask,  sl = entry - sl_dist,  tp = entry + tp_dist
SELL: entry = bid,  sl = entry + sl_dist,  tp = entry - tp_dist
```

## Lot Sizing with Confidence Boost

```python
risk_amount = equity × risk_pct × confidence
sl_ticks = sl_distance / tick_size
loss_per_lot = sl_ticks × tick_value
lots = risk_amount / loss_per_lot

# Margin constraint
margin_1lot = mt5.order_calc_margin(order_type, symbol, 1.0, price)
max_by_margin = (free_margin × 0.90) / margin_1lot
lots = min(lots, max_by_margin)

# Broker limits
lots = clip(lots, lot_min, lot_max)
lots = round(lots / lot_step) × lot_step
```

## Early Exit Conditions

1. **Ensemble flip**: direction reverses, confidence > 0.70, agreement > 0.71
2. **Chaos + loss**: regime = VOLATILE_CHAOS AND pnl_pct < -0.1%
3. **Time decay**: 50+ bars held without 0.3×ATR progress

## Kill Switch Implementation

```python
def _check_kill_switch(self):
    dd = 1 - (equity / peak_equity)
    if dd >= 0.60:
        self.close_all("kill_switch")
        return True  # halt trading
    return False
```

## Performance Dashboard (every 5 min)

Log: equity, balance, return%, drawdown%, open positions, total trades, win rate, consecutive losses, regime, uptime, cycle count.

## File Structure

```
gold_tsunami/
├── config.py              # TradingConfig dataclass
├── indicators.py          # numpy indicator engine
├── regime.py              # RegimeDetector (9 states)
├── signals.py             # Entry scoring 0-100
├── nhits_ensemble.py      # 7-TF NHITS lazy prediction
├── position_manager.py    # Adaptive sizing + order exec
├── trailing_manager.py    # Multi-TP partial close + trail
└── main.py                # 1s master loop
```

Or integrate components into existing auto_trade structure incrementally.
