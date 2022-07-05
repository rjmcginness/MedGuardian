from django.db import models


class Medication(models.Model):
    generic_name = models.CharField(max_length=128,
                                    help_text='The generic name of the medication')
    brand_name = models.CharField(max_length=128,
                                  blank=True,
                                  help_text='The brand name of the medication')
    strength = models.FloatField(help_text='The strength per dosage unit')
    strength_units = models.CharField(max_length=(20),
                                      default='mg',
                                      help_text='The units of measure for the medication strength')
    dosage_form = models.CharField(max_length=80,
                                   default='tablet',
                                   help_text='The dosage form of the medication')

class MedicationProductDetails(models.Model):
    ndc = models.CharField(max_length=11,
                           help_text='The National Drug Code for a medication')
    manufacturer = models.CharField(max_length=80,
                                    default='',
                                    help_text='Medication products manufacturer')
    schedule = models.PositiveSmallIntegerField(help_text='Controlled substance category for medication',
                                                null=True,
                                                blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
