# MQL5 NeuroBook — Neural Networks for Algorithmic Trading

**Author:** Dmitriy Gizlyk  
**Source:** https://www.mql5.com/en/neurobook  
**Available in:** PDF and CHM formats  
**Code examples:** MQL5 Shared Projects > NeuroBook

> Practical guide combining neural networks with algorithmic trading on MetaTrader 5. 7 chapters covering from perceptron to Transformer attention mechanisms, all implemented in MQL5 with OpenCL parallelism.

**Total pages:** 690
**Format:** Web (multi-page), PDF (single file), CHM
**Code:** OpenCL kernels (.cl) + MQL5 classes + Python reference scripts
**Author:** Dmitriy Gizlyk (dng on mql5.com)

> "The book provides only the basic concepts without delving into the mathematical explanations of specific points. It aims to be a practical work. We invite you to explore possible solutions to a practical case and compare the effectiveness of different algorithms." — Dmitriy Gizlyk

---

## Book Structure by Size (Word Count)

| Section | Pages | Est. Words | Focus |
|---------|-------|-----------|-------|
| Introduction | 6-7 | ~1,054 | History of AI + stock trading convergence; practical mindset; risk warning |

> "The whole history of mankind is the creation and improvement of tools."
>
> "Artificial intelligence is a system's ability to correctly interpret external data, to learn from such data, and to use those learnings to achieve specific goals and tasks through flexible adaptation." — Kaplan & Heinlein
>
> "This work will be more interesting for practitioners. The book provides examples of using different algorithms to solve real-life cases."
>
> "I would like to draw the attention of all readers to the fact that stock trading is associated with high risks. The responsibility for any trading operation lies with the reader. The book looks at tools, not ready-made trading solutions."
| Ch1: AI Principles | 7-57 | ~17,682 | Neuron math, activation functions, initialisation, training theory |
| Ch2: MT5 Features | 57-84 | ~10,729 | Platform overview, program types, OpenCL, Python bridge |
| Ch3: First NN Model | 84-262 | **~62,892** | Heavy implementation — framework, FC layer, OpenCL, gradient checking |
| Ch4: Neural Layers | 262-401 | ~45,792 | CNN + LSTM architecture, MQL5 classes, OpenCL kernels |
| Ch5: Attention | 401-570 | ~58,410 | Self-Attention, Multi-Head, GPT decoder-only |
| Ch6: Convergence | 570-651 | ~23,183 | Batch Normalization + Dropout, MQL5 + OpenCL |
| Ch7: Testing | 651-690 | ~12,896 | Strategy Tester, EA template, OOS validation |

---

## Chapter 1: Basic Principles of AI Construction

### Neuron & Neural Network Foundations
- McCulloch-Pitts neuron (1943): first mathematical model
- Perceptron (Rosenblatt, 1957): basis of Mark-1 neurocomputer
- Hebbian learning (1949): "cells that fire together wire together"

### Activation Functions
| Function | Range | Use Case |
|----------|-------|----------|
| Sigmoid | (0, 1) | Binary classification output |
| Tanh | (-1, 1) | Hidden layers, zero-centered |
| ReLU | [0, ∞) | Most common hidden layer |
| Leaky ReLU | (-∞, ∞) | Avoids dying ReLU |
| Softmax | (0, 1) sum=1 | Multi-class output |

### Weight Initialization
- Zero init → symmetry problem, network cannot learn
- Random uniform: breaks symmetry but unstable with many layers
- Xavier/Glorot: `std = sqrt(2 / (fan_in + fan_out))` — good for tanh/sigmoid
- He: `std = sqrt(2 / fan_in)` — designed for ReLU

### Training Components
1. **Loss functions**: MSE (regression), Cross-Entropy (classification), MAE
2. **Backpropagation**: chain rule applied through network layers, computing gradients w.r.t each weight
3. **Optimizers**: SGD (slow convergence), SGD+Momentum (escape local minima), Adam (adaptive learning rates per parameter, most practical)

