---
name: master_of_trade
title: Master of Trade
description: Advanced autonomous trading engine integrating MT5, Smart Money patterns, economics news, AI/ML analysis, risk‑managed execution, and continuous self‑learning for sustained profitability.
version: 0.9.0
author: Noru (Hermes Agent)
license: MIT
tags: [trading, strategy, mt5, economics, python, ai, ml, risk-management, backtesting, learning, growth-mindset, profitability]
---

# Overview
This skill defines a next‑generation autonomous trading agent that:

- Connects to **MetaTrader 5** (Python API, order types, market depth).  
- Detects **Smart Money** patterns and fuses them with AI‑generated signals.  
- Ingests **economic news** and **market sentiment** from RSS/ blogs.  
- Learns from **historical XAU/USD**, **Forex**, and commodity price series.  
- Stores **long‑term market memory** (risk parameters, successful patterns, regime shifts).  
- Manages **risk** with position‑sizing, stop‑loss, take‑profit, and drawdown limits.  
- Performs **backtesting & forward‑testing** on historical windows and validates out‑of‑sample performance.  
- Optimizes strategy parameters automatically (grid/smart search).  
- Executes an **autonomous learning loop** that logs outcomes, detects errors, and refreshes models.  
- Operates with a **growth mindset**: continuously audits performance, incorporates new data sources, and spawns sub‑agents for A/B testing.  
- Guarantees **profitability** through equity guards, minimum expectancy thresholds, and profit‑target locks.

# Knowledge Base
## 1. Metatrader 5
- Multi‑asset platform (FX, CFD, commodities, crypto).  
- Python SDK (`MetaTrader5`) for live ticks, historical CSV export, trade execution.  
- Concepts: symbols, ticks, orders, spreads, swap, market depth.

## 2. Ilmu Ekonomi
- Supply‑demand, interest‑rate impact on currency strength.  
- Inflation, CPI, central‑bank policy, GDP, employment data → market reaction.  
- Economic calendars & typical volatility impact.

## 3. Python for Financial
- `pandas`, `numpy` for DataFrame manipulation.
- Technical libraries: `ta`, `ta-lib`, `bt`.
- Data‑cleaning pipelines, resampling to M5/H1, feature engineering (MA, CCI, MACD, ATR).
- **⚠️ RSI dilarang untuk XAUUSD** — Gold trending terlalu kuat, RSI menghasilkan banyak false signal. Diganti **CCI (Commodity Channel Index)** untuk overbought/oversold. Lihat `§8 Analisis Teknikal` dan `references/cci-macd-for-gold.md`.

## 4. AI & Machine Learning for Financial
- Supervised: regression (price forecast), classification (up/down).  \n- Unsupervised: clustering of regime states, anomaly detection.  \n- Sequence models: LSTM, Temporal Convolutional Nets for time‑series.  
- **MQL5-Native NN Alternative (NeuroBook approach)**: Instead of Python-only models, neural networks can be implemented **directly in MQL5** with OpenCL GPU acceleration. This means inference runs inside MT5's Strategy Tester or live EA — no Python subprocess needed. The book provides complete MQL5 classes for: fully connected (perceptron), CNN, LSTM, Self-Attention, Multi-Head Attention, GPT decoder-only. Combined with Python for training/weight export → MQL5 for live inference. See `references/mql5-neurobook-neural-networks.md`.
- **Hybrid approach**: Use Python NHITS ensemble for medium-term trend (current setup) + MQL5-native fast model (e.g. CNN for pattern confirmation) inside the EA for tick-level signals. OpenCL ensures sub-second inference.<｜end▁of▁thinking｜>  \n- **NHITS Ensemble (Neural Hierarchical Interpolation)**: 4-model × 7-TF ensemble via PyTorch CUDA. **28 independent models** trained offline by `_ensemble_train.py`; forecasts averaged per TF, then **weighted consensus** across M3→D1 for final signal. Inference is **GPU-free** — `EnsembleLoader` reads pre-computed `ensemble_results.json`. Training is decoupled from the live loop (never blocks entry). See `references/nhits-pytorch-cuda.md`.
  - **TF Presets** (lookback → horizon, pool): M3=200→20 [4,8,12], M5=96→12 [2,4,8], M15=48→10 [2,4], M30=40→8 [2,4], H1=36→6 [2], H4=30→5 [2], D1=20→3 [1].
  - **4 variants per TF**: seed/depth/width diversity → robust average. Variants share per-TF preset but differ in architecture hyperparams.
  - **Weighted consensus**: weights equalized so H4/D1 don't dominate: M3=0.8×, M5=1.0×, M15=1.2×, M30=1.5×, H1=1.5×, H4=1.5×, D1=1.5×. Short TFs get equal or near-equal voice to long TFs. Agreement multiplier: ≥80%→1.0×, ≥50%→0.7×, else 0.4×.
  - **Decoupled training**: `_ensemble_train.py` runs as subprocess (kill bot first to free GPU). Results persist across bot restarts. No GPU needed during live trading.  \n- Ensemble: XGBoost, LightGBM for feature‑rich prediction.  \n- Reinforcement Learning basics for trade‑execution policies (future extension).

## 5. Historis GOLD/XAUUSD
- Long‑term chart shows 2000‑2025 cycles, key support/resistance at $1,800‑$2,000.  
- Correlation with USDX, inflation expectations.  
- Typical volatility patterns (spikes during geopolitical events).

## 6. Historis Forex Market
- Major pairs (EUR/USD, GBP/USD, USD/JPY) dominate volume.  
- Session overlaps (London‑NY, Tokyo‑London) affect liquidity.  
- Historical volatility clusters; GARCH‑type patterns.

## 7. How the Market Move
- Liquidity provision by banks, ECN, and HFT firms.  
- Order flow: market orders vs. pending orders, impact on price.  
- Liquidity sweeps and stop‑run dynamics.

## 8. Analisis Teknikal
- Chart patterns: head‑and‑shoulders, triangles, flags.
- Indicators: EMA, SMA, CCI (Commodity Channel Index), MACD, Bollinger Bands.
- **⚠️ JANGAN GUNAKAN RSI untuk XAUUSD**: RSI terlalu banyak false signal di gold yang trending kuat. Gunakan **CCI** sebagai gantinya — lebih akurat untuk mendeteksi overbought/oversold pada trending market.
- **CCI (Commodity Channel Index)**:
  - Level: >+100 = overbought (potensi reversal turun), <−100 = oversold (potensi reversal naik).
  - Di XAUUSD yang trending, CCI bisa staying di overbought/oversold = konfirmasi kekuatan trend, bukan sinyal reversal.
  - CCI cross ±100 = entry trigger, divergence CCI vs price = reversal signal.
- **MACD**: digunakan untuk konfirmasi momentum dan arah trend.
  - MACD line > signal line = bullish momentum.
  - MACD histogram meningkat = momentum menguat.
  - MACD cross zero = trend shift.
- **Multi‑timeframe confirmation** (wajib minimal 2 TF).

## 9. Price Action
- Candlestick patterns: engulfing, pin‑bar, inside‑bar.  \n- Support/resistance, break of structure, retracement vs. extension.  \n- Role of Fibonacci levels in conjunction with OB/FVG.
- **ICT/SMC Structural Analysis (via OpenMobius-skill)**: For deeper price-structure analysis, the installed `OpenMobius-skill` provides:
  - Order Block (OB) detection — institutional entry zones
  - Fair Value Gap (FVG) identification — imbalance zones likely to refill
  - Break of Structure (BOS) / Change of Character (CHoCH) — trend analysis
  - Premium/Discount zone mapping — smart money entry areas
  - Liquidity Sweep detection — stop-hunts before reversals
  - Fresh data mandate — always pulls live OHLCV from api.mobiusquant.ai, never uses cached prices
  - Chart annotation — renders OB/FVG/BOS directly on chart images
  - Use for entry confirmation: NHITS ML signal → SMC structural check → final entry decision

## 10. Fundamental Analisis
- Macro news: employment, CPI, central‑bank minutes.  
- Geopolitical risk and safe‑haven flows (XAUUSD).  
- Balance of trade, retail sales, PMI.

