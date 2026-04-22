from __future__ import annotations

import hashlib
import hmac
import time
from typing import Any
from urllib.parse import urlencode

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed

from bt_api_valr.exchange_data import ValrExchangeDataSpot


class ValrRequestData(Feed):
    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.data_queue = data_queue
        self.exchange_name = kwargs.get("exchange_name", "VALR___SPOT")
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self.api_key = kwargs.get("public_key") or kwargs.get("api_key")
        self.api_secret = kwargs.get("secret_key") or kwargs.get("api_secret")
        self._params = ValrExchangeDataSpot()

    def _generate_signature(self, timestamp: str, verb: str, path: str, body: str = "") -> str:
        if not self.api_secret:
            return ""
        sign_str = f"{timestamp}{verb.upper()}{path}{body}"
        return hmac.new(
            self.api_secret.encode("utf-8"), sign_str.encode("utf-8"), hashlib.sha512
        ).hexdigest()

    def _get_headers(self, method: str = "GET", request_path: str = "") -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            ts = str(int(time.time() * 1000))
            headers["X-VALR-API-KEY"] = self.api_key
            headers["X-VALR-TIMESTAMP"] = ts
            headers["X-VALR-SIGNATURE"] = self._generate_signature(ts, method, request_path)
        return headers

    def request(
        self,
        path: str,
        params: Any = None,
        body: Any = None,
        extra_data: Any = None,
        timeout: int = 10,
    ) -> RequestData:
        method = path.split()[0] if " " in path else "GET"
        endpoint = path.split()[1] if " " in path else path
        url = self._params.rest_url + endpoint
        if params:
            url = url + "?" + urlencode(params)
        response = self.http_request(
            method=method,
            url=url,
            headers=self._get_headers(method=method, request_path=endpoint),
            body=body,
            timeout=timeout,
        )
        return RequestData(response, extra_data)

    async def async_request(
        self,
        path: str,
        params: Any = None,
        body: Any = None,
        extra_data: Any = None,
        timeout: int = 10,
    ) -> RequestData:
        method = path.split()[0] if " " in path else "GET"
        endpoint = path.split()[1] if " " in path else path
        url = self._params.rest_url + endpoint
        if params:
            url = url + "?" + urlencode(params)
        response = await self.async_http_request(
            method=method,
            url=url,
            headers=self._get_headers(method=method, request_path=endpoint),
            body=body,
            timeout=timeout,
        )
        return RequestData(response, extra_data)

    def push_data_to_queue(self, data: Any) -> None:
        if self.data_queue is not None:
            self.data_queue.put(data)

    def async_callback(self, future: Any) -> None:
        try:
            result = future.result()
            self.push_data_to_queue(result)
        except Exception as exc:
            self.logger.warning("async_callback::%s", exc)

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        super().disconnect()

    def is_connected(self) -> bool:
        return True

    @staticmethod
    def _is_error(data: Any) -> bool:
        if data is None:
            return True
        return bool(isinstance(data, dict) and ("error" in data or "message" in data))

    def _get_server_time(self, extra_data: Any = None, **kwargs: Any):
        path = self._params.get_rest_path("get_server_time")
        extra_data = extra_data or {}
        extra_data.update(
            {
                "request_type": "get_server_time",
                "normalize_function": self._get_server_time_normalize_function,
            }
        )
        return path, None, extra_data

    def _get_tick(self, symbol: str, extra_data: Any = None, **kwargs: Any):
        path = self._params.get_rest_path("get_tick", symbol=self._params.get_symbol(symbol))
        extra_data = extra_data or {}
        extra_data.update(
            {
                "request_type": "get_tick",
                "symbol_name": symbol,
                "normalize_function": self._get_tick_normalize_function,
            }
        )
        return path, None, extra_data

    def _get_depth(self, symbol: str, count: int = 20, extra_data: Any = None, **kwargs: Any):
        path = self._params.get_rest_path("get_depth", symbol=self._params.get_symbol(symbol))
        extra_data = extra_data or {}
        extra_data.update(
            {
                "request_type": "get_depth",
                "symbol_name": symbol,
                "normalize_function": self._get_depth_normalize_function,
            }
        )
        return path, None, extra_data

    def _get_kline(
        self, symbol: str, period: str, count: int = 20, extra_data: Any = None, **kwargs: Any
    ):
        path = self._params.get_rest_path("get_kline", symbol=self._params.get_symbol(symbol))
        extra_data = extra_data or {}
        extra_data.update(
            {
                "request_type": "get_kline",
                "symbol_name": symbol,
                "normalize_function": self._get_kline_normalize_function,
            }
        )
        return path, None, extra_data

    def _get_exchange_info(self, extra_data: Any = None, **kwargs: Any):
        path = self._params.get_rest_path("get_exchange_info")
        extra_data = extra_data or {}
        extra_data.update(
            {
                "request_type": "get_exchange_info",
                "normalize_function": self._get_exchange_info_normalize_function,
            }
        )
        return path, None, extra_data

    def _get_balance(self, extra_data: Any = None, **kwargs: Any):
        path = self._params.get_rest_path("get_balance")
        extra_data = extra_data or {}
        extra_data.update(
            {
                "request_type": "get_balance",
                "normalize_function": self._get_balance_normalize_function,
            }
        )
        return path, None, extra_data

    def _get_account(self, extra_data: Any = None, **kwargs: Any):
        path = self._params.get_rest_path("get_account")
        extra_data = extra_data or {}
        extra_data.update(
            {
                "request_type": "get_account",
                "normalize_function": self._get_account_normalize_function,
            }
        )
        return path, None, extra_data

    @staticmethod
    def _get_server_time_normalize_function(data: Any, extra_data: Any):
        if data is None:
            return [], False
        return [data] if isinstance(data, dict) else [{"serverTime": data}], True

    @staticmethod
    def _get_tick_normalize_function(data: Any, extra_data: Any):
        if ValrRequestData._is_error(data):
            return [], False
        if isinstance(data, dict):
            return [data], True
        if isinstance(data, list):
            return data, bool(data)
        return [], False

    @staticmethod
    def _get_depth_normalize_function(data: Any, extra_data: Any):
        if ValrRequestData._is_error(data):
            return [], False
        if isinstance(data, dict):
            return [data], True
        return [], False

    @staticmethod
    def _get_kline_normalize_function(data: Any, extra_data: Any):
        if ValrRequestData._is_error(data):
            return [], False
        if isinstance(data, list):
            return data, bool(data)
        if isinstance(data, dict):
            return [data], True
        return [], False

    @staticmethod
    def _get_exchange_info_normalize_function(data: Any, extra_data: Any):
        if ValrRequestData._is_error(data):
            return [], False
        if isinstance(data, dict):
            return [data], True
        if isinstance(data, list):
            return data, bool(data)
        return [], False

    @staticmethod
    def _get_balance_normalize_function(data: Any, extra_data: Any):
        if ValrRequestData._is_error(data):
            return [], False
        if isinstance(data, dict):
            return [data], True
        if isinstance(data, list):
            return data, bool(data)
        return [], False

    @staticmethod
    def _get_account_normalize_function(data: Any, extra_data: Any):
        if ValrRequestData._is_error(data):
            return [], False
        if isinstance(data, dict):
            return [data], True
        if isinstance(data, list):
            return data, bool(data)
        return [], False