### Convergence Improvement
- **Dropout**: randomly deactivates neurons during training (e.g. 0.5 rate) → prevents co-adaptation
- **Batch Normalization**: normalizes layer outputs to mean=0, std=1 → stabilizes training, allows higher learning rates
- **Regularization**: L1/L2 weight penalties

---

## Chapter 2: MetaTrader 5 Features for Algorithmic Trading

### Platform Capabilities
- Multi-asset: Forex, stocks, futures, CFDs
- Depth of Market (DOM) with tick chart + Time & Sales
- 21 timeframes (M1 to MN1)
- Indicators: trend, volume, oscillators built-in; custom via MQL5
- Graphical objects: trend lines, channels, Fibonacci, Gann

### MQL5 IDE
- First-class IDE for writing Expert Advisors (EAs), custom indicators, scripts
- Built-in Strategy Tester with real tick history backtesting
- Optimization: genetic algorithm forward passes

### OpenCL in MQL5
- Parallel computing on GPU for matrix operations
- Key for neural network acceleration
- MQL5 has built-in OpenCL API via `CLBufferXXX`, `CLExecute`, `CLSetKernelArg`
- Enables training multiple network layers in parallel batches

### Python Integration
- MT5 Python SDK (`MetaTrader5` package)
- Train models in Python (PyTorch/TF), export weights, load into MQL5 EA
- On-chart testing via Strategy Tester with Python-trained weights

---

## Chapter 3: Building the First Neural Network Model in MQL5

### Problem Statement
- Practical case study directly related to financial markets
- Goal: demonstrate MQL5 neural network implementation, training, and comparison with Python

### ZigZag-Based Training Target Definition
- Uses MT5's built-in ZigZag indicator to define training targets
- ZigZag parameters: Depth (bars to search), Deviation (points between extrema), Backstep (min distance between extrema in candles)
- For each bar (and its preceding bar combo), compute direction + distance to nearest ZigZag extreme
- **Binary classification task**: UP (Buy) or DOWN (Sell) — flat is alternating small-amplitude Buy/Sell oscillations
- Evaluation metrics: proportion of correctly predicted directional movements + accuracy of movement strength
- This approach converts unsupervised price data into supervised training samples

### Indicator Selection via Correlation Analysis (Empirical)
- **Initial indicator basket**: ZigZag (target reference), CCI(12), RSI(12), Stochastic(12,8,3), MACD(12,48,12), ATR(12), Bollinger Bands(48,0,3), SAR(0.02,0.2), MFI(12) on M5
- **Step 1 — Correlation with targets**: 
  - RSI showed highest correlation: 0.40 (direction), 0.22 (magnitude) — lowest among all
  - MACD Main-Signal delta also useful: moderate correlation
  - ATR, High-Close, Close-Low deviations: near-zero correlation → **excluded**
- **Step 2 — Inter-indicator correlation**:
  - Stochastic, CCI, MFI correlated >0.70 with RSI → **excluded** (redundant)
  - Bollinger Bands all 3 lines showed strong correlation with RSI → **excluded**
  - SAR correlated -0.66 with MACD, -0.62 with RSI → **excluded**
- **Final selected basket**: RSI + MACD histogram + MACD signal line + MACD Main-Signal delta
- **Non-linear expansion**: Raising selected indicators to powers (square, cube) showed slower correlation decay with targets than with original values → can expand feature space with polynomial transforms

### MQL5 Program Structure
- Constant declarations for code robustness
- Neural network structure described via constants (array of layer sizes)
- Base neural network class with:
  - **Feed-forward pass**: forward propagation through all layers
  - **Backpropagation pass**: backward error propagation
  - **Dynamic arrays** for storing layers (simplifies complex architectures)

