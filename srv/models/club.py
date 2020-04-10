import psycopg2.extras
from datetime import date
from .event import Event
from .member import Member
from . import Model

class Club(Model):
    _table = 'clubs'
    _columns = {
        '_id': 0,
        'name': '',
        'permalink': '',
        'description': '',
        'email': '',
        'website': '',
        'admin_channel_id': '',
        'admin_role_id': '',
        'verified_role_id': '',
        'discord_id': '',
        'is_enabled': False,
        'created_at': None,
        'updated_at': None,
        'deleted_at': None
    }
    
    def __init__(self, **args):
        super().__init__(args)

    def get_events(self, is_published:bool = None):
        return Event.by_club(self._id, is_published)

    def get_users(self):
        return User.by_club(self._id)

    @classmethod
    def by_permalink(cls, permalink):
        query = f'SELECT {cls._get_columns_sql()} FROM {cls._table} WHERE permalink=%s'
        return cls._query_one(query, (permalink,))

    @classmethod
    def create(cls, data):
        return super().create(data, ['_id', 'created_at', 'updated_at'])