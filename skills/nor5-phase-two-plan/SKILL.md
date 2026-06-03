---
name: nor5-phase-two-plan
description: "Plan for completing remaining NORU5 tasks: verify discovery, implement SmartMoneyStrategy, create backtesting harness, write docs."
version: 1.0
metadata:
  hermes:
    tags: [planning, noru5, backtesting]
---
# NORU5 Phase Two Plan

## Overview
This plan translates the remaining work from the checkpoint into bite‑sized tasks that can be executed in parallel using subagents. Each task includes exact file paths, command snippets, and verification steps.

## Tasks

### Task 1: Verify StrategyManager discovery
- **Goal:** Confirm that `StrategyManager().list_strategies()` returns the expected strategy names.
- **Files:** None (execution only)
- **Commands:**
  ```bash
  PYTHONPATH=/c/Users/syahd/.openclaw/workspace/noru5/src python - <<'PY'
  import sys; sys.path.insert(0, r'C:\Users\syahd\.openclaw\workspace\noru5\src')
  from src.noru5.engine.strategies.manager import StrategyManager
  print(StrategyManager().list_strategies())
  PY
  ```
- **Verification:** Output must include `smart_money` (and any other strategies present). If not, check `PYTHONPATH` and relative imports in `manager.py`.

### Task 2: Implement SmartMoneyStrategy detection logic
- **Goal:** Replace placeholder in `src/noru5/engine/strategies/smart_money.py` with real pattern detection using market data from `df` and config constants.
- **Files:** `src/noru5/engine/strategies/smart_money.py`
- **Steps:**
  1. Read `config.SMART_MONEY` for threshold values.
  2. Implement detection of the four patterns:
     - `order_block_body_gt_60_range`
     - `bos_atr_factor_0.5`
     - `liquidity_pool_initial_sweep`
     - `fib_50_retrace_mitigation`
  3. Return `Signal(direction='BUY'/'SELL', confidence=0.x, comment='Pattern detected: ...')` based on the first triggered pattern.
  4. Add unit test updates if needed.
- **Verification:** Run `pytest tests/test_smart_money.py -v` – all tests must pass and the newly added logic should not raise errors.

### Task 3: Create backtesting harness (`runner.py`)
- **Goal:** Add `src/noru5/backtest/runner.py` that loads all strategies, iterates over a sample candle DataFrame, collects signals, and prints a summary.
- **Files:** `src/noru5/backtest/runner.py`
- **Content skeleton:**
  ```python
  import sys
  import pandas as pd
  sys.path.insert(0, r'C:\Users\syahd\.openclaw\workspace\noru5\src')

  from src.noru5.engine.strategies.manager import StrategyManager
  from src.noru5.engine.config import load_strategy_configs

  # Load sample data (replace with real CSV later)
  df = pd.read_csv(r'C:\Users\syahd\.openclaw\workspace\noru5\data\sample_candles.csv')

  def main():
      sm = StrategyManager()
      strategies = sm.list_strategies()
      print(f"Loaded strategies: {strategies}")

      signals = []
      for strat_name in strategies:
          strat = sm.get_strategy(strat_name)
          signal = strat.generate_signal(df, state={})
          if signal:
              signals.append(signal)

      print(f"Collected {len(signals)} signals:")
      for s in signals:
          print(f"  {s.direction} ({s.source}) – confidence: {s.confidence}")

  if __name__ == '__main__':
      main()
  ```
- **Verification:** Execute `python src/noru5/backtest/runner.py`. Should print strategy names and any generated signals without errors.

### Task 4: Write documentation
- **Goal:** Update `README.md` and add an architecture diagram (`architecture-diagram` skill) showing the new module layout.
- **Files:** `README.md`, optionally generate diagram using `architecture-diagram` skill.
- **Steps:**
  1. Append a “Project Structure” section describing each newly added module.
  2. Include a brief usage example for the backtesting harness.
  3. If desired, generate an SVG diagram via `architecture-diagram` and embed it as HTML.
- **Verification:** `cat README.md | grep -i "NORU5"` should show the new sections; opened HTML diagram should render without errors.

## Execution Strategy
1. **Create a todo list** with the four tasks.
2. **Spawn a subagent per task** using the `subagent-driven-development` skill (two‑stage review: spec then quality).
3. **Mark each task completed** in the todo list once both reviews pass.
4. **Run final integration review** to ensure all components work together.

## Constraints & Preferences
- Keep responses concise; avoid extra explanation unless asked.
- Use free fallback if any API call fails (e.g., replace paid market data API with a complimentary CSV sample).
- Maintain `PYTHONPATH` as specified; do not hard‑code absolute paths outside the workspace.
- Ensure no “smart‑quotes” or hidden Unicode characters in code.
- Lint and format code (`python -m flake8`, `python -m black`) before marking a task complete.