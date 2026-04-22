from __future__ import annotations

from typing import TYPE_CHECKING

from bt_api_base.balance_utils import simple_balance_handler as _valr_balance_handler

from bt_api_valr.exchange_data import ValrExchangeDataSpot
from bt_api_valr.feeds.live_valr.spot import ValrRequestDataSpot

if TYPE_CHECKING:
    from bt_api_base.registry import ExchangeRegistry


def register_valr(registry: type[ExchangeRegistry]) -> None:
    registry.register_feed("VALR___SPOT", ValrRequestDataSpot)
    registry.register_exchange_data("VALR___SPOT", ValrExchangeDataSpot)
    registry.register_balance_handler("VALR___SPOT", _valr_balance_handler)
