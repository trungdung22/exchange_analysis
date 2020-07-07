from abc import ABC

from libs.markets.binance import Binance


class MarketType:
    BITTREX = "BITTREX"
    BINANCE = "BINANCE"


class BaseEngine(object):
    """Base market interface engine"""
    def __init__(self, api_key="test", api_secret="test", logging=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.logging = logging

    def sell(self, amount, rate):
        raise NotImplementedError

    def buy(self, amount, rate):
        raise NotImplementedError

    def cancel_order(self, uuid):
        raise NotImplementedError

    def order_depth(self):
        raise NotImplementedError


class BinanceEngine(BaseEngine, ABC):
    """Binance market engine"""

    def __init__(self, api_key="test", api_secret="test", logging=None, **kwargs):
        super(BinanceEngine, self).__init__(api_key=api_key, api_secret=api_secret, logging=logging,
                                            **kwargs)
        self.market_type = MarketType.BINANCE
        self.conn = Binance(self.api_key, self.api_secret)

    def order_depth(self, pair=None, limit=10):
        """get market order depth"""
        return self.conn.get_depth(pair, limit)

    def trades_history(self, start_time, end_time, pair=None):
        """get market trades hisotry"""
        return self.conn.get_trades_history(pair, start_time, end_time)['trade']

    def close_orders(self, start_time, end_time, address=None):
        """get market closed order"""
        return self.conn.get_closed_order(address, start_time, end_time)['order']