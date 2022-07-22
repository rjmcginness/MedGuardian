"""
    Used to read data files with prescription component data
    to load and update the database
"""
from decouple import config

from .service_utils import Clock
from .db_access import get_db
from .db_access import execute_statement

def update_admin_routes(db, data_file_name: str) -> None:

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
    '''
        UPDATE DATABASE SERVICE
        uses: load or reload tables only read by user
    '''

    routes_file = config('ADMIN_ROUTE_FILE')
    frequencies_file = config('ADMIN_FREQ_FILE')

    # get db connection
    db = get_db()

    # run updates
    update_admin_routes(db, routes_file)
    create_administration_times(db)
    update_admin_frequencies(db, frequencies_file)
