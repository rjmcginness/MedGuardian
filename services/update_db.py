"""
    Used to read data files with prescription component data
    to load and update the database
"""

from decouple import config

from db_connect import DBWrapper
from db_connect import make_db_url
from db_connect import DBWrapperError

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
                                  db_name)
                     )

def update_admin_routes(db, data_file_name: str) -> None:

    routes = []
    with open(data_file_name, 'rt') as f:
        routes = [line for line in f]

    if not routes:
        return

    # if here there is a route of administration value to insert
    stmt = 'TRUNCATE prescriptions_routeofadministration CASCADE;'
    stmt += 'INSERT INTO prescriptions_routeofadministration (name, abbreviation, description) VALUES '

    for route in routes:
        stmt += '(' + route.strip() + '),' # each route is a comma delimited list

    stmt = stmt[:-1] # remove the trailing comma

    try:
        db.execute_statement(stmt)
    except DBWrapperError as e:
        print('Error occurred on insert.  check duplicate entry\n', e)




if __name__ == '__main__':
    routes_file = config('ADMIN_ROUTE_FILE')
    db = get_db()
    update_admin_routes(db, routes_file)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/