from rest_framework import serializers
from .models import MedicationProductDetails
from .models import Medication


class MedicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Medication
        fields = ['generic_name',
                  'brand_name',
                  'strength',
                  'strength_units',
                  'strength_text',
                  'dosage_form']


class MedicationProductDetailsSerializer(serializers.HyperlinkedModelSerializer):
    medication = MedicationSerializer()

    class Meta:
        model = MedicationProductDetails
        fields = ['ndc',
                  'manufacturer',
                  'schedule',
                  'price',
                  'medication']

    # ndc = serializers.CharField()
    # manufacturer = serializers.CharField()
    # schedule = serializers.IntegerField()
    # price = serializers.DecimalField(max_digits=8, decimal_places=4)



