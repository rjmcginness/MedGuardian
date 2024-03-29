from django.db import models
from django.db.models import constraints

import src.user_model
from src.user_model import ContactInformation
from src.user_model import Address
from src.user_model import Patient
from medications.models import Medication
from django.utils import timezone


class Prescriber(models.Model):
    first_name = models.CharField(max_length=30,
                                  help_text="Prescriber's first name")
    last_name = models.CharField(max_length=30,
                                 help_text="Prescriber's last name")
    federal_dea = models.CharField(max_length=9,
                                   help_text='DEA Number')
    state_dea = models.CharField(max_length=20,
                                 help_text='State controlled substance license number')
    credentials = models.CharField(max_length=20, null=True, blank=True)
    specialty = models.CharField(max_length=50, null=True, blank=True)
    contact_information = models.ForeignKey(ContactInformation, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    patients = models.ManyToManyField('src.Patient', through='PatientPrescribers')
    class Meta:
        constraints = [constraints.UniqueConstraint(fields=('federal_dea', 'address_id'),
                                                    name='prescriber_address_unique')]

    def __str__(self) -> str:
        return f'{self.last_name}, {self.first_name} {self.credentials} in {self.address.city}'

class RouteOfAdministration(models.Model):
    name = models.CharField(max_length=80,
                            unique=True,
                            help_text='Name of route of administration')
    abbreviation = models.CharField(max_length=12,
                                    help_text='Route of administration abbreviation')
    description = models.CharField(max_length=256,
                                   blank=True,
                                   null=True,
                                   help_text='Description of route of administration')

    def __str__(self)-> str:
        return f'{self.name}'


class AdministrationFrequency(models.Model):
    name = models.CharField(max_length=80,
                            unique=True,
                            help_text='Name of administration frequency')
    abbreviation = models.CharField(max_length=12,
                                    help_text='Abbreviation for administration frequency')
    description = models.CharField(max_length=256,
                                   help_text='Description of administration frequency')
    is_continuous = models.BooleanField(default=False,
                                        help_text='Is this a continuous administration')
    value = models.FloatField(default=1,
                              help_text='Number of times administered per unit')
    units = models.CharField(max_length=30,
                             help_text='Units for frequency: hour, day, etc')

    def __str__(self) -> str:
        return f'{self.name}'


class AdministrationTime(models.Model):
    value = models.TimeField()
    description = models.CharField(max_length=256, null=True)


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prescriber = models.ForeignKey(Prescriber, null=True, on_delete=models.SET_NULL)
    medications = models.ManyToManyField('medications.Medication', through='PrescriptionMedication')
    routes = models.ManyToManyField('RouteOfAdministration', through='PrescriptionRoute')
    frequencies = models.ManyToManyField('AdministrationFrequency', through='PrescriptionFrequency')
    quantity_per_dose = models.FloatField(default=1,
                                          help_text='Quantity to be administered for each dose')
    dose_units = models.CharField(max_length=20,
                                  help_text='Units of quantity per dose')
    is_prn = models.BooleanField(default=False,
                                 help_text='Is this an "as needed" medication',
                                 blank=True)
    prn_reason = models.CharField(max_length=128,
                                  help_text='Reason for "as needed" use',
                                  null=True,
                                  blank=True)
    instructions = models.TextField('SIG: how is the medication to be used')
    quantity = models.FloatField(help_text='Amount of medication purchased or prescribed',
                                 null=True,
                                 blank=True)
    duration_of_therapy = models.PositiveIntegerField(blank=True,
                                                      null=True,
                                                      help_text='How long to take this medication')
    duration_units = models.CharField(max_length=40,
                                      blank=True,
                                      null=True,
                                      help_text='Units for duration: days, hours, etc')
    refills = models.PositiveSmallIntegerField(blank=True,
                                               null=True,
                                               help_text='Refills authorized')
    signature = models.BinaryField(help_text='Signature image', null=True, blank=True)
    date_written = models.DateField(help_text='Date Written', null=True, blank=True)
    expiration_date = models.DateField(help_text='Expiration date', null=True, blank=True)
    is_active = models.BooleanField(default=True,
                                    help_text='Is this prescription still active')
    administration_times = models.ManyToManyField('AdministrationTime', through='PrescriptionAdminTime')

    class Meta:
        constraints = [constraints.UniqueConstraint(fields=['id', 'patient_id', 'prescriber_id'],
                                                    name='rx_unique'),]


class Administration(models.Model):
    quantity_administered = models.FloatField(help_text='Quantity administered')
    date_time_taken = models.DateTimeField(default=timezone.now(),
                                           help_text='Date and time taken')
    description = models.CharField(max_length=256,
                                   help_text='Details about this administration of medication')
    outcome = models.TextField(help_text='Outcome of this administration of medication')

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)


