"""
    Provides a single module to allow access to db
"""

from decouple import config

from .db_connect import DBWrapper
from .db_connect import make_db_url
from .db_connect import DBWrapperError

def get_db():
    db_name = config('DB_NAME')
    db_user = config('DB_USER')
    db_password = config('DB_PASSWORD')
    db_host = config('DB_HOST')
    db_port = config('DB_PORT')

    return DBWrapper(make_db_url(db_user + 'ql',
                                 'psycopg2',
                                 db_user,
                                 db_password,
                                 db_host,
                                 db_port,
                                 db_name),
                     )

def execute_statement(db, stmt: str, error_msg: str):
    result = None
    try:
        result = db.execute_statement(stmt)
    except DBWrapperError as e:
        print(error_msg + '\n', e)

    return result