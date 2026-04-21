from __future__ import annotations

from typing import Any

from bt_api_valr.feeds.live_valr.request_base import ValrRequestData


class ValrRequestDataSpot(ValrRequestData):
    def get_server_time(self, extra_data: Any = None, **kwargs: Any):
        path, params, extra = self._get_server_time(extra_data, **kwargs)
        return self.request(path, params, extra_data=extra)

    async def async_get_server_time(self, extra_data: Any = None, **kwargs: Any):
        path, params, extra = self._get_server_time(extra_data, **kwargs)
        return await self.async_request(path, params, extra_data=extra)

    def get_tick(self, symbol: Any, extra_data: Any = None, **kwargs: Any):
        path, params, extra = self._get_tick(symbol, extra_data, **kwargs)
        return self.request(path, params, extra_data=extra)

    async def async_get_tick(self, symbol: Any, extra_data: Any = None, **kwargs: Any):
        path, params, extra = self._get_tick(symbol, extra_data, **kwargs)
        return await self.async_request(path, params, extra_data=extra)

    get_ticker = get_tick
    async_get_ticker = async_get_tick

    def get_depth(self, symbol: Any, count: int = 20, extra_data: Any = None, **kwargs: Any):
        path, params, extra = self._get_depth(symbol, count, extra_data, **kwargs)
        return self.request(path, params, extra_data=extra)

    async def async_get_depth(
        self, symbol: Any, count: int = 20, extra_data: Any = None, **kwargs: Any
    ):
        path, params, extra = self._get_depth(symbol, count, extra_data, **kwargs)
        return await self.async_request(path, params, extra_data=extra)

    def get_kline(
        self, symbol: Any, period: Any, count: int = 20, extra_data: Any = None, **kwargs: Any
    ):
        path, params, extra = self._get_kline(symbol, period, count, extra_data, **kwargs)
        return self.request(path, params, extra_data=extra)

    async def async_get_kline(
        self, symbol: Any, period: Any, count: int = 20, extra_data: Any = None, **kwargs: Any
    ):
        path, params, extra = self._get_kline(symbol, period, count, extra_data, **kwargs)
        return await self.async_request(path, params, extra_data=extra)

    def get_exchange_info(self, extra_data: Any = None, **kwargs: Any):
        path, params, extra = self._get_exchange_info(extra_data, **kwargs)
        return self.request(path, params, extra_data=extra)

    async def async_get_exchange_info(self, extra_data: Any = None, **kwargs: Any):
        path, params, extra = self._get_exchange_info(extra_data, **kwargs)
        return await self.async_request(path, params, extra_data=extra)

    def get_balance(self, symbol: Any = None, extra_data: Any = None, **kwargs: Any):
        path, params, extra = self._get_balance(extra_data, **kwargs)
        return self.request(path, params, extra_data=extra)

    async def async_get_balance(self, symbol: Any = None, extra_data: Any = None, **kwargs: Any):
        path, params, extra = self._get_balance(extra_data, **kwargs)
        return await self.async_request(path, params, extra_data=extra)

    def get_account(self, symbol: Any = None, extra_data: Any = None, **kwargs: Any):
        path, params, extra = self._get_account(extra_data, **kwargs)
        return self.request(path, params, extra_data=extra)

    async def async_get_account(self, symbol: Any = None, extra_data: Any = None, **kwargs: Any):
        path, params, extra = self._get_account(extra_data, **kwargs)
        return await self.async_request(path, params, extra_data=extra)
