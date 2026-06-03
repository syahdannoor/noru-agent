---
name: ensemble
description: "Aggregate and weight signals from multiple strategies, persist weights, provide weighted signal list."
version: 0.2.0
author: Hermes Agent
license: MIT
tags: [strategy, ensemble, weighting, signals, noru5]
---
# Ensemble Strategy

## Purpose
Aggregate signals from all loaded strategies, compute a weighted vote, and return a list of `WeightedSignal` objects.  Weights are derived from historic win‑rate stored in `MarketMemory`.

## Inputs
- `signals: List[Signal]` – raw signals from strategies.
- `state: dict` – runtime context (includes current market regime, equity, etc.).

## Outputs
- `List[WeightedSignal]` where each entry adds `weight: float` (0‑1) representing confidence based on historic performance.

## Configuration
- Weights are calculated as `win_rate / max_win_rate` across all strategies.  
- Optional decay factor can be applied via `config.ENSEMBLE_DECAY` (default 0.0, no decay).

## Implementation
```python
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
from ..base import Signal, BaseStrategy
from ..memory.market_memory import MarketMemory
import json
import pathlib

@dataclass
class WeightedSignal:
    """Extension of Signal that adds a `weight` field."""
    direction: str
    source: str
    confidence: float
    comment: str
    weight: float

class Ensemble:
    """
    Core ensemble logic.
    - `aggregate_and_weight(signals, state)` converts a list of `Signal` objects
      into `WeightedSignal` instances, assigning each a weight derived from
      its historic win‑rate.
    - `update_weights()` recomputes win‑rates via `MarketMemory.get_win_rate_for_pattern`
      and persists the resulting weight mapping to `engine/ensemble/weights.json`.
    """
    def __init__(self, memory: MarketMemory | None = None):
        self.memory = memory or MarketMemory()
        self.weights_path = pathlib.Path(__file__).parents[2] / "ensemble" / "weights.json"
        self.weights: Dict[str, float] = {}

    def aggregate_and_weight(self, signals: List[Signal], state: dict) -> List[WeightedSignal]:
        """Convert raw signals into weighted signals."""
        weighted: List[WeightedSignal] = []
        win_rates = {}
        # Retrieve win‑rate for each signal's comment (pattern label)
        for sig in signals:
            rate = self.memory.get_win_rate_for_pattern(sig.comment) if self.memory else 0.0
            win_rates[sig.comment] = rate
        max_rate = max(win_rates.values()) if win_rates else 1.0
        for sig in signals:
            weight = (win_rates.get(sig.comment, 0.0) / max_rate) if max_rate > 0 else 0.0
            weighted.append(WeightedSignal(
                direction=sig.direction,
                source=sig.source,
                confidence=sig.confidence,
                comment=sig.comment,
                weight=weight,
            ))
        # Store latest weights for potential later retrieval
        self.weights = {sig.comment: weight for sig, weight in zip(signals, [w.weight for w in weighted])}
        return weighted

    def update_weights(self) -> None:
        """Re‑calculate win‑rates and persist them."""
        # Example: assume each signal comment maps to a known pattern key
        pattern_keys = list(self.weights.keys())
        rates = [self.memory.get_win_rate_for_pattern(k) for k in pattern_keys]
        avg_rate = sum(rates) / len(rates) if rates else 1.0
        self.weights = {k: (r / avg_rate) if avg_rate > 0 else 0.0 for k, r in zip(pattern_keys, rates)}
        # Persist to JSON
        self.weights_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.weights_path, "w") as f:
            json.dump(self.weights, f, indent=2)