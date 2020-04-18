import psycopg2.extras
from datetime import datetime
from . import Model
from .club import Club

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
    
    # ignoring OOP
    def get_club_discord_ids(self):
        with super()._conn, super()._conn.cursor() as cur:
            cur.execute(
                f"SELECT c._id, c.discord_id, c.verified_role_id FROM members m" + 
                " JOIN clubs c ON c._id=m.club_id JOIN users u ON u._id=m.user_id" +
                " WHERE m.user_id=%s", (self._id,))
            return cur.fetchall()
        
    # set user as verified
    def set_verified(self):
        with super()._conn, super()._conn.cursor() as cur:
            cur.execute(f"UPDATE {self.__class__._table} SET is_verified=TRUE WHERE _id=%s", (self._id,))
            self.is_verified = True
            return

    @classmethod
    def create(cls, data):
        return super().create({
            'is_verified': False,
            **data
        }, ['_id', 'created_at', 'updated_at'])

    @classmethod
    def by_discord_id(cls, discord_id):
        return cls.by_id(discord_id, id_col='discord_id')