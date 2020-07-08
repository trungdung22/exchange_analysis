from bson import ObjectId
from web.charts.models import Pairs, SpreadData


PAIR_OBJECT_ID_1 = ObjectId()
PAIR_OBJECT_ID_2 = ObjectId()

PAIR_OBJECTS = [
    {
        'id': PAIR_OBJECT_ID_1,
        'name': 'BNB_USDSB-1AC',
        'is_active': True
    },
    {
        'id': PAIR_OBJECT_ID_2,
        'name': 'BTCB-1DE_BUSD-BD1',
        'is_active': True
    }
]

SPREAD_DATA_OBJS = [
    {
        'timestamp': '2020-07-03T15:05:00.000Z',
        'pair': 'BTCB-1DE_BUSD-BD1',
        'value': 342.37
    },
    {
        'timestamp': '2020-07-03T16:25:00.000Z',
        'pair': 'BTCB-1DE_BUSD-BD1',
        'value': -9063.7988792
    },
    {
        'timestamp': '2020-07-03T16:25:00.000Z',
        'pair': 'BTCB-1DE_BUSD-BD1',
        'value': -9063.7988792
    },
    {
        'timestamp': '2020-07-03T05:30:00.000Z',
        'pair': 'BNB_USDSB-1AC',
        'value': 32.7988792
    }
]


def init_db():
    for pair_obj in PAIR_OBJECTS:
        pair = Pairs(**pair_obj)
        pair.save()

    for data_obj in SPREAD_DATA_OBJS:
        spread = SpreadData(**data_obj)
        spread.save()
