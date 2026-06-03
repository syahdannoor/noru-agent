# NHITS Forecast Engine — PyTorch CUDA

## Overview
NHITS (Neural Hierarchical Interpolation for Time Series) via the **`neuralforecast`** library (PyTorch CUDA). Runs **7 independent models** across M3, M5, M15, M30, H1, H4, D1 for multi‑scale price forecast and consensus‑based entry blocking/boosting.

## Architecture
```
input (B, L, F)
  └─ Stack 1: AvgPool1d(k=2,s=2) ─→ MLP ─→ backcast + forecast
  └─ Stack 2: AvgPool1d(k=4,s=4) ─→ MLP ─→ backcast + forecast   (residual ← prev backcast)
  └─ Stack N: AvgPool1d(k=N,s=N) ─→ MLP ─→ backcast + forecast   (residual ← prev backcast)
  └─ Sum all forecasts → (B, H, 1)
```

- **L** = lookback (candles), **F** = features (OHLCV, 5), **H** = horizon (candles ahead)
- Backcast heads reconstruct input for gradient boosting residual
- Final forecast = sum of all stack forecasts

## Timeframe Presets

| Preset | Lookback | Horizon | Pool Sizes | n_stacks | mlp_units | Params | Data |
|--------|----------|---------|------------|----------|-----------|--------|------|
| **M5** | 96 (~8h) | 12 (~1h) | [2, 4, 8] | **4** | **[512, 256]** | **1.5M** | 500+ candles |
| **M3** | 200 (~10h) | 20 (~1h) | [4, 8, 12] | **4** | **[256, 256]** | **1.89M** | 1000+ candles |

Switching:
```python
engine = NHITSEngine({"timeframe": "M3"})  # or "M5"
```

Each preset has unique model & stats paths:
- `nhits_model_m5.pth` + `nhits_stats_m5.json`
- `nhits_model_m3.pth` + `nhits_stats_m3.json`

## Parameter Tuning Results

### Methodology
A grid-search benchmark runs 11 parameter variants per timeframe, training on live MT5 data. Each test changes ONE hyperparameter from baseline. 22 total training runs, ~45s on GTX 1050 Ti.

Parameters tested: `mlp_units`, `learning_rate`, `n_stacks`, `batch_size`.

Metrics tracked: `val_loss`, `val_mae`, training time, model parameter count.

Benchmark script: `benchmark_nhits.py` — saves full JSON results to `nhits_benchmark.json`.

### M5 Results
| Config | val_loss | val_mae | Time | Params |
|--------|----------|---------|------|--------|
| Baseline (256/256, 3st, lr=0.001) | 0.01488 | 0.09877 | 2.4s | 761K |
| MLP [128,128] | 0.01060 | **0.08127** | 1.6s | 370K |
| **MLP [512,256]** | 0.00884 | 0.08107 | 1.8s | 1.07M |
| LR 0.0005 | 0.01078 | 0.09112 | 1.5s | 761K |
| **Stacks 4** | **0.00875** | **0.07428** | 1.9s | 1.07M |
| Batch 32 | 0.01062 | 0.08550 | 2.2s | 761K |

**Winners**: Stacks 4 (best loss/mae) and MLP [512,256] (close second).
**Final best combos**: Stacks 4 + MLP [512,256] → val_loss=0.01021, val_mae=0.07993, 1.5M params

### M3 Results
| Config | val_loss | val_mae | Time | Params |
|--------|----------|---------|------|--------|
| Baseline (256/256, 3st, lr=0.001) | 0.00877 | 0.06556 | 3.2s | 1.19M |
| **Stacks 4** | **0.00787** | **0.06448** | 4.3s | 1.89M |
| Stacks 2 | 0.01057 | 0.07275 | 2.2s | 831K |
| LR 0.0003 | 0.01180 | 0.07949 | 3.2s | 1.19M |

**Winner**: Stacks 4 — best on both loss and mae.
**Final best**: Stacks 4 + MLP [256,256] → val_loss=0.01132, val_mae=0.07803, 1.89M params

### Key Insights
- **Stacks 4** consistently outperforms for both M5 and M3 — the extra hierarchy captures multi-scale patterns better.
- **MLP size effect**: M5 benefits from wider MLP ([512,256]); M3 prefers [256,256] — likely because M3 already has more data granularity.
- **Lower LR** (0.0003/0.0005) does NOT improve results — the model converges fine at 0.001.
- **Batch size**: 64 is the sweet spot. Batch 32 is too noisy, batch 128 is too coarse.

## TF → PyTorch Migration Notes

