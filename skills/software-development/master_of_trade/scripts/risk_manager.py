# Risk Management Module for Master of Trade
# Provides position sizing, stop‑loss/take‑profit setting, drawdown control and risk budgeting.

import math
from ..config import RISK_CFG

# ----------------------------------------------------------------------
# Configuration (loaded from skill's config.py placeholders)
# ----------------------------------------------------------------------
# RISK_CFG = {
#     "risk_per_trade_pct": 1.0,          # % of equity to risk on a single trade
#     "max_drawdown_pct": 5.0,            # Max allowable drawdown before halting
#     "stop_loss_atr_multiplier": 1.5,    # SL distance = ATR * multiplier
#     "take_profit_risk_reward": 2.0,     # TP distance = RR * SL distance
#     "volatility_adjusted_scaling": True # Scale lot size by recent volatility
# }

# ----------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------
def compute_lot_size(equity: float, symbol: str) -> float:
    """
    Calculate lot size based on risk percentage and stop‑loss distance.
    Uses ATR to estimate stop‑loss distance.
    """
    risk_pct = RISK_CFG["risk_per_trade_pct"] / 100.0
    # Get recent ATR (14) for the symbol – placeholder function
    atr = get_atr(symbol, period=14)  # assumes function exists in market data layer
    sl_distance = atr * RISK_CFG["stop_loss_atr_multiplier"]
    
    # Approximate pip/point value for XAUUSD: $1 per pip per standard lot (adjust as needed)
    pip_value_per_lot = 0.01  # example value; replace with actual contract specs
    
    # Risk amount in monetary terms
    risk_amount = equity * risk_pct
    # Lot size = risk amount / (stop distance * pip value)
    lot = risk_amount / (sl_distance * pip_value_per_lot)
    return round(max(lot, 0.01), 2)  # minimum lot = 0.01


def set_stop_take_protect(entry_price: float, symbol: str) -> tuple:
    """
    Determine SL and TP levels based on ATR multiplier and risk‑reward ratio.
    Returns (sl_price, tp_price).
    """
    atr = get_atr(symbol, period=14)
    sl_points = atr * RISK_CFG["stop_loss_atr_multiplier"]
    rr = RISK_CFG["take_profit_risk_reward"]
    tp_points = sl_points * rr
    
    sl_price = entry_price - sl_points if RISK_CFG.get("sl_direction") == "below" else entry_price + sl_points
    tp_price = entry_price + tp_points if RISK_CFG.get("tp_direction") == "above" else entry_price - tp_points
    
    return sl_price, tp_price


def enforce_drawdown_limit(current_equity: float, peak_equity: float, max_dd_pct: float) -> bool:
    """
    Check if the drawdown exceeds the allowed threshold.
    Returns True if trading should continue, False if halt.
    """
    drawdown_pct = (peak_equity - current_equity) / peak_equity * 100
    return drawdown_pct < max_dd_pct


def volatility_adjusted_lot(equity: float, base_lot: float, symbol: str) -> float:
    """
    Optional scaling of lot size based on recent volatility regime.
    Lower volatility -> reduce lot; higher volatility -> increase cautiously.
    """
    if not RISK_CFG["volatility_adjusted_scaling"]:
        return base_lot
    
    # Get recent ATR ratio (current ATR / average ATR over last 50 periods)
    current_atr = get_atr(symbol, period=14)
    avg_atr = get_atr(symbol, period=50)
    ratio = current_atr / avg_atr if avg_atr else 1.0
    
    # Simple scaling: lot * ratio, capped between 0.5 and 1.5
    scaled = base_lot * max(0.5, min(1.5, ratio))
    return round(scaled, 2)