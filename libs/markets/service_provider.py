from libs.markets.engine import MarketType, BinanceEngine


class MarketServiceProvider(object):
    """Market service provider mapping"""
    @staticmethod
    def get_market_engine(type=MarketType.BINANCE, **kwargs):
        if type == MarketType.BINANCE:
            return BinanceEngine(**kwargs)
        else:
            raise ValueError(format)
