import celery
from libs.markets.engine import MarketType
from web.charts.models import SpreadData
from datetime import datetime
from web.utility.utils import MarketDataService, convert_time
from libs.markets.service_provider import MarketServiceProvider
from mongoengine import connect, Q


@celery.task()
def fetch_spread_bucket():
    current_time = datetime.utcnow()
    connect('exchange', 'default', host='localhost')
    pair = 'BTCB-1DE_BUSD-BD1'
    engine = MarketServiceProvider.get_market_engine(MarketType.BINANCE)
    data = engine.order_depth(pair=pair)
    bid = float(data['bids'][0][0])
    ask = float(data['asks'][0][0])
    spread_value = float((ask - bid) / ask) * 100
    spread_data = SpreadData()
    spread_data.timestamp = current_time
    spread_data.value = spread_value
    spread_data.pair = pair
    spread_data.save()


def crawl_market_data(start_time, end_time, pair):
    print("Start:crawl_market_data")
    #connect('exchange', 'default', host='localhost')
    start_time = convert_time(start_time)
    end_time = convert_time(end_time)
    service = MarketDataService(start_time, end_time, pair)
    spread_datas = service.fetch_data()
    SpreadData.objects((Q(timestamp__gte=start_time) & Q(timestamp__lte=end_time))).delete()
    for data in spread_datas:
        spread_data = SpreadData(**data)
        spread_data.save()
    print("Done:crawl_market_data")

