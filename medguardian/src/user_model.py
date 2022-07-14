from django.db import models
from django.contrib.auth.models import User


class ContactInformation(models.Model):

    class ContactTypes(models.TextChoices):
        HOME = 'home'
        MOBILE = 'mobile'
        EMAIL = 'email'
        TEXT = 'text'
        FAX = 'fax'

    preferred_type = models.CharField(max_length=6,
                                      help_text='Preferred contact type',
                                      choices=ContactTypes.choices)
    home_phone = models.CharField(max_length=15,
                                  help_text='Home telephone number',
                                  null=True,
                                  blank=True)
    mobile_phone = models.CharField(max_length=15,
                                    help_text='Mobile device number',
                                    null=True,
                                    blank=True)
    fax_number = models.CharField(max_length=15,
                                  help_text='Fax number',
                                  null=True,
                                  blank=True)
    # email = models.EmailField(help_text='Email address')


class Address(models.Model):
    street = models.CharField(max_length=256,
                              help_text='Street address 1')
    street2 = models.CharField(max_length=256,
                               help_text='Street address 2',
                               null=True,
                               blank=True)
    city = models.CharField(max_length=80,
                            help_text='City')
    state_name = models.CharField(max_length=80,
                                  help_text='State')
    county = models.CharField(max_length=80,
                              help_text='State',
                              null=True,
                              blank=True)
    zip_code = models.CharField(max_length=10,
                                help_text='Zip Code')


class Patient(User):
    birth_date = models.DateField()
    contact_information = models.ForeignKey(ContactInformation, null=True, on_delete=models.SET_NULL)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
