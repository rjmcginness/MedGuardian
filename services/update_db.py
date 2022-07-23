"""
    Used to read data files with prescription component data
    to load and update the database
"""
from decouple import config
import csv

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


def preprocess_strength(strength: str) -> tuple:
    '''
        Removes comments from medication strength data.
        :param strength: string containing data representing a
                         medication strength
        :return: string representing the medication strength: value
                 and units
    '''
    # remove FDA comments
    if '**' in strength:
        idx = strength.index('*')
        strength = strength[idx].strip()

    # remove quotes
    if '"' in strength:
        strength.replace('"', '')

    # dump portions after the ; - these are percentages, etc
    if ';' in strength:
        idx = strength.index(';')
        strength = strength[idx].strip()

    return strength


def process_strength(strength: str) -> tuple:
    '''
        Splits out the value and units for medication strength.
        Handles concentrations and medications more than one
        active ingredient
        :param strength: string containing unprocessed medications
               strength data
        :return: tuple containing the dicts of medication strengths
    '''

    ########################FINISH
    ######ONLY PERFORMS PREPROCESSING, NOT COMPLETE
    return preprocess_strength(strength)


def process_medication_data(med_file) -> str:
    reader = csv.DictReader(med_file, delimiter='\t')

    values = []
    for medication in reader:
        strength = process_strength(medication['Strength'])

        ######THIS DOES NOT HAVE STRENGTH VALUE AND UNITS SEPARATED
        values_str = ("'" + medication['ActiveIngredient'] + "'",
                      "'" + medication['DrugName'] + "'",
                      "'" + strength + "'",
                      "'" + medication['Form'] + "'")
        values.append('(' + ','.join(values_str) + ')')

    return ','.join(values)


def update_medications(db, date_file_name: str) -> None:
    with open(date_file_name, 'rt') as med_file:
        values_str = process_medication_data(med_file)

    stmt = 'TRUNCATE medications_medication CASCADE;'
    stmt += 'INSERT INTO medications_medication '
    stmt += f'VALUES (generic_name, brand_name, strength_text, dosage_form) {values_str}'

    execute_statement(db, stmt, 'Error updating medications in db')


if __name__ == '__main__':
    '''
        UPDATE DATABASE SERVICE
        uses: load or reload tables only read by user
    '''

    routes_file = config('ADMIN_ROUTE_FILE')
    frequencies_file = config('ADMIN_FREQ_FILE')
    medication_file = config('MEDICATION_DATA_FILE')

    # get db connection
    db = get_db()

    # run updates
    update_admin_routes(db, routes_file)
    create_administration_times(db)
    update_admin_frequencies(db, frequencies_file)
    update_medications(db, medication_file)
