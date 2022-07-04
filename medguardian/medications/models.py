from django.db import models


class Medication(models.Model):
    generic_name = models.CharField(max_length=128,
                                    help_text='The generic name of the medication')
    brand_name = models.CharField(max_length=128,
                                  help_text='The brand name of the medication')
    strength = models.FloatField(help_text='The strength per dosage unit')
    manufacturer = models.CharField(max_length=128,
                                    help_text='The name of the manufacturer')
