#!/usr/bin/env python
"""
Deterministic validation script for the Smart Money placeholder detector.

Usage:
    python -m smart_money.validate
"""

import pandas as pd
from src.noru5.engine.strategies.smart_money import SmartMoneyStrategy
from src.noru5.config import config

def generate_sample_df():
    """Create a synthetic DataFrame with a clear bullish order‑block."""
    # Generate 40 rows of random-walk price data
    import numpy as np
    np.random.seed(42)
    price = 1900 + np.cumsum(np.random.normal(0, 1, 40))
    high = price * 1.02
    low = price * 0.98
    open_ = price
    close = price + np.random.normal(0, 0.5, 40)
    volume = np.random.randint(1, 100, 40)

    df = pd.DataFrame({
        "open": open_,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume,
    }, index=pd.date_range(start="2026-01-01 00:00", periods=40, freq="5T"))

    # Insert a clear bullish OB candle near the end
    # Make the 38th candle a strong bullish body
    df.loc[38, "open"] = 1970
    df.loc[38, "close"] = 1990  # strong bullish move
    df.loc[38, "high"] = 1995
    df.loc[38, "low"] = 1965
    df.loc[38, "volume"] = 80

    # The next candle should be a small retreat (mitigation)
    df.loc[39, "open"] = 1990
    df.loc[39, "close"] = 1985  # retreat of 5 points
    df.loc[39, "high"] = 1995
    df.loc[39, "low"] = 1980
    df.loc[39, "volume"] = 30

    return df

def main():
    df = generate_sample_df()
    strategy = SmartMoneyStrategy()
    state = {}  # empty runtime context
    signal = strategy.generate_signal(df, state)
    print("Generated signal:", signal)

if __name__ == "__main__":
    main()