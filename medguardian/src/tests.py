from django.test import TestCase
import pytest
from .user_model import Patient
from .user_model import Address
from .user_model import ContactInformation

import datetime


@pytest.fixture
def test_patient(db):
    patient = Patient.objects.filter(username='Bronwyn')
    return patient


def test_get_prescribers(test_patient):
    assert test_patient.count() > 0
    # prescribers = test_patient.objects.prescriber_set
    # assert prescribers.count() > 0