## 11. Risk Management
- Position‑sizing methods: fixed % of equity, volatility‑adjusted lot sizing, Kelly criterion. \n- Stop‑loss models: ATR‑based, percentage‑based, dynamic break‑even. \n- Take‑profit strategies: trailing stop (ATR‑based Chandelier exit), fixed TP, dynamic TP linked to market regime, **NHITS‑based TP override** (see §11.4 below).\n- **Risk‑budgeting** across symbols and timeframes.\n- Scalp counter only trades when ADX < threshold (default 20) indicating ranging market, and requires proximity to support/resistance to avoid whipsaw.\n- **max_positions**: Maximum total number of open positions allowed (combined BUY and SELL positions). For example, max_positions=2 allows: 2 BUY + 0 SELL, 1 BUY + 1 SELL, or 0 BUY + 2 SELL. To limit to 1 position total regardless of direction, set max_positions=1.\n- **Trailing stop logic** (simplified ATR-based, no extreme-price tracker):\n   * For BUY: `new_sl = current_price - atr * trail_dist`. Update if `new_sl > old_sl` (SL trails up as price rises).\n   * For SELL: `new_sl = current_price + atr * trail_dist`. Update if `new_sl < old_sl` (SL trails down as price drops).\n   * When price moves AGAINST the position, SL stays put (does NOT widen loss).\n   * `trail_dist` read from config key `trailing_distance_atr` (default 0.3).\n   * ⚠️ NOT from `trailing_atr_multiplier` (2.0) — that's for initial SL/TP calculation, not trailing.\n   * Debug log: `[TRAIL DEBUG] BUY: price=..., atr=..., dist=..., new_sl=..., old_sl=...` (similarly for SELL).\n   * Called every tick from `auto_trade._manage_positions()`. `get_trailing_stop(pos, current_price, atr)` → `trail_stop(current_price, position)`.\n- **Adaptive lot sizing by NHITS confidence**: base lot from fixed % risk, boosted by NHITS consensus confidence: `boost = 0.5 + (consensus_confidence × 1.5)`. **Capped at 1.5× total max boost** (min 1.1×, max 1.5× base lot regardless of confidence). Clamped to `lot_min`/`lot_max`.\\n  - ⚠️ **CRITICAL: Total lot boost from ALL sources must never exceed 1.5×.** The -64% drawdown was partly caused by StrategyEngine applying its own independent boost (4× amplification: 0.01→0.04 lot) on top of ensemble boost, turning a $90K loss into $356K. One source, one cap. No stacking.\n- **NHITS‑based TP (from short TFs)**: entry TP set to average of M3/M5/M15/M30 bullish forecasts only (not H4/D1). Ensures TP is reachable within 1-2 hours, not hours-to-days away like H4/D1 extremes. Auto-raises TP to minimum 2:1 risk-reward if short-TF forecast is too tight. Fallback: 0.5% ATR-based TP when no short-TF forecast aligns.\n- **Dynamic TP update during position**: while profiting, `_manage_positions()` re‑queries NHITS forecast. If latest forecast extends in position's direction, TP pushed further out (never pulled back).\n- **Early exit by opposing weight**: When position is in loss AND the opposing TF weight exceeds 30% of total ensemble weight, close immediately. For BUY: if sell_weight/total > 0.30 → exit. For SELL: if buy_weight/total > 0.30 → exit. Prevents holding through direction weakness without waiting for full ensemble flip. Only triggers on losing positions (profit < 0).\n- **Critical MT5 note**: When modifying SL/TP with TRADE_ACTION_SLTP, both SL and TP must be included in the request; otherwise MT5 resets the missing field to 0. Always retrieve the current position's SL and TP and pass both, even if only one is changing.  \n- Performance metrics: net P&L, win‑rate, expectancy, Sharpe, max‑drawdown, recovery factor.  \n- Out‑of‑sample validation: walk‑forward with rolling window (e.g., 30 days training, 7 days testing).  \n- Automation: schedule weekly forward‑test via `cronjob`.
- Stop‑loss models: ATR‑based, percentage‑based, dynamic break‑even. 
- Take‑profit strategies: trailing stop (ATR‑based Chandelier exit), fixed TP, dynamic TP linked to market regime, **NHITS‑based TP override** (see §11.4 below).
- **Risk‑budgeting** across symbols and timeframes.
- Scalp counter only trades when ADX < threshold (default 20) indicating ranging market, and requires proximity to support/resistance to avoid whipsaw.
- **Trailing stop logic** (simplified ATR-based, no extreme-price tracker):
   * For BUY: `new_sl = current_price - atr * trail_dist`. Update if `new_sl > old_sl` (SL trails up as price rises).
   * For SELL: `new_sl = current_price + atr * trail_dist`. Update if `new_sl < old_sl` (SL trails down as price drops).
   * When price moves AGAINST the position, SL stays put (does NOT widen loss).
   * `trail_dist` read from config key `trailing_distance_atr` (default 0.3).
   * ⚠️ NOT from `trailing_atr_multiplier` (2.0) — that's for initial SL/TP calculation, not trailing.
   * Debug log: `[TRAIL DEBUG] BUY: price=..., atr=..., dist=..., new_sl=..., old_sl=...` (similarly for SELL).
   * Called every tick from `auto_trade._manage_positions()`. `get_trailing_stop(pos, current_price, atr)` → `trail_stop(current_price, position)`.
- **Adaptive lot sizing by NHITS confidence**: base lot from fixed % risk, boosted by NHITS consensus confidence: `boost = 0.5 + (consensus_confidence × 1.5)`. **Capped at 1.5× total max boost** (min 1.1×, max 1.5× base lot regardless of confidence). Clamped to `lot_min`/`lot_max`.\n  - ⚠️ **CRITICAL: Total lot boost from ALL sources must never exceed 1.5×.** The -64% drawdown was partly caused by StrategyEngine applying its own independent boost (4× amplification: 0.01→0.04 lot) on top of ensemble boost, turning a $90K loss into $356K. One source, one cap. No stacking.
- **NHITS‑based TP (from short TFs)**: entry TP set to average of M3/M5/M15/M30 bullish forecasts only (not H4/D1). Ensures TP is reachable within 1-2 hours, not hours-to-days away like H4/D1 extremes. Auto-raises TP to minimum 2:1 risk-reward if short-TF forecast is too tight. Fallback: 0.5% ATR-based TP when no short-TF forecast aligns.
- **Dynamic TP update during position**: while profiting, `_manage_positions()` re‑queries NHITS forecast. If latest forecast extends in position's direction, TP pushed further out (never pulled back).
- **Early exit by opposing weight**: When position is in loss AND the opposing TF weight exceeds 30% of total ensemble weight, close immediately. For BUY: if sell_weight/total > 0.30 → exit. For SELL: if buy_weight/total > 0.30 → exit. Prevents holding through direction weakness without waiting for full ensemble flip. Only triggers on losing positions (profit < 0).
- **Critical MT5 note**: When modifying SL/TP with TRADE_ACTION_SLTP, both SL and TP must be included in the request; otherwise MT5 resets the missing field to 0. Always retrieve the current position's SL and TP and pass both, even if only one is changing.  
- Performance metrics: net P&L, win‑rate, expectancy, Sharpe, max‑drawdown, recovery factor.  
- Out‑of‑sample validation: walk‑forward with rolling window (e.g., 30 days training, 7 days testing).  
- Automation: schedule weekly forward‑test via `cronjob`.

## 13. Autonomous Learning & Self‑Improvement
- Persistent **Memory Integration**: store each trade’s signal, outcome, confidence, market regime.  
- Error detection: flag trades with negative expectancy; compute pattern of failures.  
- Model refresh: retrain AI/ML components when error threshold exceeded.  
- Knowledge base update: add newly discovered patterns or macro events.

## 14. Growth Mindset & Decision Excellence
- Continuous monitoring of performance dashboards.  
- Parameter audit: review risk limits and strategy rules periodically.  
- Embrace new data sources (e.g., additional news feeds, alternative data) as they become available.  
- Encourage experimentation: spawn sub‑agents for A/B testing of minor strategy tweaks.

## 15. Profitability Assurance
- Daily equity check; enforce stop‑trading if drawdown > X% of initial capital.  
- Minimum expectancy threshold before allowing new trades.  
- Profit‑target monitoring: lock‑in profits when daily/weekly profit exceeds target; optionally scale back exposure.

# Workflow
1. Initialize MT5 adapter.  
2. Pull latest candles for selected symbol.  
3. Run Smart Money detection and combine with AI/ML forecast.  
4. Pull latest economic headlines via News Ingestor, compute sentiment.  
5. Apply Risk Manager: compute lot size, set SL/TP, enforce max‑drawdown limits.  
6. Execute Backtesting / Forward‑test cycle on recent data.  
7. Apply Strategy Optimizer to refine parameters.  
8. Feed data into Autonomous Learning loop; update models if needed.  
9. Combine signals & execute order via MT5 adapter if profitability thresholds satisfied.  
10. Log outcome to Memory Integration for future learning.  
10a. Schedule next cycle with cronjob (e.g., every 5 min).  

# Quick Real-Time Market Scan

Live structural analysis for any symbol/timeframe. **Two data-source paths** — always prefer Path A when MT5 is connected.

## ⚠️ Step 0: Always Load OpenMobius-skill FIRST

Before ANY analysis, ALWAYS load and follow `OpenMobius-skill` for market structure:

1. `skill_view(name='OpenMobius-skill')` → load its `workflows/klines.md`
2. Try `kb_klines.py indicators --query "XAUUSD" --interval 5m` for SMC structural data
3. If supported, generate annotated chart: `kb_klines.py chart → render`
4. Output uses mandatory 4-section format: Conclusion, Analysis, Outcome Cases, Risks & Invalidation

**Why Mobius first**: Proper SMC analysis (exact OB/FVG levels, BOS/CHoCH timestamps, sweep detection, premium/discount zones) with annotated chart — far superior to any manual scraping.

## Path A: MT5 Data → Mobius Analysis (✅ Preferred — MT5 Active)

When MT5 terminal is connected, use this path. Native XAUUSD spot data, no GC=F premium, full timeframe range, broker-accurate prices.

### 1. Pull data from MT5

```bash
cd "C:/Users/syahd/auto-trade-noru"
/c/Users/syahd/AppData/Local/Programs/Python/Python312/python.exe -c "
import MetaTrader5 as mt5, json, time

path = 'C:/Program Files/MetaTrader 5/terminal64.exe'
if not mt5.initialize(path=path, timeout=30000):
    print('MT5 init failed:', mt5.last_error())
    exit()

login = 235001316
authorized = mt5.login(login, password='Noru1369!', server='HFMarketsGlobal-Demo4')
if not authorized:
    print('Login failed:', mt5.last_error())
    mt5.shutdown()
    exit()

mt5.symbol_select('XAUUSD', True)
time.sleep(2)

rates = mt5.copy_rates_from_pos('XAUUSD', mt5.TIMEFRAME_M5, 0, 200)
if rates is None:
    print('No data:', mt5.last_error())
    mt5.shutdown()
    exit()

rows = []
for r in rates:
    rows.append([int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]), float(r[5])])

out = {
    'exchange': 'mt5', 'market': 'spot', 'symbol': 'XAUUSD',
    'asset_class': 'commodity', 'interval': '5m', 'candles': rows
}
with open('C:/Users/syahd/AppData/Local/Temp/xauusd_m5_data.json', 'w') as f:
    json.dump(out, f, indent=2)

mt5.shutdown()
print(f'OK: {len(rows)} candles at {rows[-1][0]}')
"
```

### 2. Feed into Mobius local analyze

```bash
cd "C:/Users/syahd/AppData/Local/hermes/skills/market-data/OpenMobius-skill"
.venv/Scripts/python scripts/kb_klines.py analyze \
    --input "C:/Users/syahd/AppData/Local/Temp/xauusd_m5_data.json" \
    --output "C:/Users/syahd/AppData/Local/Temp/xauusd_m5_analysis.txt"

# Read analysis:
cat "C:/Users/syahd/AppData/Local/Temp/xauusd_m5_analysis.txt"
```