class TransactionType(models.Model):
    name = models.CharField(max_length=80,
                            help_text='Name of transaction type')
    code = models.PositiveSmallIntegerField(help_text='Transaction code')


class Pharmacy(models.Model):
    name = models.CharField(max_length=128,
                            help_text='Pharmacy name')
    federal_dea = models.CharField(max_length=9,
                                   help_text='Federal DEA number')
    state_license = models.CharField(max_length=20,
                                     help_text='State license number')
    contact_information = models.ForeignKey(ContactInformation, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    pharmacists = models.ManyToManyField('Pharmacist', through='PharmacyPharmacist')


class Pharmacist(models.Model):
    first_name = models.CharField(max_length=30,
                                  help_text="Pharmacist's first name")
    last_name = models.CharField(max_length=30,
                                 help_text="Pharmacist's last name")
    license_number = models.CharField(max_length=20,
                                      help_text='State Pharmacist license number')
    license_state = models.CharField(max_length=20,
                                     help_text="State of pharmacist's license")


class PrescriptionCustomer(models.Model):
    first_name = models.CharField(max_length=30,
                                  help_text="Customer's first name")
    last_name = models.CharField(max_length=30,
                                 help_text="Customer's last name")
    license_number = models.CharField(max_length=20,
                                      help_text="Customer's id number")
    license_state = models.CharField(max_length=20,
                                     help_text="State of customer's id")


class PrescriptionTransaction(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              help_text='Status of prescription')
    transaction_date_time = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(PrescriptionCustomer, null=True, on_delete=models.SET_NULL)
    pharmacists = models.ManyToManyField('Pharmacist', through='PharmacistTransaction')


class PrescriptionRoute(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    administration_route = models.ForeignKey(RouteOfAdministration, on_delete=models.CASCADE)

    class Meta:
        constraints = [constraints.UniqueConstraint(fields=['prescription', 'administration_route'],
                                                    name='rx_route_unique'),]


class PrescriptionFrequency(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    frequency = models.ForeignKey(AdministrationFrequency, on_delete=models.CASCADE)

    class Meta:
        constraints = [constraints.UniqueConstraint(fields=['prescription', 'frequency'],
                                                    name='rx_frequency_unique'),]


class PharmacyPharmacist(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    pharmacist = models.ForeignKey(Pharmacist, on_delete=models.CASCADE)

    classMeta:\
        constraints = [constraints.UniqueConstraint(fields=['pharmacy', 'pharmacist'],
                                                    name='pharmacist_pharmacy_unique'),]


class PrescriptionAdminTime(models.Model):
    ######does this cascade to the RX??????
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    administration_time = models.ForeignKey(AdministrationTime, on_delete=models.CASCADE)

    class Meta:
        constraints = [constraints.UniqueConstraint(fields=['prescription', 'administration_time'],
                                                    name='rx_admin_time_unique'),]


class PrescriptionMedication(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)

    constraints = [constraints.UniqueConstraint(fields=['prescription_id', 'medication_id'],
                                                name='rx_med_unique')]


class PharmacistTransaction(models.Model):
    pharmacist = models.ForeignKey(Pharmacist, on_delete=models.CASCADE)
    transaction = models.ForeignKey(PrescriptionTransaction, on_delete=models.CASCADE)

class PatientPrescribers(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prescriber = models.ForeignKey(Prescriber, on_delete=models.CASCADE)

    class Meta:
        constraints = [constraints.UniqueConstraint(fields=['patient', 'prescriber'],
                                                    name='patient_prescriber_unique')]


class ContactTimes(models.Model):
    contact = models.ForeignKey(src.user_model.ContactInformation,
                                   on_delete=models.CASCADE)
    administration_time = models.ForeignKey(AdministrationTime,
                                               on_delete=models.CASCADE)
    instances = models.PositiveIntegerField(default=1, blank=True)

    class Meta:
        constraints = [constraints.UniqueConstraint(fields=['contact_id', 'administration_time_id'],
                                                    name='contact_time_unique'),
                      ]
