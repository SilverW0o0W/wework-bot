#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: Silver (silver.codingcat@gmail.com)
@create: 2022/1/5
@brief:
"""

import sqlalchemy


def init_engine(db_uri):
    return sqlalchemy.create_engine(
        db_uri,
        pool_recycle=5, pool_size=10,
        convert_unicode=True,
        execution_options={"autocommit": True})


def build_db_uri(db_conf):
    return "mysql+pymysql://{user}:{password}@{host}/{database}?charset={charset}".format(**db_conf)


class Connection(object):
    def __init__(self, engine):
        self.engine = engine
        self.db = None

    def __enter__(self):
        if self.db:
            return
        self.db = self.engine.connect()
        self.db.execute("SET character_set_client='utf8mb4'")
        self.db.execute("SET character_set_connection='utf8mb4'")
        self.db.execute("SET character_set_results='utf8mb4'")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.db:
            return
        self.db.close()
        self.db = None

    def insert(self, sql, params, raise_exception=False):
        trans = self.db.begin()
        _id = 0
        try:
            result = self.db.exec_driver_sql(sql, params)
            trans.commit()
            _id = result.lastrowid
        except Exception as e:
            trans.rollback()
            if raise_exception:
                raise e
            return -1, str(e)
        return _id, ""

    def insert_many(self, sql, params_list, raise_exception=False):
        trans = self.db.begin()
        try:
            result = None
            for params in params_list:
                result = self.db.exec_driver_sql(sql, params)
            trans.commit()
            last_rowid = result.lastrowid
        except Exception as e:
            trans.rollback()
            if raise_exception:
                raise e
            return -1, str(e)
        return last_rowid, ""

    def read_list(self, sql, params):
        return [
            dict(item)
            for item in self.db.execute(sql, params).fetchall()
        ]
