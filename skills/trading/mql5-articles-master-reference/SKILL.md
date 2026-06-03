---
name: mql5-articles-master-reference
description: >-
  Master reference of ALL MQL5 articles read from the MQL5 Articles Library
  (pages 1-10) — SMC, Market Structure, Price Action, ML, Neural Networks,
  EA Architecture, Optimization, Risk Management, and more. Contains detailed
  article summaries, key parameters, implementation patterns, and applicability
  to XAUUSD M5 trading.
---

# MQL5 Articles Master Reference — Complete Knowledge Base

> **Source:** https://www.mql5.com/en/articles — Pages 1-10 (hundreds of articles)
> **Compiled:** Real-time batch reading by Noru
> **⚠ Website access:** MQL5.com blocks automated requests (browser + curl). Article bodies are JS-rendered and inaccessible without a residential proxy or logged-in session. Use the RSS feed (`/en/articles/rss`) for title/link discovery; rely on this harvested skill for full content. See `url_fetch_troubleshooting` skill for details.

## 🎯 MARKET STRUCTURE / SMC / ICT (Langsung Apply ke XAUUSD M5)

### Top Articles

| ID | Title | Author | Key Concept | XAUUSD M5 Use |
|----|-------|--------|------------|---------------|
| 22526 | Integrating AI into 3 Smart Money Concepts (SMC): OB, BOS, FVG | Latest | AI-enhanced SMC detection | Core entry logic |
| 22249 | Building the Market Structure Sentinel Indicator | — | Real-time structure monitoring | MTF structure overlay |
| 22264 | Building an Object-Oriented FVG Scanner | — | OOP FVG detection engine | Fair Value Gap scanner |
| 22140 | Building a Dynamic STF Liquidity Sweep Indicator | Chukwubuikem Okeke | Wick sweep + dual-candle sweep | Liquidity grab detection M5 |
| 20387 | Master Market Structure with Multi-Timeframe Visual Analysis (Part 52) | Christian Benjamin | MTF candle overlay | Overlay H1/H4 on M5 |
| 21212 | Optimizing Liquidity Raids: Mastering the Difference Between Liquidity Raids and Market Structure Shifts | Eugene Mmene | Purge → volume → engulfing → trend | M15 entry, H1 trend, M5 confirm |
| 20323 | CRT — Accumulation, Manipulation, Distribution (Part 41) | Allan Munene Mutiiria | Range breach → reversal | H1 range, M5 confirm |
| 22078 | Order Blocks, Inducement, Break of Structure (Part 48) | Allan Munene Mutiiria | OB + FVG + BOS combo | OB zone with inducement filter |
| 20569 | Liquidity Sweep on Break of Structure (BoS) (Part 46) | Allan Munene Mutiiria | Sweep after BOS confirmation | Entry after trap |
| 20361 | Inverse Fair Value Gap (IFVG) (Part 45) | Allan Munene Mutiiria | FVG state machine: Normal→Mitigated→Retraced→Inverted | Mean reversion M5 |
| 20355 | Change of Character (CHoCH) Detection (Part 44) | Allan Munene Mutiiria | Swing label → CHoCH → entry | Trend reversal M5 |
| 22469 | Encoding Candlestick Patterns (Part 1) — Alphabetical System | Daniel Opoku | Body-to-wick ratio encoding | Pattern filter AH/HE etc |
| 21246 | Mastering PD Arrays: Optimizing Trading from Imbalances | Eugene Mmene | ICT PD arrays + Asia sweep for XAUUSD | **Gold-specific EA** |

### Key Parameters for XAUUSD M5

- **Swing Strength:** 3-5 bars for M5 (15-25 min)
- **SL Buffer:** 20-30 pips for XAUUSD
- **ATR Period:** 14 for volatility normalization
- **FVG minPts:** 20-30 points (not 100)
- **RR Ratio:** 1:2 to 1:4
- **Max Positions:** 1-2 per direction
- **Trailing:** ATR-based or points-based

---

## 📊 PRICE ACTION & PATTERN RECOGNITION

