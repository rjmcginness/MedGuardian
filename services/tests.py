import pytest
from decouple import config
from datetime import datetime
from db_connect import DBWrapper
from db_connect import make_db_url

def test_db_connect():
    db_name = config('DB_NAME')
    db_user = config('DB_USER')
    db_password = config('DB_PASSWORD')
    db_host = config('DB_HOST')
    db_port = config('DB_PORT')

    db = DBWrapper(make_db_url(db_user + 'ql',
                               'psycopg2',
                               db_user,
                               db_password,
                               db_host,
                               db_port,
                               db_name)
                  )

    result = db.execute_statement("SELECT * FROM src_patient").first()

    assert result.birth_date == datetime(year=2013, month=2, day=8).date()