### Fully Connected Neural Layer
- Architecture: `y = f(W·x + b)`
- Activation function class (separate from layer class)
- Selection of appropriate activation functions for each layer type

### OpenCL Parallel Computing
- Technique to distribute computations across GPU devices
- Significantly speeds up matrix multiplications in forward/backward passes
- OpenCL kernels written in C-like syntax embedded in MQL5

### Perceptron Model in Python
- Python reference implementation for comparison
- Same architecture trained and tested on identical data
- MQL5 implementation should match Python output within floating point tolerance

### Gradient Distribution Verification
- Check: forward pass → loss → backward → weight deltas
- Numerical gradient checking (finite differences) to verify backprop correctness
- Both MQL5 and Python should produce the same gradient directions

### Comparative Testing
- MQL5 OpenCL vs MQL5 CPU vs Python implementations
- Training speed, convergence curves, final accuracy

---

## Chapter 4: Basic Types of Neural Layers

### Limitation of Fully Connected Networks
- Analyzes each data packet in informational vacuum (no context)
- To enlarge analyzed data → must increase model size → exponential cost
- Cannot reveal dependencies between individual elements

### Convolutional Neural Networks (CNN)
- **Architecture**: convolution kernels slide over input, extracting local features
- **Key operation**: `output = input * kernel + bias` (* = convolution)
- **Properties**: translation invariance, parameter sharing (much fewer params than FC)
- **Implementation in MQL5**: OpenCL kernels for convolution forward/backward
- **Practical use for trading**: pattern detection (candlestick formations, multi-bar structures)

### Recurrent Neural Networks (RNN) & LSTM
- **Architecture**: hidden state carries information across time steps
- `h_t = f(W_h · h_{t-1} + W_x · x_t + b)`
- **Vanishing gradient problem**: gradients shrink exponentially over long sequences
- **LSTM (Long Short-Term Memory)**:
  - Forget gate: what to discard from cell state
  - Input gate: what new info to store
  - Output gate: what to output based on cell state
  - Cell state: long-term memory highway (gradients flow through unchanged)
- **Implementation in MQL5**: LSTM block as custom layer class, OpenCL for parallel sequence processing
- **Use case**: time series forecasting where sequence order matters (price bars, tick sequences)

### Comparative Testing
- CNN vs RNN vs fully connected on same financial dataset
- Training time, accuracy, generalization to unseen data

---

## Chapter 5: Attention Mechanisms

### Why Attention?
- Human perception: focuses on relevant parts, ignores rest
- Reading a book → eyes focus on specific letters/words
- Looking at a photo → attention on faces first, background later
- Previous models (FC, CNN, RNN) treat ALL input equally — no focus mechanism

### Early Attention (Encoder-Decoder)
- First proposed 2014 for machine translation
- Components:
  1. **Encoder**: processes input sequence → hidden states
  2. **Attention block**: stores ALL encoder hidden states
  3. **Decoder**: at each output step, queries attention for relevant context
- **Alignment scores**: how relevant is each encoder state to current decoder position
- **Context vector**: weighted sum of encoder states by alignment scores
- **Softmax normalization**: ensures attention weights sum to 1

### Self-Attention
- **Key innovation**: no RNN needed — attention over input to itself
- Compute: `Attention(Q, K, V) = softmax(Q·K^T / sqrt(d_k)) · V`
  - **Q (Query)**: what I'm looking for
  - **K (Key)**: what I contain
  - **V (Value)**: what I'll pass forward
  - Q, K, V are linear projections of the same input (hence "self")
- **Scaled dot-product**: divide by `sqrt(d_k)` to prevent softmax saturation

### Multi-Head Attention
- Instead of one attention, project Q/K/V into **h subspaces** (heads)
- Each head learns different relationships
- Heads concatenated and projected back to model dimension
- Enables model to attend to different positions/reasons simultaneously

