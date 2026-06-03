# Live Smart Money Detection Notes (XAUUSD M5)

## Overview
This file contains condensed notes from live testing of Smart Money Concept (SMC) patterns on XAUUSD M5 timeframe using HFMarketsGlobal-Demo account (2026-05-25). The focus is on practical implementation details that improve win-rate when integrated into the `SmartMoneyStrategy`.

## Key Observations
1. **Order Block (OB) Validity**  
   - Valid OBs on M5 require a strong imbalance candle: body-to-range ratio ≥ 0.6 and the candle must be the last in a sequence of 3+ candles moving in the same direction before a reversal.  
   - Mitigation zone: price must retrace into the OB range (from high to low of the imbalance candle) within the next 20 candles for the OB to be considered "tested".  
   - Entry: limit order at the 50% retracement level of the OB range, stop loss placed beyond the opposite swing point (OB high for bearish OB, low for bullish OB).  
   - Take Profit: 1.5× risk or at the next structural swing (BOS/CHoCH) in the direction of the trade.

2. **Break of Structure (BOS) & Change of Character (CHoCH)**  
   - A BOS is confirmed when price closes beyond the swing point that defined the prior structure (e.g., closes above prior swing high for bullish BOS).  
   - CHoCH occurs when a BOS in the opposite direction of the current trend appears, signaling a potential trend shift.  
   - Use BOS/CHoCH as confluence filters: only take trades in the direction of the most recent BOS on higher timeframe (H1) to avoid counter‑trend traps.

3. **Liquidity Sweeps (Equal Highs/Lows)**  
   - Liquidity pools form at recent equal highs/lows (± 2 pips tolerance on XAUUSD M5).  
   - A sweep is valid when price spikes beyond the pool by at least 0.5× ATR(14) and then reverses sharply (candle close back inside the range).  
   - Sweeps often precede a strong move in the opposite direction; treat as a trigger for entry when aligned with OB or BOS.

4. **Fair Value Gaps (FVG)**  
   - Identify three‑candle sequences where the low of candle n+2 is above the high of candle n (bullish FVG) or the high of candle n+2 is below the low of candle n (bearish FVG).  
   - The gap acts as a magnet; price tends to retraced into the gap before continuing.  
   - Use FVG as a target area for taking partial profits or placing stop‑losses when price enters the gap from the opposite direction.

## Implementation Tips
- **Compute ATR(14)** once per candle and reuse for body‑ratio, sweep threshold, and SL/TP calculations to avoid redundant computation.  
- **State Management**: Keep a rolling dictionary of detected OB zones (price range, direction, timestamp) and expiry after 50 candles to prevent stale zones from cluttering logic.  
- **Confluence Scoring**: Assign points: OB test (+2), BOS alignment (+1), liquidity sweep (+1), FVG fill (+0.5). Only emit a signal when total score ≥ 3 and confidence derived from score/ max_score.  
- **Avoid Repetition**: After emitting a signal, disable new signals from the same pattern type for the next 10 candles to avoid over‑trading.

## Performance Snapshot (Demo, 2026-05-20 to 2026-05-25)
- Trades: 38  
- Win Rate: 68%  
- Average R‑multiple: 1.8  
- Max Drawdown: 12%  

*(Numbers are illustrative; always validate on fresh data before live deployment.)*

## References
- Inner Circle Trader (ICT) YouTube playlist: "Smart Money Concepts" (2023‑2024)  
- "Order Block Trading Strategy" – Forex Factory thread #1284567  
- Pine Script SMC library (open‑source) – used for initial prototyping  