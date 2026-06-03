# MT5 Multi-Timeframe Analysis Pattern

## Purpose
Fetch live OHLCV data from MT5 across multiple timeframes (M5, M15, H1, H4, D1), compute technical indicators (SMA20/50/200, RSI 14, ATR 14), generate a 3-panel matplotlib chart, and produce a structured bias prediction.

## Pattern

### 1. Connection
Use standalone Python (NOT Microsoft Store):
```python
# /c/Users/<user>/AppData/Local/Programs/Python/Python312/python.exe
import MetaTrader5 as mt5

mt5.initialize(path="C:/Program Files/MetaTrader 5/terminal64.exe", timeout=60000)
mt5.symbol_select("XAUUSD", True)
```

### 2. Data Fetch Per Timeframe
```python
TIMEFRAMES = {"M5": mt5.TIMEFRAME_M5, "M15": mt5.TIMEFRAME_M15,
              "H1": mt5.TIMEFRAME_H1, "H4": mt5.TIMEFRAME_H4,
              "D1": mt5.TIMEFRAME_D1}
all_data = {}
for tf_name, tf_enum in TIMEFRAMES.items():
    bars = mt5.copy_rates_from_pos("XAUUSD", tf_enum, 0, 250)
    df = pd.DataFrame(bars)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    all_data[tf_name] = df
```

### 3. Indicators
```python
# SMA
df['sma20'] = df['close'].rolling(20).mean()
df['sma50'] = df['close'].rolling(50).mean()
df['sma200'] = df['close'].rolling(200).mean()

# RSI 14
delta = df['close'].diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
rs = gain / loss
df['rsi'] = 100 - (100 / (1 + rs))

# ATR 14
high_low = df['high'] - df['low']
high_close = np.abs(df['high'] - df['close'].shift())
low_close = np.abs(df['low'] - df['close'].shift())
tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
df['atr'] = tr.rolling(14).mean()
```

### 4. Trend Classification
| Condition | Classification |
|---|---|
| SMA20 > SMA50 > SMA200 | BULLISH |
| SMA20 < SMA50 < SMA200 | BEARISH |
| Mixed alignment | SIDEWAYS / MIXED |

### 5. RSI Bands
| RSI | Signal |
|---|---|
| ≥ 70 | OVERBOUGHT |
| 55–69 | BULLISH |
| 45–54 | NEUTRAL |
| 31–44 | BEARISH |
| ≤ 30 | OVERSOLD |

### 6. Multi-Timeframe Consensus
Weight higher TFs more (D1=5, H4=4, H1=3, M15=2, M5=1). Count bull/bear signals across TFs. If bull count ≥ bear → BULLISH bias; if bear > bull → BEARISH; tie → SIDEWAYS. Conviction HIGH if ≥ 4 TFs agree, MODERATE if 2-3, LOW if 1 or mixed.

### 7. Matplotlib Chart (3-panel)
```
Panel 1: Candlestick chart + SMA20/50/200 + S/R lines
Panel 2: RSI line with 30/50/70 thresholds
Panel 3: Volume bars (colored by up/down candle)
```

### 8. Key Levels
- Resistance: nearest swing high above current price (from each TF)
- Support: nearest swing low below current price (from each TF)
- Use 20-bar lookback window for swing detection

## Full script example
See `xauud_analysis.py` in the hermes-agent working directory for a complete implementation with matplotlib dark theme and dataframe-backed computation.
