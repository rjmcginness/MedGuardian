from django.test import TestCase
import pytest
from .user_model import Patient
from .user_model import Address
from .user_model import ContactInformation

import datetime

# @pytest.mark.django_db
# def test_create_patient(db):
#     address = Address(street='20 Overlook Dr',
#                       street2='',
#                       city='Newfields',
#                       county='Rockingham',
#                       state_name='NH',
#                       zip_code='03856'
#                       )
#
#     # one of phone, mobile, or fax will have a value (form validation)
#     contact = ContactInformation(home_phone=None,
#                                  mobile_phone='6038458072',
#                                  fax_number=None,
#                                  preferred_type='text'
#                                  )
#
#     address.save()
#     contact.save()
#
#     patient = Patient.objects.create(username='Bronwyn',
#                       first_name='Bronwyn',
#                       last_name='McGinness',
#                       email='browwyn@horsegirl.com',
#                       is_staff=False,
#                       is_superuser=False,
#                       is_active=True,
#                       date_joined=datetime.datetime.now(),
#                       birth_date=datetime.date(year=2013, month=2, day=8),
#                       address=address,
#                       contact_information=contact
#                       )
#
#     # call User.set_password to set the password (preforms hashing)
#     patient.set_password('Password123!')
#     patient.save()
#
#     assert patient.username == 'Bronwyn'

@pytest.fixture
def test_patient(db):
    patient = Patient.objects.filter(username='Bronwyn')
    return patient


def test_get_prescribers(test_patient):
    assert test_patient.count() > 0
    # prescribers = test_patient.objects.prescriber_set
    # assert prescribers.count() > 0