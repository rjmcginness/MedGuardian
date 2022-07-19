from django.test import TestCase
import pytest
from .models import Prescriber
from .models import PatientPrescribers
from src.user_model import Address
from src.user_model import ContactInformation
from src.user_model import Patient
from datetime import datetime


@pytest.fixture
def create_prescriber(db):
    address = Address(street='14 Front St',
                      street2='',
                      city='Exeter',
                      county='Rockingham',
                      state_name='NH',
                      zip_code='03833'
                      )

    # home (office) phone number is required
    contact = ContactInformation(home_phone='6035480220',
                                 mobile_phone=None,
                                 fax_number=None,
                                 preferred_type='office'
                                 )

    address.save()
    contact.save()

    prescriber = Prescriber(first_name='Tiffany',
                            last_name='McGinness',
                            federal_dea='MM1234567',
                            state_dea='MM1234',
                            address=address,
                            contact_information=contact
                            )

    prescriber.save()

    return prescriber

def test_create_prescriber(create_prescriber):
    prescriber = create_prescriber

    assert (prescriber.last_name == 'McGinness' and
            prescriber.address.state_name == 'NH' and
            prescriber.address.city == 'Exeter')

@pytest.fixture
def prescriber_list(db, create_prescriber):

    create_prescriber

    prescribers = Prescriber.objects.filter(address__state_name='NH',
                                            address__city='Exeter',
                                            last_name='McGinness')
    return prescribers


def test_retrieve_prescribers(prescriber_list):

    assert prescriber_list.count() > 0

def test_select_prescriber(prescriber_list):
    prescriber = prescriber_list.first()

    assert prescriber.last_name == 'McGinness'

@pytest.fixture
def create_patient(db):
    address = Address(street='20 Overlook Dr',
                      street2='',
                      city='Newfields',
                      county='Rockingham',
                      state_name='NH',
                      zip_code='03856'
                      )

    # one of phone, mobile, or fax will have a value (form validation)
    contact = ContactInformation(home_phone=None,
                                 mobile_phone='6038458072',
                                 fax_number=None,
                                 preferred_type='text'
                                 )

    address.save()
    contact.save()

    patient = Patient(username='Bronwyn',
                      first_name='Bronwyn',
                      last_name='McGinness',
                      email='bronwyn@horsegirl.com',
                      is_staff=False,
                      is_superuser=False,
                      is_active=True,
                      date_joined=datetime.now(),
                      birth_date=datetime(year=2013, month=2, day=8).date(),
                      address=address,
                      contact_information=contact
                      )

    # call User.set_password to set the password (preforms hashing)
    patient.set_password('admin123')
    patient.save()

    return patient

def test_create_patient(create_patient):
    patient = create_patient

    assert patient.first_name == 'Bronwyn' and patient.username == 'Bronwyn'

@pytest.mark.django_db
def test_patient_prescriber(create_patient, create_prescriber):
    patient = create_patient
    prescriber = create_prescriber

    pp_association = PatientPrescribers.objects.create(patient_id=patient.id,
                                                       prescriber_id=prescriber.id)

    pp_association = PatientPrescribers.objects.filter(patient_id=patient.id)

    assert pp_association.count() > 0

