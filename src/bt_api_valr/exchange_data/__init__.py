from __future__ import annotations

import re

from bt_api_base.containers.exchanges.exchange_data import ExchangeData


_FALLBACK_REST_PATHS = {
    "get_server_time": "GET /v1/public/time",
    "get_tick": "GET /v1/public/{symbol}/ticker",
    "get_ticker": "GET /v1/public/{symbol}/ticker",
    "get_all_tickers": "GET /v1/public/marketsummary",
    "get_depth": "GET /v1/public/{symbol}/orderbook",
    "get_kline": "GET /v1/public/{symbol}/marketsummary",
    "get_trades": "GET /v1/public/{symbol}/trades",
    "get_exchange_info": "GET /v1/public/pairs",
    "get_currencies": "GET /v1/public/currencies",
    "get_account": "GET /v1/account/balances",
    "get_balance": "GET /v1/account/balances",
    "make_order": "POST /v1/orders/market",
    "make_limit_order": "POST /v1/orders/limit",
    "cancel_order": "DELETE /v1/order/{order_id}",
    "query_order": "GET /v1/order/{order_id}",
    "get_open_orders": "GET /v1/orders/open",
}


class ValrExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "VALR___SPOT"
        self.rest_url = "https://api.valr.com"
        self.wss_url = "wss://api.valr.com/ws"
        self.rest_paths = dict(_FALLBACK_REST_PATHS)
        self.wss_paths = {}
        self.kline_periods = {
            "1m": "1m",
            "3m": "3m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1h": "1h",
            "2h": "2h",
            "4h": "4h",
            "6h": "6h",
            "12h": "12h",
            "1d": "1d",
            "1w": "1w",
            "1M": "1M",
        }
        self.legal_currency = ["USDC", "ZAR", "BTC", "ETH"]

    @staticmethod
    def get_symbol(symbol: str) -> str:
        s = symbol.strip()
        s = re.sub(r"[-/_]", "", s)
        return s.upper()

    @staticmethod
    def get_reverse_symbol(symbol: str) -> str:
        s = symbol.strip()
        s = re.sub(r"[-/_]", "", s)
        return s.upper()

    def get_period(self, period: str) -> str:
        return self.kline_periods.get(period, period)

    def get_reverse_period(self, period: str) -> str:
        for k, v in self.kline_periods.items():
            if v == period:
                return k
        return period

    def get_rest_path(self, key: str, **kwargs) -> str:
        path = self.rest_paths.get(key, "")
        if not path:
            raise ValueError(f"[{self.exchange_name}] REST path not found: {key}")
        if kwargs:
            path = path.format(**kwargs)
        return path


class ValrExchangeDataSpot(ValrExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "SPOT"