### 3. Render chart (if needed — may fail on low-RAM systems, see Pitfalls)

```bash
cd "C:/Users/syahd/AppData/Local/hermes/skills/market-data/OpenMobius-skill"
.venv/Scripts/python -c "
import json
with open('C:/Users/syahd/AppData/Local/Temp/xauusd_m5_data.json') as f:
    data = json.load(f)
candles = [{'time': c[0], 'open': c[1], 'high': c[2], 'low': c[3], 'close': c[4], 'volume': c[5]} for c in data['candles']]
panels = {'panels': [{'candles': candles, 'items': []}]}
with open('C:/Users/syahd/AppData/Local/Temp/xauusd_m5_annotated.json', 'w') as f:
    json.dump(panels, f, indent=2)
"

.venv/Scripts/python scripts/kb_klines.py render \
    --input "C:/Users/syahd/AppData/Local/Temp/xauusd_m5_annotated.json" \
    --output "C:/Users/syahd/AppData/Local/Temp/xauusd_m5_chart.png" \
    --theme dark --width 1400 --height 900
```

### 4. Synthesize analysis for the user

Use the features output (OB levels, FVG boundaries, BOS/CHoCH events, sweep detection) to produce a narrative report in the user's language with:
- **Trend Direction** (BOS/CHoCH sequence)
- **Key Levels** (OB support/resistance, FVG imbalance zones, sweep wick levels)
- **Entry Setup** (premium/discount, order block entry, invalidation below/above)
- **Risk** (level boundaries that would invalidate the structure)

## Path B: Web-Based Fallback (No MT5 Available)

Only when MT5 is unavailable/not connected. Provides live price, SMC structural indicators, and analysis using Yahoo Finance + Mobius local.

**Why MT5 first**: User explicitly corrected that MT5 data should be used when active. Web fallbacks use GC=F COMEX futures (~$36 premium over XAUUSD spot) and are less accurate.

### Fetch Yahoo Data → Mobius Analyze

```bash
# 1. Fetch M5 data from Yahoo Finance (GC=F tracks XAUUSD closely)
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=5m&range=1d" \
  -H "User-Agent: Mozilla/5.0" \
  -o "C:/Users/syahd/AppData/Local/Temp/yahoo_gc_raw.json"

# 2. Convert to Mobius format
cd "C:/Users/syahd/AppData/Local/hermes/skills/market-data/OpenMobius-skill"
.venv/Scripts/python -c "
import json
with open('C:/Users/syahd/AppData/Local/Temp/yahoo_gc_raw.json') as f:
    data = json.load(f)
result = data['chart']['result'][0]
timestamps = result['timestamp']
quotes = result['indicators']['quote'][0]
rows = []
for i in range(len(timestamps)):
    rows.append([timestamps[i], quotes['open'][i], quotes['high'][i],
                 quotes['low'][i], quotes['close'][i], quotes['volume'][i]])
out = {
    'exchange': 'comex', 'market': 'futures', 'symbol': 'GC=F',
    'asset_class': 'commodity', 'interval': '5m', 'candles': rows
}
with open('C:/Users/syahd/AppData/Local/Temp/xauusd_m5_rows.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f'Converted {len(rows)} candles')
"

# 3. Local feature extraction (same as Path A step 2)
.venv/Scripts/python scripts/kb_klines.py analyze \
    --input "C:/Users/syahd/AppData/Local/Temp/xauusd_m5_rows.json" \
    --output "C:/Users/syahd/AppData/Local/Temp/xauusd_m5_features.txt"
```

### TradingView Quick Check (Optional)

Navigate to TradingView symbol page for a quick visual overview:
```
https://www.tradingview.com/symbols/XAUUSD/
```

Key data to collect:
- **Overview**: current price, previous close, open, day's range, volume
- **Technicals → Oscillators**: CCI(20), ADX(14), MACD, Momentum(10), Williams %R, Bull Bear Power. **(Jangan pakai RSI)**
- **Technicals → Moving Averages**: EMA(10), SMA(10), EMA(20), SMA(20) levels and signals

### Synthesize Structured Analysis

Produce a report in the user's language with these sections:

**Price Snapshot**: Current price, daily change ($ + %), open, prev close, day range.

**Timeframe Performance**: 1d/5d/1m/6m/YTD/1y returns.

**Technical Summary**:
- Oscillators: count of Buy/Neutral/Sell → overall signal
- Moving Averages: count of Buy/Neutral/Sell → overall signal
- Key indicator values with signal color (🟢 Buy / 🟡 Neutral / 🔴 Sell)

**Bullish Case**: factors supporting upside (bounce from support, momentum signals, multi-day trend)

**Bearish Case**: factors supporting downside (below MAs, negative MACD, bearish monthly trend)

**Key Levels**: resistance (day high → psychological) and support (day low → prev close → psychological)

**Conclusion & Bias**: directional bias with clear entry/stop levels.

## 1. Fetch Live Spot Price
```bash
curl -s "https://api.gold-api.com/price/XAU"
```
Returns: price, change, timestamp in JSON (free, no key required).

## 2. Get Technical Indicators
Navigate to TradingView symbol page:
```
https://www.tradingview.com/symbols/XAUUSD/
```
- Read price, day range, change % from the overview snapshot.
- Click the **"Technicals"** tab for oscillator/MA data.
- Extract: RSI, Stochastic, CCI, MACD, Momentum, MA levels.
- Check multiple timeframes (1H, 4H, Daily) for confluence.

Key data to collect from the page:
- **Overview**: current price, previous close, open, day's range, volume, time-window returns (1d, 5d, 1m, 6m, YTD, 1y).
- **Technicals → Oscillators table**: CCI(20), ADX(14), MACD, Momentum(10), Williams %R, Bull Bear Power, Ultimate Oscillator. **(Jangan pakai RSI — false signal untuk XAUUSD)**
- **Technicals → Moving Averages table**: EMA(10), SMA(10), EMA(20), SMA(20) etc. — note each level and signal (Buy/Sell/Neutral).

## 3. Synthesize Structured Analysis
Produce a report in the user's language with these sections:

**Price Snapshot**: Current price, daily change ($ + %), open, prev close, day range.

**Timeframe Performance**: 1d/5d/1m/6m/YTD/1y returns.

**Technical Summary**:
- Oscillators: count of Buy/Neutral/Sell → overall signal
- Moving Averages: count of Buy/Neutral/Sell → overall signal
- Key indicator values with signal color (🟢 Buy / 🟡 Neutral / 🔴 Sell)

**Bullish Case**: factors supporting upside (bounce from support, momentum signals, multi-day trend)

**Bearish Case**: factors supporting downside (below MAs, negative MACD, bearish monthly trend)

**Key Levels**: resistance (day high → psychological) and support (day low → prev close → psychological)

**Conclusion & Bias**: directional bias with clear entry/stop levels.

## Pitfalls (Quick Real-Time Market Scan)
- ⚠️ **ALWAYS load OpenMobius-skill first for SMC analysis. Do NOT skip to manual TradingView/Yahoo scraping** — user corrected this workflow. Mobius produces proper structure (BOS, FVG, OB, sweeps) with exact price levels, not hand-guessed levels from a TradingView glance. Only fall back to manual methods when Mobius is confirmed unavailable for the asset/interval.
- ⚠️ **Prefer MT5 over web data when MT5 is active** — User explicitly corrected: "kenapa ga pake data dari metatrader 5, kan aktif". MT5 provides native XAUUSD spot data (no GC=F ~$36 premium), broker-accurate prices, and full timeframe range (M1–W1). Always use Path A first if MT5 login succeeds. Only fall back to Path B (Yahoo/TradingView) when MT5 connectivity fails.
- ⚠️ **Mobius forex:spot XAUUSD only supports daily (1d) interval** — intraday queries fail with "Interval not supported on forex:spot". Use MT5 data (Path A) as primary substitute; fall back to GC=F futures from Yahoo Finance (Path B) only when MT5 is unavailable.
- ⚠️ **kb_klines.py chart render may crash on low-memory Windows systems** — Playwright/Chromium rendering triggers "Your computer has run out of resources" (TargetClosedError) when system RAM is exhausted. Symptoms: Playwright-browser opens headless Chromium → broker process killed by OOM. 
  - **Fix A (data-only)**: Skip render step, synthesize report from feature analysis alone.
  - **Fix B (matplotlib fallback)**: Write a custom matplotlib chart with Agg backend as fallback. Close all heavy apps (VS Code, Chrome) first, then use a simple Python script with Agg backend:
    ```python
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import json, pandas as pd
    from mplfin import mpf  # or manual candlestick
    
    with open('data.json') as f:
        data = json.load(f)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), gridspec_kw={'height_ratios': [3, 1]})
    
    # Candlesticks via matplotlib
    df = pd.DataFrame(data['candles'], columns=['time','open','high','low','close','volume'])
    df['time'] = pd.to_datetime(df['time'], unit='s')
    # Manual OHLC lines
    for i, row in df.iterrows():
        color = '#26a69a' if row['close'] >= row['open'] else '#ef5350'
        ax1.vlines(row['time'], row['low'], row['high'], color=color, linewidth=0.8)
        ax1.vlines(row['time'], row['open'], row['close'], color=color, linewidth=3)
    
    # SMC annotations: OB zones, BOS lines, FVG regions
    # ... (custom matplotlib patches for each)
    
    # Formatting
    ax1.set_facecolor('#1e1e1e')
    fig.patch.set_facecolor('#1e1e1e')
    ax1.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig('chart.png', dpi=120, bbox_inches='tight')
    print('OK: chart.png')
    ```
  - **Fix C**: Close all heavy apps (VS Code, Chrome, etc.) before retrying the Playwright render.
