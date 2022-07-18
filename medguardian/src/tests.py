from django.test import TestCase
import pytest
from .user_model import Patient

@pytest.mark.django_db
def test_patient():
    assert Patient.objects.filter(username='Bronwyn').exists
    # return patient

# @pytest.fixture
# def test_get_prescribers(db, test_patient):
#     patient = test_patient
#     prescribers = patient.prescriber_set
#     assert prescribers.count() > 0