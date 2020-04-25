import psycopg2.extras
from datetime import date
from . import Model
import models.user
import models.member
import psycopg2.extras

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

    def get_members(self):
        user_columns = models.user.User._get_columns_sql(prefix=True)
        print(user_columns)
        with super()._conn, super()._conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                f"SELECT {user_columns} FROM {models.member._table} m" + 
                " JOIN users ON users._id=m.user_id" +
                " WHERE m.club_id=%s AND users.is_verified=TRUE", (self._id,))
            return [models.user.User(**i) for i in cur.fetchall()]

    @classmethod
    def create(cls, data):
        return super().create({
            'is_enabled': False,
            **data
        }, ['_id', 'created_at', 'updated_at'])

    @classmethod
    def by_discord_id(cls, discord_id):
        return super().by_id(discord_id, id_col='discord_id')
