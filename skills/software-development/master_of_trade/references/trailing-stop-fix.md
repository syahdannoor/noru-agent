# Trailing Stop Fix Notes

## Problem
Trailing stop was not updating despite profit exceeding activation threshold (0.5%). Root cause: Two issues:

1. **TP Reset Bug**: When modifying only SL via `TRADE_ACTION_SLTP`, MT5 resets TP to 0 if TP not included in request. This caused invalid stops (SL > TP for BUY) and error 10025.
2. **Missing Debug**: No visibility into why trailing decision was not triggering.

## Fix Applied
1. Updated `risk_manager.py` `trail_stop()` to include detailed debug logs (`[TRAIL DEBUG] ...`) showing:
   - entry price
   - current price
   - profit_pct
   - trail_pct threshold
   - new_sl vs current sl
   - min_trail_dist check
2. Updated `auto_trade.py` `_manage_positions()` to pass both SL and TP to `modify_position()`:
   ```python
   self.executor.modify_position(pos[\"ticket\"], sl=new_sl, tp=pos.get(\"tp\", 0))
   ```
3. Ensured `modify_position()` in `executor.py` already handles default values correctly (uses current SL/TP if not provided).

## Verification
After fix, when profit >= 0.5% and new SL improves by >0.15, log shows:
```
[TRAIL DEBUG] BUY: entry=4554.72, price=4577.63, profit_pct=0.50%, new_sl=4561.59, sl=4549.36
📍 Trailing 1128452819: SL moved to 4561.59
```

## Configuration
- `trailing_activation_pct` in `config.py` (default 0.5)
- `min_trail_dist` hardcoded to 0.15 (can be made configurable)

## Related Pitfalls
- Always send both SL and TP in `TRADE_ACTION_SLTP` requests.
- Gate modify calls with meaningful change check to avoid retcode=10025 (no-op or too small).
- Use current bid price (not candle high) for trailing evaluation.