### Key Articles

| ID | Title | Type | Key Innovation |
|----|-------|------|---------------|
| 22503 | Flag Pattern Detection (Part 69) | Continuation | ATR-normalized pole, slanted channel |
| 22194 | Head and Shoulders Scanner (Part 66) | Reversal | Triangle-based detection, scoring |
| 22419 | Adaptive Malaysian Engulfing (Part 1) | Reversal | Perfect engulfing strict definition + state machine |
| 22420 | Adaptive Malaysian Engulfing (Part 2) | Self-optimizing | MFE/MAE auto-optimize retest range |
| 20996 | Market State Classification Module (Part 57) | State classifier | 4 states: Compression/Transition/Expansion/Trend |
| 21109 | Range Contraction Analysis (Part 58) | Compression | Maturity scoring: Early→Building→Mature |
| 21277 | Slanted Trendline Breakout (Part 61) | Breakout | 3-swing validation, ATR tolerance |
| 22572 | Megaphone Pattern Indicator | Broadening | 4-swing expanding formation + SL/TP |
| 22342 | Liquidity Spectrum Volume Profile | Volume Profile | Volume distribution across price bins |

---

## 🤖 MACHINE LEARNING & FORECASTING

### Feature Engineering Series (Patrick Murimi Njoroge)

**22014 — Fractional Differentiation (Part 1):**
- FFD based on López de Prado AFML Ch.5
- d* optimal untuk stasionaritas tanpa memory loss
- EURUSD H1 → d* ~0.15
- Implementasi Numba-Parallel di Python, <1ms untuk 10K bar
- Binary search + ADF test untuk cari d* optimal

**22516 — Session-Aware Time Features (Part 3):**
- Fourier cyclical encoding (sin/cos harmonics)
- Forex Session: Sydney(21-06), Tokyo(00-09), London(07-16), NY(13-22) UTC
- Session volatility (rolling std 20-bar), forward-filled
- Calendar effects: Friday NY close, Sunday open, month/quarter end
- **Insight:** Session volatility 25.6% feature importance!

**22517 — MQL5 Implementation CTimeFeatures.mqh:**
- CRingBuffer for incremental volatility
- UTC offset correction: TimeGMT() - TimeCurrent()
- 24 features for M1-M30, 20 for H1-H12

### Advanced Forecasting

**22096 — TimesFM 2.5 (Google) in MT5:**
- 200M parameter decoder-only transformer
- Pre-trained on 100B real-world time points
- LoRA fine-tuning (~102K params trained)
- 40+ covariates (moon phases, FRED economic calendar, session features)
- XAUUSD included in default 14 instruments
- MQL5 indicator with 90%/10% confidence bands

**22474 — ML Pipeline → ONNX:**
- Python: indicators → StandardScaler → PCA → LSTM → ONNX
- MQL5: matrix/vector reproduces normalization+PCA identically
- EURUSD H1 Profit Factor 2.56, Sharpe 15.38

### Meta-Labeling

**22274 — Meta-Labeling the Classics (Part 1): RSI:**
- RSI as primary model → Random Forest as secondary
- 27 features (11 price/volatility + 16 time)
- Plain RSI: -625 pips, Max DD -1,392 pips
- Meta + Bet-sized: **-86 pips, Max DD -96 pips** (93% drawdown reduction!)
- Feature importance: Session vol 25.6%, ADX only 8th

---

## 📈 ADVANCED QUANTITATIVE

### Beyond GARCH Trilogy (Muhammad Minhas Qamar)

**22438 — Part I: MMAR vs GARCH:**
- GARCH 3 blind spots: thin tails, short memory, no scale consistency
- MMAR: X(t) = B_H[θ(t)] — Fractional Brownian Motion + Multifractal Trading Time
- Pipeline 7-step: Partition function → Scaling τ(q) → Spectrum fit → Cascade → FBM → MMAR → Monte Carlo