- ⚠️ **Windows path mismatch between MSYS bash and Python** — Files written via bash `/tmp/` may not be found by the venv Python (which uses `C:\\Users\\...\\AppData\\Local\\Temp\\`). Always use absolute Windows paths (`C:/Users/.../Temp/`) when passing files between bash curl and Mobius Python scripts.
- ⚠️ **MT5 initialize timeout** — On first call after system boot or long idle, MT5 terminal may need 10-30s to start. Always use `timeout=30000` in `mt5.initialize()`. If it fails with `-10005 (IPC timeout)`, the terminal may be hung — kill terminal64.exe first with `taskkill /F /IM terminal64.exe`, wait 5s, then retry.
- TradingView has Cloudflare bot detection — if blocked, retry with browser_navigate. Some requests work where direct terminal curl to investing.com gets blocked.
- gold-api.com free tier has no history endpoint; only live spot price.
- Prices update every few seconds on TradingView — read the snapshot quickly, note the timestamp.
- Always state the timezone (GMT+7 WIB) and timestamp alongside prices.
- The Technicals tab shows Daily timeframe by default; click H4 or 1H tab for lower-timeframe confluence.

# Testing
- Unit tests for each module (MT5 mock, AI model inference, news sentiment, risk manager).  
- Integration test using backtesting harness to evaluate net‑PnL over a historical window and forward‑test out‑of‑sample performance.  
- Performance dashboard (HTML/console) summarizing trade count, win‑rate, Sharpe, max‑drawdown, expectancy, and profit‑target adherence.

# Real-Time Auto-Trade Deployment (Windows MT5)

Use this section when deploying an auto-trade engine that connects live to MT5.

## Project Structure

```
auto-trade-noru/
├── config.py            # All parameters: risk, strategy, MT5 path, monitor interval
├── mt5_connector.py     # MT5 connection, data fetching, account/positions (supports M1–W1)
├── strategy.py          # Smart Money + RSI + EMA + S/R + PA signal generator
├── nhits_forecast.py    # (DEPRECATED — use ensemble training instead) NHITS PyTorch CUDA engine
├── ensemble_loader.py   # Pre-computed ensemble: load JSON, weighted consensus, TF signals
├── risk_manager.py      # Position sizing, SL/TP, drawdown guard, trailing
├── executor.py          # market_order(), modify_position(), close_position()
├── auto_trade.py        # Main loop orchestrator (uses EnsembleLoader, no live NHITS)
├── run.py               # Entry point (has its own singleton guard: enforce_singleton())
├── scripts/
│   └── _ensemble_train.py  # Train 28 NHITS models → ensemble_results.json
├── ensemble/
│   └── ensemble_results.json  # Pre-computed forecasts (generated by _ensemble_train.py)
└── live_trade.log       # Auto-generated runtime log
└── .noru.pid            # PID lock file (auto-generated by auto_trade._lock_pid())
└── .run.pid             # PID lock file (auto-generated by run.py enforce_singleton())
```

## Module Responsibilities

| Module | Key Classes/Methods | Role |
|--------|-------------------|------|
| `config.py` | `MT5_CONFIG`, `RISK`, `STRATEGY`, `MONITOR` | Single source of truth for all params |
| `mt5_connector.py` | `MT5Connector.connect()`, `get_rates()`, `get_symbol_info()` | Wraps `MetaTrader5` SDK, auto-reconnect. TF mapping: M1..W1 |
| `strategy.py` | `StrategyEngine.analyze()` | Combines OB detection, trend, RSI, S/R, PA into buy/sell scores |
| `nhits_forecast.py` | `NHITSEngine.train()`, `predict_signal()`, `get_signal()` | PyTorch CUDA NHITS — M5/M3 presets, signal veto for auto_trade |
| `risk_manager.py` | `calculate_position_size()`, `calculate_sl_tp()`, `check_drawdown()` | 1% risk per trade, ATR-based SL/TP, trailing |
| `ensemble_loader.py` | `EnsembleLoader._load()`, `get_consensus()`, `get_tf_signal()` | Loads `ensemble_results.json`, weighted multi-TF consensus |
| `executor.py` | `market_order()`, `modify_position()`, `close_position()` | Sends/modifies/closes orders via MT5 |
| `auto_trade.py` | `AutoTradeNoru._tick()`, `_evaluate_entry()`, `_manage_positions()` | 1s cycle loop, uses `EnsembleLoader` instead of live NHITS |
| `run.py` | `enforce_singleton()` + `AutoTradeNoru()` | Entry point — WMIC singleton guard (kills older instances), then delegates to `auto_trade.py` |

## Deployment Steps (Windows + Git-Bash)

1. **Verify Python & MT5 SDK**:
   ```bash
   /c/Users/<user>/AppData/Local/Programs/Python/Python312/python.exe -c "import MetaTrader5; print(MetaTrader5.__version__)"
   ```

2. **Verify MT5 Terminal** installed at `C:/Program Files/MetaTrader 5/terminal64.exe` — pass this path to `mt5.initialize(path=...)`.

3. **Start the engine**:
   ```bash
   cd /c/Users/<user>/auto-trade-noru
   /c/Users/syahd/AppData/Local/Programs/Python/Python312/python.exe -u run.py
   ```
   The `-u` flag is **critical** for unbuffered output when redirecting to log file.

4. **Run in background with log**:
   ```bash
   nohup python -u run.py > live_trade.log 2>&1 &
   ```

## Telegram Execution Reporting

Every MT5 execution (OPEN/MODIFY/CLOSE) is logged to `logs/executions.jsonl` as JSON lines. A **cron job** (`no_agent=True`) tails this file and delivers new events to Telegram every minute.

### Setup

```bash
# 1. Copy reporter script to Hermes scripts dir (done once)
cp /c/Users/syahd/auto-trade-noru/scripts/telegram_reporter.py ~/AppData/Local/hermes/scripts/

# 2. Create cron (done once)
# cron name: "Telegram Execution Reporter"
# schedule: every 1m
# no_agent: True
# script: telegram_reporter.py
# workdir: C:\Users\syahd\auto-trade-noru
# deliver: origin (auto-sends to current Telegram chat)
```

### How it works
- `auto_trade.py` calls `_log_execution(action, **kwargs)` at every order open/modify/close
- Writes structured JSON to `logs/executions.jsonl`
- `telegram_reporter.py` (no_agent cron) reads new lines since last offset
- Outputs formatted Telegram messages: OPEN (🟢/🔴 with SL/TP), MODIFY (📎), CLOSE (🟢 WIN / 🔴 LOSS)
- Empty output = silent — no spam when nothing happens
- State tracked in `logs/.telegram_reporter_offset`

### Message format examples
```
┌─ 🟢 OPEN BUY ─────────────
│ Ticket: `12345`
│ Lot: 0.1 | Price: $4520.00
│ SL: $4500.00 | TP: $4550.00
│ Reason: H4 bullish + ensemble conf
└─ Balance: $500,000.00

┌─ 🟢 WIN +$200.00 ─────────
│ Ticket: `12345` BUY
│ Lot: 0.1 | Close: $4540.00
│ Reason: TP hit
└─ Balance: $500,200.00

┌─ 📎 MODIFY ────────────────
│ Ticket: `12345`
│ SL: $4520.00 | TP: $4560.00
│ Reason: trailing
└───────────────────────────
```

## PID Lock (Anti-Double-Instance) — WMIC-Based Singleton

**Prevents process accumulation across Hermes sessions.** Every `auto_trade.py` instance scans WMIC for other python processes running `auto_trade.py` OR `run.py`, and kills older instances before starting. Two-layer defense:

| Layer | File | What It Detects | When It Runs |
|-------|------|----------------|-------------|
| 1 | `run.py`'s `enforce_singleton()` | Other `run.py` instances | Immediately on startup, before any import |
| 2 | `auto_trade.py`'s `_lock_pid()` | Both `auto_trade.py` AND `run.py` | Inside `bot.start()`, after MT5 connect |

**Critical fix from old mechanism:**
- **Old**: Used `os.kill(pid, signal.SIGTERM)` then `os.kill(pid, signal.SIGKILL)` — but **`signal.SIGKILL` does NOT exist on Windows** → `AttributeError` crash, exception NOT caught (caught `OSError`/`ValueError` only), stale instance survived.
- **New**: Uses `subprocess.run(["taskkill", "/F", "/PID", str(pid)])` — reliable Windows force-kill.
- **Old**: File-based `.noru.pid` check only — if lock file was deleted, couldn't detect dupe.
- **New**: WMIC scan — finds all instances even without lock file. Also detects cross-script (`run.py` vs `auto_trade.py`) as the same bot.

See `references/pid-lock-and-process-management.md` for full implementation details and edge cases.

## Engine Cycle

