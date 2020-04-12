import psycopg2.extras
from datetime import datetime
from . import Model

class Member(Model):
    _table = 'members'
    _columns = {
        'user_id': 0,
        'club_id': 0,
        'created_at': None,
        'deleted_at': None
    }

    def __init__(self, **args):
        super().__init__(args)
    
    @classmethod
    def create(cls, data):
        return super().create({
            'user_id': data['user_id'],
            'club_id': data['club_id']
        }, ['created_at'])
    
    @classmethod
    def check_existence(cls, user_id, club_id):
        return super()._query_one(
            'SELECT 1 FROM members WHERE user_id=%s and club_id=%s',
            (user_id, club_id), True
        ) is not None