**22484 — Part II: Fractal Dimension:**
- 3-Component Multifractality Test (Score 0-9)
- Hurst via R/S analysis with Anis-Lloyd-Peters correction
- Spectrum fitting: Lognormal, Binomial, Poisson, Gamma (L-BFGS-B)
- EURUSD tipikal spectrum width 0.3-0.5

**22476 — Part III: The Verdict:**
- MMAR error 64.43% vs GARCH 193.88% (129pp reduction!)
- 1,000 Monte Carlo simulations
- Davies-Harte FBM via FFT O(n log n)

### RQA Library (Hammad Dilber)

**22288 — RQA in MQL5 — Complete Library:**
- 5 modules: Matrix, Metrics, Epsilon, Window (OpenCL GPU), Facade
- 12 metrics: RR, DET, LAM, TT, ⟨L⟩, Lmax, ENTR, DIV, Vmax, TREND, RATIO, COMPLEXITY
- CPU fallback with fused compute

**22500 — CRQA (Cross-RQA):**
- 2 series comparison: is X-state near Y-state?
- 10 metrics (no TREND/COMPLEXITY)
- Timestamp alignment across different session/holiday patterns

**22610 — JRQA (Joint RQA):**
- Simultaneous self-recurrence detection
- More strict than individual RQA: JRR ≤ min(RR_X, RR_Y)
- OpenCL kernel computes distX & distY in single pass

### Market Microstructure (Max Brown)

**22263 — Part 1: Robust Foundation:**
- Safe math: SafeDivide, SafeLog, SafeSqrt, SafeExp, SafeTanh
- Cooley-Tukey FFT in MQL5
- 5 guarantees: no NaN/Inf, degenerate skipped, min 8 bars, clamped, status message

**22553 — Part 2: Hurst Estimators:**
- 3 independent estimators: R/S, Aggregated Variance, Absolute Moments
- Confidence-weighted blend
- NQ M1 empirical: H≈0.511 (near random walk)
- **Session reset required** — pre-open + post-open data must NOT mix
- H does NOT predict short-term trending (p=0.094), but useful as characterization filter

---

## 🔌 PYTHON/MT5 INTEGRATION

**21905 — AI Agents via MCP:**
- MCP Server: 14 tools (account, market data, positions, orders, history)
- Stack: Python 3.10+ + MetaTrader5 + fastmcp
- Transport: stdio (no HTTP/Docker)
- 676 lines total

**17981 — Computer Vision in MQL5 (2 parts):**
- Image generation → CV analysis → trade signals
- Extends to 2D RGB image analysis

**18451 — IMF Data Download via Python:**
- International Monetary Fund financial data → MT5

**21676 — MQL5 + Python Data Processing (9 parts):**
- Multi-agent environments, Graph Neural Networks, Entropy-based volatility

---

## 🏗️ EA ARCHITECTURE & RISK

### Critical Infrastructure

| ID | Article | Key Concept |
|----|---------|-------------|
| 22532 | Self-Healing EA (Part 1) | SQLite persistence for trade state recovery |
| 22363 | Leak-Free Multi-Timeframe Engine | Closed-bar reads ONLY, no handle leaks |
| 22383 | Event-Driven Architecture | OnTick → lightweight router, custom events |
| 21720 | RiskGate: Centralized Risk Management | TCP service for multi-EA risk |
| 22187 | Safe Pyramiding with Unified Stop | Decreasing lots + unified SL |
| 22580 | News Filtering with MT5 Calendar | 30min pre/post news window, CSV fallback |

### Risk Management Patterns

- **Per-trade risk:** 0.5-1% of equity
- **Daily loss limit:** 2% of equity
- **Max positions per symbol:** 2
- **Correlated exposure:** 50% lot reduction
- **Daily max trades:** 6

---

## 🧮 WIZARD TECHNIQUES SERIES (Stephen Njuki)

| Part | Concept | Tech | Test Result |
|------|---------|------|-------------|
| 89 (22499) | Bitwise Vectorization + Perceptron | 64-bar→uint64, two-gate signal | DD 18.66%→16.75% |
| 90 (22558) | Fenwick Tree + 1D CNN MM | BIT volume topography, CNN gatekeeper | -$773→+$115, 83% loss→100% win |
| 91 (22609) | Skip List + Hopfield Trailing | O(log n) gap-jumping, energy veto | DD 18.63%→6.79% |

