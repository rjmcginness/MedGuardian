from django.db import models
from src.user_model import ContactInformation
from src.user_model import Address
from users.models import Patient
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
    contact_information = models.ForeignKey(ContactInformation, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


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


class AdministrationTime(models.Model):
    value = models.TimeField()
    description = models.CharField(max_length=256, null=True)


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prescriber = models.ForeignKey(Prescriber, null=True, on_delete=models.SET_NULL)
    quantity_per_dose = models.FloatField(default=1,
                                          help_text='Quantity to be administered for each dose')
    dose_units = models.CharField(max_length=20,
                                  help_text='Units of quantity per dose')
    instructions = models.TextField('SIG: how is the medication to be used')
    quantity = models.FloatField(help_text='Amount of medication purchased or prescribed')
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
    date_written = models.DateField(help_text='Date Written')
    expiration_date = models.DateField(help_text='Expiration date')
    is_prn = models.BooleanField(default=False,
                                 help_text='Is this an "as needed" medication')
    prn_reason = models.CharField(max_length=128,
                                  help_text='Reason for "as needed" use')
    is_active = models.BooleanField(default=True,
                                    help_text='Is this prescription still active')
    routes = models.ManyToManyField('RouteOfAdministration', through='PrescriptionRoute')
    medications = models.ManyToManyField('medications.Medication', through='PrescriptionMedication')
    administration_times = models.ManyToManyField('AdministrationTime', through='PrescriptionAdminTime')
    frequencies = models.ManyToManyField('AdministrationFrequency', through='PrescriptionFrequency')


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


class PrescriptionFrequency(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    frequency = models.ForeignKey(AdministrationFrequency, on_delete=models.CASCADE)


class PharmacyPharmacist(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    pharmacist = models.ForeignKey(Pharmacist, on_delete=models.CASCADE)


class PrescriptionAdminTime(models.Model):
    ######does this cascade to the RX??????
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    administration_time = models.ForeignKey(AdministrationTime, on_delete=models.CASCADE)


class PrescriptionMedication(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)


class PharmacistTransaction(models.Model):
    pharmacist = models.ForeignKey(Pharmacist, on_delete=models.CASCADE)
    transaction = models.ForeignKey(PrescriptionTransaction, on_delete=models.CASCADE)
