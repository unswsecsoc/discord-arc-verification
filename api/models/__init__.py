from lib.db import conn
import psycopg2.extras
from datetime import datetime, date
import logging
import psycopg2
from typing import List, Tuple
from lib.errors import BaseError, DBUniqueError

logger = logging.getLogger(__name__)

class Model(object):
    _table = ''
    _columns = {}
    _default_exclude = []
    _conn = conn

    def __init__(self, args: dict):
        for i in self.__class__._columns:
            setattr(self, i, args.get(i, self.__class__._columns[i]))
    
    def toJSON(self, include=None, exclude=None):
        out = {}
        if include:
            for i in include:
                out[i] = getattr(self, i)
            return out

        if exclude == None: exclude = self.__class__._default_exclude
        for i in self.__class__._columns:
            if i in exclude: continue
            out[i] = getattr(self, i)
            if isinstance(out[i], datetime):
                out[i] = int(out[i].timestamp())
            elif isinstance(out[i], date):
                out[i] = out[i].strftime("%Y-%m-%d")

        return out

    def _one_to_many(self, cls2, col, col2, offset=0, limit=50, exclude=None):
        if exclude == None: exclude = cls._default_exclude
        query = (f'SELECT {cls2._get_columns_sql(exclude=exclude)} FROM {cls2._table} '+
            'WHERE {col2}=%s ' + 
            'LIMIT %s OFFSET %s' if limit else '')
        with cls._conn, cls._conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(query, (getattr(self, col, self.__class__._columns[col]), limit, offset))
            return [cls(**i) for i in cur.fetchall()]
    
    # IMPORTANT (make sure you don't let the user pick any arbitrary key when calling this function, this could open up the DB to SQLi)
    def update_value(self, key, value):
        if key not in self.__class__._columns:
            return False
        return self.__class__._query_one(f'UPDATE {self.__class__._table} SET {key}=%s WHERE _id=%s RETURNING {key}', (value, self._id))
    
    @classmethod
    def _get_columns_sql(cls, exclude=None, prefix=False):
        # since its only a small number of columns, we can do a linear
        # search through the array
        if exclude == None: exclude = cls._default_exclude
        return ','.join((f'{cls._table}.' if prefix else '') + i 
            for i in cls._columns.keys() if i not in exclude)
    
    @classmethod
    def _query_many(cls, query, params=tuple(), raw=False):
        with cls._conn, cls._conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            logger.debug(f'SQL Query: {query}')
            cur.execute(query, params)
            if raw: return cur.fetchall()
            
            return [cls(**i) for i in cur.fetchall()]
    
    @classmethod
    def _query_one(cls, query, params=tuple(), raw=False):
        with cls._conn, cls._conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            logger.debug(f'SQL Query: {query}')
            try:
                cur.execute(query, params)
                if cur.rowcount == -1: return None
                res = cur.fetchone()
                if not res: return None
                if raw: return res
                return cls(**res)
            except psycopg2.errors.UniqueViolation as e:
                raise DBUniqueError(e)
            except Exception as e:
                raise BaseError(e)
    
    @classmethod
    def _insert(cls, data: dict, returning: List=[]):
        query = f'INSERT INTO {cls._table} ({",".join(data.keys())}) VALUES ({("%s,"*len(data.keys()))[:-1]})'
        if returning:
            query += f' RETURNING {",".join(returning)}'
        obj = cls._query_one(query, tuple(data.values()))
        for i in data:
            setattr(obj, i, data[i])

        return obj

    @classmethod
    def by_id(cls, _id, exclude=None, id_col='_id'):
        if exclude == None: exclude = cls._default_exclude
        query = f'SELECT {cls._get_columns_sql(exclude=exclude)} FROM {cls._table} WHERE {id_col}=%s'
        return cls._query_one(query, (_id,))
    
    @classmethod
    def get_all(cls, offset=0, limit=50, where:List[Tuple[str, str, any]] = [], exclude=None):
        if exclude == None: exclude = cls._default_exclude
        query = f'SELECT {cls._get_columns_sql(exclude=exclude)} FROM {cls._table}'
        if where:
            query += f' WHERE {"AND ".join(i[0] + i[1] + "%s" for i in where)}'
        query += ' LIMIT %s OFFSET %s'
        return cls._query_many(query, tuple(i[2] for i in where) + (limit, offset))
    
    @classmethod
    def create(cls, data, ret=[]):
        obj = {}
        for i in data:
            if i in cls._columns:
                obj[i] = data[i]
        return cls._insert(obj, ret)