### Key Code Changes
| TensorFlow | PyTorch |
|-----------|---------|
| `tf.keras.layers.AveragePooling1D` | `nn.AvgPool1d` + `permute` |
| `tf.keras.layers.Dense` | `nn.Linear` |
| `tf.keras.Sequential` | `nn.Sequential` |
| `model.fit()` | Manual training loop |
| `model.save_weights(.weights.h5)` | `torch.save(model.state_dict(), .pth)` |
| `tf.keras.callbacks.EarlyStopping` | Manual patience loop |
| `ReduceLROnPlateau` | (not needed — Adam sufficient + early-stop) |

### GPU Setup (Windows)
```bash
# PyTorch CUDA 12.6 for Windows — large download (~2.6GB)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
# Always use terminal(background=true, timeout=600) to handle the download size
```

### Common Pitfalls
- **numpy float64 → torch float32 mismatch**: Always `.astype(np.float32)` before `torch.from_numpy()`, otherwise model weights (float32) mismatch input (float64).
- **Partial PyTorch CUDA install**: If pip times out, you get `caffe2_nvrtc.dll` but missing `torch_cuda.dll`. Uninstall (`pip uninstall torch torchvision torchaudio`) and retry with background mode + long timeout.
- **Data format**: PyTorch `nn.AvgPool1d` expects `(N, C, L)` — permute from `(N, L, C)` then back.
- **Model file extension**: TF saves `.weights.h5`, PyTorch saves `.pth`. Old TF weight files must be removed manually.
- **TensorFlow removal**: After migration, `pip uninstall tensorflow` saves ~9GB disk space.
- **NHITSEngine._last_val**: After training, `engine._last_val` dict contains `{"val_loss": ..., "val_mae": ...}` for programmatic access.

## Signal Integration in Auto-Trade

In `auto_trade.py`, NHITS runs as a confirmation layer:
```python
if nhits_signal["signal"] != signal["direction"]:
    # NHITS disagrees — skip entry
    return
```

NHITS signal uses 0.05% threshold (configurable). If forecast Δ < 0.05%, returns `NONE_FORECAST` (no veto).

## Performance (GPU vs CPU)

| Model | CPU (TF) | GPU (Torch CUDA) | Speedup |
|-------|----------|-------------------|---------|
| M5 (500 candles) | 4.3s | **1.1s** | ~4× |
| M3 (1000 candles) | — | **2.7s** | — |

## MT5 Connector — Timeframe Support

The `mt5_connector.py` `get_rates()` method must support the timeframe used. Added mappings:

```python
tf_map = {
    "M1": mt5.TIMEFRAME_M1,
    "M2": mt5.TIMEFRAME_M2,   # ← ADDED
    "M3": mt5.TIMEFRAME_M3,   # ← ADDED
    "M4": mt5.TIMEFRAME_M4,   # ← ADDED
    "M5": mt5.TIMEFRAME_M5,
    ...
}
```

---

## 7-TF Ensemble Consensus Engine (v3)

Replaces the old Dual NHITS (v2). **4 models × 7 timeframes = 28 independent NHITS trainings**, forecasts averaged per TF, then a weighted consensus across all TFs for the final signal.

### Architecture: Decoupled Training → Inference

```
                    TRAINING (offline, on-demand)
  ┌─────────────────────────────────────────────────────┐
  │ _ensemble_train.py                                   │
  │  ├─ 4 variants per TF: seed=42,99,123,456           │
  │  │   different architectures (stacks, mlp, pool)     │
  │  │   different lr (0.0005–0.002) and epochs (50–80) │
  │  ├─ average forecasts per TF → ensemble_results.json │
  │  └─ 28 models, ~90s on GTX 1050 Ti                  │
  └──────────────────────┬──────────────────────────────┘
                         │ writes
                         ▼
              ensemble_results.json
  ┌──────────────────────────────┐
  │ Key: "M3".."D1"              │
  │ Per TF: avg_forecast,        │
  │   signal, conf, change_pct,  │
  │   agreement_pct, buy/sell    │
  │   votes, individual signals  │
  └──────────────────────────────┘
                         │ reads
                         ▼
                    INFERENCE (live, no GPU)
  ┌─────────────────────────────────────────────────────┐
  │ EnsembleLoader (ensemble_loader.py)                  │
  │  ├─ loads ensemble_results.json on startup           │
  │  ├─ refresh(max_age=30min) checks file mtime         │
  │  ├─ get_consensus(price) → weighted signal           │
  │  └─ get_tf_signal(tf) → per-TF details              │
  └──────────────────────┬──────────────────────────────┘
                         │
                         ▼
                  auto_trade.py
              (no live NHITS training)
```

