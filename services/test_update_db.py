import pytest
from datetime import datetime
from .update_db import get_db
from .update_db import update_admin_routes
from .update_db import create_administration_times
from .update_db import update_admin_frequencies

def test_update_admin_routes():
    db = get_db()
    test_data = './test_data/routes.data'
    update_admin_routes(db, test_data)

    route = db.execute_statement("SELECT * FROM prescriptions_routeofadministration WHERE name='by mouth'")

    assert route.first().name == "by mouth"

def test_load_admin_times():
    db = get_db()
    create_administration_times(db)

    time = db.execute_statement('SELECT * FROM prescriptions_administrationtime')

    assert time.first().value == datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0).time()

def test_update_admin_frequencies():
    db = get_db()
    test_data = './test_data/frequencies.data'
    update_admin_frequencies(db, test_data)

    frequency = db.execute_statement("SELECT * FROM prescriptions_administrationfrequency WHERE abbreviation='bid'")

    assert frequency.first().abbreviation == "bid"


def test_process_medication_data():
    from .update_db import process_medication_data
    with open('../data/medications.txt', 'rt') as f:
        result = process_medication_data(f)

    assert result > 0