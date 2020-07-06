from flask_mongoengine import MongoEngine
from datetime import datetime

db = MongoEngine()


class Base(db.Document):
    created_at = db.DateTimeField(default=datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.utcnow)

    meta = {
        'abstract': True,
        'strict': False
    }

    @classmethod
    def collection(cls):
        return cls._get_collection()

    def get_id(self):
        return str(self.pk)