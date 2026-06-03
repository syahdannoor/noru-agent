# IDR Account Lot Sizing on XAUUSD

## The Problem

`risk_manager.py` `calculate_position_size()` computes:
```python
risk_amount_ccy = equity * (risk_pct / 100.0)  # e.g. IDR 150,000
lot_risk = risk_amount_ccy / ((sl_distance / tick_size) * tick_value)
```

`tick_value` from `mt5.symbol_info("XAUUSD").trade_tick_value` is returned in **USD**, not the account currency. For IDR-denominated accounts, this inflates `lot_risk` because `risk_amount_ccy` is in IDR but the denominator is in USD.

### Actual Numbers (May 2026)

Account: HFMarketsGlobal-Demo (IDR-denominated)
Balance: IDR 300,000
Risk: 50% → risk_amount_ccy = IDR 150,000

```python
symbol_info("XAUUSD"):
  trade_tick_value = 1.0  # $1 per tick per lot (XAUUSD on this broker)
  trade_tick_size = 0.01

sl_distance = 25.71  # ATR × 0.5

lot_risk = 150000 / ((25.71 / 0.01) * 1.0)
        = 150000 / 2571
        = 58.34 lots  ← WAY too high for IDR 300k!
```

### The Safety Chain

The inflated `lot_risk` is caught downstream:
1. `lot = min(lot_risk, max_lot)` — max_lot from binary search
2. `lot = max(lot, lot_min)` — clamp to 0.01
3. `lot = min(lot, lot_max)` — hard cap to 0.01

So the order goes through at 0.01 despite the calculation. **But**: if `lot_max` is increased without adjusting the conversion, the inflated calculation can pass through.

### No Money Error (retcode=10019)

With `lot_max = 0.05` and IDR 300k balance:
- 0.05 lot XAUUSD = 5 oz
- Margin at 1:500 = 5 × $4,508 / 500 = $45.08 ≈ IDR 743,820
- Balance = IDR 300,000 — margin exceeds balance!
- Result: `retcode=10019 (No money)`

With `lot_max = 0.01`:
- 0.01 lot = 1 oz
- Margin at 1:500 = 1 × $4,508 / 500 = $9.02 ≈ IDR 148,830
- Balance = IDR 300,000 — affordable

### Long-term Fix

Convert `risk_amount_ccy` to USD before division:
```python
# Get XAUUSD price to convert risk from account currency to USD
tick = mt5.symbol_info_tick("XAUUSD")
current_price = (tick.ask + tick.bid) / 2 if tick else entry_price
risk_amount_usd = risk_amount_ccy * (1.0 / usd_idr_rate)  # needs live FX rate
```

Or better, use MT5's `order_calc_margin` to back-derive the correct lot:
```python
# Already done via binary search — the safety cap
```

### Quick Margin Table (XAUUSD, IDR account, 1:500 leverage)

| Balance | lot_max | Margin Required | Safe? |
|---------|---------|----------------|-------|
| IDR 300k | 0.01 | ~IDR 149k | ✅ |
| IDR 300k | 0.05 | ~IDR 744k | ❌ |
| IDR 1M | 0.02 | ~IDR 298k | ✅ |
| IDR 5M | 0.05 | ~IDR 744k | ✅ |
| IDR 10M | 0.10 | ~IDR 1.49M | ✅ |

### Always verify before deployment

```python
import MetaTrader5 as mt5
mt5.initialize()
margin = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, "XAUUSD", lot_max, 
                                mt5.symbol_info_tick("XAUUSD").ask)
print(f"Margin: {margin}, Free: {mt5.account_info().margin_free}")
```
