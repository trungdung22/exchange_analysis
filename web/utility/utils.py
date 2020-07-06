import datetime
import pytz
import time
from libs.markets.service_provider import MarketServiceProvider
from libs.markets.engine import MarketType
from collections import OrderedDict

DATETIME_TIMEZONE = u"%Y-%m-%dT%H:%M:%S.%f%z"
DATETIME_TIMEZONE_2 = u"%Y-%m-%dT%H:%M:%S.%fZ"
DATETIME = '%Y-%m-%d'
DATETIME_2 = '%Y-%m-%dT%H:%M:%S'


def convert_time(time_str, timezone=1):
    """covert to time"""
    try:
        if timezone == 1:
            return datetime.datetime.strptime(time_str, DATETIME_TIMEZONE)
        elif timezone == 2:
            return datetime.datetime.strptime(time_str, DATETIME_TIMEZONE_2)
    except:
        pass

    if 'T' in time_str:
        format_type = DATETIME_2
    else:
        format_type = DATETIME
    time_value = datetime.datetime.strptime(time_str, format_type)
    return time_value.astimezone(pytz.utc)


def current_time_range():
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=2)
    return start, end


def convert_time_local(utc_datetime):
    """covert to time local"""
    now_timestamp = time.time()
    offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


def time_to_millisecond(time_obj):
    """covert to time millisecon"""
    return round(time_obj.timestamp() * 1000)


class MarketDataService(object):
    """Market data service"""
    BUY_ORDER = 'buy_orders'
    SELL_ORDER = 'sell_orders'

    def __init__(self, start_time, end_time, pair, market_type=MarketType.BINANCE, delta=300):
        self.start_time = convert_time(start_time) if isinstance(start_time, str) else start_time
        self.end_time = convert_time(end_time) if isinstance(end_time, str) else end_time
        self.pair = pair
        self.engine = MarketServiceProvider.get_market_engine(market_type)
        self.trader_ids = []
        self.starts = []
        self.ends = []
        self.time_delta = datetime.timedelta(seconds=delta)
        self.dict_orders = OrderedDict()

    def _fetch_traders_id(self):
        """GET all traders data in time range"""
        start_time = self.end_time - datetime.timedelta(days=30)
        results = self.engine.trades_history(time_to_millisecond(start_time),
                                             time_to_millisecond(self.end_time),
                                             self.pair)
        for result in results:
            if result['buyerId'] not in self.trader_ids:
                self.trader_ids.append(result['buyerId'])
            if result['sellerId'] not in self.trader_ids:
                self.trader_ids.append(result['sellerId'])

    def _fetch_orders(self, address):
        """GET all orders by address"""
        return self.engine.close_orders(time_to_millisecond(self.start_time),
                                        time_to_millisecond(self.end_time), address)

    def _set_order(self, start_key, order):
        """Mapping order within time interval"""
        sub_key = MarketDataService.BUY_ORDER
        sub_key_2 = MarketDataService.SELL_ORDER
        if order['side'] != 1:
            sub_key = MarketDataService.SELL_ORDER
            sub_key_2 = MarketDataService.BUY_ORDER
        if start_key not in self.dict_orders:
            self.dict_orders[start_key] = {sub_key: [order], sub_key_2: []}
        else:
            self.dict_orders[start_key][sub_key].append(order)

    def _construct_time_interval(self):
        """Init time interval"""
        dt_start = self.start_time
        dt_end = self.end_time
        while dt_start < dt_end:
            self.starts.append(dt_start)
            dt_start = dt_start + self.time_delta
            self.ends.append(dt_start)

    def _process_orders(self, orders):
        """GET all orders"""
        while len(orders) > 0:
            item = orders.pop(0)
            item_time = convert_time(item['orderCreateTime'], 2)
            for start, end in zip(self.starts, self.ends):
                start_timestamp = time_to_millisecond(start)
                item_timestamp = time_to_millisecond(item_time)
                end_timestamp = time_to_millisecond(end)
                if start_timestamp <= item_timestamp <= end_timestamp:
                    self._set_order(start_timestamp, item)

    def fetch_data(self):
        """GET statistic data to bucket of time interval"""
        self._construct_time_interval()
        self._fetch_traders_id()

        count = 0
        for address in self.trader_ids:
            if count == 3:
                time.sleep(1)
                count = 0
            orders = self._fetch_orders(address)
            self._process_orders(orders)
            count += 1

        spread_datas = []
        for key_timestamp, dict_obj in self.dict_orders.items():
            buy_ls = dict_obj[MarketDataService.BUY_ORDER]
            sel_ls = dict_obj[MarketDataService.SELL_ORDER]
            if len(buy_ls) == 0 or len(sel_ls) == 0:
                continue

            highest_bid_order = max(buy_ls, key=lambda x: float(x['price']))
            lowst_ask_order = min(sel_ls, key=lambda x: float(x['price']))
            spread_value = float(lowst_ask_order['price']) - float(highest_bid_order['price'])
            obj = {
                'timestamp': datetime.datetime.fromtimestamp(key_timestamp/1000.0),
                'value': spread_value,
                'pair': self.pair
            }
            spread_datas.append(obj)
        return spread_datas