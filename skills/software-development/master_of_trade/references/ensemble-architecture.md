# NHITS Ensemble Architecture — Noru v2

## Overview
28 independent NHITS models (4 variants × 7 timeframes) for XAUUSD.

**Decoupled design**: `_ensemble_train.py` trains all models offline → saves `ensemble_results.json`. `EnsembleLoader` reads it during live trading. **Zero GPU during inference.**

**⚠️ CRITICAL ARCHITECTURE RULE: Ensemble = primary direction decider.**
Dulu ensemble cuma dipakai sebagai BLOCK filter — jika StrategyEngine dan ensemble mismatch, BLOCK. Tapi celah: tiap TF punya sinyal sendiri. StrategyEngine bisa baca M5 bearish dan entry SELL, sementara ensemble H4/D1 bullish 84% — dan BLOCK tidak aktif karena mismatch tidak terdeteksi seragam. Hasil: 6× SELL beruntun loss $200K+, lalu BUY 0.04 kena SL -$356K. **Total drawdown -64% ($450K→$161K).**

**Fix: ensemble signal = arah entry utama. StrategyEngine = fallback hanya saat ensemble NEUTRAL + conf > 0.7.**
Lihat `_evaluate_entry()` di `auto_trade.py` untuk implementasi.

## TF Presets

| TF | Lookback | Horizon | Pooling Sizes | Block Time |
|----|----------|---------|---------------|------------|
| M3 | 200 bars | 20 | [4, 8, 12] | ~15 min (15m candles) |
| M5 | 96 | 12 | [2, 4, 8] | ~8 min |
| M15 | 48 | 10 | [2, 4] | ~5 min |
| M30 | 40 | 8 | [2, 4] | ~3 min |
| H1 | 36 | 6 | [2] | ~2 min |
| H4 | 30 | 5 | [2] | ~2 min |
| D1 | 20 | 3 | [1] | ~1 min |

## 4 Model Variants

All variants share the per-TF preset above but differ in architecture:

| Variant | Seed | MLP Units | Stacks | Pool Size Mult | Epochs | Dropout |
|---------|------|-----------|--------|----------------|--------|---------|
| baseline (0) | 42 | 512 | 2 | 1.0× | 100 | 0 |
| larger MLP (1) | 99 | 1024 | 2 | 1.0× | 150 | 0 |
| wider pools (2) | 123 | 512 | 3 | 2.0× | 100 | 0 |
| deeper+dropout (3) | 456 | 768 | 3 | 1.0× | 150 | 0.1 |

Saved to: `ensemble/{name}_{tf}.pt` where name = TF lower (e.g. `m5_baseline`, `m5_variant1`, etc.)

## Weighted Consensus

```
buy_weight = Σ(tf.weight × tf.agreement_mult × tf.avg_forecast_change_pct_in_buy_direction)
sell_weight = same but in sell direction
```

**TF weights**: D1=3, H4=2, H1=1.5, M30=1.2, M15=1.0, M5=0.8, M3=0.6

**Agreement multiplier**: agreement_pct ≥ 80% → 1.0×, ≥ 50% → 0.7×, else 0.4×.

Final bias: buy_weight > sell_weight → BULLISH, sell_weight > buy_weight → BEARISH, ratio < 5% → NEUTRAL.

Confidence: absolute difference capped at 0.95.

## Atomic Retrain (Race Fix)

`_ensemble_train.py` writes to `ensemble_results.json.tmp` then renames atomically:

```python
tmp_path = save_path + ".tmp"
with open(tmp_path, "w") as f:
    json.dump(ensemble_data, f, indent=2, default=str)
    f.flush()
    os.fsync(f.fileno())
shutil.move(tmp_path, save_path)  # atomic on same filesystem
```

Retrain is non-blocking (subprocess.Popen) with 6-hour cooldown.

## JSON Output Format

```json
{
  "generated_at": "2026-05-26 20:00",
  "price": 4524.07,
  "final_bias": "BULLISH",
  "buy_weight": 4.8,
  "ensemble": {
    "M3": {"signal": "NEUTRAL", "confidence": 0.0, "avg_forecast": 4523.5, "change_pct": -0.01, "agreement_pct": 50, "n_models": 4, ...},
    "M5": {"signal": "SELL", ...},
    ...
  }
}
```

Key mapping loaded by EnsembleLoader: `forecast_prices` → `avg_forecast`, `agreement` → `agreement_pct`.

## Telegram Reporting

Every MT5 action logs to `logs/executions.jsonl`. Cron `no_agent=True` script tails and delivers to Telegram every minute. See `## Telegram Execution Reporting` in SKILL.md.

## Pitfalls

- **⚠️ CRITICAL: Ensemble as filter (BLOCK) ≠ Ensemble as decider.** Jangan pernah setting ensemble sebagai BLOCK filter saja. Celah: StrategyEngine pake TF berbeda (M5) yang bisa neutral → BLOCK tidak aktif → StrategyEngine override. Fix total: ensemble signal = arah entry utama, StrategyEngine = fallback dengan guard ketat.
- **Stale forecasts**: ensemble_results.json is a snapshot. Retrain at least once daily.
- **GPU contention**: Never run `_ensemble_train.py` while auto_trade is live. Kill bot first.
- **CUDA memory**: 28 models × GTX 1050 Ti (4GB) → ~90s total. Each model uses ~100MB VRAM.
- **File sync**: Always use `.tmp` + rename pattern. `open("w")` directly to the shared file causes partial reads.
- **Retrain throttle**: 6-hour cooldown via `self._last_retrain_time`. Reset to 0 if you force a manual retrain.
