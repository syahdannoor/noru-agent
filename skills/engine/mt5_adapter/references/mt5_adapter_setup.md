# MT5 Adapter Setup Guide

## Credential Placeholder

Do **not** store real passwords in the repository. Use the following placeholder in `config.py`:

```python
MT5 = {
    "login": "[REDACTED]",
    "password": "[REDACTED]",
    "server": "[REDACTED]",
    "account_type": "demo",  # or "live"
}
```

Replace `[REDACTED]` with your actual credentials only when running locally and never commit the real values.

## Installation

```bash
pip install MetaTrader5
```

Ensure the environment where the script runs has network access to the MT5 server.

## Basic Usage

```python
from src.noru5.engine.execution.mt5_adapter import Mt5Adapter
adapter = Mt5Adapter()
info = adapter.get_account_info()
print(info)
```