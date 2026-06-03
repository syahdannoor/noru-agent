# Mobius Fallback Workflow — XAUUSD Intraday Analysis

When OpenMobius-skill's API doesn't support intraday intervals for forex spot XAUUSD (only 1d supported), use this proven Windows workaround to still produce proper SMC analysis with chart.

## Why This Exists

Mobius Quant API (api.mobiusquant.ai) classifies XAUUSD as `forex:spot:XAUUSD` and only serves daily candles. Intraday queries return:
```
Interval '5m' not supported on forex:spot; valid: ['1d']
```

## Workflow (Windows + Git-Bash)

### Step 1: Fetch M5 Data from Yahoo Finance

GC=F (COMEX Gold Futures) tracks XAUUSD spot closely (~$36 futures premium). The M5 structure is effectively identical.

```bash
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=5m&range=1d" \
  -H "User-Agent: Mozilla/5.0" \
  -o "C:/Users/syahd/AppData/Local/Temp/yahoo_gc_raw.json"
```

### Step 2: Convert to Mobius-Compatible Format

Yahoo returns JSON with nested `chart.result[0]` structure. Convert to Mobius's list-of-lists format:

```bash
cd "C:/Users/syahd/AppData/Local/hermes/skills/market-data/OpenMobius-skill"
.venv/Scripts/python -c "
import json
with open('C:/Users/syahd/AppData/Local/Temp/yahoo_gc_raw.json') as f:
    data = json.load(f)
result = data['chart']['result'][0]
timestamps = result['timestamp']
quotes = result['indicators']['quote'][0]
rows = []
for i in range(len(timestamps)):
    rows.append([timestamps[i], quotes['open'][i], quotes['high'][i],
                 quotes['low'][i], quotes['close'][i], quotes['volume'][i]])
out = {
    'exchange': 'comex', 'market': 'futures', 'symbol': 'GC=F',
    'asset_class': 'commodity', 'interval': '5m', 'candles': rows
}
with open('C:/Users/syahd/AppData/Local/Temp/xauusd_m5_rows.json', 'w') as f:
    json.dump(out, f, indent=2)
print(f'Converted {len(rows)} candles')
"
```

### Step 3: Run Local Feature Extraction

```bash
cd "C:/Users/syahd/AppData/Local/hermes/skills/market-data/OpenMobius-skill"
.venv/Scripts/python scripts/kb_klines.py analyze \
    --input "C:/Users/syahd/AppData/Local/Temp/xauusd_m5_rows.json" \
    --output "C:/Users/syahd/AppData/Local/Temp/xauusd_m5_features.txt"
```

Read the output — it contains:
- Current close, range, ATR(14)
- Swing sequence with BOS/CHoCH events
- FVG candidates (mitigation %, bar age, size)
- Order Block candidates
- Liquidity Sweep candidates (direction, wick size)
- Volume anomalies

### Step 4: Generate Chart

Build panels JSON with structural overlay items from the features, then render:

```bash
# Build panels
.venv/Scripts/python -c "
import json
with open('C:/Users/syahd/AppData/Local/Temp/xauusd_m5_rows.json') as f:
    data = json.load(f)

candles = []
for c in data['candles']:
    candles.append({'time': c[0], 'open': c[1], 'high': c[2], 'low': c[3], 'close': c[4], 'volume': c[5]})

panels = {'panels': [{'candles': candles, 'items': []}]}

# Add OB, FVG rectangles from feature analysis (manual from features.txt)
# See the features output for exact levels

with open('C:/Users/syahd/AppData/Local/Temp/xauusd_m5_annotated.json', 'w') as f:
    json.dump(panels, f, indent=2)
"

# Render
.venv/Scripts/python scripts/kb_klines.py render \
    --input "C:/Users/syahd/AppData/Local/Temp/xauusd_m5_annotated.json" \
    --output "C:/Users/syahd/AppData/Local/Temp/xauusd_m5_chart.png" \
    --theme dark --width 1400 --height 900
```

## Known Issues

- **Path mismatch**: MSYS bash `/tmp/` = `C:\Users\syahd\AppData\Local\Temp\` in Windows. The Mobius venv Python runs as native Windows Python, so it expects Windows paths. Always use full paths like `C:/Users/.../Temp/` when passing files between bash and the Python scripts.
- **Analyze format**: The `analyze` command expects `{'candles': [[time, o, h, l, c, v], ...]}` (list-of-lists), NOT dict format `[{'time':..., 'open':...}, ...]`. Convert first.
- **GC=F premium**: COMEX futures trade ~$36 above XAUUSD spot. The structural pattern (BOS, FVG, sweeps) is identical — report the bias direction using pattern analysis, but note absolute prices are futures, not spot.
- **No HTF context**: The fallback workflow doesn't fetch higher timeframe. For HTF bias, fetch daily separately from gold-api.com or Mobius (which supports 1d for forex).