```
[TICK N] every 1 second
├── Ensure MT5 connected
├── Get account info (balance, equity)
├── Check drawdown & daily loss limits
├── Get open positions → manage trailing stops\n│   └── (Ensemble short-TF forecast for dynamic TP extension if profitable)\n│   └── (Early exit check: if opposing weight > 30% AND losing → close)
├── Fetch D1 + H1 + M15 + M5 data
├── Run StrategyEngine.analyze()
├── If signal != NONE:
│   ├── (ENSEMBLE CONSENSUS via EnsembleLoader) → load ensemble_results.json:
│   │   ├── Per-TF log: M3..D1 signal + conf + change%
│   │   ├── Weighted vote: equalized weights across TFs (M3=0.8, M5=1.0, M15=1.2, M30=1.5, H1=1.5, H4=1.5, D1=1.5). H4/D1 no longer dominate.
│   │   ├── Agreement multiplier: ≥80%→1×, ≥50%→0.7×, else 0.4×
│   │   ├── ⚠️ ENSEMBLE SIGNAL = PRIMARY direction decider
│   │   │   - consensus["signal"] (BUY/SELL/NEUTRAL) = arah entry utama
│   │   │   - Lot = base_lot × min(1.5, 0.5 + conf × 1.5) — max boost 1.5×
│   │   │   - TP = short-TF forecast average (M3/M5/M15/M30 only, not H4/D1) — closer targets
│   │   │   - Reason log = "Ensemble: {bias} {conf}% — {TF details}"
│   │   ├── StrategyEngine → ONLY as fallback when ensemble NEUTRAL
│   │   │   AND strategy confidence > 0.7 (threshold tinggi)
│   │   ├── ⚠️ JANGAN izinkan StrategyEngine override ensemble:
│   │   │   Bug ini PERNAH sebabkan -64% drawdown ($450K→$161K).
│   │   │   StrategyEngine baca M5 bearish → entry SELL 6× SL beruntun,
│   │   │   sementara ensemble H4/D1 bilang BULLISH 84% → total loss $200K+.
│   │   │   Ensemble = panglima. StrategyEngine = cadangan dengan guard ketat.
│   │   └── Ensemble NEUTRAL + strategy neutral → SKIP (no entry)
│   ├── Validate risk entry filters
│   ├── Calculate SL (ATR-based), ensemble TP from short TFs (M3-M30 only, min 2:1 RR)
│   ├── Calculate lot size (1% risk × ensemble confidence boost)
│   └── Executor.market_order()
├── Ensemble periodic retrain (manual or cron — no auto-tick training)
└── Log status + sleep 1s

## Full Stop Procedure

When user says "stop bot", execute ALL steps below — killing auto_trade.py alone is NOT sufficient.

### ⚠️ CRITICAL CHAIN: auto_trade.py → terminal64.exe

Killing `auto_trade.py` stops the Python loop, but **terminal64.exe (MT5) stays alive** with active broker connections. The parent Python process (auto_trade.py or `from auto_trade import AutoTradeNoru; bot.start()`) can even auto-restart terminal64.exe if killed — creating an infinite restart loop.

**On this Windows system, `ps aux` in git-bash does NOT show Windows-native processes (terminal64.exe, etc.)**. Only PowerShell `Get-Process terminal64` can see them. See Pitfalls section below.

### Step-by-step Kill Chain

1. **Kill auto_trade loop**:
   ```bash
   # If background process via Hermes:
   process(action="kill", session_id="<proc_id>")
   
   # Or via terminal (check with ps aux):
   kill -9 <PID>  # find with: ps aux | grep auto_trade.py
   ```

2. **Check for orphaned terminal64.exe (MT5)**:
   ```bash
   # ps aux does NOT show Windows processes — use PowerShell:
   powershell.exe -Command "Get-Process terminal64, python -ErrorAction SilentlyContinue | Select-Object Id, ProcessName"
   ```
   If terminal64.exe is still running after step 1, it's orphaned or auto-restarted by a parent Python process.

3. **Kill orphaned terminal64.exe + training processes**:
   ```bash
   # Kill any running auto_trade or ensemble_train:
   ps aux | grep -E "auto_trade|ensemble_train" | grep -v grep | awk '{print $2}' | xargs -r kill -9
   
   # Kill MT5 terminal via PowerShell (check parent PID first):
   powershell.exe -Command "Get-WmiObject Win32_Process -Filter \"Name='terminal64.exe'\" | Select-Object ProcessId,ParentProcessId"
   # If parent is a Python PID, kill that Python process first (it may restart MT5)
   # Then kill terminal64.exe:
   powershell.exe -Command "taskkill /F /PID <terminal64_PID> /T"
   ```

4. **Kill ALL orphaned Python bot processes** (most important — they accumulate across sessions):
   ```bash
   # List ALL python processes with their command lines:
   powershell.exe -Command "Get-WmiObject Win32_Process -Filter \"Name='python.exe' OR Name='python3.12.exe'\" | Select-Object ProcessId, CommandLine | Format-Table -Wrap -AutoSize"
   ```
   Look for: `auto_trade.py`, `from auto_trade import AutoTradeNoru`, `_ensemble_train.py`. These are bot instances.
   **Ignore**: `wmiexec.py`, Hermes scripts, and any Python processes with no visible command line (those are system/Hermes).
   
   Kill remaining bot PIDs:
   ```bash
   # Kill a specific orphaned PID:
   kill -9 <bot_PID>
   ```

5. **Break the auto-restart loop**:
   If terminal64.exe keeps restarting after being killed:
   ```bash
   # Find its parent chain:
   powershell.exe -Command "Get-WmiObject Win32_Process -Filter \"Name='terminal64.exe'\" | ForEach-Object { \$parent = Get-Process -Id \$_.ParentProcessId -ErrorAction SilentlyContinue; Write-Output \"terminal64 PID=\$(\$_.ProcessId) parent=\$(\$_.ParentProcessId) \$(\$parent.ProcessName)\" }"
   # Kill the parent Python process (this stops the restart loop):
   powershell.exe -Command "Stop-Process -Id <parent_PID> -Force"
   # Wait 2s, then kill terminal64:
   powershell.exe -Command "Start-Sleep -Seconds 2; Get-Process terminal64 -ErrorAction SilentlyContinue | Stop-Process -Force"
   ```

6. **Final verification**:
   ```bash
   # Check for Python bot processes:
   ps aux | grep -E "auto_trade|ensemble_train" | grep -v grep  # should be empty
   
   # Check for terminal64:
   powershell.exe -Command "Get-Process terminal64 -ErrorAction SilentlyContinue | Select-Object Id, ProcessName"
   # Should return nothing (or empty)
   
   # Check remaining Python processes (should only be Hermes agent):
   powershell.exe -Command "Get-Process python, python3.12 -ErrorAction SilentlyContinue | Select-Object Id, ProcessName"
   # Hermes = PID 6032 (protected). Everything else should be gone.
   ```

### Why Orphaned Processes Accumulate (Critical)

Hermes background processes (`terminal(background=true)`) are **tied to the Hermes session context**. When context compresses (compact or session rotates), the agent loses the `session_id` handle — but the actual Windows processes continue running indefinitely:

- 14× orphaned `auto_trade.py` instances were found in one session, all with live MT5 connections
- Each was spawned from a different Hermes context that had since been compacted
- They don't interfere with each other (separate Python processes) but drain system resources and keep MT5 terminal alive
- MT5 terminal auto-restarts as long as ANY Python parent process is alive

**Prevention**: After every bot start/stop cycle, verify no orphaned instances remain. Run the verification steps above.

## Key Decision Logic (strategy.py `_analyze_confluence`)

```python
# Buy score contributions:
trend_match         += 3   (H1 > EMA50)
d1_trend_match      += 2   (D1 > EMA20)
cci_oversold        += 2   (CCI < -100)
at_support          += 2   (price within 0.3% of pivot low)
bullish_ob_detected += 2.5
bullish_pa_confirm  += 1.5 (M15 engulfs/streaks)
volume_spike        += 0.5

# Sell score: inverse of above
# Signal when buy OR sell > 5.0 threshold
# Confidence = max_score / 10.0, capped at 0.95

**RSI dilarang untuk XAUUSD** — Gunakan CCI (+MACD) sebagai gantinya. Lihat §8 untuk detail.
```

## Starting Fresh with New Demo Balance

When user says "restart from beginning with new balance" (e.g. IDR 300k → 20jt), execute ALL steps:

### 1. Full Stop Cleanup
```bash
# Kill background process (if via Hermes)
process(action="kill", session_id="<proc_id>")

