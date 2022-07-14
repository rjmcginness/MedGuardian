from rest_framework import serializers
from src.user_model import Address
from src.user_model import ContactInformation
from src.user_model import Patient


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('street',
                  'street2',
                  'city',
                  'county',
                  'state_name',
                  'zip_code')


class ContactInformationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContactInformation
        fields = ('phone_number',
                  'mobile_number',
                  'fax_number')


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    address = AddressSerializer()
    contacts = ContactInformationSerializer()

    class Meta:
        model = Patient
        fields = ('first_name',
                  'last_name',
                  'username',
                  'birth_date',
                  'email')