---

## 🧠 NEURAL NETWORKS SERIES (Dmitriy Gizlyk)

All use OpenCL GPU acceleration via NeuroNet.mqh/cl library. Train EURUSD M1 2024, test 2025.

| Framework | Concept | PF | Trades |
|-----------|---------|-----|--------|
| CATCH (17649) | Frequency domain anomaly detection via FFT + masked attention | — | — |
| DADA (17577) | Adaptive bottlenecks + dual adversarial decoders | 1.53 | 57 |
| DUET (17459+17487) | Temporal MoE + Channel Clustering via FFT distance | **2.44** | 53 |
| Attraos (17351+17371) | Chaos theory + phase space reconstruction + PScan | 1.15 | 287 |
| Chimera (17210+17241) | 2D State Space Model (time × variable axes) | 1.53 | 27 |
| ResNeXt (17157) | Multi-task learning with grouped convolutions | 1.52 | 60 |

---

## 🗺️ LARRY WILLIAMS SERIES (Chacha Ian Maroa)

| Part | Strategy | Results |
|------|----------|---------|
| 1 (20511) | Swing Structure Indicator (3-tier) | Visual structure |
| 2 (20512) | Market Structure EA | XAUUSD H1: +$8,950 (+80%) |
| 5 (20745) | Volatility Breakout | XAUUSD: +$6,203 (+62%) |
| 13 (21391) | Hidden Smash Day Reversal | XAUUSD D1: +$1,371 (+13.7%), **100% WR** |
| 15 (21393) | Hidden Smash Day + Context | +$1,862 (+18.6%), trend filter improved |

---

## 🔬 OPTIMIZATION ALGORITHMS (Andrey Dik)

| Algorithm | Type | Rating | Pros/Cons |
|-----------|------|--------|-----------|
| CMA-ES (18227) | Evolution strategy | N/A | O(n²) mem, O(n³) compute |
| BBO (18354) | Biogeography-inspired | 58.50% (#12/45) | Cepat, simpel |
| Eagle Strategy (18460) | Levy + Firefly | N/A | Adaptive λ |
| BRO (17688) | Game-based (Battle Royale) | 39.02% (#45/45) | Idea menarik, lemah diskrit |

---

## 🏆 RECOMMENDED COMBINATION FOR XAUUSD M5

### The Ultimate Pipeline:

```
1. LIQUIDITY SPECTRUM VP (22342) → Identify high-volume nodes as S/R
2. MARKET STATE CLASSIFIER (20996) → Know if Compression/Expansion/Trend
3. COMPRESSION READINESS (21109) → Wait for "Mature" compression
4. PD ARRAYS (21246) → Define premium/discount zones
5. IFVG/CHoCH/OB (20361+20355+22078) → Entry signal generation
6. LIQUIDITY SWEEP (20569) → Confirm with sweep after BOS
7. NEWS FILTER (22580) → Block trading during high-impact news
8. SELF-HEALING EA (22532) → Persist state through restarts
9. RISKGATE (21720) → Centralized risk for multi-EA
10. MTF ENGINE (22363) → Leak-free multi-timeframe orchestration
```

### Win Rate Enhancement Pattern:
- Feature Engineering (22516/22517) + Meta-Labeling (22274) → 93% drawdown reduction on RSI
- Fractional Differentiation (22014) → Stationarity without memory loss
- TimesFM 2.5 (22096) → Foundation model forecasting

All files from these articles can be downloaded from the MQL5 Code Base at https://www.mql5.com/en/code

---

## 🗺️ Visual Mind Map

Load the mind map with:\n`skill_view(name='mql5-articles-master-reference', file_path='references/mindmap.excalidraw')`

Then drag-and-drop the `.excalidraw` file onto [excalidraw.com](https://excalidraw.com).

Dark-theme mind map covering all 7 knowledge categories with 21 key techniques and article IDs.