# Verify no orphans left
powershell.exe -Command "Get-Process terminal64, python, python3.12 -ErrorAction SilentlyContinue | Select-Object Id, ProcessName"
# Only PID 6032 (Hermes) should remain for Python
# terminal64 should NOT appear
```

### 2. Clean PID Lock & Logs
```bash
rm -f /c/Users/syahd/auto-trade-noru/.noru.pid
rm -f /c/Users/syahd/auto-trade-noru/logs/noru_v2.log
```
Without cleaning `.noru.pid`, the old PID is stale (process killed in step 1) → on next start, the WMIC scan won't find the dead process → lock file is auto-overwritten. Cleaning is explicit insurance. With the new WMIC-based singleton, the lock file is secondary — the primary detection is active process scanning.

### 3. Tune Config for New Balance
Update `config.py`:
- **`lot_max`** — critical safety cap:
  - IDR 300k: `lot_max: 0.01` (margin for 0.01 lot XAUUSD ≈ IDR 15-150k depending on leverage)
  - IDR 1M: `lot_max: 0.02`
  - $100 USD: `lot_max: 0.01`
  - $500 USD: `lot_max: 0.02`
  - General guideline: `lot_max = min(0.01, account_balance_in_IDR / 500_000)` for IDR accounts
- **`risk_per_trade_pct`** — 50% is aggressive-compound mode; only suitable for small demo balances where 0.01 lot is the minimum. For larger balances, reduce to 1-5%.
- **`target`** — update the file header comment to match the new goal (e.g. `IDR 300k → 20jt MODE`)
- **Verify margin affordability**: Before starting, run this check in Python:
  ```python
  import MetaTrader5 as mt5
  mt5.initialize(path="C:/Program Files/MetaTrader 5/terminal64.exe")
  margin = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, "XAUUSD", 0.01, mt5.symbol_info_tick("XAUUSD").ask)
  print(f"Margin for 0.01 lot: {margin} (balance: {balance})")
  ```
  If `margin > balance * 0.95`, reduce `lot_max`.

### 4. Start Bot
```bash
cd /c/Users/syahd/auto-trade-noru && python -u auto_trade.py > logs/noru_v2.log 2>&1
```

### 5. Verify Startup
Check `logs/noru_v2.log` within 10 seconds:
- ✅ `[LOCK] 🔐 PID <N> locked` — PID lock active
- ✅ `[MT5] Connected | Login: <N> | Server: <server> | Balance: $<expected>` — balance matches
- ✅ `[ENSEMBLE] ✅ Loaded N TF forecasts` — ensemble data loaded
- ✅ No "No money" errors on first entry attempt

### Compounding Math (IDR 300k → 20jt)

With 0.01 lot, TP = $4,760, entry ≈ $4,507:
- TP profit ≈ $253 (IDR ~4.2jt at typical rate)
- Loss (SL): ~IDR 80k per trade
- Win/Loss ratio ≈ 52:1 (but only if TP hits — large TP is hard to reach)
- Target 20jt from 300k ≈ 66× growth

**Realistic path**: 0.01 lot x 4-6 winning trades compounding ≈ 20jt.
**Risk warning**: at 50% risk per trade with 0.01 lot floor, drawdown is bounded but recovery requires consecutive wins.

## Pitfalls (Auto-Trade Deployment)

- **⚠️ MT5 credentials in memory may be stale — always check config.py first**: The MT5 login/password/server stored in memory may be outdated. When `mt5.login()` fails with authorization errors, do NOT immediately retry with memory values — first read the actual config: `grep -n -E 'password|server|login' /c/Users/syahd/auto-trade-noru/config.py | head -10`. The config file is the single source of truth. Real example: memory had `HFMarketsGlobal-Demo` (missing "4"), config had `HFMarketsGlobal-Demo4` — exact server name matters. The config may also reference env vars like `NORU_MT5_PASSWORD`.
- **⚠️ `signal.SIGKILL` does NOT exist on Windows Python**: Python's `signal` module on Windows only defines `SIGABRT`, `SIGFPE`, `SIGILL`, `SIGINT`, `SIGSEGV`, `SIGTERM`. Calling `os.kill(pid, signal.SIGKILL)` raises `AttributeError` — and if your except clause only catches `(OSError, ValueError)`, the AttributeError CRASHES silently and the stale instance survives. **Always use `taskkill /F /PID` on Windows** via `subprocess.run()` instead. This is why the old `.noru.pid` lock file mechanism failed to kill duplicates. See `references/pid-lock-and-process-management.md` for the WMIC-based replacement.

- **⚠️ Process accumulation across Hermes sessions (CRITICAL)**: Each time the bot is started via `terminal(background=true)`, it's tied to the current Hermes session. When context compacts or the session ends, the agent loses the `session_id` handle — but **the Windows Python process continues running indefinitely**. In one session, 14 orphaned `auto_trade.py` instances were found, all with live MT5 connections. After every bot start/stop cycle, always verify with: `powershell.exe -Command "Get-WmiObject Win32_Process -Filter \"Name='python.exe' OR Name='python3.12.exe'\" | Select-Object ProcessId, CommandLine"` to check for orphaned instances.\n\n  **🔧 PERMANENT FIX**: `auto_trade.py` now has a **PID lock** mechanism (`_lock_pid()` / `_unlock_pid()`). On start, it checks `.noru.pid` — if an old instance is alive, it kills it before proceeding. This prevents accumulation even across Hermes session boundaries. See `references/pid-lock-and-process-management.md` for implementation details.

- **⚠️ MT5 terminal auto-restart loop**: When you kill `terminal64.exe` while a Python parent process is alive (e.g. orphaned `auto_trade.py`), the parent re-spawns terminal64.exe automatically, creating an infinite restart loop. The fix is to identify and kill the parent Python PID first: `powershell.exe -Command "Get-WmiObject Win32_Process -Filter \"Name='terminal64.exe'\" | Select-Object ProcessId,ParentProcessId"` → kill the parent PID, wait 2s, then kill terminal64.exe.

- **Python buffering**: Always use `python -u` (unbuffered) when running in background with file redirect — without it, log output is delayed/batched into OS pipe buffers and may never appear until the process exits.
- **⚠️  pyc cache stale after hot patch**: If you patch `*.py` files in the `auto-trade-noru/` directory while the bot is running, stop the bot AND delete `__pycache__/` before restarting. Python's import system reuses cached `*.pyc` files even after source changes if the `mtime` was not updated atomically. A missed cache purge will silently serve the OLD code. Command: `rm -rf /c/Users/syahd/auto-trade-noru/__pycache__`
- **MT5 path**: On Windows, `mt5.initialize()` needs the full path to `terminal64.exe`. Default: `C:/Program Files/MetaTrader 5/terminal64.exe`.
- **Python discovery**: On this system, Python is at `C:\\Users\\<user>\\AppData\\Local\\Programs\\Python\\Python312\\python.exe`. Not in PATH for git-bash.
- **Symbol selection**: Always call `mt5.symbol_select('XAUUSD', True)` before reading data or trading.
- **Order filling**: XAUUSD on HFMarketsGlobal uses `ORDER_FILLING_IOC` (Immediate-or-Cancel). Avoid `ORDER_FILLING_FOK`.
- **Concurrent sessions**: MT5 only allows one `initialize()` call per process. Always `shutdown()` before re-initializing.
- **Risk guard**: All risk parameters are defined in `config.py` (`RISK` dict). The engine reads `risk_per_trade_pct`, `max_drawdown_pct`, `max_daily_risk_pct`, and `lot_min`/`lot_max` from config — always check that config values match the user's current risk appetite before deploying. See `config.py` for the active values.
- **⚠️ CRITICAL: StrategyEngine override ensemble = ded** (penyebab -64% drawdown). Entry logic dulu: StrategyEngine primary → ensemble cuma BLOCK filter kalo beda. Tapi StrategyEngine bisa override karena logic "neutral at some TF = not blocked". Akibatnya: StrategyEngine ngasih SELL 6× (M5 bearish) sementara ensemble H4/D1 bilang BULLISH 84% → 6 SL beruntun +$200K loss, lalu BUY 0.04 lot kena SL -$356K. **Fix: Ensemble = primary direction decider.** StrategyEngine cuma fallback kalo ensemble NEUTRAL, itupun butuh conf > 0.7. Jangan pernah balik ke ensemble-as-filter. Lihat `_evaluate_entry()` di auto_trade.py untuk implementasi.
- **⚠️ CRITICAL: `TRADE_ACTION_SLTP` resets unset fields**: When calling `mt5.order_send()` with `action=mt5.TRADE_ACTION_SLTP`, MT5 **clears any field not explicitly included in the request**. If you only send `sl` without `tp`, the position's TP gets reset to 0. Always retrieve the current position's SL and TP (`pos.sl`, `pos.tp`) and pass both — even if only one is changing. Use: `request["sl"] = new_sl if new_sl > 0 else (pos.sl or 0)` and similarly for `tp`.
- **⚠️ Position type format**: MT5 returns `pos.type` as **int** (0=BUY, 1=SELL). If you create a helper that converts positions (e.g. `get_positions()` returning dicts), store the type consistently. Mixing `"BUY"` strings with `0` ints breaks downstream logic like trailing stop direction detection.
- **⚠️ Margin calculation**: Do NOT calculate margin manually with `(entry_price * contract_size) / leverage`. This formula fails for non-USD account currencies and exotic pairs. Always use `mt5.order_calc_margin(order_type, symbol, volume, price)` — it returns the exact margin in account currency, accounting for broker-specific margin rules, currency conversions, and leverage tiers.
- **Trailing stop activation**: Calculate activation threshold as a **percentage of entry price** (`(current - entry) / entry * 100`), not as a percentage of account equity. A 0.5% price move on XAUUSD ≈ $22.77 — much larger than account-level gains which can look inflated by currency conversion.
- **Trailing stop modify guard**: Only call `modify_position()` when the new SL is meaningfully different from the current SL (e.g. > 0.15 price improvement). Otherwise you'll hit retcode=10025 (invalid stops) and spam error logs. Return 0 from trailing function when no update needed, and gate the modify call with `if new_sl and new_sl != current_sl`.

- **⚠️ trailing stop config confusion**: `risk_manager.py` `trail_stop()` reads `trailing_distance_atr` (default 0.3) from config, NOT `trailing_atr_multiplier` (default 2.0). These are different parameters:
  - `trailing_distance_atr` = small multiplier (0.3) → tight trailing, SL follows price closely
  - `trailing_atr_multiplier` = larger multiplier (2.0) → wide trailing, not clipped to trailing
  - Using the wrong key (2.0) makes new_sl absurdly far from current price, causing `new_sl >= old_sl` on SELLs, effectively disabling trailing entirely. **Always verify which key `trail_stop()` reads.**
- **⚠️ SELL trailing logic sign**: For SELL trailing, `new_sl = current_price + atr * trail_dist`. When price drops (profitable), new_sl < old_sl → SL trails down (correct). When price rises (losing), new_sl > old_sl → SL stays put (correct — you don't widen a losing stop). The condition `if new_sl < old_sl` only updates on profit direction — this is intentional and correct.
- **Config key consistency**: The engine references config keys like `risk_per_trade_pct`, `max_positions`, `max_daily_drawdown_pct`, `max_open_positions`. Ensure all keys referenced in `risk_manager.py` actually exist in `config.py`. A `KeyError` on startup kills the entire engine.
- **Scalp counter失效**: 仅在ADX < 20（震荡市场）时开展反向 scalp，否则易被止损。
- **⚠️ GPU contention before ensemble retrain**: Before running `_ensemble_train.py` (28 models, ~90s on GTX 1050 Ti), kill any running auto-trade bot first. The subprocess inherits GPU context, and CUDA out-of-memory kills both processes. Command: `ps aux | grep auto_trade.py` → kill old PID, then run training.
- **⚠️ ORPHANED `_ensemble_train.py` processes after bot stop**: Killing `auto_trade.py` does NOT kill independently-running `_ensemble_train.py` processes. These persist with live MT5 connections, consuming API quota and holding GPU memory. After `Haduh stop bot` scenario, ALWAYS verify: `ps aux | grep -E "auto_trade|ensemble_train" | grep -v grep`. If `_ensemble_train.py` shows, kill them individually. Full stop sequence:
  1. `process(action="kill", session_id=...)` or `kill -9 <PID>` for auto_trade
  2. Check: `ps aux | grep -E "auto_trade|ensemble_train" | grep -v grep`
  3. Kill any remaining `_ensemble_train.py` PIDs
  4. Verify: `netstat -an | grep 443` — no new MT5-originated connections if user reports lingering activity
- **⚠️ CRITICAL: StrategyEngine override ensemble = penyebab -64% drawdown**. Jangan pernah setting StrategyEngine sebagai primary direction decider. Logika lama: StrategyEngine primary → ensemble sebagai BLOCK filter (block only if mismatch). Tapi celah: karena tiap TF punya sinyal sendiri, StrategyEngine bisa pake M5 bearish sementara ensemble H4/D1 bullish 84% — dan BLOCK tidak aktif karena mismatch tidak terdeteksi di semua TF. Akibat: 6× SELL beruntun loss $200K, lalu BUY kena SL -$356K. **Fix: ensemble signal = arah entry utama. StrategyEngine = fallback hanya saat ensemble NEUTRAL + conf > 0.7.**
- **⚠️ Account currency mismatch in lot calculation (CRITICAL for IDR accounts)**: `risk_manager.py` `calculate_position_size()` computes `risk_amount_ccy = equity * (risk_pct / 100.0)` in the account currency (e.g. IDR 150,000), but the formula `lot_risk = risk_amount_ccy / ((sl_distance / tick_size) * tick_value)` uses MT5's `trade_tick_value` which is in USD, not the account currency. For IDR accounts, this inflates `lot_risk` by ~16,500× (IDR/USD rate). **Fix**: The safety chain `lot = min(lot_risk, max_lot)` then `lot = min(lot, lot_max)` with a low `lot_max` (e.g. 0.01 for IDR 300k) prevents the inflated lot from being used. For USD accounts, this bug does not manifest because tick_value is already in USD. **Long-term fix**: convert risk_amount_ccy to USD using the current XAUUSD-to-account-currency conversion rate before dividing. See `references/idr-account-lot-sizing.md` for concrete margin numbers and the "No Money" error breakdown.
- **⚠️ `order_calc_margin` returns None/0 crash guard** (FIXED): The binary search in `risk_manager.calculate_position_size()` computes `max_lot` by checking `order_calc_margin(order_type, symbol, volume, price)`. When MT5 returns `None` or `0` (offline, disconnected, or symbol not selected), the old code set `margin = 0` and then `0 <= margin_free * 0.95` is always True, causing the binary search to converge to an artificially high `max_lot` (~0.5-1.0 lot). **Fix**: Added `margin_free > 0` guard before the binary search; if free margin is 0 or None, fall through to `max_lot = lot_min`. Also changed binary search `hi` from hardcoded `1.0` to `RISK["lot_max"]` so even if the search goes wrong, the upper bound is safe.
- **⚠️ `lot_max` must be matched to account balance**: IDR 300k (~$19) on XAUUSD requires `lot_max: 0.01` — even 0.05 lot exceeds available margin (margin for 5 oz at $4,508 ≈ IDR 743k at 1:500 leverage). Guideline: `lot_max = min(0.01, account_balance_in_IDR / 500_000)` for IDR accounts on XAUUSD. For USD accounts: `lot_max = min(0.1, account_balance_in_USD / 5_000)`. Always verify before deployment by running `mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, "XAUUSD", lot_max, current_price)` — if margin > balance, reduce lot_max.
- **⚠️ Race condition on retrain** (FIXED): `_retrain_nhits()` launches `subprocess.Popen(_ensemble_train.py)` in background (non-blocking). The training script writes to `ensemble_results.json.tmp`, flushes+fsyncs, then `shutil.move()` renames to `ensemble_results.json` — atomic on the same filesystem. EnsembleLoader never reads a half-written file. Retrain throttle: max once per 6 hours via `self._last_retrain_time`.
- **⚠️ EnsembleLoader JSON key mapping**: `ensemble_results.json` keys use `avg_forecast` (not `forecast_prices`), `agreement_pct` (not `agreement`). `EnsembleLoader` maps these internally but if the JSON format changes (e.g. from an updated `_ensemble_train.py`), the loader must be updated in sync.
- **Stale ensemble forecasts**: Ensemble results are snapshots. `EnsembleLoader.refresh(max_age=30)` checks file mtime every 30m. If the bot runs for hours without retraining, forecasts become stale — monitor `generated_at` timestamp in the JSON.
- **No GPU during live inference**: `EnsembleLoader` is pure JSON parsing — zero GPU. All 28-model training is batch/offline via `_ensemble_train.py`. This avoids the old dual NHITS bottleneck where inference competed with trading for GPU.

# General Pitfalls
- Over-fitting and over-optimization → keep validation window truly out-of-sample.
- Memory bloat → prune old trade logs after 30 days; keep memory entries concise.
- Model drift → schedule periodic retraining with fresh data.
- Risk breaches → hard stop-trading guard; enforce daily loss limit.

# Advanced Strategy Enhancements — Gold Tsunami Framework

This section documents the "Gold Tsunami" strategy framework discovered via multi-model research (mixture_of_agents) when web search was blocked. It extends the base `master_of_trade` with regime-aware execution, multi-level partial takes, and adaptive risk scaling.

## 16.1 Market Regime Detection (ADX-Based)

Classifies current market into 9 regimes to gate entries and size risk:

| Regime | Tradeable | Risk Adj | Detection Logic |
|--------|-----------|----------|-----------------|
| STRONG_TREND_UP/DOWN | ✅ YES | 1.00× | ADX>30, DI aligned, EMA stacked |
| BREAKOUT_UP/DOWN | ✅ YES | 0.95× | Squeeze release (BB inside KC → expansion) |
| TREND_UP/DOWN | ✅ YES | 0.85× | ADX>20, partial alignment |
| VOLATILE_CHAOS | ⚠️ REDUCE | 0.40× | Extreme ATR but low ADX |
| SQUEEZE | ❌ WAIT | 0.00× | BB inside Keltner, bandwidth at lows |
| RANGING | ❌ NO | 0.00× | ADX<20, no EMA structure |

**Implementation flow per tick:**
1. Compute indicators on M15 (200 bars): ATR, ADX(14), BB(20,2), KC(20,1.5), EMAs(8/21/55)
2. Check squeeze: BB upper < KC upper AND BB lower > KC lower
3. Check bandwidth percentile vs 100-bar history (bottom 20% = tight)
4. Cascade: extreme volatility + low ADX → CHAOS → squeeze → breakout → strong trend → trend → ranging
5. `forced_direction()` returns +1 (long-only), -1 (short-only), or 0 (either) for regime alignment

**Why M15**: Gold's intraday structure is clearest on M15 — enough noise filtering for regime classification without the lag of H1.

## 16.2 Multi-Level Partial Take Profit (40/30/20/10%)

Instead of a single TP, lock profits progressively while letting a runner ride:

| Level | ATR Multiple | Close % | What Happens |
|-------|-------------|---------|--------------|
| TP1 | 2.5× ATR | 40% | SL → breakeven + 0.1 ATR buffer |
| TP2 | 4.0× ATR | 30% | Activate ATR trailing (1.8× ATR) |
| TP3 | 7.0× ATR | 20% | Tighten trail to 1.0× ATR |
| Runner | ∞ | 10% | Trailing until stopped |

**Math**: After TP1: 60% remains, risk-free (SL at breakeven). After TP2: 30% remains with trail. After TP3: 10% rides for outsized moves → the 10,000% compounder.

**Implementation**: Use `mt5.order_send(action=TRADE_ACTION_SLTP)` to set initial SL + TP1 as MT5 target. After TP1 hits (detected via `positions_get()` or `history_deals_get()`), call `order_send(action=TRADE_ACTION_DEAL, volume=partial)` to close the partial amount, then modify SL to breakeven. Remove MT5 TP so it doesn't interfere with subsequent manual targets.

## 16.3 Entry Scoring Engine (0-100)

Composite score combining 4 weighted components:

| Component | Max | Measures |
|-----------|-----|----------|
| NHITS Ensemble Forecast | 40 | Multi-TF agreement + confidence |
| Regime Alignment | 20 | Direction matches regime |
| Price Action Confirmation | 25 | EMA stack + RSI zone + MACD + BB position |
| Session & Volatility | 15 | London-NY overlap + volume ratio |

**Thresholds**: ≥ 65 for 1st position, ≥ 75 for 2nd position. Below threshold → no entry.

**PA sub-scores (direction-aware)**:
- EMA alignment (0-8): ef > em > es for BUY (or inverse for SELL)
- RSI zone (0-5): 40-70 for BUY, 30-60 for SELL (good momentum zones)
- MACD histogram (0-5): positive AND accelerating = best
- BB position (0-7): inside band trending = best; breakout/reversal = less

**Session scoring**:
- London-NY overlap (13-16 UTC): +10 pts — peak Gold liquidity
- London or NY open: +7 pts
- Asian session: +1 pt — least ideal for XAUUSD

## 16.4 Adaptive Risk Scaling

Scale risk down after losses to preserve capital:

| State | Risk per Trade |
|-------|---------------|
| Normal | 50% (aggressive compound mode) |
| After 1 consecutive loss | 35% |
| After 2 consecutive losses | 20% |
| After 3+ losses | PAUSED for 1 hour |
| 25% drawdown from peak | max 25% |
| 35% drawdown | max 15% |
| 40%+ drawdown | PAUSED |
| 60% drawdown | **KILL SWITCH** — close all positions |

**Kill switch implementation**: Every tick, check `equity / peak_equity < 0.40`. If true, call `position_manager.close_all("kill_switch")` and log CRITICAL. Resume only after manual reset.

## 16.5 Session Timing for XAUUSD

Gold's volatility and directional consistency vary by session:

```
UTC 0-7   (Asian)     → Low vol, choppy → avoid or reduce size
UTC 7-13  (London)    → Directional begins → tradable
UTC 13-16 (Overlap)   → PEAK liquidity, largest moves → best entries
UTC 16-21 (NY)        → Momentum continuation → tradable
UTC 21-24 (Post-NY)   → Declining vol → avoid new entries
```

**Implementation**: Pass `utc_hour` to entry scorer. In overlap, the session + volume score adds up to +15 to the composite signal, making it much easier to hit the 65 threshold. Outside prime hours, the score is capped to prevent marginal entries.

## 16.6 Early Exit Conditions

Exit before SL/TP hit when:
1. **Ensemble Flip**: Ensemble direction reverses with >70% confidence AND >71% TF agreement
2. **Chaos + Loss**: Regime switches to VOLATILE_CHAOS while position is losing (>0.1% loss)
3. **Time Decay**: Position held >50 bars without moving ≥0.3× ATR in profit direction

## 16.7 Research via Mixture of Agents (When Web Is Blocked)

When building or enhancing trading strategies and all web search methods fail (Google/Bing/DDG blocked by captcha/Cloudflare), use `mixture_of_agents` to:
- **Generate strategy designs**: Describe market, leverage, risk parameters, and target returns → get architecture + code
- **Compare approaches**: Ask about grid vs trend vs momentum for your specific constraints
- **Design indicator logic**: Request detailed numpy/pandas indicator implementations
- **Analyze failure modes**: "Why might this strategy blow up at 50% risk with 1:2000 leverage?"

**Limitation**: MoA knowledge stops at model training cutoffs — cannot fetch live prices, current news, or real-time data. For live data, use gold-api.com or TradingView.

## 16.8 Quick-Reference: Key Parameter Ranges

| Parameter | Suggested Range | Default | Notes |
|-----------|----------------|---------|-------|
| SL_ATR_MULTIPLIER | 1.2-2.0 | 1.5 | Tighter = higher winrate, harder to hold |
| TP1_ATR_MULTIPLIER | 2.0-3.0 | 2.5 | First profit target |
| TP2_ATR_MULTIPLIER | 3.5-5.0 | 4.0 | Second target |
| TP3_ATR_MULTIPLIER | 6.0-10.0 | 7.0 | Runner target |
| TRAIL_ATR_MULTIPLIER | 1.5-3.0 | 1.8 | Tighter after TP2, 1.0 after TP3 |
| ENTRY_THRESHOLD | 55-75 | 65 | Lower = more entries, lower quality |
| ADX_STRONG_TREND | 25-35 | 30 | Above = strong trend regime |
| BB_SQUEEZE_PERCENTILE | 15-25 | 20 | Bottom % of BB bandwidth = squeeze |

## 16.9 File Structure Reference (Gold Tsunami)

When implementing the full Gold Tsunami standalone:

```
gold_tsunami/
├── config.py              # All constants + TradingConfig dataclass
├── indicators.py          # numpy indicator engine (ATR, RSI, MACD, BB, KC, ADX)
├── regime.py              # RegimeDetector class (9 regimes)
├── signals.py             # Entry scoring 0-100 + early exit logic
├── nhits_ensemble.py      # NHITS 7-TF ensemble (lazy predict on new bar)
├── position_manager.py    # Adaptive lot sizing + multi-TP execution
├── trailing_manager.py    # TP1/TP2/TP3 partial close + ATR trail
└── main.py                # 1-second master loop orchestrator
```

Or integrate individual modules into the existing auto-trade structure (recommended for incremental improvement).

## 16.10 Backtesting Gold Tsunami — Methodology & Pitfalls

### Workflow Rule: Stop Bot Before Developing Replacement
When the current strategy is losing and a replacement is being developed, **stop the running bot first**. Kill MT5 terminal, disable watchdog cron jobs, terminate orphan Python processes. Letting a losing bot run while developing a replacement wastes demo balance and distracts from validation.

### ADX Breakout Momentum (Validated Stand-Alone Strategy)
Tested as a clean, non-NHITS alternative on XAUUSD M15 (15,000 bars, Oct 2025–May 2026):

**Entry condition**: ADX crosses from below 22 to ≥ 22 within 5 bars + DI alignment.
**Exit**: 50% close at 2.5× ATR TP, trail remaining at 1.2× ATR.
**Risk**: 15% per trade (survives more than 2 losses).

**Results**:
- LONG signals: 57.1% WR, +21.0% net, PF ~1.85
- SHORT signals: 29.2% WR, -28.3% net, PF ~0.60
- **Conclusion**: Pure ADX breakout works for LONG on XAUUSD. SHORT requires additional filter (ensemble, higher timeframe confirmation). Gold's structural upward bias invalidates short-only ADX breakout.

See `references/adx-breakout-momentum.md` for full strategy spec and tuning parameters.

### Kill Switch Must Not Block Per-Bar Data Collection

**BUG FOUND**: In backtest simulations with a drawdown kill switch (DD ≥ 60% → emergency close), placing the `_regime(i)` call AFTER the kill check causes ALL subsequent bars to skip regime tracking. With 50% risk per trade, 2 consecutive losses trigger DD > 60%, and the remaining 99%+ of historical bars lose their regime classification.

**FIX**: Always call per-bar data collectors (regime detection, equity tracking) BEFORE the kill switch check:

```
for each bar:
    _regime(i)           # ← ALWAYS track regime first
    if equity < 0.40 × peak:
        close_all()
        continue         # OK to skip signal detection, but data is saved
    _signals()
