"""
    Used to read data files with prescription component data
    to load and update the database
"""

from decouple import config

# from db_connect import DBWrapper
# from db_connect import make_db_url
# from db_connect import DBWrapperError
# from service_utils import Clock

from .db_connect import DBWrapper
from .db_connect import make_db_url
from .db_connect import DBWrapperError
from .service_utils import Clock

def get_db():
    db_name = config('DB_NAME')
    db_user = config('DB_USER')
    db_password = config('DB_PASSWORD')
    db_host = config('DB_HOST')
    db_port = config('DB_PORT')

    return  DBWrapper(make_db_url(db_user + 'ql',
                                  'psycopg2',
                                  db_user,
                                  db_password,
                                  db_host,
                                  db_port,
                                  db_name),
                     )

def execute_statement(db, stmt: str, error_msg: str) -> None:
    try:
        db.execute_statement(stmt)
    except DBWrapperError as e:
        print(error_msg + '\n', e)

def update_admin_routes(db, data_file_name: str) -> None:

    routes = []
    with open(data_file_name, 'rt') as f:
        routes = [line for line in f]

    if not routes:
        return

    # build insert values for SQL from frequency data
    # assumes that string values are in quotes
    routes = [f'({route.strip()})' for route in routes]
    routes = ','.join(routes)

    # if here there is a route of administration value to insert
    stmt = 'TRUNCATE prescriptions_routeofadministration CASCADE;'
    stmt += 'INSERT INTO prescriptions_routeofadministration '
    stmt += f'(name, abbreviation, description) VALUES {routes}'

    execute_statement(db, stmt, 'Error occurred on insert.  check duplicate entry')


def create_administration_times(db) -> None:
    #default of every 5 minutes within 24 hours from midnight
    times = Clock.times_in_24hours()

    if not times:
        return

    # bundle times as strings for SQL
    times = [f"('{time}')" for time in times]
    times = ','.join(times)

    # create INSERT statement with times (description left as null)
    stmt = 'TRUNCATE prescriptions_administrationtime CASCADE;'
    stmt += f'INSERT INTO prescriptions_administrationtime (value) VALUES {times}'

    execute_statement(db, stmt, 'Error occurred on insert.  check duplicate entry')


def update_admin_frequencies(db, data_file_name: str) -> None:
    frequencies = []
    with open(data_file_name, 'rt') as f:
        frequencies = [line for line in f]

    if not frequencies:
        return

    # if here there is a route of administration value to insert

    # build insert values for SQL from frequency data
    # expects that string values are in quotes
    frequencies = [f'({frequency.strip()})' for frequency in frequencies]
    frequencies = ','.join(frequencies)

    stmt = 'TRUNCATE prescriptions_administrationfrequency CASCADE;'
    stmt += 'INSERT INTO prescriptions_administrationfrequency '
    stmt += f'(name, abbreviation, description, is_continuous, value, units) VALUES {frequencies}'

    execute_statement(db, stmt, 'Error occurred on insert.  check duplicate entry')


if __name__ == '__main__':
    # routes_file = config('ADMIN_ROUTE_FILE')
    # db = get_db()
    # update_admin_routes(db, routes_file)

    db = get_db()
    create_administration_times(None)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/