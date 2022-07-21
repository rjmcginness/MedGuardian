import pytest
from .update_db import get_db
from .update_db import update_admin_routes

def test_admin_routes():
    db = get_db()
    test_data = './test_data/routes.data'
    update_admin_routes(db, test_data)

    route = db.execute_statement("SELECT * FROM prescriptions_routeofadministration WHERE name='by mouth'")

    assert route.first().name == "by mouth"