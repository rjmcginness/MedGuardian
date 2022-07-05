from django.db import models
from ..src.user_model import ContactInformation
from ..src.user_model import Address


class Patient(models.Model):
    first_name = models.CharField(max_length=30,
                                  help_text="Patient's first name")
    last_name = models.CharField(max_length=30,
                                 help_text="Patient's last name")
    birth_date = models.DateField(help_text="Patient's date of birth")

    contact_information = models.ForeignKey(ContactInformation, ondelete=models.SET_NULL)
    address = models.ForeignKey(Address, ondelete=models.SET_NULL)