```

### Entry Signal Proxy Without NHITS Ensemble

During backtesting, NHITS ensemble forecasts are unavailable. Use a score-based proxy that mimics the real strategy's components:

| Component | Max Score | Real Equivalent |
|-----------|-----------|-----------------|
| EMA alignment (ef>em>es) | 3 | NHITS trend component |
| RSI zone (30-40 / 60-70) | 2 | Ensemble momentum |
| Engulfing candle | 3 | Price action confirmation |
| Strong candle body>60% range | 2 | Momentum |
| ADX trend boost | 2 | Regime filter |

**Threshold**: With *all* components, score ≥ 5 matches real strategy.py's threshold (which has 10 components). But since the proxy has fewer components (only 5), lower the threshold to **4** to generate enough trades for statistical significance (50+ trades recommended).

### Correct P&L Formula for Partial TP Structure

The partial TP (40/30/20/10%) requires per-level P&L calculation — not a single exit R:R:

```
TP1:  PnL = init_risk × (tp1_dist / sl_dist) × 0.40   # 40% at 2.5× ATR
TP2:  PnL = init_risk × (tp2_dist / sl_dist) × 0.30   # 30% at 4.0× ATR
TP3:  PnL = init_risk × (tp3_dist / sl_dist) × 0.20   # 20% at 7.0× ATR
SL:   PnL = -init_risk                                  # 100% loss (if no TP hit)
BE:   PnL = 0                                            # breakeven after TP1
TRAIL: PnL = rem_risk × (trail_exit_move / sl_dist)      # runner
```

**Remaining risk** after each partial close:
- After TP1: `rem = init_risk × 0.60` (SL moved to breakeven)
- After TP2: `rem = init_risk × 0.30` (trailing activated)
- After TP3: `rem = init_risk × 0.10` (tight trail)

**Expected value per trade** at various winrates (with TP1-only wins):
- WR 50%: EV = 0.50×0.667 − 0.50×1.0 = −0.167 → LOSING
- WR 60%: EV = 0.60×0.667 − 0.40×1.0 = 0.0 → BREAKEVEN
- WR 70%: EV = 0.70×0.667 − 0.30×1.0 = +0.167 → PROFITABLE

With TP1+TP2 wins (avg win = 0.987×risk):
- WR 60%: EV = 0.60×0.987 − 0.40×1.0 = +0.192 → PROFITABLE

### Risk Scaling Invalidation

With 50% risk per trade and 1.5× ATR SL:
- 2 consecutive losses → equity drops to 25% of peak → DD ≥ 60% → kill switch
- Backtest becomes uninformative after 2 losses (all remaining bars skipped for signal detection)
- **Workaround**: Reduce risk to 10-15% during backtesting to survive enough trades for statistical validity. Scale results proportionally.
- **Alternative**: Test signal quality first (winrate, average R:R of entries) WITHOUT risk scaling, then apply risk model afterward.

### Minimum Sample Size

- **50+ trades** needed for winrate ±15% confidence (binomial proportion CI)
- **100+ trades** for ±10% confidence
- With 50% risk, expect only ~5-10 trades per 8 months (5,000+ M15 bars)
- Either increase backtest duration or reduce sample period
- Low trade count (< 20) is NOT statistically meaningful even if winrate looks high

## Reference Files
The following structured reference files live under this skill's `references/` directory. Load them with `skill_view(name='master_of_trade', file_path='references/<name>')`:
  - `pine-indicator-to-strategy.md` — Pattern for converting Pine Script indicators (ST+SQZMOM+SMC+FVG+Fibo) into executable TradingView strategies with entry/exit logic, TP/SL, and visual overlay.

## Template Files
Load with `skill_view(name='master_of_trade', file_path='templates/<name>')`:
  - `ST_SQZMOM_Strategy_V6.0a.pine` — Complete Pine v6 strategy converting the ST+SQZMOM+SMC indicator to strategy.entry/exit with AT-based TP/SL, K-means clustering, and SMC/FVG visuals. Ready to paste into TradingView Pine Editor and "Add to chart".

## References
- `mt5_adapter` skill documentation.  \
- `smart_money` skill documentation.  \
- `blogwatcher` skill for news ingestion.  \
- `memory` tool for persistent storage.  \
- `ensemble_loader.py` — loads pre-computed ensemble JSON, no GPU needed during live trading.  \
- Python libraries: `pandas`, `numpy`, `ta`, `xgboost`, `lightgbm`, `torch`, `scikit‑learn`.  \
- Market microstructure papers.  \
- MetaTrader 5 Python SDK: https://www.mql5.com/en/docs/python\n\n# Linked Files\n- `references/master_of_trade_setup.md`\n- `references/mt5-error-codes-and-pitfalls.md` — real-world MT5 error codes (10019, 10025, TP reset bug)\n- `references/trailing-stop-fix.md` — detailed fix for trailing stop TP reset and debug logs\n- `references/nhits-pytorch-cuda.md` — NHITS PyTorch CUDA: architecture, presets, migration, pitfalls
- `references/ensemble-architecture.md` — 28-model ensemble: TF presets, 4 variants, weighted consensus, atomic retrain, Telegram reporter
- `references/pid-lock-and-process-management.md` — PID lock file, process accumulation fix, kill chain for auto_trade.py
- `references/idr-account-lot-sizing.md` — IDR account margin, lot sizing table, "No Money" error fix
- `references/backtesting-pitfalls.md` — Backtesting methodology: kill switch bugs, P&L formula, entry proxy, statistical validity
- `references/mql5-neurobook-neural-networks.md` — MQL5 NeuroBook summary: NN layer types, attention mechanisms, OpenCL implementation, MQL5-Python integration, MT5 Strategy Tester workflow
- `scripts/risk_manager.py`\n- `scripts/optimizer.py`\n- `scripts/learning_loop.py`\n- `tests/test_master_of_trade.py`