### 4-Model Variants per TF

| Variant | seed | stacks | mlp | pool | lr | epochs | Purpose |
|---------|------|--------|-----|------|----|--------|---------|
| ensemble_0 | 42 | Per-TF default | Default | Default | 0.001 | 50 | Baseline |
| ensemble_1 | 99 | Same | 1.5× wider | Same | 0.0005 | 80 | Larger capacity, slower learn |
| ensemble_2 | 123 | +1 stack | Same | 2× wider | 0.002 | 50 | More hierarchy, wider pooling |
| ensemble_3 | 456 | +2 stacks | 0.8× narrower | Same | 0.001 | 50 | Deeper, regularised via width reduction |

Each TF has its own lookback/horizon/pool preset (M3=200→20, pool[4,8,12]; M5=96→12, pool[2,4,8]; etc.). All 4 variants share the same preset.

### Weighted Consensus Formula (`EnsembleLoader.get_consensus()`)

```python
for tf in TF_ORDER:
    w = TF_WEIGHTS[tf]          # M3=0.6, M5=0.8, M15=1.0, M30=1.2, H1=1.5, H4=2.0, D1=3.0
    aggr_mult = 1.0 if agreement >= 80 else 0.7 if >= 50 else 0.4
    tf_weight = confidence * w * aggr_mult

    if signal == "BUY" and confidence >= 0.5:
        buy_weight += tf_weight
    elif signal == "SELL" and confidence >= 0.5:
        sell_weight += tf_weight

# Final direction
if buy_weight > sell_weight:  consensus = "BUY"
elif sell_weight > buy_weight: consensus = "SELL"
else: consensus = "NONE"
```

Weight shape: longer TFs (H4=2×, D1=3×) dominate, short TFs (M3=0.6×, M5=0.8×) act as noise filters.

### Dynamic TP Update in `_manage_positions()`

Uses **M5 ensemble forecast** (not live NHITS) for near-term directional TP extension:

```python
m5_data = ensemble.get_tf_signal("M5")
if m5_data and m5_data.get("forecast_prices"):
    fp = m5_data["forecast_prices"]
    fut_dir = "BUY" if fp[-1] > fp[0] else "SELL"
    if pos["type"] == "BUY" and fut_dir == "BUY":
        new_tp = max(fp[-1], current_tp)   # extend, never retract
```

### Consensus Flow Diagram

```
Strategy Signal (direction=X)
    │
    ▼
┌──────────────────────────────────────────┐
│  EnsembleLoader (7-TF weighted)          │
│  ├─ Load ensemble_results.json           │
│  ├─ Per TF: M3..D1 signal/log           │
│  └─ Weighted → BUY/SELL/NONE            │
└──────────┬───────────────────────────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
  = direction  ≠ direction   / neutral
     │           │
     ▼           ▼
 HIGH conf    BLOCK entry
 + TP override   │
 + lot boost  Or: ≥2 TFs oppose → block
     │           │
     ▼           ▼
 Executor.market_order()
```

### Pitfalls

- **Race condition on retrain**: `_retrain_nhits()` launches `subprocess.run(_ensemble_train.py)` which writes to `ensemble_results.json` while `EnsembleLoader` may be reading it. **Fix**: training script writes to a temp file then atomically renames (`os.replace()`). Currently known — not yet fixed in codebase.
- **GPU contention**: Before running `_ensemble_train.py`, kill the auto-trade bot first (it no longer uses GPU during inference, but the subprocess subprocess inherits GPU context). Check with `ps aux | grep auto_trade.py` and kill if running.
- **Stale forecasts**: Ensemble results are snapshots. If the bot runs for hours without retraining, forecasts become stale. `EnsembleLoader.refresh()` checks mtime every 30 min.
- **Cold start**: All 28 models train on first run. TFs with fewer candles (D1 ~200, H4 ~150) have higher val_loss. First ensemble may produce weak signals until enough data accumulates.
- **No GPU for inference**: `EnsembleLoader` is pure JSON parsing — zero GPU usage during live trading. All 28-model training is batch/offline.
- **JSON format mismatch**: `ensemble_results.json` keys: `ensemble.{TF}.avg_forecast` (not `forecast_prices`), `agreement_pct` (not `agreement`). `EnsembleLoader` maps these keys. If format changes, update the loader.
- **Subprocess timeout**: 28-model training takes ~90s on GTX 1050 Ti. The subprocess timeout in auto_trade is 1200s (20min) — safe even if GPU is throttled.
