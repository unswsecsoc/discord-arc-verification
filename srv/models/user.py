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