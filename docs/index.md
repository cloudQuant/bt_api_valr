# VALR Documentation

## English

Welcome to the VALR documentation for bt_api.

### Quick Start

```bash
pip install bt_api_valr
```

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "VALR___SPOT": {
        "api_key": "your_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("VALR___SPOT", "BTCUSDT")
balance = api.get_balance("VALR___SPOT")
```

## 中文

欢迎使用 bt_api 的 VALR 文档。

### 快速开始

```bash
pip install bt_api_valr
```

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "VALR___SPOT": {
        "api_key": "your_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("VALR___SPOT", "BTCUSDT")
balance = api.get_balance("VALR___SPOT")
```

## API Reference

See source code in `src/bt_api_valr/` for detailed API documentation.