### GPT Architecture
- Decoder-only Transformer with masked self-attention
- Causal masking: each position can only attend to previous positions (not future)
  - Attention coefficients in the Score matrix for SUBSEQUENT elements are ZEROED (not masked with -inf — the book zeros them directly after normalization)
- Stack of transformer blocks → final linear + softmax for token prediction
- Block count defines model size: GPT-1=12, GPT-2 Small=12, GPT-2 XL=48, GPT-3=96
- **Autoregressive**: generates one token at a time, appends it to input sequence, feeds back to model
- **KV Cache optimization**: each layer saves Query/Key/Value vectors per element so only new tokens are computed on each iteration (no need to recalculate all vectors from scratch)
- Each transformer block has its OWN weight matrices (not shared across blocks)
- Components: Multi-Head Self-Attention + Layer Normalization + Feed Forward + Layer Normalization (per block)

### Relevance to Trading
- Time series attention: which historical bars matter most for current prediction
- Multi-head: one head learns trend, another learns volatility clustering, another learns session patterns
- Contextual embedding: market regime conditions inform price prediction

### GPT Architecture — Empirical Test Results
- **1-layer GPT** (baseline): outperformed all previous models (CNN, LSTM, FC) on the same dataset — lowest error of any architecture tested, but with larger fluctuations due to gradient propagation limited to current state
- **4-layer GPT**: further reduced minimum error; more parameters required more training iterations; more prone to overfitting (consistent with universal scaling laws)
- **Larger stack (60 candles vs default)**: improved error without changing model parameters — purely from more historical context in Key/Value tensors. Stack size is an architectural hyperparameter that doesn't affect weight matrix count
- **KV Cache optimization**: each layer saves Query/Key/Value vectors per element → only new tokens computed each iteration, dramatically reducing computation for long sequences
- **Causal masking**: attention coefficients for subsequent elements are ZEROED (not masked with -inf) after Softmax normalization — a deliberate implementation choice in the book's MQL5 code
- **Key finding**: GPT architecture's benefit is most pronounced with long input sequences; for short sequences (<20 bars), simpler models may suffice; for Noru's 200-bar NHITS input windows, attention mechanisms could add value

### Backpropagation in GPT (Implementation Detail)
- Gradient propagates through 3 paths: Query, Key, Value tensors
- Softmax derivative requires complete set of function outputs (not just individual elements)
- Error gradient from previous states is NOT recomputed — each iteration assumes gradient from past states was already handled in previous backprop passes
- This is a deliberate optimization: computing gradient through all past states requires storing all past inputs, which is memory-prohibitive for long sequences

---

## Chapter 6: Architectural Solutions for Improving Model Convergence

### Batch Normalization
- **Problem**: internal covariate shift — distribution of layer inputs changes during training
- **Solution**: normalize each mini-batch to mean=0, std=1
  ```
  μ = mean(x_batch)
  σ² = variance(x_batch)
  x_norm = (x - μ) / sqrt(σ² + ε)
  y = γ · x_norm + β    (learnable scale γ and shift β)
  ```
- **Benefits**: higher learning rates, less sensitive to initialization, regularizing effect
- **Implementation in MQL5**: forward pass (normalize batch), backward pass (gradients w.r.t x, γ, β)

### Dropout
- **Problem**: co-adaptation — neurons become overly reliant on specific other neurons
- **Solution**: randomly drop (zero out) a fraction of neurons each training step
  ```
  mask = Bernoulli(p)  // p = keep probability
  output = input * mask / p  // scaling ensures consistent magnitude at test time
  ```
- **At training**: dropout active = stochastic regularization
- **At inference**: dropout disabled = full network with scaled weights
- **Typical rate**: p=0.5 for fully connected, p=0.2-0.3 for CNN/RNN
- **Implementation in MQL5**: random mask generation (OpenCL parallel), forward masking, backward gradient routing

### Comparative Testing
- Model without normalization/dropout vs. with batch norm vs. with dropout vs. with both
- Convergence speed, final accuracy, generalization gap (train vs test)

