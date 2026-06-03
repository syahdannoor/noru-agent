# Smart Money Strategy – placeholder implementation.
# ---------------------------------------------------
# This stub mirrors the behaviour of a full‑featured Smart Money
# detector that would analyse order‑block footprints, liquidity
# sweeps, Fibonacci convergences, etc.  Until the real model is
# available, the detector uses a deterministic surrogate that
# respects the parameters defined in ``config.SMART_MONEY``.
# 
# Expected public interface:
#   ``generate_signal(df: pd.DataFrame, state: dict) -> Signal | None``
# 
# The stub implements a very common “order‑block” heuristic:
#   1️⃣ Scan the recent ``lookback`` candles for a strong bullish or
#      bearish candle whose body occupies > ``body_ratio`` of the total
#      candle range (high‑low).  That candle becomes the “order block”.
#   2️⃣ Validate that the next candle shows a “mitigation” – i.e. price
#      retraces only a small fraction (``confluence_window``) of the
#      prior body before resuming the original direction.
#   3️⃣ If the pattern is found, emit a ``'BUY'`` (for a bullish OB) or
#      ``'SELL'`` (for a bearish OB) signal with a confidence score
#      derived from the size of the OB relative to the recent average
#      body size.
# 
# All parameters are read from ``config.SMART_MONEY`` so they can be
# tweaked without touching code.

from __future__ import annotations

import pandas as pd
from ..base import BaseStrategy, Signal
from ...config import config

class SmartMoneyStrategy(BaseStrategy):
    """
    Placeholder Smart Money pattern detector.
    """

    def __init__(self) -> None:
        # Load configuration values – they are defined in config.py.
        p = config.SMART_MONEY
        self.body_ratio: float = float(p.get("body_ratio", 0.6))        # min body / total range
        self.lookback: int = int(p.get("lookback", 30))                 # candles to scan
        self.confluence_window: float = float(p.get("confluence_window", 0.5))  # max retrace fraction
        self.min_ob_size: float = float(p.get("min_ob_size", 0.02))      # min OB size as fraction of recent avg body

    def generate_signal(self, df: pd.DataFrame, state: dict) -> Signal | None:
        """
        Detect a Smart Money order‑block pattern.

        Parameters
        ----------
        df : pd.DataFrame
            Market candles. Must contain ``open``, ``high``, ``low``, ``close`` and ``volume``.
        state : dict
            Runtime context (unused in this stub but retained for future compatibility).

        Returns
        -------
        Signal | None
            ``'BUY'`` when a bullish order‑block is detected,
            ``'SELL'`` when a bearish order‑block is detected,
            ``None`` when the pattern is not present.
        """
        if df.empty or len(df) < self.lookback + 2:
            return None

        # ---- 1️⃣ Compute recent candle bodies ------------------------------
        df["body"] = abs(df["close"] - df["open"])
        df["trange"] = df["high"] - df["low"]
        # Average body of the most recent candles (excluding the last one)
        recent_bodies = df["body"].iloc[-self.lookback:-1]
        avg_body = recent_bodies.mean() if len(recent_bodies) > 0 else 1e-6

        # ---- 2️⃣ Scan for a qualifying order‑block candle -----------------
        # Look at the candle just before the most recent one (index -2)
        # because we need a “next‑candle” to verify mitigation.
        cand_idx = -2
        candle = df.iloc[cand_idx]

        # Condition A: body is a substantial fraction of the total range
        body_frac = candle["body"] / candle["trange"]
        if body_frac < self.body_ratio:
            return None

        # Direction of that large body
        is_bullish_ob = candle["close"] > candle["open"]
        direction = "BUY" if is_bullish_ob else "SELL"

        # ---- 3️⃣ Verify mitigation on the following candle -----------------
        # The next candle must retrace only a small part of the prior body
        next_candle = df.iloc[cand_idx + 1]
        # Price move against the OB direction should be limited
        if is_bullish_ob:
            # After a bullish OB we expect price to continue upward;
            # a retreat > confluence_window of the OB body invalidates it.
            retreat = (next_candle["low"] - candle["close"]) / candle["body"]
        else:
            # After a bearish OB we expect price to continue downward;
            # a rally > confluence_window of the OB body invalidates it.
            retreat = (next_candle["high"] - candle["close"]) / candle["body"]

        if retreat > self.confluence_window:
            return None

        # ---- 4️⃣ Confidence based on OB size ---------------------------------
        # Confidence = (OB body size) / (average recent body size), capped at 1.0
        confidence = min(float(candle["body"]) / self.min_ob_size / avg_body, 1.0)

        # ---- 5️⃣ Emit Signal ---------------------------------------------------
        comment = (
            f"SmartMoney OB {direction} detected at {candle.name:.0f} "
            f"body_frac={body_frac:.2f} retreat={retreat:.2f}"
        )
        return Signal(
            direction=direction,
            source="smart_money",
            confidence=float(confidence),
            comment=comment,
        )