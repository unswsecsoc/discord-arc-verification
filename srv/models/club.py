import psycopg2.extras
from datetime import date
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

    def get_users(self):
        return User.by_club(self._id)

    @classmethod
    def create(cls, data):
        return super().create({
            'is_enabled': False,
            **data
        }, ['_id', 'created_at', 'updated_at'])

    @classmethod
    def by_discord_id(cls, discord_id):
        return cls.by_id(discord_id, id_col='discord_id')