import psycopg2.extras
from datetime import datetime
from . import Model

class User(Model):
    _table = 'users'
    _columns = {
        '_id': 0,
        'given_name': '',
        'family_name': '',
        'zid': '',
        'arc_member': False,
        'email': '',
        'phone': '',
        'discord_id': '',
        'is_verified': False,
        'created_at': None,
        'updated_at': None,
        'deleted_at': None
    }

    def __init__(self, **args):
        super().__init__(args)
    
    @classmethod
    def create(cls, data):
        return super().create({
            'is_verified': False,
            **data
        }, ['_id', 'created_at', 'updated_at'])

    @classmethod
    def by_discord_id(cls, discord_id):
        return cls.by_id(discord_id, id_col='discord_id')