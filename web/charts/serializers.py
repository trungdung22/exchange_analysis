from flask_restful import fields
from web.utility.utils import convert_time_local

chart_fields = {
    'timestamp': fields.DateTime(dt_format='iso8601', attribute=lambda x: convert_time_local(x.timestamp)),
    'pair': fields.String(default=''),
    'value': fields.Float(default=0)
}

pair_fields = {
    'id': fields.String(default=''),
    'name': fields.String(default=''),
    'is_active': fields.Boolean(default=True),
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601'),
}