### Dropout Effectiveness Nuances (Empirical)
- On small models (few neurons, uncorrelated features), Dropout **worsened** MSE and accuracy — masking limited capacity further
- On larger models (3 hidden layers), Dropout reduced the **gap between train and validation** curves → confirmed anti-overfitting benefit
- Combined use of Dropout + Batch Normalization showed mixed results; some studies suggest they antagonize each other
- **Key insight**: Dropout's value increases with model size. For Noru's 28-model NHITS ensemble (already diversity-regularized), Dropout may offer diminishing returns

---

## Chapter 7: Testing Trading Capabilities

### MT5 Strategy Tester
- Built-in backtesting engine
- Mode: every tick (most accurate), control points, open prices only
- Historical data: real ticks from broker (if available)
- Multi-threaded optimization runs

### Expert Advisor Template
- Standard EA structure for neural network integration:
  ```
  OnInit()         → load NN weights from file, initialize layers
  OnTick()         → prepare input data, run forward pass, interpret signal
  OnDeinit()       → clean up, close resources
  ```
- **Key design**: separate NN inference from trading logic
- NN module: class that loads, infers, returns signal (-1/0/+1)
- Trading module: receives signal, applies risk rules, executes

### Model Creation for Testing
- Prepare input features: OHLCV, indicators, normalized and scaled identically to training
- Normalization: same mean/std (or min/max) computed during training, stored in file
- Input window size matches training: last N bars of features
- Output interpreted as: direction (classification) or magnitude (regression)

### Expert Advisor Parameters
- User-facing parameters exposed to MT5 testing interface:
  - `InpModelFile` — path to trained NN weights
  - `InpNormFile` — path to normalization parameters
  - `InpTakeProfit` — TP in points
  - `InpStopLoss` — SL in points
  - `InpLotSize` — fixed or risk %
  - `InpMagicNumber` — EA identifier

### Testing on New Data (Out-of-Sample) — Empirical Results

**Forward test on 2021 data** (untouched during training/optimization on 2015-2020):

**Optimized parameters** (via Strategy Tester):
- Confidence factor: 0.8
- Stop-loss: 400 points
- MinTarget (decision threshold): 500 points
- MaxTP (profit cap): 600 points
- TradeLevel (probability threshold): 0.6

**Performance metrics**:
- 36 total positions opened
- 21 profitable (58.33% win rate — matches the 60% threshold expectation)
- Profit Factor: 1.48 (vs 1.22 during training — OOS performance exceeded IS)
- Max consecutive losses: 3
- Max consecutive wins: 6

**Day-of-week analysis**:
| Day | Positions | Profitability |
|-----|-----------|---------------|
| Wednesday | ~30% of all | Highest profit |
| Monday | 2nd most | Best profit-to-loss ratio |
| Friday | Moderate | Break-even |
| Tuesday | Low | **Net loss** |
| Thursday | Low | **Net loss** |

**Key insight**: Adding a simple day-of-week filter (trade only Mon+Wed) could eliminate inherently unprofitable sessions without changing the model.

**Walk-forward**: train on window T, test on window T+1, slide and repeat
- Metrics to evaluate:
  - Net profit, win rate, profit factor, Sharpe ratio, max drawdown
  - **Confusion matrix**: TP/FP/TN/FN of NN predictions
  - **Equity curve**: visualize stability
- Compare NN-based EA against benchmark (buy-and-hold, simple MA crossover)

---

## Key Takeaways for Noru's Master of Trade

### The Book's 3 Core Findings (from Conclusion)

