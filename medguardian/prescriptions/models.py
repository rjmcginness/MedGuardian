from django.db import models
from src.user_model import ContactInformation
from src.user_model import Address


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
                                        help_text='Is this a continuoue administration')
    value = models.FloatField(default=1,
                              help_text='Number of times administered per unit')
    units = models.CharField(max_length=30,
                             help_text='Units for frequency, hours, dats')