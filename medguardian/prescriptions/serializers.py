from rest_framework import serializers
from .models import Prescriber
from .models import Prescription
from .models import RouteOfAdministration
from .models import AdministrationFrequency
from .models import AdministrationTime
from medguardian.serializers import AddressSerializer
from medguardian.serializers import ContactInformationSerializer
from medguardian.serializers import PatientSerializer
from medications.serializers import MedicationSerializer


class PrescriberSerializer(serializers.HyperlinkedModelSerializer):
    address = AddressSerializer()
    contact_information = ContactInformationSerializer()

    class Meta:
        model = Prescriber
        fields = ['first_name',
                  'last_name',
                  'address',
                  'contact_information',
                  'credentials',
                  'specialty',
                  'id'
                 ]


class RouteOfAdministrationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RouteOfAdministration
        fields = [
                    'name',
                    'abbreviation',
                    'description'
                 ]


class AdministrationFrequencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AdministrationFrequency
        fields = [
                    'name',
                    'abbreviation',
                    'description',
                    'is_continuous',
                    'value',
                    'units'
                 ]

class AdministrationTimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AdministrationTime
        fields = [
                    'value',
                    'description'
                 ]

class PrescriptionSerializer(serializers.HyperlinkedModelSerializer):
    medications = MedicationSerializer(many=True)
    patient = PatientSerializer()
    prescriber = PrescriberSerializer()
    routes = RouteOfAdministrationSerializer(many=True)
    frequencies = AdministrationFrequencySerializer(many=True)
    administration_times = AdministrationTimeSerializer(many=True)

    class Meta:
        model = Prescription
        fields = [
                    'id',
                    'date_written',
                    'patient',
                    'prescriber',
                    'medications',
                    'routes',
                    'frequencies',
                    'administration_times',
                    'quantity_per_dose',
                    'dose_units',
                    'duration_of_therapy',
                    'duration_units',
                    'refills',
                    'expiration_date',
                    'is_prn',
                    'prn_reason'
                 ]