> "My intention in showcasing these diverse architectural solutions wasn't merely to provide examples. It's a reminder to never fear to experiment. While it's easier to follow the beaten path, it only leads to repeating what has already been achieved, no matter how good these achievements may be... true innovation and personal growth come from venturing off-road and embracing the unknown."
>
> "In this book, we have built a library that will assist you in implementing your own neural network models, training them on historical data, and testing their performance in the strategy tester using the provided Expert Advisor template."
>
> "I wish you to find the model that will bring you profit and prosperity. It is important to remember: Make sure to thoroughly verify and comprehensively test the Expert Advisor before entrusting it with your savings."

1. **Technical analysis can identify stable patterns** with at least 60% profitability — chart patterns exist that generate reliable signals
2. **Neural network models can identify such patterns** — the library built in the book detects the same patterns machine-learned traders identify manually
3. **NN-based Expert Advisors can achieve stable profitability** over extended periods when properly trained and validated

### Architectural Principles
1. **MQL5 implements NN from scratch** — layer classes, activation functions, OpenCL kernels
2. **OpenCL acceleration is mandatory** for real-time inference on tick data (CPU-only is too slow for multi-layer networks at 1s intervals)
3. **Python is complementary** — prototyping, training, backtesting; MQL5 handles live execution

### Layer Selection Guide
| Data Type | Recommended Layer | Rationale |
|-----------|------------------|-----------|
| Raw OHLCV sequence | LSTM / GRU | Temporal dependencies, sequence order matters |
| Multi-bar patterns | CNN 1D | Pattern detection across bars |
| Complex multi-input | Transformer Attention | Weigh which historical context matters now |
| High-dimensional features | Fully Connected w/ Batch Norm | Feature interaction, stable training |

### MQL5 Implementation Notes
- Neural network library structure: base layer class → derived classes (FCLayer, ConvLayer, LSTMLayer, AttnLayer)
- Each layer: forward(), backward(), save(), load()
- OpenCL kernels in `.cl` files, compiled at runtime
- Weight storage: binary file matching Python `numpy.save()` format
- Normalization params stored alongside weights

### Integration with Noru's Existing System
- Current system uses Python-based NHITS ensemble + `auto_trade.py` loop
- NeuroBook approach: train in Python, deploy in MQL5 → inference runs inside MT5 Strategy Tester or MT5's Expert Advisor
- Hybrid approach possible: Python handles ensemble (current), MQL5 handles fast secondary model (e.g. CNN for pattern confirmation)
- OpenCL acceleration in MQL5 could complement GPU-free inference design

### Critical Warnings
- **Overfitting**: NN with many parameters on limited price data → perfect backtest, failing live
- **Out-of-sample validation**: must test on data never seen during training/validation
- **Non-stationarity**: market regimes change → models must be retrained periodically
- **Execution lag**: MQL5 NN inference must complete within tick interval (sub-second for MT5 ticks)
- **Risk integration**: NN signal is ONE component — combine with risk management, don't trade NN blindly

---

## Content Retrieval Pattern (JS-Heavy MQL5 Pages)

The NeuroBook is served as a JavaScript-heavy single-page app. The browser may show "404 Not Found" in the rendered DOM while `curl` returns HTTP 200 with the full HTML. To extract content:

```bash
# Fetch TOC from main page
curl -sL "https://www.mql5.com/en/neurobook" | grep -oP 'href="/en/neurobook/index/[^"]*"' | sort -u

# Extract chapter summary text from /index/ sub-pages
curl -sL "https://www.mql5.com/en/neurobook/index/<slug>" | sed -n '/<div class="docsContainer">/,/<\/div>/p' | sed 's/<[^>]*>//g' | sed '/^$/d'

# Available slug paths: intro, about_ai, algotrading, realization, main_layer_types, transformer, improvement_realization, trade_check, conclusion
```

---

## References
- MQL5 NeuroBook PDF: https://www.mql5.com/en/neurobook
- MT5 Python SDK: https://www.mql5.com/en/docs/python
- OpenCL in MQL5: https://www.mql5.com/en/docs/ocl
- See `master_of_trade` skill §4 (AI & ML for Financial) for NHITS ensemble integration
