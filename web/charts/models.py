from web.base.model import db, Base


class SpreadData(Base):
    timestamp = db.DateTimeField(required=True)
    pair = db.StringField(max_length=50)
    value = db.FloatField(default=0)

    meta = {'collection': 'spread_data', "db_alias":"default"}


class Pairs(Base):
    name = db.StringField(max_length=50)
    is_active = db.BooleanField(default=True)

    meta = {'collection': 'pairs', "db_alias": "default"}