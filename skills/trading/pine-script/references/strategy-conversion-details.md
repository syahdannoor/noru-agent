# ST_SQZMOM_SMC V6.0a → Strategy Conversion

Converted from a combined indicator (Supertrend + Squeeze Momentum + SMC structures + FVG + Fibo) into a pure strategy.

## Indicator Structure Recap

The V6.0a indicator has three independent signal layers:
1. **ST+SQZMOM** — dynamic supertrend (k-means clustered factors) + squeeze momentum oscillator → BUY/SELL signals + TP/SL lines
2. **SMC** — BOS/CHoCH structure breaks + FVG boxes (visual only, no entry logic)
3. **Fibo** — Fibonacci retracement/extension lines from current structure (visual only)

Strategy only needs layer 1.

## Signal Conditions Extracted

### BUY
```
upTrend = (os == 1)          // Supertrend bullish
triangUp = sqzOff            // Squeeze released
    and dir > dir[1]         // Momentum increasing
    and dir >= upperThreshold // Above threshold (ATR-adaptive or fixed)
buyCondition = upTrend and triangUp and (saveEntryBuy or not addsave)
```

### SELL
```
downTrend = (os == 0)
triangDown = sqzOff and dir < dir[1] and dir <= lowerThreshold
sellCondition = downTrend and triangDown and (saveEntrySell or not addsave)
```

### MA Filter
```
saveEntryBuy = MA2 < MA1  (EMA21 < EMA9)
saveEntrySell = MA2 > MA1 (EMA21 > EMA9)
addsave toggle enables/disables
```

## TP/SL from original

The indicator used these multipliers:
- TP1 = 1× ATR (stopLossMultiplier was also 3 but TP1 was 1 for basic 1:1)
- TP2 = 3× ATR
- TP3 = 5× ATR
- SL = 3× ATR

Original drew lines at these levels. In strategy, use `strategy.exit()` with `limit` and `stop`.

## Clustering Behavior

K-means runs only on recent bars (`last_bar_index - bar_index <= maxData`, default 1000). On historical bars outside this window, `perfclusters` is `na` and signals still fire using `target_factor = na` — the supertrend calc still works, just without adaptive factor optimization until enough bars pass.

This means backtest results on bars older than `maxData` use unoptimized factors. Set `maxData` high (e.g. 5000) to cover the full backtest range.

## Removed Visual Components

Removed to save compute and avoid strategy conflict:
- SMC structure lines/labels (BOS, CHoCH)
- FVG boxes and labels
- All 14 Fibonacci levels
- Dashboard table (cluster stats)
- Candle coloring gradient
- Trailing stop line drawing (replaced by strategy.exit stop)

## Kept Components
- Full k-means clustering loop
- Squeeze momentum oscillator
- MA calculations
- TP/SL at ATR multiples
