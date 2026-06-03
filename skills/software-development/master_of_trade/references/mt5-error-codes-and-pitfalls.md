# MT5 Error Codes & Real-World Pitfalls

## Retcode 10019 — TRADE_RETCODE_NO_MONEY

**Scenario**: Order fails with `FOK: retcode=10019 (No money)` even though the account has sufficient balance.

**Root causes on HFMarketsGlobal-Demo (XAUUSD)**:

### 1. Lot size exceeds available margin
Even with `lot_max` capped, if the margin requirement for the minimum lot exceeds the account balance, this error fires.

**Debug procedure**:
```python
# Check margin requirement for your planned lot:
margin = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, "XAUUSD", 0.01, current_price)
print(f"Margin for 0.01 lot XAUUSD: {margin}")  # In account currency

# Check free margin:
account = mt5.account_info()
print(f"Free margin: {account.margin_free}")  # In account currency
```

**Common values** (IDR account, IDR 300k balance, XAUUSD @ $4,508):
- 0.01 lot: ~IDR 148k margin (OK if leverage 1:500)
- 0.05 lot: ~IDR 743k margin (FAILS — exceeds IDR 300k balance)

**Fix**: Reduce `lot_max` in `config.py` until margin < balance. See `references/lot-sizing-guidelines.md`.

### 2. Binary search margin bug (FIXED)

**Old code**: `risk_manager.calculate_position_size()` binary search started with `hi = 1.0` and did not guard against `order_calc_margin` returning `None` or `0`.

**Bug chain**:
1. `order_calc_margin()` returns `None` (MT5 temporarily disconnected)
2. Code sets `margin = 0`
3. `0 <= margin_free * 0.95` → True → max_lot set to current `mid`
4. Binary search converges to ~0.5-1.0 lot
5. `min(lot_risk, max_lot)` picks the inflated value
6. Order fails with retcode 10019

**Fix** (deployed):
- Binary search `hi` bounds to `RISK["lot_max"]` (not hardcoded 1.0)
- Added `margin_free > 0` guard: skip binary search entirely if free margin is 0
- When `margin is None or margin <= 0`, set `lo = mid` BUT `hi` is already capped by `lot_max`

### 3. Account currency mismatch (IDR accounts)

`risk_manager.py` line 49:
```python
lot_risk = risk_amount_ccy / ((sl_distance / tick_size) * tick_value)
```

- `risk_amount_ccy` = account currency amount (e.g. IDR 150,000)
- `tick_value` = from `mt5.symbol_info().trade_tick_value` (always in USD)
- For IDR accounts, this divides IDR by USD → lot_risk inflated by exchange rate
- The `lot_max` cap is the safety net; without it, lot_risk would be 58+ lots for IDR 150k risk

**Long-term fix**: Convert `risk_amount_ccy` to USD before the formula:
```python
# Get XAUUSD-to-account-currency rate
xau_usd = mt5.symbol_info_tick("XAUUSD").ask
account_currency = ...  # detect from mt5.account_info().currency
if account_currency.upper() == "IDR":
    # Convert IDR to USD
    usd_idr = mt5.symbol_info_tick("USDIDR").bid if mt5.symbol_select("USDIDR", True) else 16500
    risk_amount_ccy = risk_amount_ccy / usd_idr
```

---

## Retcode 10025 — TRADE_RETCODE_INVALID_STOPS

**Scenario**: `modify_position()` fails because the new SL/TP is too close to current price or on the wrong side.

**Real-world causes**:

1. **Trailing stop modifies too frequently**: Trailing stop recalculates every tick (1s). SL price changes by $0.01-0.05 per tick. If the trailing function returns a new SL that's only $0.01 different from the current SL, MT5 rejects it.

   **Fix**: Only call `modify_position()` when `abs(new_sl - current_sl) > 0.15`. Return 0 from `trail_stop()` when the improvement is below the threshold.

2. **Trailing from wrong direction**: For BUY, SL must be below entry price. For SELL, SL must be above. If `trail_stop()` reverses the sign (e.g. BUY SL above entry), MT5 returns 10025.

   **Check**: `new_sl > 0 and new_sl != current_sl` — this gate alone isn't enough. The SL must be on the **right side** of current price.

3. **TP reset to 0 by TRADE_ACTION_SLTP** (see TP reset bug below).

---

## Critical: TP Reset Bug with TRADE_ACTION_SLTP

**MT5 behavior**: When calling `mt5.order_send()` with `action=mt5.TRADE_ACTION_SLTP`, MT5 **clears any field not explicitly included in the request**.

**Scenario**: You only want to update SL:
```python
request = {
    "action": mt5.TRADE_ACTION_SLTP,
    "symbol": "XAUUSD",
    "position": ticket,
    "sl": new_sl,
    # TP NOT included
}
```
→ MT5 resets the position's TP to 0 → broker rejects → retcode 10025 or order modified without TP.

**Fix**: Always retrieve current position SL and TP, and pass both:
```python
request["sl"] = new_sl if new_sl > 0 else (pos.sl or 0)
# ⚠️ Must include TP — even if not changing it!
request["tp"] = pos.tp or 0 if tp <= 0 else tp
```

---

## Position Type Format (int vs str)

**MT5 returns** `pos.type` as an **integer**: 0 = BUY, 1 = SELL.

**Common bug**: Downstream code checks `if pos["type"] == "BUY"` but `pos["type"]` is `0`. Fix the check or convert in `get_positions()`:
```python
positions = mt5.positions_get()
for pos in positions:
    yield {
        "ticket": pos.ticket,
        "type": "BUY" if pos.type == 0 else "SELL",
        ...
    }
```

Consistency matters — trailing stop, entry filter, and modify_position all depend on this field.
